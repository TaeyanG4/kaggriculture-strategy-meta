"""Team login gateway: accounts, sessions, role limits and request forwarding."""
import gzip
import http.client
import io
import json
import tempfile
import threading
import unicodedata
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from src.kaggriculture_meta import league_gateway as gw


class FakeLeague(BaseHTTPRequestHandler):
    seen = []

    def log_message(self, *args):
        pass

    def _reply(self, body, content_type="application/json; charset=utf-8", extra=()):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        for key, value in extra:
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        FakeLeague.seen.append(("GET", self.path, dict(self.headers), b""))
        if self.path == "/":
            return self._reply(b"<html><head><title>league</title></head><body>ok</body></html>",
                               "text/html; charset=utf-8")
        if self.path.startswith("/api/agent-download"):
            return self._reply(b"print('agent')\n", "text/x-python",
                               [("Content-Disposition", "attachment; filename=\"a.py\"")])
        self._reply(json.dumps({"path": self.path, "pad": "x" * 4000}).encode())

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        FakeLeague.seen.append(("POST", self.path, dict(self.headers), body))
        self._reply(json.dumps({"ok": True, "size": len(body)}).encode())


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.iterations = patch.object(gw, "PBKDF2_ITERATIONS", 1000)
        self.iterations.start()
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        root = Path(self.tmp.name)
        FakeLeague.seen = []
        self.league = ThreadingHTTPServer(("127.0.0.1", 0), FakeLeague)
        threading.Thread(target=self.league.serve_forever, daemon=True).start()
        self.server = gw.make_server("127.0.0.1", 0, f"http://127.0.0.1:{self.league.server_address[1]}",
                                     root / "users.json", root / "audit.jsonl")
        self.server.users.add("태양", "admin-pass-1", "admin")
        self.server.users.add("minsu", "member-pass-1", "member")
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.port = self.server.server_address[1]
        self.audit = root / "audit.jsonl"

    def tearDown(self):
        for server in (self.server, self.league):
            if server is not None:
                server.shutdown()
                server.server_close()
        self.tmp.cleanup()
        self.iterations.stop()

    def request(self, method, path, body=None, headers=None, cookie=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        headers = dict(headers or {})
        if cookie:
            headers["Cookie"] = cookie
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response, data

    def login(self, nickname, password, headers=None):
        body = urllib.parse.urlencode({"nickname": nickname, "password": password, "next": "/"})
        response, _ = self.request("POST", "/gateway/login", body,
                                   {"Content-Type": "application/x-www-form-urlencoded", **(headers or {})})
        return response, (response.getheader("Set-Cookie") or "").split(";", 1)[0]

    def test_accounts_are_hashed_normalized_and_validated(self):
        users = self.server.users
        raw = json.loads(Path(users.path).read_text(encoding="utf-8"))
        self.assertNotIn("member-pass-1", json.dumps(raw))
        self.assertTrue(gw.verify_password("member-pass-1", users.get("MINSU")))
        self.assertFalse(gw.verify_password("wrong-pass", users.get("minsu")))
        self.assertEqual(users.get(unicodedata.normalize("NFD", "태양"))["nickname"], "태양")
        for nickname, password in (("Minsu", "long-enough"), ("a b", "long-enough"), ("new", "short")):
            with self.assertRaises(ValueError):
                users.add(nickname, password)
        self.assertEqual(sorted(x["nickname"] for x in users.listing()), ["minsu", "태양"])
        self.assertNotIn("hash", users.listing()[0])

    def test_login_is_required_before_anything_reaches_the_league(self):
        response, _ = self.request("GET", "/?tab=1")
        self.assertEqual(response.status, 303)
        self.assertEqual(response.getheader("Location"), "/gateway/login?next=%2F%3Ftab%3D1")
        response, data = self.request("GET", "/api/status")
        self.assertEqual(response.status, 401)
        self.assertIn("error", json.loads(data))
        response, _ = self.request("POST", "/api/battle/toggle", b"")
        self.assertEqual(response.status, 401)
        self.assertEqual(FakeLeague.seen, [])

    def test_login_sets_hardened_cookie_and_forwards_verified_nickname(self):
        response, cookie = self.login("태양", "admin-pass-1")
        self.assertEqual((response.status, response.getheader("Location")), (303, "/"))
        flags = response.getheader("Set-Cookie")
        self.assertIn("HttpOnly", flags)
        self.assertIn("SameSite=Lax", flags)
        self.assertNotIn("Secure", flags)
        response, data = self.request("GET", "/api/status", cookie=cookie,
                                      headers={"X-League-User": "spoof", "Origin": "http://evil"})
        self.assertEqual(response.status, 200)
        self.assertIsNone(response.getheader("Access-Control-Allow-Origin"))
        self.assertEqual(response.getheader("Cache-Control"), "no-store")
        _, path, headers, _ = FakeLeague.seen[-1]
        self.assertEqual(path, "/api/status")
        self.assertEqual(urllib.parse.unquote(headers["X-League-User"]), "태양")
        self.assertEqual(headers["Host"], f"127.0.0.1:{self.league.server_address[1]}")
        self.assertNotIn("Cookie", headers)
        self.assertNotIn("Origin", headers)
        response, _ = self.login("minsu", "member-pass-1", {"X-Forwarded-Proto": "https"})
        self.assertIn("Secure", response.getheader("Set-Cookie"))

    def test_me_gzip_and_download_headers(self):
        _, cookie = self.login("minsu", "member-pass-1")
        response, data = self.request("GET", "/gateway/me", cookie=cookie)
        self.assertEqual(json.loads(data), {"nickname": "minsu", "role": "member"})
        response, data = self.request("GET", "/api/status", cookie=cookie,
                                      headers={"Accept-Encoding": "gzip"})
        self.assertEqual(response.getheader("Content-Encoding"), "gzip")
        self.assertEqual(json.loads(gzip.decompress(data))["path"], "/api/status")
        response, data = self.request("GET", "/api/agent-download?agent_id=3", cookie=cookie)
        self.assertEqual(data, b"print('agent')\n")
        self.assertEqual(response.getheader("Content-Disposition"), "attachment; filename=\"a.py\"")

    def test_members_cannot_change_machine_settings(self):
        _, member = self.login("minsu", "member-pass-1")
        _, admin = self.login("태양", "admin-pass-1")
        for path in ("/api/settings", "/api/auto-collect/toggle"):
            response, data = self.request("POST", path, b"{}", cookie=member)
            self.assertEqual(response.status, 403)
            self.assertIn("message", json.loads(data))
        self.assertEqual(FakeLeague.seen, [])
        response, _ = self.request("POST", "/api/battle/toggle", b"", cookie=member)
        self.assertEqual(response.status, 200)
        response, _ = self.request("POST", "/api/settings", b"{}", cookie=admin)
        self.assertEqual(response.status, 200)
        self.assertEqual([x[1] for x in FakeLeague.seen], ["/api/battle/toggle", "/api/settings"])

    def test_cross_site_posts_are_rejected(self):
        _, cookie = self.login("minsu", "member-pass-1")
        for headers in ({"Sec-Fetch-Site": "cross-site"}, {"Origin": "http://evil.example"}):
            response, _ = self.request("POST", "/api/focus", b"{}", headers, cookie)
            self.assertEqual(response.status, 403)
        same = {"Origin": f"http://127.0.0.1:{self.port}", "Content-Type": "application/json"}
        response, _ = self.request("POST", "/api/focus", b'{"agent_id":1}', same, cookie)
        self.assertEqual(response.status, 200)
        self.assertEqual(FakeLeague.seen[-1][3], b'{"agent_id":1}')

    def test_upload_body_and_marker_are_forwarded_intact(self):
        _, cookie = self.login("minsu", "member-pass-1")
        payload = bytes(range(256)) * 8192
        response, data = self.request("POST", "/api/upload-agent?filename=a.py", payload,
                                      {"X-League-Upload": "1", "Content-Type": "application/octet-stream",
                                       "Sec-Fetch-Site": "same-origin"}, cookie)
        self.assertEqual(json.loads(data)["size"], len(payload))
        _, _, headers, body = FakeLeague.seen[-1]
        self.assertEqual(body, payload)
        self.assertEqual(headers["X-League-Upload"], "1")
        self.assertEqual(urllib.parse.unquote(headers["X-League-User"]), "minsu")
        events = [json.loads(x) for x in self.audit.read_text(encoding="utf-8").splitlines()]
        self.assertIn({"event": "request", "nickname": "minsu", "path": "/api/upload-agent", "status": 200},
                      [{k: x[k] for k in ("event", "nickname", "path", "status") if k in x} for x in events])

    def test_unlimited_attempts_by_default(self):
        self.assertEqual(self.server.throttle.limit, 0)
        for _ in range(8):
            self.assertEqual(self.login("minsu", "wrong-password")[0].status, 401)
        response, cookie = self.login("minsu", "member-pass-1")
        self.assertEqual(response.status, 303)
        self.assertTrue(cookie)

    def test_optional_limit_blocks_even_the_right_password(self):
        self.server.throttle.limit = 5
        for _ in range(5):
            response, cookie = self.login("minsu", "wrong-password")
            self.assertEqual((response.status, cookie), (401, ""))
        response, cookie = self.login("minsu", "member-pass-1")
        self.assertEqual((response.status, cookie), (429, ""))
        response, cookie = self.login("태양", "admin-pass-1")
        self.assertEqual(response.status, 303)
        events = [json.loads(x)["event"] for x in self.audit.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(events.count("login_failed"), 5)
        self.assertIn("login_blocked", events)

    def test_dashboard_returns_to_login_when_session_ends_and_heartbeats_are_not_audited(self):
        _, cookie = self.login("minsu", "member-pass-1")
        response, page = self.request("GET", "/", cookie=cookie)
        self.assertIn(gw.SESSION_GUARD + b"</head>", page)
        response, data = self.request("GET", "/api/status", cookie=cookie)
        self.assertNotIn(b"<script>", data)
        self.request("POST", "/api/session", b'{"id":"t"}', {"Content-Type": "application/json"}, cookie)
        self.request("POST", "/api/battle/toggle", b"", cookie=cookie)
        paths = [json.loads(x).get("path") for x in self.audit.read_text(encoding="utf-8").splitlines()]
        self.assertIn("/api/battle/toggle", paths)
        self.assertNotIn("/api/session", paths)

    def test_proxy_forwarded_client_is_throttled_and_logged(self):
        # Caddy on the same PC forwards the visitor as the right-most X-Forwarded-For entry.
        self.server.throttle.limit = 5
        visitor ={"X-Forwarded-For": "198.51.100.1, 203.0.113.7", "X-Forwarded-Proto": "https"}
        for nickname in ("a1", "a2", "a3", "a4", "a5"):
            self.assertEqual(self.login(nickname, "wrong-password", visitor)[0].status, 401)
        response, _ = self.login("minsu", "member-pass-1", visitor)
        self.assertEqual(response.status, 429)
        response, cookie = self.login("minsu", "member-pass-1",
                                      {"X-Forwarded-For": "203.0.113.8", "X-Forwarded-Proto": "https"})
        self.assertEqual(response.status, 303)
        self.assertIn("Secure", response.getheader("Set-Cookie"))
        clients = {json.loads(x)["client"] for x in self.audit.read_text(encoding="utf-8").splitlines()}
        self.assertEqual(clients, {"203.0.113.7", "203.0.113.8"})

    def test_password_change_removal_and_logout_end_sessions(self):
        _, cookie = self.login("minsu", "member-pass-1")
        self.assertEqual(self.request("GET", "/api/status", cookie=cookie)[0].status, 200)
        self.server.users.set_password("minsu", "member-pass-2")
        self.assertEqual(self.request("GET", "/api/status", cookie=cookie)[0].status, 401)
        _, cookie = self.login("minsu", "member-pass-2")
        self.server.users.set_role("minsu", "admin")
        response, _ = self.request("POST", "/api/settings", b"{}", cookie=cookie)
        self.assertEqual(response.status, 200)
        response, _ = self.request("POST", "/gateway/logout", b"", cookie=cookie)
        self.assertEqual(response.getheader("Location"), "/gateway/login")
        self.assertIn("Max-Age=0", response.getheader("Set-Cookie"))
        self.assertEqual(self.request("GET", "/api/status", cookie=cookie)[0].status, 401)
        _, cookie = self.login("minsu", "member-pass-2")
        self.server.users.remove("minsu")
        self.assertEqual(self.request("GET", "/api/status", cookie=cookie)[0].status, 401)

    def test_league_offline_is_reported(self):
        _, cookie = self.login("minsu", "member-pass-1")
        self.league.shutdown()
        self.league.server_close()
        self.league = None
        response, data = self.request("GET", "/", cookie=cookie)
        self.assertEqual(response.status, 502)
        self.assertIn("리그 서버", data.decode("utf-8"))
        response, data = self.request("GET", "/api/status", cookie=cookie)
        self.assertEqual(response.status, 502)
        self.assertIn("error", json.loads(data))

    def test_login_redirect_targets_stay_on_site(self):
        for value, expected in (("/?tab=1", "/?tab=1"), ("//evil.example", "/"), ("https://evil", "/"),
                                ("/\\evil", "/"), ("/a\r\nSet-Cookie: x", "/"), ("/gateway/logout", "/")):
            self.assertEqual(gw.safe_next(value), expected)

    def test_cli_manages_accounts_and_serve_refuses_without_any(self):
        path = Path(self.tmp.name) / "cli-users.json"
        self.assertEqual(gw.main(["--users", str(path), "check"]), 2)
        self.assertEqual(gw.main(["--users", str(path), "serve", "--port", "0"]), 2)
        with patch("sys.stdin", io.StringIO("secret-pass-9\n")):
            self.assertEqual(gw.main(["--users", str(path), "user", "add", "철수", "--role", "admin",
                                      "--password-stdin"]), 0)
        self.assertEqual(gw.main(["--users", str(path), "check"]), 0)
        self.assertTrue(gw.verify_password("secret-pass-9", gw.UserStore(path).get("철수")))
        self.assertEqual(gw.main(["--users", str(path), "user", "role", "철수", "member"]), 0)
        self.assertEqual(gw.UserStore(path).get("철수")["role"], "member")
        self.assertEqual(gw.main(["--users", str(path), "user", "remove", "없는사람"]), 1)
        # PowerShell pipes "\xef\xbb\xbf<text>\r\n"; the BOM must not become part of the password.
        piped = io.TextIOWrapper(io.BytesIO(b"\xef\xbb\xbfpiped-pass-7\r\n"), encoding="cp949")
        with patch("sys.stdin", piped):
            self.assertEqual(gw.main(["--users", str(path), "user", "passwd", "철수", "--password-stdin"]), 0)
        self.assertTrue(gw.verify_password("piped-pass-7", gw.UserStore(path).get("철수")))


if __name__ == "__main__":
    unittest.main()
