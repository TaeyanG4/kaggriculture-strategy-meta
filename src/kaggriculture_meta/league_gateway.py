"""Nickname/password gateway that lets a small team use the local public league.

The league server keeps listening on 127.0.0.1 only. This gateway adds login,
forwards the signed-in nickname as X-League-User, and is the only port a tunnel
should expose. Accounts live in state/public_league/team_users.json.
"""
from __future__ import annotations

import argparse
import getpass
import gzip
import hashlib
import hmac
import html
import http.client
import http.cookies
import json
import os
import re
import secrets
import sys
import threading
import time
import unicodedata
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state" / "public_league"
DEFAULT_USERS = STATE / "team_users.json"
DEFAULT_AUDIT = STATE / "team_gateway_audit.jsonl"
DEFAULT_UPSTREAM = "http://127.0.0.1:8791"
DEFAULT_PORT = 8792
COOKIE = "kgl_team_session"
USER_HEADER = "X-League-User"
ROLES = ("admin", "member")
# Machine configuration stays with admins; members may upload, focus and battle.
ADMIN_ONLY_POST = frozenset({"/api/settings", "/api/auto-collect/toggle"})
PBKDF2_ITERATIONS = 600_000
MIN_PASSWORD_LENGTH = 8
MAX_BODY_BYTES = 101 * 1024 * 1024
UPSTREAM_TIMEOUT_SECONDS = 1800
# 0 = unlimited login attempts (owner request 2026-09-23); `serve --login-limit N` re-enables it.
LOGIN_FAILURE_LIMIT = 0
LOGIN_WINDOW_SECONDS = 600
# Dashboard heartbeats are not worth an audit line every 5 seconds.
UNAUDITED_POSTS = ("/api/session",)
# Sends the dashboard back to the login page once its session is gone (restart, password change).
SESSION_GUARD = (b"<script>(()=>{const f=window.fetch;window.fetch=async(...a)=>{const r=await f(...a);"
                 b"if(r.status===401)location.href='/gateway/login?next='+encodeURIComponent("
                 b"location.pathname+location.search);return r}})()</script>")
NICKNAME = re.compile(r"[\w.-]{1,32}")
DROP_REQUEST_HEADERS = frozenset({
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailer",
    "transfer-encoding", "upgrade", "host", "content-length", "cookie", "origin", "referer",
    "accept-encoding", USER_HEADER.lower()})
DROP_RESPONSE_HEADERS = frozenset({
    "connection", "keep-alive", "transfer-encoding", "content-length", "content-encoding",
    "content-type", "access-control-allow-origin", "cache-control", "server", "date"})
COMPRESSIBLE = ("application/json", "text/html", "text/plain")

