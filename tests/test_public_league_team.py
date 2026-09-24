"""Team features of the league server: presence, uploader credit, head-to-head, downloads."""
import http.client
import io
import json
import os
import socket
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import unicodedata
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch

from tests import test_public_league as fixtures
from src.kaggriculture_meta import league_gateway as gw
from src.kaggriculture_meta import public_league as league

AGENT = fixtures.AGENT
QA_PASS = {"ok": True, "entrypoint": "agent"}


def bundle(files):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, data in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    return buffer.getvalue()


class TeamFeatureTests(unittest.TestCase):
    setUp = fixtures.PublicLeagueTests.setUp
    tearDown = fixtures.PublicLeagueTests.tearDown

    def upload(self, name, source, uploader="", title=""):
        with patch.object(league, "qa_source", return_value=QA_PASS):
            return league.register_local_upload(self.store, name, source.encode(), title, uploader=uploader)

    def add_match(self, a, b, outcome_a, margin_a, status="complete"):
        index = self.store.db.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        with self.store.db:
            self.store.db.execute("""INSERT INTO matches(match_key,engine_sha,agent_a,agent_b,seed,seat_a,
                status,outcome_a,reward_a,reward_b,margin_a,created_at,completed_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (f"k{index}", "e", a, b, index + 1, index % 2, status,
                 outcome_a if status == "complete" else None,
                 10000 + margin_a, 10000, margin_a, league.utcnow(), league.utcnow()))

    def test_gateway_nickname_header_is_decoded_and_validated(self):
        quoted = urllib.parse.quote(unicodedata.normalize("NFD", "민수"))
        self.assertEqual(league.league_user({"X-League-User": quoted}), "민수")
        for value in ("a b", "", "x" * 33, "%3Cscript%3E"):
            self.assertEqual(league.league_user({"X-League-User": value}), "")
        self.assertEqual(league.league_user({}), "")

    def test_upload_is_credited_to_first_uploader(self):
        first = self.upload("main.py", AGENT, uploader="민수")
        self.assertEqual((first["title"], first["uploader"], first["registered_by"]),
                         ("민수 · main.py", "민수", "민수"))
        self.assertEqual(self.store.db.execute("SELECT author FROM notebooks").fetchone()[0], "민수")
        self.assertEqual(self.store.db.execute("SELECT author FROM aliases").fetchone()[0], "민수")
        again = self.upload("copy.py", AGENT, uploader="태양")
        self.assertEqual((again["agent_id"], again["registered_by"]), (first["agent_id"], "민수"))
        messages = [row[0] for row in self.store.db.execute(
            "SELECT message FROM events WHERE kind='local_upload' ORDER BY id")]
        self.assertTrue(messages[-1].startswith("[태양] "))
        local = self.upload("owner.py", AGENT + "\n# owner\n")
        self.assertEqual((local["title"], local["registered_by"]), ("owner.py", "Taeyang"))

    def test_opponent_records_group_valid_games_per_artifact(self):
        x = self.upload("x.py", AGENT, title="X")["agent_id"]
        y = self.upload("y.py", AGENT + "\n# y\n", title="Y")["agent_id"]
        z = self.upload("z.py", AGENT + "\n# z\n", title="Z")["agent_id"]
        self.upload("y-copy.py", AGENT + "\n# y\n", uploader="민수")
        with self.store.db:
            self.store.db.execute("UPDATE agents SET rating=CASE id WHEN ? THEN 1600 WHEN ? THEN 1400 ELSE 1500 END",
                                  (y, z))
        self.add_match(x, y, 1, 500)
        self.add_match(y, x, 1, 300)
        self.add_match(y, x, .5, 0)
        self.add_match(x, z, 0, -200)
        self.add_match(x, y, None, 0, status="invalid")
        records = league.agent_opponent_records(self.store, x)
        self.assertEqual([r["opponent_id"] for r in records["opponents"]], [y, z])
        vs_y, vs_z = records["opponents"]
        self.assertEqual((vs_y["games"], vs_y["wins"], vs_y["losses"], vs_y["ties"]), (3, 1, 1, 1))
        self.assertAlmostEqual(vs_y["score_rate"], .5)
        self.assertAlmostEqual(vs_y["avg_margin"], 200 / 3)
        self.assertAlmostEqual(vs_y["avg_own"] - vs_y["avg_opponent"], 200 / 3)
        self.assertEqual(vs_y["name"], "Y")
        self.assertEqual(len(vs_y["notebooks"]), 1)
        self.assertEqual((vs_z["wins"], vs_z["losses"], vs_z["avg_margin"]), (0, 1, -200))
        self.assertLess(vs_z["score_high"], 1)
        mirrored = league.agent_opponent_records(self.store, y)["opponents"][0]
        self.assertEqual((mirrored["wins"], mirrored["losses"], mirrored["ties"]), (1, 1, 1))
        with self.assertRaises(ValueError):
            league.agent_opponent_records(self.store, 999)

    def test_match_history_can_be_limited_to_one_opponent(self):
        x = self.upload("x.py", AGENT)["agent_id"]
        y = self.upload("y.py", AGENT + "\n# y\n")["agent_id"]
        z = self.upload("z.py", AGENT + "\n# z\n")["agent_id"]
        self.add_match(x, y, 1, 10)
        self.add_match(z, x, 1, 10)
        self.add_match(y, z, 1, 10)
        everything = league.agent_match_history(self.store, x)
        self.assertEqual((everything["total"], everything["opponent_id"]), (2, None))
        only_z = league.agent_match_history(self.store, x, opponent_id=z)
        self.assertEqual((only_z["total"], len(only_z["matches"])), (1, 1))
        self.assertEqual(only_z["matches"][0]["opponent_id"], z)
        self.assertEqual(only_z["matches"][0]["result_label"], "패")

    def test_download_returns_exact_runtime_files(self):
        single = self.upload("single.py", AGENT, title="Moon Counts Melons")
        name, data, kind = league.agent_download(self.store, single["agent_id"])
        self.assertEqual(name, f"Moon-Counts-Melons-{single['sha256'][:8]}.py")
        self.assertEqual(data, league.canonical_source(AGENT))
        self.assertTrue(kind.startswith("text/x-python"))
        credited = self.upload("main.py", AGENT + "\n# team\n", uploader="민수")
        self.assertEqual(league.agent_download(self.store, credited["agent_id"])[0],
                         f"민수-main-{credited['sha256'][:8]}.py")
        with patch.object(league, "qa_source", return_value=QA_PASS):
            packed = league.register_local_upload(
                self.store, "bundle.tgz", bundle({"main.py": AGENT.encode(), "agent.so": b"\0binary"}), "번들")
        name, data, kind = league.agent_download(self.store, packed["agent_id"])
        self.assertTrue(name.startswith("번들-") and name.endswith(".tar.gz"))
        self.assertEqual(kind, "application/gzip")
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            self.assertEqual(archive.getnames(), ["agent.so", "main.py"])
            self.assertEqual(archive.extractfile("agent.so").read(), b"\0binary")
        with self.assertRaises(ValueError):
            league.agent_download(self.store, 999)

    def test_presence_groups_tabs_and_expires(self):
        tracker = league.BrowserSessionTracker()
        tracker.touch("t1", now=100, user="민수")
        tracker.touch("t2", now=110, user="민수")
        tracker.touch("t3", now=50)
        self.assertEqual(tracker.presence(now=120), [
            {"nickname": "민수", "tabs": 2, "idle_seconds": 10},
            {"nickname": "", "tabs": 1, "idle_seconds": 70}])
        self.assertEqual([p["nickname"] for p in tracker.presence(now=145)], ["민수"])
        tracker.close("t1")
        self.assertEqual(tracker.presence(now=145)[0]["tabs"], 1)
        self.assertEqual(tracker.presence(now=1000), [])
        self.assertEqual(tracker.users, {})

    def test_battle_records_who_started_it(self):
        with patch.object(league, "run_league", return_value={"stopped": True}):
            controller = league.BattleController(self.root / "state")
            self.assertEqual(controller.toggle(actor="민수")["started_by"], "민수")
            controller.thread.join(5)
        self.assertEqual(controller.snapshot()["started_by"], "민수")
        self.assertEqual(controller.snapshot()["phase"], "stopped")

    def test_lock_left_by_dead_process_is_reclaimed(self):
        lock = self.root / "league.lock"
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        self.assertFalse(league._pid_alive(dead.pid))
        self.assertTrue(league._pid_alive(os.getpid()))
        lock.write_text(json.dumps({"pid": dead.pid, "created_at": league.utcnow()}), encoding="utf-8")
        with league.process_lock(lock) as acquired:
            self.assertTrue(acquired)
            self.assertEqual(json.loads(lock.read_text(encoding="utf-8"))["pid"], os.getpid())
        self.assertFalse(lock.exists())
        lock.write_text(json.dumps({"pid": os.getpid(), "created_at": league.utcnow()}), encoding="utf-8")
        with league.process_lock(lock) as acquired:
            self.assertFalse(acquired)
        self.assertTrue(lock.exists())
        lock.write_text("", encoding="utf-8")  # half-written lock is respected
        with league.process_lock(lock) as acquired:
            self.assertFalse(acquired)

    def test_dashboard_has_team_controls(self):
        for marker in ('id="localDrop"', 'id="dropOverlay"', 'id="agentopptable"', "downloadAgent(",
                       "/gateway/me", "renderWho(d.presence", 'class="adminonly"'):
            self.assertIn(marker, league.DASHBOARD)


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


class GatewayIntegrationTests(unittest.TestCase):
    """A member signs in through the gateway and uses the real league server."""

    def setUp(self):
        self.patches = [patch.object(league, "qa_source", return_value=QA_PASS),
                        patch.object(gw, "PBKDF2_ITERATIONS", 1000)]
        for item in self.patches:
            item.start()
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        root = Path(self.tmp.name)
        state = root / "state"
        league.Store(state).close()
        port = free_port()
        threading.Thread(target=league.serve, args=(state, "127.0.0.1", port), daemon=True).start()
        deadline = time.time() + 10
        while True:
            try:
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
                connection.request("GET", "/api/progress")
                connection.getresponse().read()
                connection.close()
                break
            except OSError:
                if time.time() > deadline:
                    raise
                time.sleep(.05)
        self.gateway = gw.make_server("127.0.0.1", 0, f"http://127.0.0.1:{port}",
                                      root / "users.json", root / "audit.jsonl")
        self.gateway.users.add("민수", "member-pass-1", "member")
        threading.Thread(target=self.gateway.serve_forever, daemon=True).start()
        self.port = self.gateway.server_address[1]

    def tearDown(self):
        self.gateway.shutdown()
        self.gateway.server_close()
        for item in self.patches:
            item.stop()
        self.tmp.cleanup()

    def call(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=30)
        connection.request(method, path, body=body, headers={"Cookie": self.cookie, **(headers or {})})
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response, data

    def test_member_session_upload_presence_and_download(self):
        self.cookie = ""
        form = urllib.parse.urlencode({"nickname": "민수", "password": "member-pass-1", "next": "/"})
        response, _ = self.call("POST", "/gateway/login", form,
                                {"Content-Type": "application/x-www-form-urlencoded"})
        self.cookie = response.getheader("Set-Cookie").split(";", 1)[0]
        response, page = self.call("GET", "/")
        self.assertIn('id="dropOverlay"', page.decode("utf-8"))
        same = {"Sec-Fetch-Site": "same-origin"}
        response, _ = self.call("POST", "/api/session", json.dumps({"id": "tab-1"}),
                                {"Content-Type": "application/json", **same})
        self.assertEqual(response.status, 204)
        progress = json.loads(self.call("GET", "/api/progress")[1])
        self.assertEqual([(p["nickname"], p["tabs"]) for p in progress["presence"]], [("민수", 1)])
        response, data = self.call("POST", "/api/upload-agent?filename=main.py&title=&url=", AGENT.encode(),
                                   {"X-League-Upload": "1", "Content-Type": "application/octet-stream", **same})
        uploaded = json.loads(data)
        self.assertEqual(response.status, 200, uploaded)
        self.assertEqual((uploaded["registered_by"], uploaded["title"]), ("민수", "민수 · main.py"))
        agents = json.loads(self.call("GET", "/api/status")[1])["agents"]
        self.assertEqual(agents[0]["author"], "민수")
        response, source = self.call("GET", f"/api/agent-download?agent_id={uploaded['agent_id']}")
        self.assertEqual(source, league.canonical_source(AGENT))
        self.assertIn("filename*=UTF-8''", response.getheader("Content-Disposition"))
        response, data = self.call("GET", f"/api/agent-opponents?agent_id={uploaded['agent_id']}")
        self.assertEqual(json.loads(data)["opponents"], [])
        response, _ = self.call("POST", "/api/settings", b"{}", same)
        self.assertEqual(response.status, 403)


if __name__ == "__main__":
    unittest.main()