LOGIN_PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Kaggriculture 팀 리그 로그인</title>
<style>:root{color-scheme:dark;--bg:#09110d;--card:#111d17;--line:#284034;--text:#e9f3ec;--muted:#9db0a4;--red:#ef7b74}
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--text);font:15px system-ui,sans-serif}
main{width:min(380px,calc(100% - 32px));padding:28px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
h1{margin:0 0 6px;font-size:22px}p{color:var(--muted);margin:0 0 14px;line-height:1.5}label{display:block;margin:12px 0 6px;color:var(--muted)}
input{width:100%;padding:10px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--text);font-size:15px}
button{width:100%;margin-top:18px;padding:11px;border:0;border-radius:8px;background:#247849;color:#fff;font-weight:700;font-size:15px;cursor:pointer}
.error{color:var(--red);min-height:1.4em;margin-top:12px}</style></head><body><main>
<h1>Kaggriculture 팀 리그</h1><p>관리자가 발급한 닉네임과 비밀번호로 로그인하세요.</p>
<form method="post" action="/gateway/login"><input type="hidden" name="next" value="%NEXT%">
<label for="nickname">닉네임</label><input id="nickname" name="nickname" autocomplete="username" autocapitalize="off" spellcheck="false" maxlength="32" required value="%NICKNAME%" autofocus>
<label for="password">비밀번호</label><input id="password" name="password" type="password" autocomplete="current-password" required>
<button>로그인</button><div class="error" role="alert">%ERROR%</div></form></main></body></html>"""

OFFLINE_PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>리그 서버 꺼짐</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#09110d;color:#e9f3ec;font:15px system-ui,sans-serif}
main{width:min(460px,calc(100% - 32px));padding:28px;border:1px solid #284034;border-radius:14px;background:#111d17;line-height:1.6}</style>
</head><body><main><h1>리그 서버가 꺼져 있습니다</h1><p>%MESSAGE%</p><p><a style="color:#76c8ff" href="/">다시 시도</a></p></main></body></html>"""


class GatewayError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def normalize_nickname(value: str) -> str:
    name = unicodedata.normalize("NFC", str(value)).strip()
    if not NICKNAME.fullmatch(name):
        raise ValueError("닉네임은 한글·영문·숫자와 . _ - 로 1~32자여야 합니다.")
    return name


def _password_bytes(password: str) -> bytes:
    return unicodedata.normalize("NFC", str(password)).encode("utf-8")


def hash_password(password: str, iterations=None) -> dict:
    iterations = int(iterations or PBKDF2_ITERATIONS)
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", _password_bytes(password), salt, iterations)
    return {"salt": salt.hex(), "hash": digest.hex(), "iterations": iterations}


def verify_password(password: str, record: dict) -> bool:
    try:
        digest = hashlib.pbkdf2_hmac("sha256", _password_bytes(password),
                                     bytes.fromhex(record["salt"]), int(record["iterations"]))
    except (KeyError, TypeError, ValueError):
        return False
    return hmac.compare_digest(digest.hex(), str(record.get("hash", "")))


_DUMMY = {}


def _dummy_record() -> dict:
    # Unknown nicknames still pay one hash so timing does not reveal accounts.
    if not _DUMMY:
        _DUMMY.update(hash_password(secrets.token_hex(8)))
    return _DUMMY


def _check_password(password: str):
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"비밀번호는 {MIN_PASSWORD_LENGTH}자 이상이어야 합니다.")


def _check_role(role: str):
    if role not in ROLES:
        raise ValueError(f"역할은 {', '.join(ROLES)} 중 하나여야 합니다.")


class UserStore:
    """Team accounts in a JSON file; CLI edits apply to a running gateway."""

    def __init__(self, path=DEFAULT_USERS):
        self.path = Path(path)
        self.lock = threading.Lock()
        self._cache, self._stamp, self._loaded = {}, None, 0.0

    def _stat(self):
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            return None
        return stat.st_mtime_ns, stat.st_size

    def _read(self) -> dict:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {}
        return dict(data.get("users", {}))

    def _write(self, users: dict):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps({"version": 1, "users": users}, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        os.replace(tmp, self.path)
        with self.lock:
            self._cache, self._stamp, self._loaded = users, self._stat(), time.monotonic()

    def users(self) -> dict:
        # Re-read on change, and at least every 2 s in case two edits share a file-time tick.
        with self.lock:
            stamp = self._stat()
            if stamp != self._stamp or time.monotonic() - self._loaded > 2:
                self._cache = self._read() if stamp else {}
                self._stamp, self._loaded = stamp, time.monotonic()
            return self._cache

    def get(self, nickname: str):
        try:
            return self.users().get(normalize_nickname(nickname).casefold())
        except ValueError:
            return None

    def _existing(self, users: dict, nickname: str) -> str:
        key = normalize_nickname(nickname).casefold()
        if key not in users:
            raise ValueError(f"없는 닉네임입니다: {nickname}")
        return key

    def add(self, nickname: str, password: str, role="member", iterations=None):
        name = normalize_nickname(nickname)
        _check_password(password)
        _check_role(role)
        users = self._read()
        if name.casefold() in users:
            raise ValueError(f"이미 있는 닉네임입니다: {name}")
        now = _now()
        users[name.casefold()] = {"nickname": name, "role": role, **hash_password(password, iterations),
                                  "created_at": now, "updated_at": now}
        self._write(users)

    def set_password(self, nickname: str, password: str, iterations=None):
        _check_password(password)
        users = self._read()
        key = self._existing(users, nickname)
        users[key].update(hash_password(password, iterations), updated_at=_now())
        self._write(users)

    def set_role(self, nickname: str, role: str):
        _check_role(role)
        users = self._read()
        key = self._existing(users, nickname)
        users[key].update(role=role, updated_at=_now())
        self._write(users)

    def remove(self, nickname: str):
        users = self._read()
        del users[self._existing(users, nickname)]
        self._write(users)

    def listing(self) -> list[dict]:
        return [{k: record.get(k) for k in ("nickname", "role", "created_at", "updated_at")}
                for record in self._read().values()]


class Sessions:
    """In-memory login sessions; a password change or account removal ends them."""

    def __init__(self, ttl_seconds: float):
        self.ttl = int(ttl_seconds)
        self.items = {}
        self.lock = threading.Lock()

    def create(self, key: str, stamp: str) -> str:
        token = secrets.token_urlsafe(32)
        now = time.time()
        with self.lock:
            self.items = {k: v for k, v in self.items.items() if v[2] > now}
            self.items[token] = (key, stamp, now + self.ttl)
        return token

    def get(self, token: str):
        with self.lock:
            item = self.items.get(token or "")
            if item and item[2] > time.time():
                return item[0], item[1]
            self.items.pop(token or "", None)
        return None

    def drop(self, token: str):
        with self.lock:
            self.items.pop(token or "", None)


class LoginThrottle:
    """Blocks a nickname or client after repeated failures within a window."""

    def __init__(self, limit=LOGIN_FAILURE_LIMIT, window=LOGIN_WINDOW_SECONDS):
        self.limit, self.window = limit, window
        self.failures = {}
        self.lock = threading.Lock()

    def _recent(self, key: str, now: float) -> list:
        values = [t for t in self.failures.get(key, []) if now - t < self.window]
        if values:
            self.failures[key] = values
        else:
            self.failures.pop(key, None)
        return values

    def blocked(self, keys, now=None) -> bool:
        if self.limit <= 0:
            return False
        now = time.time() if now is None else now
        with self.lock:
            return any(len(self._recent(key, now)) >= self.limit for key in keys)

    def fail(self, keys, now=None):
        if self.limit <= 0:
            return
        now = time.time() if now is None else now
        with self.lock:
            for key in keys:
                self.failures.setdefault(key, []).append(now)

    def clear(self, keys):
        with self.lock:
            for key in keys:
                self.failures.pop(key, None)


def safe_next(value: str) -> str:
    """Only same-site paths are valid login redirect targets."""
    value = str(value or "/")
    if (not value.startswith("/") or value.startswith("//") or "\\" in value
            or any(c in value for c in "\r\n") or value.startswith("/gateway/")):
        return "/"
    return value


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "KaggricultureTeamGateway/1"
    timeout = 120

    def log_message(self, fmt, *args):
        # pythonw has no stderr; logins and changes go to the audit file instead.
        pass

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def _handle(self, method: str):
        try:
            self._route(method)
        except GatewayError as exc:
            self._error(exc.code, str(exc))
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    # Responses
    def _send(self, code: int, body, content_type: str, headers=()):
        body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        for key, value in headers:
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, payload: dict):
        self._send(code, json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8")

    def _error(self, code: int, message: str):
        # Dashboard handlers display either field.
        self._json(code, {"error": message, "message": message})

    def _redirect(self, location: str, headers=()):
        self._send(303, b"", "text/plain; charset=utf-8", [("Location", location), *headers])

    # Request context
    def _behind_proxy(self) -> bool:
        return self.client_address[0] in ("127.0.0.1", "::1")

    def _client(self) -> str:
        """Best-known client address; empty when a local proxy does not say.

        Behind a local proxy (cloudflared, Caddy, tailscale serve) the proxy's
        own entry is the right-most X-Forwarded-For value.
        """
        if self._behind_proxy():
            forwarded = (self.headers.get("Cf-Connecting-Ip")
                         or self.headers.get("X-Forwarded-For", "").split(",")[-1])
            return forwarded.strip()
        return self.client_address[0]

    def _https(self) -> bool:
        return self.server.secure_cookies or (
            self._behind_proxy() and self.headers.get("X-Forwarded-Proto", "").lower() == "https")

    def _token(self) -> str:
        cookie = http.cookies.SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except http.cookies.CookieError:
            return ""
        morsel = cookie.get(COOKIE)
        return morsel.value if morsel else ""

    def _user(self):
        token = self._token()
        found = self.server.sessions.get(token)
        if not found:
            return None
        key, stamp = found
        record = self.server.users.users().get(key)
        if not record or record.get("hash", "")[:16] != stamp:
            self.server.sessions.drop(token)
            return None
        return record

    def _same_origin(self) -> bool:
        site = self.headers.get("Sec-Fetch-Site")
        if site:
            return site in ("same-origin", "none")
        origin = self.headers.get("Origin")
        if not origin:
            return True
        hosts = {self.headers.get("Host", ""), self.headers.get("X-Forwarded-Host", "")} - {""}
        return urllib.parse.urlsplit(origin).netloc in hosts

    def _cookie(self, token: str, max_age: int) -> str:
        parts = [f"{COOKIE}={token}", "Path=/", "HttpOnly", "SameSite=Lax", f"Max-Age={int(max_age)}"]
        if self._https():
            parts.append("Secure")
        return "; ".join(parts)

    def _read_body(self, limit: int) -> bytes:
        if self.headers.get("Transfer-Encoding"):
            raise GatewayError(411, "Content-Length가 필요합니다.")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise GatewayError(400, "잘못된 Content-Length입니다.") from None
        if length < 0 or length > limit:
            raise GatewayError(413, "요청이 너무 큽니다.")
        data = bytearray()
        while len(data) < length:
            chunk = self.rfile.read(length - len(data))
            if not chunk:
                raise GatewayError(400, "요청 본문이 중간에 끊겼습니다.")
            data += chunk
        return bytes(data)

    def _audit(self, event: str, **fields):
        record = {"at": _now(), "event": event,
                  "client": self._client() or self.client_address[0], **fields}
        try:
            with self.server.audit_lock, open(self.server.audit_path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            pass

    # Routing
    def _route(self, method: str):
        if not self.path.startswith("/") or self.path.startswith("//"):
            raise GatewayError(400, "잘못된 요청 경로입니다.")
        path = urllib.parse.urlsplit(self.path).path
        if path == "/gateway/login":
            return self._login_page() if method == "GET" else self._login()
        if path == "/gateway/logout" and method == "POST":
            return self._logout()
        user = self._user()
        if user is None:
            if method == "GET" and not path.startswith(("/api/", "/gateway/")):
                return self._redirect("/gateway/login?next=" + urllib.parse.quote(self.path, safe=""))
            raise GatewayError(401, "로그인이 필요합니다. 페이지를 새로고침해 주세요.")
        if method != "GET" and not self._same_origin():
            raise GatewayError(403, "다른 사이트에서 보낸 요청은 허용하지 않습니다.")
        if path == "/gateway/me":
            return self._json(200, {"nickname": user["nickname"], "role": user["role"]})
        if path.startswith("/gateway/"):
            raise GatewayError(404, "없는 주소입니다.")
        if method == "POST" and path in ADMIN_ONLY_POST and user["role"] != "admin":
            raise GatewayError(403, "관리자만 바꿀 수 있는 설정입니다.")
        self._proxy(method, user, path)

    def _login_page(self, code=200, error="", nickname="", target=None):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        target = target or safe_next(query.get("next", ["/"])[0])
        if code == 200 and self._user():
            return self._redirect(target)
        page = (LOGIN_PAGE.replace("%NEXT%", html.escape(target))
                .replace("%NICKNAME%", html.escape(nickname)).replace("%ERROR%", html.escape(error)))
        self._send(code, page, "text/html; charset=utf-8")

    def _login(self):
        form = urllib.parse.parse_qs(self._read_body(8192).decode("utf-8", "replace"))
        nickname = (form.get("nickname") or [""])[0][:64]
        password = (form.get("password") or [""])[0]
        target = safe_next((form.get("next") or ["/"])[0])
        keys = ["n:" + unicodedata.normalize("NFC", nickname).strip().casefold()]
        if self._client():
            keys.append("c:" + self._client())
        if self.server.throttle.blocked(keys):
            self._audit("login_blocked", nickname=nickname)
            return self._login_page(429, "로그인 시도가 너무 많습니다. 10분 뒤 다시 시도하세요.",
                                    nickname, target)
        record = self.server.users.get(nickname)
        valid = verify_password(password, record or _dummy_record()) and record is not None
        if not valid:
            self.server.throttle.fail(keys)
            self._audit("login_failed", nickname=nickname)
            return self._login_page(401, "닉네임 또는 비밀번호가 올바르지 않습니다.", nickname, target)
        self.server.throttle.clear(keys)
        token = self.server.sessions.create(record["nickname"].casefold(), record["hash"][:16])
        self._audit("login", nickname=record["nickname"])
        self._redirect(target, [("Set-Cookie", self._cookie(token, self.server.sessions.ttl))])

    def _logout(self):
        user = self._user()
        self.server.sessions.drop(self._token())
        if user:
            self._audit("logout", nickname=user["nickname"])
        self._redirect("/gateway/login", [("Set-Cookie", self._cookie("", 0))])

    def _proxy(self, method: str, user: dict, path: str):
        body = self._read_body(MAX_BODY_BYTES) if method == "POST" else None
        headers = {key: value for key, value in self.headers.items()
                   if key.lower() not in DROP_REQUEST_HEADERS}
        headers[USER_HEADER] = urllib.parse.quote(user["nickname"], safe="")
        upstream = self.server.upstream
        headers["Host"] = upstream.netloc
        connection = http.client.HTTPConnection(upstream.hostname, upstream.port or 80,
                                                timeout=self.server.upstream_timeout)
        try:
            connection.request(method, self.path, body=body, headers=headers)
            response = connection.getresponse()
            data = response.read()
            status, upstream_headers = response.status, response.getheaders()
        except (OSError, http.client.HTTPException):
            return self._offline(method, path)
        finally:
            connection.close()
        if method == "POST" and not path.startswith(UNAUDITED_POSTS):
            self._audit("request", nickname=user["nickname"], path=path, status=status)
        content_type = next((v for k, v in upstream_headers if k.lower() == "content-type"),
                            "application/octet-stream")
        if path in ("/", "/index.html") and content_type.startswith("text/html"):
            data = data.replace(b"</head>", SESSION_GUARD + b"</head>", 1)
        extra = [(k, v) for k, v in upstream_headers if k.lower() not in DROP_RESPONSE_HEADERS]
        if (len(data) > 1024 and content_type.startswith(COMPRESSIBLE)
                and "gzip" in self.headers.get("Accept-Encoding", "")):
            data = gzip.compress(data, compresslevel=5)
            extra += [("Content-Encoding", "gzip"), ("Vary", "Accept-Encoding")]
        self._send(status, data, content_type, extra)

    def _offline(self, method: str, path: str):
        message = (f"리그 서버({self.server.upstream.netloc})에 연결할 수 없습니다. "
                   "관리자에게 서버 실행을 요청하세요.")
        if method != "GET" or path.startswith("/api/"):
            return self._error(502, message)
        self._send(502, OFFLINE_PAGE.replace("%MESSAGE%", html.escape(message)),
                   "text/html; charset=utf-8")


def make_server(host="127.0.0.1", port=DEFAULT_PORT, upstream=DEFAULT_UPSTREAM,
                users_path=DEFAULT_USERS, audit_path=DEFAULT_AUDIT, session_days=7.0,
                secure_cookies=False, login_limit=None) -> ThreadingHTTPServer:
    target = urllib.parse.urlsplit(upstream)
    if target.scheme != "http" or not target.hostname:
        raise ValueError("--upstream must look like http://127.0.0.1:8791")
    server = ThreadingHTTPServer((host, port), GatewayHandler)
    server.upstream = target
    server.upstream_timeout = UPSTREAM_TIMEOUT_SECONDS
    server.users = UserStore(users_path)
    server.sessions = Sessions(session_days * 86400)
    server.throttle = LoginThrottle(LOGIN_FAILURE_LIMIT if login_limit is None else login_limit)
    server.audit_path = Path(audit_path)
    server.audit_path.parent.mkdir(parents=True, exist_ok=True)
    server.audit_lock = threading.Lock()
    server.secure_cookies = bool(secure_cookies)
    return server


def _read_password(from_stdin: bool, confirm=True) -> str:
    if from_stdin:
        # PowerShell pipes a UTF-8 BOM in front of the text.
        stream = getattr(sys.stdin, "buffer", None)
        line = stream.readline().decode("utf-8-sig") if stream else sys.stdin.readline()
        return line.lstrip("﻿").rstrip("\r\n")
    password = getpass.getpass("비밀번호: ")
    if confirm and getpass.getpass("비밀번호 확인: ") != password:
        raise ValueError("두 비밀번호가 다릅니다.")
    return password


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--users", type=Path, default=DEFAULT_USERS)
    sub = ap.add_subparsers(dest="command", required=True)
    web = sub.add_parser("serve", help="run the login gateway")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=DEFAULT_PORT)
    web.add_argument("--upstream", default=DEFAULT_UPSTREAM)
    web.add_argument("--session-days", type=float, default=7.0)
    web.add_argument("--secure-cookies", action="store_true")
    web.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    web.add_argument("--login-limit", type=int, default=LOGIN_FAILURE_LIMIT,
                     help="failed logins per nickname/client per 10 minutes; 0 = unlimited")
    sub.add_parser("check", help="exit 0 when at least one account exists")
    user = sub.add_parser("user", help="manage team accounts")
    actions = user.add_subparsers(dest="action", required=True)
    add = actions.add_parser("add")
    add.add_argument("nickname")
    add.add_argument("--role", choices=ROLES, default="member")
    add.add_argument("--password-stdin", action="store_true")
    passwd = actions.add_parser("passwd")
    passwd.add_argument("nickname")
    passwd.add_argument("--password-stdin", action="store_true")
    role = actions.add_parser("role")
    role.add_argument("nickname")
    role.add_argument("role", choices=ROLES)
    remove = actions.add_parser("remove")
    remove.add_argument("nickname")
    actions.add_parser("list")
    args = ap.parse_args(argv)
    store = UserStore(args.users)
    try:
        if args.command == "check":
            count = len(store.users())
            print(f"accounts: {count}")
            return 0 if count else 2
        if args.command == "serve":
            if not store.users():
                print("등록된 계정이 없습니다. 먼저 'user add <닉네임> --role admin'으로 만드세요.",
                      file=sys.stderr)
                return 2
            server = make_server(args.host, args.port, args.upstream, args.users, args.audit,
                                 args.session_days, args.secure_cookies, args.login_limit)
            print(f"Team gateway: http://{args.host}:{server.server_address[1]} -> {args.upstream}",
                  flush=True)
            try:
                server.serve_forever()
            finally:
                server.server_close()
            return 0
        if args.action == "add":
            store.add(args.nickname, _read_password(args.password_stdin), args.role)
            print(f"추가함: {normalize_nickname(args.nickname)} ({args.role})")
        elif args.action == "passwd":
            store.set_password(args.nickname, _read_password(args.password_stdin))
            print("비밀번호를 바꿨습니다. 기존 로그인은 끊깁니다.")
        elif args.action == "role":
            store.set_role(args.nickname, args.role)
            print(f"역할 변경: {args.nickname} -> {args.role}")
        elif args.action == "remove":
            store.remove(args.nickname)
            print(f"삭제함: {args.nickname}")
        else:
            rows = store.listing()
            for row in rows:
                print(f"{row['nickname']}\t{row['role']}\t생성 {row['created_at']}\t변경 {row['updated_at']}")
            if not rows:
                print("(계정 없음)")
    except ValueError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
