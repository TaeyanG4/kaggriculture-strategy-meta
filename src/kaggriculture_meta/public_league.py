"""Unattended public-notebook collector and native Kaggriculture league.

The service keeps immutable notebook versions and canonical agent sources, while
only the strongest ``top_k`` agents remain active.  Exact source duplicates are
represented by aliases, so the dashboard can show every original notebook title
and URL without wasting matches.
"""
from __future__ import annotations

import argparse
import ast
import base64
import csv
import codeop
import concurrent.futures
import contextlib
import datetime as dt
import hashlib
import io
import json
import lzma
import math
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import urllib.parse
import urllib.request
import zlib
import gzip
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE = ROOT / "state" / "public_league"
DEFAULT_LOCAL_AGENTS = ROOT / "configs" / "public_league_local_agents.json"
KAGGLE = Path(os.environ.get(
    "KAGGLE_EXE",
    r"C:/Users/Taeyang/AppData/Local/Programs/Python/Python312/Scripts/kaggle.exe",
))
SCHEMA_VERSION = 2
RULES_VERSION = "public_league_v2"
ENGINE_CONFIG = {"episodeSteps": 720}
DEFAULT_SETTINGS = {"interval_hours": 3.0, "workers": 8, "max_matches": 240, "port": 8791,
                    "auto_collect_enabled": True}
NONFATAL_TELEMETRY_FAILURES = {"overflow_contract_errors"}
PUBLIC_LEAGUE_CODE_FAILURE_THRESHOLD = 2
PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS = 1220
PUBLIC_LEAGUE_DOCKER_IMAGE = "kaggriculture-public-league:1.32.7"
PUBLIC_LEAGUE_MAX_DATASET_BYTES = 100 * 1024 * 1024
NEWCOMER_PRIORITY_GAMES = 32
DEFAULT_TOP_K = 100
BROWSER_HEARTBEAT_TTL_SECONDS = 180
BROWSER_CLOSE_GRACE_SECONDS = 5


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_source(data: bytes | str) -> bytes:
    if isinstance(data, str):
        data = data.encode("utf-8")
    text = data.decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def subprocess_no_window_flags() -> int:
    """Keep console executables such as docker.exe hidden under pythonw."""
    return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0


def safe_relative_path(value: str) -> str:
    """Return a portable artifact member path, rejecting traversal/absolute paths."""
    value = str(value).replace("\\", "/")
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise ValueError(f"unsafe artifact path: {value!r}")
    while value.startswith("./"):
        value = value[2:]
    parts = value.split("/")
    if not value or any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"unsafe artifact path: {value!r}")
    return "/".join(parts)


def artifact_digest(files: dict[str, bytes]) -> str:
    """Keep the historical main-only identity; hash every byte for bundles."""
    normalized = {safe_relative_path(name): bytes(data) for name, data in files.items()}
    if set(normalized) == {"main.py"}:
        return sha256(canonical_source(normalized["main.py"]))
    digest = hashlib.sha256()
    for name in sorted(normalized):
        payload = canonical_source(normalized[name]) if name.endswith(".py") else normalized[name]
        encoded = name.encode("utf-8")
        digest.update(len(encoded).to_bytes(4, "big")); digest.update(encoded)
        digest.update(len(payload).to_bytes(8, "big")); digest.update(payload)
    return digest.hexdigest()


def safe_component(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-.")
    return value[:100] or "unknown"


@contextmanager
def process_lock(path: Path, stale_seconds=8 * 3600):
    """Cross-process single-cycle lock using an atomic lock-file create."""
    path = Path(path)
    acquired = False
    for _ in range(2):
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, json.dumps({"pid": os.getpid(), "created_at": utcnow()}).encode())
            os.close(fd); acquired = True; break
        except FileExistsError:
            with contextlib.suppress(OSError):
                if time.time() - path.stat().st_mtime > stale_seconds:
                    path.unlink(); continue
            break
    try:
        yield acquired
    finally:
        if acquired:
            path.unlink(missing_ok=True)


class Store:
    def __init__(self, state: Path | str = DEFAULT_STATE):
        self.state = Path(state).resolve()
        self.state.mkdir(parents=True, exist_ok=True)
        (self.state / "sources").mkdir(exist_ok=True)
        (self.state / "artifacts").mkdir(exist_ok=True)
        (self.state / "notebooks").mkdir(exist_ok=True)
        (self.state / "jobs").mkdir(exist_ok=True)
        dashboard = self.state / "dashboard.html"
        if globals().get("DASHBOARD") and (not dashboard.exists() or dashboard.read_text(encoding="utf-8") != DASHBOARD):
            dashboard.write_text(DASHBOARD, encoding="utf-8")
        self.db_path = self.state / "league.sqlite3"
        self.db = sqlite3.connect(self.db_path, timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.migrate()

    def close(self):
        self.db.close()

    def migrate(self):
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS meta(
          key TEXT PRIMARY KEY, value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS notebooks(
          id INTEGER PRIMARY KEY, ref TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
          author TEXT NOT NULL, slug TEXT NOT NULL, url TEXT NOT NULL,
          public_score REAL, public_votes INTEGER, best_public_score REAL,
          score_checked_at TEXT, origin TEXT NOT NULL DEFAULT 'kaggle',
          last_run TEXT, first_seen TEXT NOT NULL,
          last_seen TEXT NOT NULL, current_version_key TEXT
        );
        CREATE TABLE IF NOT EXISTS notebook_versions(
          id INTEGER PRIMARY KEY, notebook_id INTEGER NOT NULL REFERENCES notebooks(id),
          version_key TEXT NOT NULL, metadata_json TEXT NOT NULL,
          archive_path TEXT, status TEXT NOT NULL DEFAULT 'listed', error TEXT,
          first_seen TEXT NOT NULL, pulled_at TEXT,
          UNIQUE(notebook_id, version_key)
        );
        CREATE TABLE IF NOT EXISTS agents(
          id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL UNIQUE, source_path TEXT NOT NULL,
          source_sha256 TEXT, artifact_files_json TEXT,
          execution_platform TEXT NOT NULL DEFAULT 'host',
          qa_status TEXT NOT NULL, entrypoint TEXT, qa_error TEXT,
          created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'candidate',
          rating REAL NOT NULL DEFAULT 1500, games INTEGER NOT NULL DEFAULT 0,
          wins INTEGER NOT NULL DEFAULT 0, losses INTEGER NOT NULL DEFAULT 0,
          ties INTEGER NOT NULL DEFAULT 0, score_low REAL, score_high REAL,
          last_played TEXT
        );
        CREATE TABLE IF NOT EXISTS aliases(
          id INTEGER PRIMARY KEY, agent_id INTEGER NOT NULL REFERENCES agents(id),
          version_id INTEGER NOT NULL REFERENCES notebook_versions(id),
          notebook_title TEXT NOT NULL, notebook_url TEXT NOT NULL,
          author TEXT NOT NULL, ref TEXT NOT NULL, is_current INTEGER NOT NULL DEFAULT 1,
          discovered_at TEXT NOT NULL, UNIQUE(agent_id, version_id)
        );
        CREATE TABLE IF NOT EXISTS matches(
          id INTEGER PRIMARY KEY, match_key TEXT NOT NULL UNIQUE,
          engine_sha TEXT NOT NULL, agent_a INTEGER NOT NULL REFERENCES agents(id),
          agent_b INTEGER NOT NULL REFERENCES agents(id), seed INTEGER NOT NULL,
          seat_a INTEGER NOT NULL, status TEXT NOT NULL, outcome_a REAL,
          reward_a REAL, reward_b REAL, margin_a REAL, runtime REAL,
          error TEXT, result_json TEXT, created_at TEXT NOT NULL,
          completed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS events(
          id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, level TEXT NOT NULL,
          kind TEXT NOT NULL, message TEXT NOT NULL, detail_json TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_matches_agents ON matches(agent_a, agent_b, status);
        CREATE INDEX IF NOT EXISTS idx_alias_agent ON aliases(agent_id);
        """)
        columns = {row[1] for row in self.db.execute("PRAGMA table_info(notebooks)")}
        for name, kind in (("public_votes", "INTEGER"),
                           ("best_public_score", "REAL"),
                           ("score_checked_at", "TEXT"),
                           ("origin", "TEXT NOT NULL DEFAULT 'kaggle'")):
            if name not in columns:
                self.db.execute(f"ALTER TABLE notebooks ADD COLUMN {name} {kind}")
        agent_columns = {row[1] for row in self.db.execute("PRAGMA table_info(agents)")}
        for name, kind in (("source_sha256", "TEXT"),
                           ("artifact_files_json", "TEXT"),
                           ("execution_platform", "TEXT NOT NULL DEFAULT 'host'")):
            if name not in agent_columns:
                self.db.execute(f"ALTER TABLE agents ADD COLUMN {name} {kind}")
        self.db.execute("UPDATE agents SET source_sha256=sha256 WHERE source_sha256 IS NULL")
        self.db.execute("UPDATE agents SET artifact_files_json='[\"main.py\"]' WHERE artifact_files_json IS NULL")
        self.db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)",
                        (str(SCHEMA_VERSION),))
        self.db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('rules_version',?)",
                        (json.dumps(RULES_VERSION),))
        self.db.commit()

    def event(self, kind: str, message: str, detail=None, level="info"):
        self.db.execute(
            "INSERT INTO events(created_at,level,kind,message,detail_json) VALUES(?,?,?,?,?)",
            (utcnow(), level, kind, message,
             json.dumps(detail, ensure_ascii=False, sort_keys=True) if detail is not None else None),
        )
        self.db.commit()

    def set_meta(self, key: str, value):
        self.db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)",
                        (key, json.dumps(value, ensure_ascii=False)))
        self.db.commit()

    def get_meta(self, key: str, default=None):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        if not row:
            return default
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            return row[0]


def runtime_settings(store: Store) -> dict:
    saved = store.get_meta("runtime_settings", {}) or {}
    return {**DEFAULT_SETTINGS, **{k: saved[k] for k in DEFAULT_SETTINGS if k in saved}}


def update_runtime_settings(store: Store, interval_hours, workers) -> dict:
    interval_hours = float(interval_hours)
    workers = int(workers)
    if not 0.25 <= interval_hours <= 168:
        raise ValueError("interval_hours must be between 0.25 and 168")
    if workers not in range(1, 13):
        raise ValueError("workers must be between 1 and 12")
    current = runtime_settings(store)
    minutes = max(15, int(round(interval_hours * 60)))
    script = ROOT / "tools" / "configure-public-league-task.ps1"
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
         "-EveryMinutes", str(minutes), "-Workers", str(workers),
         "-MaxMatches", str(int(current["max_matches"])),
         "-State", "Enabled" if current["auto_collect_enabled"] else "Disabled"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=30, creationflags=flags)
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout or "scheduler update failed")[-1200:])
    updated = {**current, "interval_hours": minutes / 60, "workers": workers}
    store.set_meta("runtime_settings", updated)
    store.event("settings", f"interval {minutes} minutes, workers {workers}", updated)
    return updated


def toggle_auto_collection(store: Store) -> dict:
    current = runtime_settings(store)
    enabled = not bool(current["auto_collect_enabled"])
    script = ROOT / "tools" / "set-public-league-collection.ps1"
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
         "-State", "Enabled" if enabled else "Disabled"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=30, creationflags=flags)
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout or "scheduler toggle failed")[-1200:])
    updated = {**current, "auto_collect_enabled": enabled}
    store.set_meta("runtime_settings", updated)
    store.event("settings", f"automatic collection {'enabled' if enabled else 'disabled'}", updated)
    return updated


def normalize_listing_item(raw: dict) -> dict:
    ref = raw.get("ref") or raw.get("id") or raw.get("kernelRef")
    if not ref or "/" not in ref:
        raise ValueError("missing notebook ref")
    author, slug = ref.split("/", 1)
    title = raw.get("title") or raw.get("kernelTitle") or slug.replace("-", " ")
    last_run = (raw.get("lastRunTime") or raw.get("last_run_time") or
                raw.get("lastUpdated") or raw.get("lastUpdatedTime") or "")
    version = (raw.get("scriptVersionId") or raw.get("versionNumber") or
               raw.get("currentVersionNumber") or raw.get("id_no"))
    stable = str(version) if version is not None else sha256(
        json.dumps({"last_run": last_run, "title": title}, sort_keys=True).encode())[:16]
    score = raw.get("score") or raw.get("kernelScore")
    return {
        "ref": ref, "author": author, "slug": slug, "title": title,
        "url": f"https://www.kaggle.com/code/{ref}", "last_run": str(last_run),
        "version_key": stable, "public_score": float(score) if score is not None else None,
        "public_votes": int(raw["totalVotes"]) if raw.get("totalVotes") is not None else None,
        "best_public_score": None, "score_checked_at": None,
        "raw": raw,
    }


def parse_listing(text: str) -> list[dict]:
    data = json.loads(text.lstrip("\ufeff"))
    if isinstance(data, dict):
        data = data.get("kernels") or data.get("items") or data.get("results") or []
    if not isinstance(data, list):
        raise ValueError("Kaggle listing is not an array")
    rows = []
    for item in data:
        try:
            rows.append(normalize_listing_item(item))
        except (TypeError, ValueError):
            continue
    return rows


def parse_notebook_ref(value: str) -> str | None:
    value = (value or "").strip()
    match = re.search(r"kaggle\.com/code/([^/?#]+/[^/?#]+)", value, re.I)
    if match:
        value = match.group(1)
    value = value.strip("/")
    return value if re.fullmatch(r"[A-Za-z0-9_-]+/[A-Za-z0-9_-]+", value) else None


def _search_local_state(store: Store, row: dict) -> dict:
    local = store.db.execute("""SELECT n.id AS notebook_id,v.status AS version_status,v.error,
        a.id AS agent_id,a.sha256,a.qa_status,a.status AS agent_status
        FROM notebooks n LEFT JOIN notebook_versions v
          ON v.notebook_id=n.id AND v.version_key=n.current_version_key
        LEFT JOIN aliases x ON x.version_id=v.id LEFT JOIN agents a ON a.id=x.agent_id
        WHERE n.ref=? ORDER BY x.is_current DESC,x.id DESC LIMIT 1""", (row["ref"],)).fetchone()
    if not local:
        return {**row, "collected": False, "duplicate_type": None, "duplicate_detail": None}
    if not local["agent_id"]:
        prior = store.db.execute("""SELECT a.id AS agent_id,a.sha256,a.qa_status,a.status AS agent_status,
            v.id AS version_id FROM notebook_versions v JOIN aliases x ON x.version_id=v.id
            JOIN agents a ON a.id=x.agent_id WHERE v.notebook_id=? AND a.qa_status='pass'
            ORDER BY v.id DESC LIMIT 1""", (local["notebook_id"],)).fetchone()
        if prior:
            return {**row, **dict(local), **dict(prior), "collected": True,
                    "duplicate_type": "current_no_source_prior_executable",
                    "duplicate_detail": (f"현재 버전은 실행 source가 없고 이전 실행 가능 버전 "
                                         f"{prior['version_id']}만 대전 가능")}
    detail = ("같은 노트북의 현재 버전이 이미 수집됨" if local["agent_id"] else
              f"같은 노트북이 이미 수집됐지만 실행 agent 없음 ({local['version_status']})")
    return {**row, **dict(local), "collected": True,
            "duplicate_type": "same_notebook", "duplicate_detail": detail}


def search_public_notebooks(store: Store, query: str, limit=20) -> dict:
    query = (query or "").strip()
    if not query:
        raise ValueError("검색어 또는 Kaggle 노트북 URL이 필요합니다.")
    direct = parse_notebook_ref(query)
    if direct:
        known = store.db.execute(
            "SELECT ref,title,author,url,last_run,public_votes FROM notebooks WHERE ref=?", (direct,)).fetchone()
        if known:
            rows = [{**dict(known), "version_key": None, "public_score": None,
                     "best_public_score": None, "score_checked_at": None, "raw": {}}]
        else:
            author, slug = direct.split("/", 1)
            rows = [{"ref": direct, "title": slug.replace("-", " "), "author": author,
                     "slug": slug, "url": f"https://www.kaggle.com/code/{direct}",
                     "last_run": "", "public_votes": None, "public_score": None,
                     "best_public_score": None, "score_checked_at": None, "raw": {}}]
    else:
        text = run_kaggle(["kernels", "list", "--search", query, "--page-size", str(min(int(limit), 50)),
                           "--sort-by", "relevance", "--format", "json"])
        rows = parse_listing(text)
    return {"query": query, "results": [_search_local_state(store, row) for row in rows]}


def add_public_notebook(store: Store, ref: str) -> dict:
    ref = parse_notebook_ref(ref)
    if not ref:
        raise ValueError("올바른 Kaggle 노트북 URL 또는 author/slug가 아닙니다.")
    author, slug = ref.split("/", 1)
    prior_notebook = store.db.execute("SELECT id FROM notebooks WHERE ref=?", (ref,)).fetchone()
    prior_agent_ids = set()
    if prior_notebook:
        prior_agent_ids = {r[0] for r in store.db.execute("""SELECT DISTINCT x.agent_id
            FROM aliases x JOIN notebook_versions v ON v.id=x.version_id
            WHERE v.notebook_id=?""", (prior_notebook["id"],))}
    all_agent_ids = {r[0] for r in store.db.execute("SELECT id FROM agents")}
    manual_root = store.state / "manual_pull"
    manual_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="notebook-", dir=manual_root) as tmp_name:
        tmp = Path(tmp_name)
        run_kaggle(["kernels", "pull", ref, "-p", str(tmp), "-m"], timeout=300)
        metadata_path = tmp / "kernel-metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig")) if metadata_path.exists() else {"id": ref}
        files = [p for p in tmp.rglob("*") if p.is_file()]
        content_key = sha256("".join(
            f"{p.relative_to(tmp).as_posix()}:{sha256(p.read_bytes())}" for p in sorted(files)
        ).encode())[:16]
        version_key = "manual-" + content_key
        target = store.state / "notebooks" / safe_component(author) / safe_component(slug) / version_key
        if not target.exists():
            shutil.copytree(tmp, target)
        dataset_summary = download_notebook_datasets(target, metadata)
    title = metadata.get("title") or slug.replace("-", " ")
    now = utcnow()
    score_row = {"author": author, "slug": slug, "public_votes": None}
    with contextlib.suppress(Exception):
        score_row.update(fetch_public_score(score_row))
    with store.db:
        store.db.execute("""INSERT INTO notebooks(ref,title,author,slug,url,public_score,public_votes,
            best_public_score,score_checked_at,origin,last_run,first_seen,last_seen,current_version_key)
            VALUES(?,?,?,?,?,?,?,?,?,'kaggle',?,?,?,?)
            ON CONFLICT(ref) DO UPDATE SET title=excluded.title,url=excluded.url,
            public_score=COALESCE(excluded.public_score,notebooks.public_score),
            public_votes=COALESCE(excluded.public_votes,notebooks.public_votes),
            best_public_score=COALESCE(excluded.best_public_score,notebooks.best_public_score),
            score_checked_at=COALESCE(excluded.score_checked_at,notebooks.score_checked_at),
            last_seen=excluded.last_seen,current_version_key=excluded.current_version_key""",
            (ref, title, author, slug, f"https://www.kaggle.com/code/{ref}",
             score_row.get("public_score"), score_row.get("public_votes"),
             score_row.get("best_public_score"), score_row.get("score_checked_at"),
             now, now, now, version_key))
        notebook_id = store.db.execute("SELECT id FROM notebooks WHERE ref=?", (ref,)).fetchone()[0]
        existing = store.db.execute(
            "SELECT id,status FROM notebook_versions WHERE notebook_id=? AND version_key=?",
            (notebook_id, version_key)).fetchone()
        if not existing:
            version_id = store.db.execute("""INSERT INTO notebook_versions
                (notebook_id,version_key,metadata_json,archive_path,status,first_seen,pulled_at)
                VALUES(?,?,?,?, 'pulled',?,?)""",
                (notebook_id, version_key, json.dumps(metadata, ensure_ascii=False),
                 str(target), now, now)).lastrowid
        else:
            version_id = existing["id"]
    if not existing:
        extract(store, limit=1000)
    current = store.db.execute("""SELECT v.status,v.error,a.id AS agent_id,a.sha256,a.qa_status,a.status AS agent_status
        FROM notebook_versions v LEFT JOIN aliases x ON x.version_id=v.id
        LEFT JOIN agents a ON a.id=x.agent_id WHERE v.id=?
        ORDER BY x.is_current DESC,x.id DESC LIMIT 1""", (version_id,)).fetchone()
    agent_id = current["agent_id"] if current else None
    fallback = None
    if agent_id is None:
        fallback = store.db.execute("""SELECT a.id AS agent_id,a.sha256,a.qa_status,a.status AS agent_status,
            v.id AS version_id FROM notebook_versions v JOIN aliases x ON x.version_id=v.id
            JOIN agents a ON a.id=x.agent_id WHERE v.notebook_id=? AND a.qa_status='pass'
            ORDER BY v.id DESC LIMIT 1""", (notebook_id,)).fetchone()
        if fallback:
            agent_id = fallback["agent_id"]
    if existing:
        duplicate_type = "same_notebook_same_version"
        duplicate_detail = "같은 노트북의 같은 파일 버전이 이미 수집돼 있음"
    elif fallback:
        duplicate_type = "current_no_source_prior_executable"
        duplicate_detail = (f"현재 저장본에는 실행 agent가 없어 이전 실행 가능 버전 {fallback['version_id']}의 "
                            "agent를 사용함; 현재 코드와 동일하다는 뜻은 아님")
    elif agent_id in prior_agent_ids:
        duplicate_type = "same_notebook_same_source"
        duplicate_detail = "같은 노트북의 새 저장본이지만 실행 source는 기존 버전과 완전히 동일"
    elif agent_id in all_agent_ids:
        duplicate_type = "different_notebook_exact_source"
        duplicate_detail = "다른 노트북이지만 실행 source SHA-256이 기존 agent와 완전히 동일해 별칭으로 묶음"
    elif agent_id is not None:
        duplicate_type = "unique_source"
        duplicate_detail = "기존에 없던 고유 실행 source"
    else:
        duplicate_type = current["status"] if current else "no_source"
        duplicate_detail = current["error"] if current else "실행 가능한 agent source를 찾지 못함"
    result = {"ref": ref, "title": title, "url": f"https://www.kaggle.com/code/{ref}",
              "version_id": version_id, "agent_id": agent_id,
              "datasets": dataset_summary,
              "sha256": (fallback["sha256"] if fallback else
                         current["sha256"] if current and agent_id else None),
              "qa_status": (fallback["qa_status"] if fallback else
                            current["qa_status"] if current and agent_id else None),
              "agent_status": (fallback["agent_status"] if fallback else
                               current["agent_status"] if current and agent_id else None),
              "duplicate_type": duplicate_type, "duplicate_detail": duplicate_detail}
    store.event("manual_add", f"manual notebook add: {ref}", result,
                "info" if agent_id else "warning")
    return result


def run_kaggle(args: list[str], timeout=180) -> str:
    exe = KAGGLE if KAGGLE.exists() else Path("kaggle")
    proc = subprocess.run([str(exe), *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout,
                          env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
                          creationflags=subprocess_no_window_flags())
    if proc.returncode:
        msg = (proc.stderr or proc.stdout).strip()[-1200:]
        raise RuntimeError(f"kaggle {' '.join(args[:3])} failed: {msg}")
    return proc.stdout


def parse_dataset_files_csv(text: str) -> tuple[list[dict], str | None]:
    """Parse Kaggle CLI CSV, which may prepend a pagination-token line."""
    lines = text.splitlines()
    header = next((index for index, line in enumerate(lines)
                   if line.strip().lower().startswith("name,size,")), None)
    if header is None:
        return [], None
    token_match = re.search(r"^Next Page Token\s*=\s*(\S+)\s*$", text, re.MULTILINE)
    rows = list(csv.DictReader(io.StringIO("\n".join(lines[header:]))))
    return rows, token_match.group(1) if token_match else None


def download_notebook_datasets(target: Path, metadata: dict) -> dict:
    """Download small declared datasets so the exact multi-file submission is available."""
    downloaded, skipped, failed = [], [], []
    for ref in metadata.get("dataset_sources") or []:
        if not isinstance(ref, str) or "/" not in ref:
            continue
        destination = target / "_datasets" / safe_component(ref.replace("/", "--"))
        complete_marker = destination / ".public-league-download-complete.json"
        if complete_marker.exists():
            downloaded.append(ref); continue
        try:
            rows, total, token = [], 0, None
            for _ in range(100):
                args = ["datasets", "files", ref, "--csv", "--page-size", "200"]
                if token:
                    args.extend(["--page-token", token])
                page_rows, next_token = parse_dataset_files_csv(
                    run_kaggle(args, timeout=120))
                if not page_rows:
                    break
                for row in page_rows:
                    raw_size = str(row.get("size") or "").strip().replace(",", "")
                    if not raw_size.isdigit():
                        raise ValueError(f"unknown dataset file size: {raw_size!r}")
                    total += int(raw_size)
                rows.extend(page_rows)
                token = next_token
                if total > PUBLIC_LEAGUE_MAX_DATASET_BYTES or not token:
                    break
            if not rows or total > PUBLIC_LEAGUE_MAX_DATASET_BYTES or token:
                reason = "size_limit" if total > PUBLIC_LEAGUE_MAX_DATASET_BYTES else "incomplete_listing"
                skipped.append({"ref": ref, "bytes": total, "reason": reason})
                continue
            destination.mkdir(parents=True, exist_ok=True)
            run_kaggle(["datasets", "download", "-d", ref, "-p", str(destination), "--unzip"],
                       timeout=600)
            complete_marker.write_text(json.dumps(
                {"ref": ref, "bytes": total, "files": len(rows), "completed_at": utcnow()},
                ensure_ascii=False), encoding="utf-8")
            downloaded.append(ref)
        except Exception as exc:
            failed.append({"ref": ref, "error": f"{type(exc).__name__}: {exc}"[:500]})
    return {"downloaded": downloaded, "skipped": skipped, "failed": failed}


def ensure_notebook_datasets(target: Path) -> dict:
    """Backfill attachments for versions pulled before dataset support existed."""
    metadata_path = Path(target) / "kernel-metadata.json"
    if not metadata_path.exists():
        return {"downloaded": [], "skipped": [], "failed": []}
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {"downloaded": [], "skipped": [], "failed": []}
    refs = [ref for ref in metadata.get("dataset_sources") or []
            if isinstance(ref, str) and "/" in ref]
    if not refs:
        return {"downloaded": [], "skipped": [], "failed": []}
    return download_notebook_datasets(Path(target), {"dataset_sources": refs})


def _published_output_names(text: str) -> list[str]:
    """Select runtime artifacts from a ``kaggle kernels files`` listing."""
    try:
        rows = json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return []
    if not isinstance(rows, list):
        return []
    names = []
    for row in rows:
        name = row.get("name") if isinstance(row, dict) else None
        if not isinstance(name, str):
            continue
        with contextlib.suppress(ValueError):
            name = safe_relative_path(name)
            low = name.lower()
            if (low.endswith((".py", ".so", ".dll", ".dylib", ".npz", ".npy",
                              ".pkl", ".pickle", ".joblib", ".json", ".bin", ".dat"))
                    or low.endswith((".tar.gz", ".tgz", ".tar"))):
                names.append(name)
    primary = [name for name in names if Path(name).name.lower() in
               ("main.py", "submission.py", "agent.py", "kaggle_agent.py",
                "submission.tar.gz", "submission.tgz", "submission.tar")]
    return sorted(set(names)) if primary else []


def ensure_notebook_outputs(target: Path, ref: str) -> dict:
    """Download the current saved notebook's published submission output.

    No notebook cell is executed.  Extraction and official first-action QA
    still decide whether the downloaded output is an executable agent.
    """
    target = Path(target)
    destination = target / "_published_output"
    marker = destination / ".public-league-output-complete.json"
    if marker.exists():
        with contextlib.suppress(OSError, UnicodeError, json.JSONDecodeError):
            saved = json.loads(marker.read_text(encoding="utf-8"))
            if saved.get("ref") == ref:
                return {"downloaded": saved.get("files", []), "failed": []}
    try:
        listing = run_kaggle(["kernels", "files", ref, "--format", "json",
                              "--page-size", "200"], timeout=120)
        names = _published_output_names(listing)
        if not names:
            return {"downloaded": [], "failed": []}
        pattern = "^(?:" + "|".join(re.escape(name) for name in names) + ")$"
        with tempfile.TemporaryDirectory(prefix="published-output-", dir=target) as tmp_name:
            work = Path(tmp_name)
            run_kaggle(["kernels", "output", ref, "-p", str(work), "-o", "-q",
                        "--file-pattern", pattern], timeout=600)
            selected, total = {}, 0
            for item in sorted(work.rglob("*")):
                if not item.is_file():
                    continue
                relative = item.relative_to(work).as_posix()
                # Kaggle may emit the run log despite the requested pattern.
                match = next((name for name in names
                              if relative == name or item.name == Path(name).name), None)
                if match is None:
                    continue
                size = item.stat().st_size
                if size > PUBLIC_LEAGUE_MAX_DATASET_BYTES or total + size > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                    raise ValueError("published notebook output exceeds size limit")
                selected[match] = item.read_bytes(); total += size
            if not selected:
                raise ValueError("published output listed submission files but returned none")
            destination.mkdir(parents=True, exist_ok=True)
            for name, payload in selected.items():
                output = destination / safe_relative_path(name)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(payload)
        summary = {"ref": ref, "files": sorted(selected), "bytes": total,
                   "completed_at": utcnow()}
        marker.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"downloaded": summary["files"], "failed": []}
    except Exception as exc:
        return {"downloaded": [],
                "failed": [{"ref": ref, "error": f"{type(exc).__name__}: {exc}"[:500]}]}


def fetch_public_score(row: dict, timeout=15) -> dict:
    """Read the current linked-submission score from Kaggle's public view model."""
    payload = json.dumps({"authorUserName": row["author"], "kernelSlug": row["slug"],
                          "kernelVersionId": 0}).encode()
    request = urllib.request.Request(
        "https://www.kaggle.com/api/i/kernels.LegacyKernelsService/GetKernelViewModel",
        data=payload,
        headers={"accept": "application/json", "content-type": "application/json",
                 "user-agent": "Kaggriculture-Public-League/1"},
        method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        model = json.loads(response.read())
    kernel = model.get("kernel") or {}
    submission = model.get("submission") or {}
    best = model.get("bestSubmissionScore") or {}
    current = submission.get("scoreFormatted")
    best_score = best.get("scoreFormatted")
    if best_score is None:
        best_score = kernel.get("bestPublicScore")
    return {
        "public_score": float(current) if current not in (None, "") else None,
        "best_public_score": float(best_score) if best_score not in (None, "") else None,
        "public_votes": int(kernel["upvoteCount"]) if kernel.get("upvoteCount") is not None
                        else row.get("public_votes"),
        "score_checked_at": utcnow(),
    }


def enrich_public_scores(rows: list[dict], workers=8) -> dict:
    """Fetch scores concurrently; a failed lookup leaves the prior DB value intact."""
    checked = failed = 0
    if not rows:
        return {"checked": 0, "failed": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(rows))) as pool:
        futures = {pool.submit(fetch_public_score, row): row for row in rows}
        for future in concurrent.futures.as_completed(futures):
            row = futures[future]
            try:
                row.update(future.result())
                checked += 1
            except Exception as exc:
                row["score_error"] = f"{type(exc).__name__}: {exc}"[:500]
                failed += 1
    return {"checked": checked, "failed": failed}


def collect(store: Store, limit=200, pull_limit=40) -> dict:
    """Fetch score and recency listings; pull only unseen notebook versions."""
    gathered = {}
    raw_dir = store.state / "listings"
    raw_dir.mkdir(exist_ok=True)
    listings = [
        (f"competition-{sort}", ["--competition", "kaggriculture", "--sort-by", sort])
        for sort in ("scoreDescending", "dateRun")
    ] + [
        (f"search-{sort}", ["--search", "kaggriculture", "--sort-by", sort])
        for sort in ("scoreDescending", "dateRun")
    ]
    for label, selector in listings:
        text = run_kaggle(["kernels", "list", *selector,
                           "--page-size", str(limit), "--format", "json"])
        (raw_dir / f"{dt.datetime.now():%Y%m%d-%H%M%S}-{label}.json").write_text(
            text, encoding="utf-8")
        for row in parse_listing(text):
            gathered[row["ref"]] = row
    score_summary = enrich_public_scores(list(gathered.values()))
    now = utcnow()
    unseen = []
    with store.db:
        for row in gathered.values():
            store.db.execute("""
              INSERT INTO notebooks(ref,title,author,slug,url,public_score,public_votes,best_public_score,
                score_checked_at,last_run,first_seen,last_seen,current_version_key)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
              ON CONFLICT(ref) DO UPDATE SET title=excluded.title,url=excluded.url,
                public_score=COALESCE(excluded.public_score,notebooks.public_score),
                public_votes=COALESCE(excluded.public_votes,notebooks.public_votes),
                best_public_score=COALESCE(excluded.best_public_score,notebooks.best_public_score),
                score_checked_at=COALESCE(excluded.score_checked_at,notebooks.score_checked_at),last_run=excluded.last_run,
                last_seen=excluded.last_seen,current_version_key=excluded.current_version_key
            """, (row["ref"], row["title"], row["author"], row["slug"], row["url"],
                  row["public_score"], row["public_votes"], row["best_public_score"],
                  row["score_checked_at"], row["last_run"], now, now, row["version_key"]))
            nb = store.db.execute("SELECT id FROM notebooks WHERE ref=?", (row["ref"],)).fetchone()[0]
            cur = store.db.execute(
                "SELECT id,status FROM notebook_versions WHERE notebook_id=? AND version_key=?",
                (nb, row["version_key"])).fetchone()
            if not cur:
                q = store.db.execute("""
                  INSERT INTO notebook_versions(notebook_id,version_key,metadata_json,first_seen)
                  VALUES(?,?,?,?)
                """, (nb, row["version_key"], json.dumps(row["raw"], ensure_ascii=False), now))
                unseen.append((q.lastrowid, nb, row))
    # Resume every previously listed/deferred version.  A pull limit is a queue
    # bound, not a reason to forget work after the first listing cycle.
    pending = store.db.execute("""SELECT v.id,n.ref,n.author,n.slug,n.title,n.url,
        n.public_score,n.last_run,v.version_key,v.metadata_json
        FROM notebook_versions v JOIN notebooks n ON n.id=v.notebook_id
        WHERE v.status IN ('listed','pull_failed')
        ORDER BY COALESCE(n.public_score,-1) DESC,n.last_run DESC,v.id DESC""").fetchall()
    pulled = failed = 0
    for queued in pending[:pull_limit]:
        version_id = queued["id"]
        row = dict(queued)
        target = (store.state / "notebooks" / safe_component(row["author"]) /
                  safe_component(row["slug"]) / safe_component(row["version_key"]))
        target.mkdir(parents=True, exist_ok=True)
        try:
            run_kaggle(["kernels", "pull", row["ref"], "-p", str(target), "-m"], timeout=300)
            metadata_path = target / "kernel-metadata.json"
            metadata = (json.loads(metadata_path.read_text(encoding="utf-8-sig"))
                        if metadata_path.exists() else json.loads(row["metadata_json"] or "{}"))
            dataset_summary = download_notebook_datasets(target, metadata)
            with store.db:
                store.db.execute("""UPDATE notebook_versions SET archive_path=?,status='pulled',pulled_at=?,error=NULL
                                    WHERE id=?""", (str(target), utcnow(), version_id))
            if dataset_summary["failed"] or dataset_summary["skipped"]:
                store.event("dataset", f"dataset attachment partial: {row['ref']}", dataset_summary, "warning")
            pulled += 1
        except Exception as exc:
            with store.db:
                store.db.execute("UPDATE notebook_versions SET status='pull_failed',error=? WHERE id=?",
                                 (str(exc)[:1200], version_id))
            failed += 1
    summary = {"listed": len(gathered), "scores": score_summary, "new_versions": len(unseen),
               "queued_before_pull": len(pending), "pulled": pulled, "pull_failed": failed,
               "deferred": max(0, len(pending)-pull_limit)}
    store.set_meta("last_crawl", {"at": utcnow(), **summary})
    store.event("crawl", f"listed {len(gathered)}, pulled {pulled}, failed {failed}", summary,
                "warning" if failed else "info")
    return summary


def import_existing(store: Store, roots: list[Path]) -> dict:
    """Register already-pulled public notebooks without copying or deleting them."""
    metadata_files = []
    for root in roots:
        root = Path(root).resolve()
        if root.is_file() and root.name == "kernel-metadata.json":
            metadata_files.append(root)
        elif root.exists():
            metadata_files.extend(root.rglob("kernel-metadata.json"))
    imported = skipped = failed = 0
    for metadata_path in sorted(set(metadata_files)):
        try:
            meta = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
            ref = meta.get("id") or meta.get("ref")
            if not ref or "/" not in ref:
                skipped += 1; continue
            author, slug = ref.split("/", 1)
            title = meta.get("title") or slug.replace("-", " ")
            files = [p for p in metadata_path.parent.rglob("*") if p.is_file()]
            version_key = "local-" + sha256("".join(
                f"{p.relative_to(metadata_path.parent)}:{sha256(p.read_bytes())}" for p in sorted(files)
            ).encode())[:16]
            now = utcnow()
            with store.db:
                store.db.execute("""INSERT INTO notebooks(ref,title,author,slug,url,first_seen,last_seen,current_version_key)
                    VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(ref) DO UPDATE SET title=excluded.title,
                    last_seen=excluded.last_seen,current_version_key=excluded.current_version_key""",
                    (ref, title, author, slug, f"https://www.kaggle.com/code/{ref}", now, now, version_key))
                notebook_id = store.db.execute("SELECT id FROM notebooks WHERE ref=?", (ref,)).fetchone()[0]
                cursor = store.db.execute("""INSERT OR IGNORE INTO notebook_versions
                    (notebook_id,version_key,metadata_json,archive_path,status,first_seen,pulled_at)
                    VALUES(?,?,?,?,'pulled',?,?)""",
                    (notebook_id, version_key, json.dumps(meta, ensure_ascii=False),
                     str(metadata_path.parent), now, now))
                if cursor.rowcount:
                    imported += 1
                else:
                    skipped += 1
        except Exception as exc:
            failed += 1
            store.event("import", f"failed to import {metadata_path}", {"error": str(exc)}, "warning")
    summary = {"metadata_found": len(metadata_files), "imported": imported,
               "already_known": skipped, "failed": failed}
    store.event("import", f"imported {imported} existing notebook versions", summary,
                "warning" if failed else "info")
    return summary


def import_local_agents(store: Store, config_path=DEFAULT_LOCAL_AGENTS) -> dict:
    """Add our strongest distinct source files; exact public duplicates are skipped."""
    config_path = Path(config_path)
    if not config_path.exists():
        return {"configured": 0, "imported": 0, "duplicates_skipped": 0, "failed": 0}
    configured = json.loads(config_path.read_text(encoding="utf-8-sig"))
    entries = configured.get("agents", configured) if isinstance(configured, dict) else configured
    imported = duplicates = failed = 0
    for item in entries:
        try:
            path = (ROOT / item["path"]).resolve()
            data = canonical_source(path.read_bytes())
            digest = sha256(data)
            if store.db.execute("SELECT 1 FROM agents WHERE sha256=?", (digest,)).fetchone():
                duplicates += 1
                continue
            saved = store.state / "sources" / f"{digest}.py"
            if not saved.exists():
                saved.write_bytes(data)
            qa = qa_source(saved)
            name = safe_component(item["name"])
            now = utcnow()
            ref = f"local/{name}"
            version_key = "source-" + digest[:16]
            title = item.get("title") or item["name"]
            url = item.get("url") or ""
            published = item.get("published_at") or now
            with store.db:
                store.db.execute("""INSERT INTO notebooks
                    (ref,title,author,slug,url,origin,last_run,first_seen,last_seen,current_version_key)
                    VALUES(?,?,?,?,?,'local',?,?,?,?)
                    ON CONFLICT(ref) DO UPDATE SET title=excluded.title,url=excluded.url,
                    last_run=excluded.last_run,last_seen=excluded.last_seen,
                    current_version_key=excluded.current_version_key""",
                    (ref, title, item.get("author", "Taeyang"), name, url,
                     published, now, now, version_key))
                notebook_id = store.db.execute("SELECT id FROM notebooks WHERE ref=?", (ref,)).fetchone()[0]
                version_id = store.db.execute("""INSERT INTO notebook_versions
                    (notebook_id,version_key,metadata_json,archive_path,status,error,first_seen,pulled_at)
                    VALUES(?,?,?,?,?,?,?,?)""",
                    (notebook_id, version_key, json.dumps(item, ensure_ascii=False), str(path.parent),
                     "extracted" if qa["ok"] else "quarantine", None if qa["ok"] else qa.get("error"),
                     now, now)).lastrowid
                agent_id = store.db.execute("""INSERT INTO agents
                    (sha256,source_path,source_sha256,artifact_files_json,execution_platform,
                     qa_status,entrypoint,qa_error,created_at,status)
                    VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (digest, str(saved), digest, '["main.py"]', "host",
                     "pass" if qa["ok"] else "failed", qa.get("entrypoint"),
                     qa.get("error"), now, "candidate" if qa["ok"] else "quarantine")).lastrowid
                store.db.execute("""INSERT INTO aliases
                    (agent_id,version_id,notebook_title,notebook_url,author,ref,is_current,discovered_at)
                    VALUES(?,?,?,?,?,?,1,?)""",
                    (agent_id, version_id, title, url, item.get("author", "Taeyang"), ref, now))
            imported += 1
        except Exception as exc:
            failed += 1
            store.event("local_import", f"failed to import {item.get('name', 'unknown')}",
                        {"error": str(exc)}, "warning")
    summary = {"configured": len(entries), "imported": imported,
               "duplicates_skipped": duplicates, "failed": failed}
    if imported or failed:
        store.event("local_import", f"imported {imported}, skipped duplicate {duplicates}", summary,
                    "warning" if failed else "info")
    return summary


def _cell_source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def _decompress_zlib_bounded(payload: bytes, limit=10_000_000) -> bytes:
    """Decompress a public-notebook payload without accepting a zip bomb."""
    decoder = zlib.decompressobj()
    data = decoder.decompress(payload, limit + 1)
    if len(data) > limit or decoder.unconsumed_tail or not decoder.eof:
        raise ValueError("packed source exceeds limit or is incomplete")
    data += decoder.flush(limit + 1 - len(data))
    if len(data) > limit:
        raise ValueError("packed source exceeds limit")
    return data


def _decompress_gzip_bounded(payload: bytes, limit=10_000_000) -> bytes:
    """Decompress one gzip stream while enforcing the same output limit."""
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    data = decoder.decompress(payload, limit + 1)
    if len(data) > limit or decoder.unconsumed_tail or not decoder.eof:
        raise ValueError("packed source exceeds limit or is incomplete")
    data += decoder.flush(limit + 1 - len(data))
    if len(data) > limit:
        raise ValueError("packed source exceeds limit")
    return data


def _decompress_lzma_bounded(payload: bytes, limit=10_000_000) -> bytes:
    decoder = lzma.LZMADecompressor()
    data = decoder.decompress(payload, max_length=limit + 1)
    if len(data) > limit or not decoder.eof or decoder.unused_data:
        raise ValueError("packed source exceeds limit or is incomplete")
    return data


def _static_literal_value(node: ast.AST, values: dict[str, object], depth=0):
    """Evaluate a small, side-effect-free AST subset used by artifact builders."""
    if depth > 30:
        raise ValueError("literal expression nesting limit")
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (str, bytes, int, float, bool, type(None))):
            return node.value
        raise ValueError("unsupported constant")
    if isinstance(node, ast.Name):
        if node.id not in values:
            raise ValueError(f"unknown literal name {node.id}")
        return values[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        items = [_static_literal_value(item, values, depth + 1) for item in node.elts]
        return items if isinstance(node, ast.List) else tuple(items)
    if isinstance(node, ast.JoinedStr):
        parts = []
        for item in node.values:
            if isinstance(item, ast.Constant) and isinstance(item.value, str):
                parts.append(item.value)
            elif isinstance(item, ast.FormattedValue):
                value = _static_literal_value(item.value, values, depth + 1)
                if not isinstance(value, (str, int, float)):
                    raise ValueError("unsupported formatted literal")
                parts.append(str(value))
            else:
                raise ValueError("unsupported joined string")
        return "".join(parts)
    if isinstance(node, ast.Dict):
        return {_static_literal_value(key, values, depth + 1):
                _static_literal_value(value, values, depth + 1)
                for key, value in zip(node.keys, node.values) if key is not None}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _static_literal_value(node.left, values, depth + 1)
        right = _static_literal_value(node.right, values, depth + 1)
        if isinstance(left, (str, bytes, list, tuple)) and isinstance(right, type(left)):
            return left + right
        raise ValueError("unsupported literal addition")
    if not isinstance(node, ast.Call):
        raise ValueError("unsupported literal expression")

    args = [_static_literal_value(item, values, depth + 1) for item in node.args]
    func = node.func
    if isinstance(func, ast.Name) and func.id in ("bytes", "str", "list", "tuple", "dict"):
        if len(args) != 1:
            raise ValueError("invalid literal constructor")
        return {"bytes": bytes, "str": str, "list": list, "tuple": tuple, "dict": dict}[func.id](args[0])
    if not isinstance(func, ast.Attribute):
        raise ValueError("unsupported literal call")
    if isinstance(func.value, ast.Name) and func.value.id == "base64" and len(args) == 1:
        decoder = {"b85decode": base64.b85decode, "a85decode": base64.a85decode,
                   "b64decode": base64.b64decode}.get(func.attr)
        if decoder:
            payload = args[0].encode("ascii") if isinstance(args[0], str) else args[0]
            if not isinstance(payload, bytes):
                raise ValueError("encoded payload is not bytes")
            return decoder(payload)
    if isinstance(func.value, ast.Name) and func.attr == "decompress" and len(args) == 1:
        payload = args[0]
        if not isinstance(payload, bytes):
            raise ValueError("compressed payload is not bytes")
        if func.value.id == "zlib":
            return _decompress_zlib_bounded(payload, PUBLIC_LEAGUE_MAX_DATASET_BYTES)
        if func.value.id == "gzip":
            return _decompress_gzip_bounded(payload, PUBLIC_LEAGUE_MAX_DATASET_BYTES)
        if func.value.id == "lzma":
            return _decompress_lzma_bounded(payload, PUBLIC_LEAGUE_MAX_DATASET_BYTES)
    receiver = _static_literal_value(func.value, values, depth + 1)
    if func.attr == "encode" and isinstance(receiver, str) and len(args) <= 1:
        return receiver.encode(args[0] if args else "utf-8")
    if func.attr == "decode" and isinstance(receiver, bytes) and len(args) <= 1:
        return receiver.decode(args[0] if args else "utf-8")
    if func.attr == "join" and isinstance(receiver, (str, bytes)) and len(args) == 1:
        return receiver.join(args[0])
    raise ValueError("unsupported literal call")


def _official_source(payload: object) -> bytes | None:
    if not isinstance(payload, (str, bytes)):
        return None
    with contextlib.suppress(UnicodeError, SyntaxError):
        source = canonical_source(payload)
        tree = ast.parse(source.decode("utf-8"))
        if any((isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                and (item.name in ("agent", "kaggle_submission_agent")
                     or item.name.lower().endswith("_agent"))) or
               (isinstance(item, (ast.Assign, ast.AnnAssign)) and any(
                    isinstance(target, ast.Name) and target.id in ("agent", "kaggle_submission_agent")
                    for target in (item.targets if isinstance(item, ast.Assign) else [item.target])))
               for item in tree.body):
            return source
    return None


def _packed_chunks(value: object) -> bytes | None:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, (list, tuple)) and value:
        parts = [_packed_chunks(item) for item in value]
        if all(part is not None for part in parts):
            return b"".join(parts)
    return None


def _payload_candidates(value: object) -> list[bytes]:
    """Return bounded raw/decoded/decompressed forms of a literal payload."""
    raw = _packed_chunks(value)
    if raw is None:
        return []
    queue, found, seen = [raw], [], set()
    while queue and len(seen) < 20:
        item = queue.pop(0)
        digest = sha256(item)
        if digest in seen or len(item) > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
            continue
        seen.add(digest); found.append(item)
        for transform in (base64.b85decode, base64.a85decode, base64.b64decode,
                          lambda data: _decompress_zlib_bounded(data, PUBLIC_LEAGUE_MAX_DATASET_BYTES),
                          lambda data: _decompress_gzip_bounded(data, PUBLIC_LEAGUE_MAX_DATASET_BYTES),
                          lambda data: _decompress_lzma_bounded(data, PUBLIC_LEAGUE_MAX_DATASET_BYTES)):
            with contextlib.suppress(Exception):
                result = transform(item)
                if isinstance(result, bytes) and sha256(result) not in seen:
                    queue.append(result)
    return found


def _mapping_artifact(value: object) -> dict[str, bytes] | None:
    if not isinstance(value, dict):
        return None
    files = {}
    for raw_name, descriptor in value.items():
        if not isinstance(raw_name, str):
            continue
        with contextlib.suppress(ValueError):
            name = safe_relative_path(raw_name)
            expected = None
            payload = descriptor
            if isinstance(descriptor, dict) and "payload" in descriptor:
                payload = descriptor["payload"]
                expected = descriptor.get("sha256")
            selected = None
            for candidate in _payload_candidates(payload):
                if expected and (not isinstance(expected, str) or sha256(candidate) != expected.lower()):
                    continue
                if name.endswith(".py"):
                    with contextlib.suppress(UnicodeError, SyntaxError):
                        canonical_source(candidate)
                        compile(canonical_source(candidate), name, "exec")
                        selected = canonical_source(candidate); break
                elif expected or candidate == _packed_chunks(payload):
                    selected = candidate; break
            if selected is not None:
                files[name] = selected
    return files if "main.py" in files else None


def _path_basename(node: ast.AST, paths: dict[str, str]) -> str | None:
    if isinstance(node, ast.Name):
        return paths.get(node.id)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Path" and node.args:
        with contextlib.suppress(Exception):
            return Path(str(ast.literal_eval(node.args[0]))).name
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        with contextlib.suppress(Exception):
            value = ast.literal_eval(node.right)
            if isinstance(value, str):
                return Path(value).name
    return None


def literal_packed_sources_from_tree(tree: ast.AST) -> list[tuple[str, dict[str, bytes]]]:
    """Recover literal source/maps/archives without executing a notebook cell."""
    values: dict[str, object] = {}
    paths: dict[str, str] = {}
    found: list[tuple[str, dict[str, bytes]]] = []
    for node in getattr(tree, "body", []):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else (
            node.target if isinstance(node, ast.AnnAssign) else None)
        if not isinstance(target, ast.Name):
            continue
        path_name = _path_basename(node.value, paths)
        if path_name:
            paths[target.id] = path_name
        with contextlib.suppress(Exception):
            values[target.id] = _static_literal_value(node.value, values)

    pinned = [value.lower() for name, value in values.items()
              if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value)
              and "SHA" in name.upper() and "ARCHIVE" not in name.upper()]
    written = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in ("write_bytes", "write_text") or not node.args:
            continue
        name = _path_basename(node.func.value, paths)
        if not name:
            continue
        with contextlib.suppress(Exception, ValueError):
            name = safe_relative_path(name)
            payload = _static_literal_value(node.args[0], values)
            if isinstance(payload, str):
                payload = payload.encode("utf-8")
            if isinstance(payload, bytes):
                written[name] = canonical_source(payload) if name.endswith(".py") else payload
    if "main.py" in written:
        found.append(("literal:writes", written))
    for filename, payload in written.items():
        found.extend((f"literal-written-archive:{filename}:{origin}", files)
                     for origin, files in artifacts_from_archive_bytes(payload, filename))

    for name, value in values.items():
        mapped = _mapping_artifact(value)
        if mapped:
            found.append((f"literal-map:{name}", mapped))
        for candidate in _payload_candidates(value):
            source = _official_source(candidate)
            if source and (not pinned or sha256(candidate) in pinned or sha256(source) in pinned):
                sidecars = {filename: payload for filename, payload in written.items()
                            if filename != "submission.tar.gz"
                            and (filename == "main.py" or not filename.endswith(".py"))}
                sidecars["main.py"] = source
                found.append((f"literal-source:{name}", sidecars))
            found.extend((f"literal-archive:{name}:{origin}", files)
                         for origin, files in artifacts_from_archive_bytes(candidate, name))
    return found


def _static_tree_from_cell(source: str) -> ast.AST | None:
    """Parse a cell, salvaging complete top-level literal assignments only.

    Some published notebooks contain copied display text after a valid packed
    assignment.  We do not repair or execute the cell; we isolate only
    syntactically complete column-zero assignments for the literal decoder.
    """
    try:
        return ast.parse(source)
    except SyntaxError:
        pass
    lines = source.splitlines(keepends=True)
    recovered = []
    for start, line in enumerate(lines):
        if not re.match(r"^[A-Za-z_]\w*\s*(?::[^=]+)?=", line):
            continue
        block = ""
        for end in range(start, len(lines)):
            block += lines[end]
            try:
                compiled = codeop.compile_command(block, symbol="exec")
            except (SyntaxError, OverflowError, ValueError):
                break
            if compiled is None:
                continue
            with contextlib.suppress(SyntaxError):
                tree = ast.parse(block)
                recovered.extend(node for node in tree.body
                                  if isinstance(node, (ast.Assign, ast.AnnAssign)))
            break
    return ast.Module(body=recovered, type_ignores=[]) if recovered else None


def _pinned_remote_artifacts(tree: ast.AST, cache_root: Path) -> list[tuple[str, dict[str, bytes]]]:
    """Fetch a public archive only when the cell pins its exact SHA-256."""
    values = {}
    for node in getattr(tree, "body", []):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else (
            node.target if isinstance(node, ast.AnnAssign) else None)
        if not isinstance(target, ast.Name):
            continue
        with contextlib.suppress(Exception):
            values[target.id] = _static_literal_value(node.value, values)
    urls = [(name, value) for name, value in values.items()
            if isinstance(value, str) and value.startswith("https://")
            and value.lower().endswith((".tar.gz", ".tgz", ".tar"))]
    expected = [(name, value.lower()) for name, value in values.items()
                if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value)
                and any(marker in name.upper() for marker in ("EXPECTED", "ARCHIVE_SHA"))]
    found = []
    for url_name, url in urls:
        host = (urllib.parse.urlparse(url).hostname or "").lower()
        if host not in ("raw.githubusercontent.com", "github.com"):
            continue
        # Archive builders normally expose one archive digest.  Refuse an
        # ambiguous cell instead of guessing between source/member hashes.
        archive_hashes = [digest for name, digest in expected
                          if "MAIN" not in name.upper() and "SOURCE" not in name.upper()]
        fixed_release = host == "github.com" and "/releases/download/" in url
        if len(archive_hashes) > 1 or (not archive_hashes and not fixed_release):
            continue
        digest = archive_hashes[0] if archive_hashes else None
        cache_key = digest or ("url-" + sha256(url.encode()))
        cache = cache_root / "_remote" / f"{cache_key}.tar.gz"
        payload = None
        if cache.exists() and cache.stat().st_size <= PUBLIC_LEAGUE_MAX_DATASET_BYTES:
            candidate = cache.read_bytes()
            if digest is None or sha256(candidate) == digest:
                payload = candidate
        if payload is None:
            request = urllib.request.Request(url, headers={"user-agent": "Kaggriculture-Public-League/1"})
            with urllib.request.urlopen(request, timeout=60) as response:
                chunks, total = [], 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                        raise ValueError("remote archive exceeds size limit")
                    chunks.append(chunk)
            candidate = b"".join(chunks)
            if digest is not None and sha256(candidate) != digest:
                continue
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(candidate)
            payload = candidate
        provenance = "pinned-remote" if digest else "fixed-release-remote"
        found.extend((f"{provenance}:{url_name}:{origin}", files)
                     for origin, files in artifacts_from_archive_bytes(payload, Path(url).name))
    return found


def _v23_external_output_artifact(doc: dict, cache_root: Path) -> list[tuple[str, dict[str, bytes]]]:
    """Reproduce the published V23 recipe from its SHA-pinned donor output."""
    cells = [_cell_source(cell) for cell in doc.get("cells", []) if cell.get("cell_type") == "code"]
    joined = "\n".join(cells)
    if "__V23_ROUTE_BLOB__" not in joined or "DONOR_HANDLE" not in joined:
        return []
    values = {}
    for source in cells:
        tree = _static_tree_from_cell(source)
        if tree is None:
            continue
        local = dict(values)
        for node in tree.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else (
                node.target if isinstance(node, ast.AnnAssign) else None)
            if not isinstance(target, ast.Name):
                continue
            with contextlib.suppress(Exception):
                local[target.id] = _static_literal_value(node.value, local)
        values.update(local)
    required = ("EXPECTED_MAIN_SHA256", "DONOR_HANDLE", "DONOR_SHA256", "V23_TEMPLATE_B64")
    if not all(isinstance(values.get(name), str) for name in required):
        return []
    expected_main = values["EXPECTED_MAIN_SHA256"].lower()
    donor_sha = values["DONOR_SHA256"].lower()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_main) or not re.fullmatch(r"[0-9a-f]{64}", donor_sha):
        return []
    handle = values["DONOR_HANDLE"].replace("/versions/", "/")
    destination = cache_root / "_notebook_outputs" / safe_component(handle.replace("/", "--"))
    donor = destination / "main.py"
    if not donor.exists() or sha256(donor.read_bytes()) != donor_sha:
        destination.mkdir(parents=True, exist_ok=True)
        run_kaggle(["kernels", "output", handle, "-p", str(destination), "-o",
                    "--file-pattern", "^main\\.py$"], timeout=300)
    donor_bytes = donor.read_bytes()
    if sha256(donor_bytes) != donor_sha:
        return []
    donor_tree = ast.parse(donor_bytes)
    assignment = next((node for node in donor_tree.body
                       if isinstance(node, ast.Assign) and node.targets
                       and isinstance(node.targets[0], ast.Tuple)
                       and [item.id for item in node.targets[0].elts if isinstance(item, ast.Name)]
                       == ["SCHEDULES", "POLICY"]), None)
    if assignment is None:
        return []
    donor_blob = next((node.value for node in ast.walk(assignment.value)
                       if isinstance(node, ast.Constant) and isinstance(node.value, str)), None)
    if donor_blob is None:
        return []
    schedules, _ = json.loads(_decompress_zlib_bounded(base64.b85decode(donor_blob)))
    if len(schedules) != 5 or any(len(route) != 719 for route in schedules):
        return []
    base = json.loads(json.dumps(schedules[0]))
    route_payload = {"base": base, "patches": {}}
    for branch in (1, 2, 3, 4):
        tape = json.loads(json.dumps(schedules[branch]))
        tape[:144] = json.loads(json.dumps(base[:144]))
        if branch in (3, 4):
            tape[144:288] = json.loads(json.dumps(schedules[2][144:288]))
        route_payload["patches"][str(branch)] = [
            [step, action] for step, action in enumerate(tape) if action != base[step]
        ]
    route_blob = base64.b85encode(zlib.compress(
        json.dumps(route_payload, separators=(",", ":")).encode(), 9)).decode()
    template_b64 = "".join(values["V23_TEMPLATE_B64"].split())
    template_b64 = template_b64.replace("j1upVZZ0tyhW", "j1upVZ0tyhW")
    template_b64 = template_b64.replace("xHeLNAMGEliRp", "xHeLNAMdliRp")
    template = _decompress_zlib_bounded(base64.b64decode(template_b64, validate=True)).decode("utf-8")
    request = urllib.request.Request("https://www.apache.org/licenses/LICENSE-2.0.txt",
                                     headers={"user-agent": "Kaggriculture-Public-League/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        license_text = response.read().decode("utf-8").replace("\r\n", "\n")
    if sha256(license_text.encode()) != "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30":
        return []
    notice = "# SPDX-License-Identifier: Apache-2.0\n"
    notice += "# v23 modifications: public production router, audited Python chassis, and build tooling.\n"
    notice += "# Credits: thomastschinkel, yhay81, tetsutani; offline simulator: destbreso/nikital7.\n"
    notice += "".join("# " + line + "\n" for line in license_text.splitlines())
    source = (notice + template.replace("__V23_ROUTE_BLOB__", repr(route_blob))).encode("utf-8")
    if sha256(source) != expected_main or not _official_source(source):
        return []
    return [("pinned-kaggle-output:v23-recipe", {"main.py": canonical_source(source)})]


def packed_artifacts_from_tree(tree: ast.AST) -> list[tuple[str, dict[str, bytes]]]:
    """Statically recover literal packed-file dictionaries without executing code."""
    mappings: dict[str, dict] = {}
    for node in getattr(tree, "body", []):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = node.targets[0] if isinstance(node, ast.Assign) and node.targets else node.target
        if not isinstance(target, ast.Name) or not isinstance(node.value, ast.Dict):
            continue
        with contextlib.suppress(ValueError, TypeError, SyntaxError):
            value = ast.literal_eval(node.value)
            if isinstance(value, dict):
                mappings[target.id] = value

    expected = next((value for name, value in mappings.items()
                     if name.upper().startswith("EXPECTED")), {})
    found = []
    for name, files in mappings.items():
        if name.upper().startswith("EXPECTED"):
            continue
        recovered = {}
        for filename, encoded in files.items():
            if not isinstance(filename, str):
                continue
            with contextlib.suppress(ValueError):
                filename = safe_relative_path(filename)
            if not filename or not isinstance(encoded, (str, bytes)):
                continue
            try:
                packed = encoded.encode("ascii") if isinstance(encoded, str) else encoded
            except UnicodeEncodeError:
                continue
            decoded = []
            for decoder in (base64.b85decode, base64.a85decode, base64.b64decode):
                with contextlib.suppress(ValueError, TypeError, zlib.error):
                    decoded.append(decoder(packed))
            for compressed in decoded:
                try:
                    source = _decompress_zlib_bounded(compressed)
                except (ValueError, zlib.error):
                    continue
                pinned = expected.get(filename) if isinstance(expected, dict) else None
                if pinned and (not isinstance(pinned, str) or sha256(source) != pinned.lower()):
                    continue
                recovered[filename] = canonical_source(source) if filename.endswith(".py") else source
                break
        if "main.py" in recovered:
            found.append((f"packed:{name}", recovered))
    return found


def packed_sources_from_tree(tree: ast.AST) -> list[tuple[str, bytes]]:
    """Compatibility wrapper used by older tests/tools."""
    return [(origin + ":main.py", files["main.py"])
            for origin, files in packed_artifacts_from_tree(tree)]


def _gzip_json_artifact(tree: ast.AST) -> dict[str, bytes] | None:
    """Recover ``json.loads(gzip.decompress(base64.b64decode(LITERAL)))`` maps."""
    values = {}
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            with contextlib.suppress(ValueError, TypeError):
                values[node.targets[0].id] = ast.literal_eval(node.value)
    for name, payload in values.items():
        if not isinstance(payload, (str, bytes)) or len(payload) < 100:
            continue
        with contextlib.suppress(ValueError, TypeError, gzip.BadGzipFile, UnicodeError,
                                 json.JSONDecodeError):
            raw = payload.encode("ascii") if isinstance(payload, str) else payload
            decoded = json.loads(gzip.decompress(base64.b64decode(raw)))
            if not isinstance(decoded, dict):
                continue
            files = {}
            for filename, content in decoded.items():
                filename = safe_relative_path(filename)
                if isinstance(content, str):
                    files[filename] = canonical_source(content) if filename.endswith(".py") else content.encode()
                elif isinstance(content, bytes):
                    files[filename] = canonical_source(content) if filename.endswith(".py") else content
            if files:
                return files
    return None


def artifacts_from_notebook(path: Path) -> list[tuple[str, dict[str, bytes]]]:
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    found, writefiles, sidecars = [], {}, {}
    literals: dict[str, str] = {}
    for index, cell in enumerate(doc.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = _cell_source(cell)
        lines = src.splitlines()
        write_match = re.match(r"^\s*%%writefile\s+(.+?)\s*$", lines[0], re.I) if lines else None
        agentfile_match = re.match(r"^\s*%%agentfile(?:\s+(.+?))?\s*$", lines[0], re.I) if lines else None
        if write_match or agentfile_match:
            with contextlib.suppress(ValueError):
                raw_name = ((write_match or agentfile_match).group(1) or "main.py").strip().strip("'\"")
                # Kaggle examples commonly write to /kaggle/working/main.py.
                # That path is the archive root at submission time, so retain
                # only its relative suffix while still rejecting arbitrary
                # absolute paths and traversal.
                normalized = raw_name.replace("\\", "/")
                prefix = "/kaggle/working/"
                if normalized.lower().startswith(prefix):
                    normalized = normalized[len(prefix):]
                filename = safe_relative_path(normalized)
                payload = "\n".join(lines[1:]) + "\n"
                writefiles[filename] = canonical_source(payload) if filename.endswith(".py") else payload.encode()
        # Common public notebooks store the full submission in a string literal.
        tree = _static_tree_from_cell(src)
        if tree is None:
            continue
        # Some public notebooks put a complete submission directly in one code
        # cell instead of writing main.py or packing it into a literal.  Treat
        # that cell as a candidate only when it parses independently and
        # defines an official entry point; normal compile/loader/first-action
        # QA still decides whether it enters the league.
        if _official_source(src):
            found.append((f"{path.name}:cell{index}:direct-agent-cell",
                          {"main.py": canonical_source(src)}))
        for origin, files in literal_packed_sources_from_tree(tree):
            found.append((f"{path.name}:cell{index}:{origin}", files))
        for origin, files in _pinned_remote_artifacts(tree, path.parent):
            found.append((f"{path.name}:cell{index}:{origin}", files))
        for origin, files in packed_artifacts_from_tree(tree):
            found.append((f"{path.name}:cell{index}:{origin}", files))
        packed_map = _gzip_json_artifact(tree)
        if packed_map:
            sidecars.update(packed_map)
            if "main.py" in packed_map:
                found.append((f"{path.name}:cell{index}:gzip-json-map", packed_map))
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                value = node.value
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    if len(value.value) >= 500 and ("def agent(" in value.value or "class Agent" in value.value):
                        name = "literal"
                        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                            name = node.targets[0].id
                        literals[name] = value.value
    for name, value in literals.items():
        found.append((f"{path.name}:literal:{name}", {"main.py": canonical_source(value)}))
    if "main.py" not in writefiles:
        # Many notebooks write one executable agent as submission.py,
        # my_agent.py, or parent_v*.py and rename it only while creating the
        # tarball.  Promote exactly one independently parsable file that
        # defines an official top-level entry point.  Ambiguous multi-agent
        # notebooks remain uncollected instead of guessing.
        main_candidates = []
        for name, data in writefiles.items():
            if not name.endswith(".py"):
                continue
            with contextlib.suppress(SyntaxError, UnicodeError):
                candidate_tree = ast.parse(data.decode("utf-8"))
                if _official_source(data):
                    main_candidates.append(name)
        if len(main_candidates) == 1:
            source_name = main_candidates[0]
            writefiles["main.py"] = writefiles.pop(source_name)
        elif len([name for name in writefiles if name.endswith(".py")]) == 1:
            # An explicit submission.py/agent.py writefile is itself stronger
            # evidence than a function name: Kaggle officially selects the
            # last callable and does not require it to be named ``agent``.
            source_name = next(name for name in writefiles if name.endswith(".py"))
            if Path(source_name).name.lower() in ("submission.py", "agent.py", "kaggle_agent.py"):
                writefiles["main.py"] = writefiles.pop(source_name)
    writefiles.update({name: data for name, data in sidecars.items() if name not in writefiles})
    if "main.py" in writefiles:
        found.insert(0, (f"{path.name}:writefile", writefiles))
    found.extend((f"{path.name}:{origin}", files)
                 for origin, files in _v23_external_output_artifact(doc, path.parent))
    return found


def sources_from_notebook(path: Path) -> list[tuple[str, bytes]]:
    return [(origin, files["main.py"]) for origin, files in artifacts_from_notebook(path)]


def sources_from_builder_cells(path: Path, timeout=30) -> list[tuple[str, bytes]]:
    """Run only self-contained artifact-builder cells in an isolated temp cwd.

    Several leading notebooks store their exact submission as compressed base85,
    base64, or a tuple of bytes literals.  Static string extraction cannot safely
    reconstruct every expression.  The cell must explicitly mention ``main.py``
    and a pinned/payload marker before it is considered; visualisation and arena
    cells are never executed here.
    """
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    found = []
    markers = ("source_bytes", "source_b64", "submission_b85", "payload=", "payload =",
               "expected_main_sha256", "expected_sha256")
    for index, cell in enumerate(doc.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        src = _cell_source(cell)
        low = src.lower()
        if len(src) < 200 or "main.py" not in low or not any(x in low for x in markers):
            continue
        if "%%writefile" in low:
            continue
        with tempfile.TemporaryDirectory(prefix="public-league-builder-") as tmp:
            work = Path(tmp)
            script = work / "builder.py"
            # Common builder cells rely on Path imported by an earlier notebook cell.
            script.write_text("from pathlib import Path\nWORKDIR = Path('.')\n" + src, encoding="utf-8")
            try:
                subprocess.run([sys.executable, str(script)], cwd=work, capture_output=True,
                               timeout=timeout, check=False,
                               env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            except subprocess.TimeoutExpired:
                continue
            main = work / "main.py"
            if main.exists():
                with contextlib.suppress(OSError, UnicodeError):
                    found.append((f"{path.name}:cell{index}:builder-main", canonical_source(main.read_bytes())))
            for archive in work.glob("*.tar*"):
                for origin, data in sources_from_archive(archive):
                    found.append((f"{path.name}:cell{index}:builder-{origin}", data))
    return found


def artifacts_from_archive_bytes(payload: bytes, label="literal.tar") -> list[tuple[str, dict[str, bytes]]]:
    """Read a bounded in-memory tar artifact and reject unsafe member paths."""
    found = []
    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as tf:
            files = {}
            total = 0
            for member in tf.getmembers():
                if not member.isfile() or member.size > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                    continue
                total += member.size
                if total > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                    raise ValueError("archive exceeds extraction limit")
                with contextlib.suppress(ValueError):
                    name = safe_relative_path(member.name)
                    stream = tf.extractfile(member)
                    if stream:
                        payload = stream.read()
                        files[name] = canonical_source(payload) if name.endswith(".py") else payload
            mains = [name for name in files if Path(name).name.lower() == "main.py"]
            for main in mains:
                parent = str(Path(main).parent).replace("\\", "/")
                prefix = "" if parent == "." else parent + "/"
                bundle = {name[len(prefix):]: data for name, data in files.items()
                          if not prefix or name.startswith(prefix)}
                if "main.py" in bundle:
                    found.append((f"{label}:{main}", bundle))
    except (tarfile.TarError, OSError, UnicodeError, ValueError):
        pass
    return found


def artifacts_from_archive(path: Path) -> list[tuple[str, dict[str, bytes]]]:
    try:
        if path.stat().st_size > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
            return []
        return artifacts_from_archive_bytes(path.read_bytes(), path.name)
    except OSError:
        return []


def sources_from_archive(path: Path) -> list[tuple[str, bytes]]:
    return [(origin, files["main.py"]) for origin, files in artifacts_from_archive(path)]


def _directory_artifacts(root: Path) -> list[tuple[str, dict[str, bytes]]]:
    found = []
    ignored = {"kernel-metadata.json", "submission-metadata.json",
               ".public-league-download-complete.json",
               ".public-league-output-complete.json"}
    cache_dirs = {"_notebook_outputs", "_remote"}
    for main in sorted(root.rglob("main.py")):
        if any(part in cache_dirs for part in main.relative_to(root).parts):
            continue
        parent = main.parent
        files = {}
        total = 0
        selected = None
        manifest_path = parent / "agent_manifest.json"
        if manifest_path.exists():
            with contextlib.suppress(OSError, UnicodeError, json.JSONDecodeError):
                manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
                if isinstance(manifest.get("files"), dict):
                    selected = set(manifest["files"])
        for item in sorted(parent.iterdir()):
            if not item.is_file() or item.name in ignored or item.suffix.lower() in (".ipynb", ".tar", ".tgz") or item.name.endswith(".tar.gz"):
                continue
            if selected is not None and item.name not in selected:
                continue
            size = item.stat().st_size
            if size > PUBLIC_LEAGUE_MAX_DATASET_BYTES or total + size > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                continue
            rel = safe_relative_path(item.relative_to(parent).as_posix())
            payload = item.read_bytes(); total += len(payload)
            if selected is not None:
                expected = manifest["files"].get(item.name)
                if expected and sha256(payload) != expected:
                    files = {}; break
            files[rel] = canonical_source(payload) if rel.endswith(".py") else payload
        if "main.py" in files:
            found.append((str(main.relative_to(root)), files))
    # Attached source datasets sometimes name the runtime shim agent_main.py
    # and compile a sibling C++ policy into agent.so in the notebook.  Promote
    # exactly one top-level official Python entry point and retain every small
    # sibling so prepare_artifact_files can reproduce the runtime bundle.
    for directory in sorted({path.parent for path in root.rglob("*.py")
                             if not any(part in cache_dirs for part in path.relative_to(root).parts)}):
        if (directory / "main.py").exists():
            continue
        if not (any(directory.glob("*.cpp")) or (directory / "source_manifest.json").exists()):
            continue
        candidates = []
        for path in directory.glob("*.py"):
            with contextlib.suppress(OSError, UnicodeError, SyntaxError):
                payload = canonical_source(path.read_bytes())
                if _official_source(payload):
                    candidates.append((path, payload))
        if len(candidates) != 1:
            continue
        promoted, main_payload = candidates[0]
        files, total = {"main.py": main_payload}, len(main_payload)
        for item in sorted(directory.iterdir()):
            if not item.is_file() or item == promoted or item.name in ignored:
                continue
            if item.suffix.lower() in (".ipynb", ".tar", ".tgz") or item.name.endswith(".tar.gz"):
                continue
            size = item.stat().st_size
            if size > PUBLIC_LEAGUE_MAX_DATASET_BYTES or total + size > PUBLIC_LEAGUE_MAX_DATASET_BYTES:
                continue
            files[safe_relative_path(item.name)] = item.read_bytes(); total += size
        found.append((str(promoted.relative_to(root)) + ":promoted-main", files))
    return found


def _assemble_explicit_plan_placeholder(root: Path, files: dict[str, bytes]) -> dict[str, bytes]:
    """Reproduce the Fieldbook's documented single-file assembly recipe."""
    main = files.get("main.py")
    if not main or b"# <FIELD_BOOK_PLAN_SCRIPTS>" not in main:
        return files
    candidates = list(root.rglob("fieldbook_tapes.py"))
    if len(candidates) != 1:
        return files
    try:
        logic = main.decode("utf-8")
        tape = candidates[0].read_text(encoding="utf-8")
        placeholder = "from fieldbook_tapes import PLAN_SCRIPTS\n\n# <FIELD_BOOK_PLAN_SCRIPTS>"
        begin_marker = "# === BEGIN FIELD BOOK PLAN SCRIPTS ==="
        end_marker = "# === END FIELD BOOK PLAN SCRIPTS ==="
        begin = tape.index(begin_marker) + len(begin_marker) + 1
        end = tape.index("\n" + end_marker, begin)
        if logic.count(placeholder) != 1:
            return files
        assembled = canonical_source(logic.replace(placeholder, tape[begin:end]))
        if not _official_source(assembled):
            return files
        return {**files, "main.py": assembled}
    except (OSError, UnicodeError, ValueError):
        return files


def discover_artifacts(archive: Path) -> list[tuple[str, dict[str, bytes]]]:
    found = []
    found.extend(_directory_artifacts(archive))
    for path in sorted(archive.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(archive).parts
        if any(part in {"_notebook_outputs", "_remote"} for part in relative_parts):
            continue
        try:
            if path.suffix.lower() == ".ipynb":
                found.extend(artifacts_from_notebook(path))
            elif path.name.lower().endswith((".tar.gz", ".tgz", ".tar")):
                found.extend(artifacts_from_archive(path))
            elif (path.suffix.lower() == ".py" and path.name != "kernel-metadata.py"
                  and "_datasets" not in relative_parts):
                data = canonical_source(path.read_bytes())
                if b"def agent(" in data or b"class Agent" in data:
                    found.append((str(path.relative_to(archive)), {"main.py": data}))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
    # Only if normal extraction found no plausible source, execute narrowly
    # selected compressed-artifact builder cells.
    if not found:
        for path in sorted(archive.rglob("*.ipynb")):
            with contextlib.suppress(OSError, UnicodeError, json.JSONDecodeError):
                found.extend((origin, {"main.py": data})
                             for origin, data in sources_from_builder_cells(path))
    # Explicit writefile/tar/main candidates first, exact candidates once.
    priority = lambda x: (0 if "writefile" in x[0] else 1 if "main.py" in x[0].lower() else 2,
                          -len(x[1]), -sum(map(len, x[1].values())))
    unique = {}
    for origin, files in sorted(found, key=priority):
        if "main.py" not in files:
            continue
        files = _assemble_explicit_plan_placeholder(archive, files)
        normalized = {safe_relative_path(n): (canonical_source(d) if n.endswith(".py") else d)
                      for n, d in files.items()}
        unique.setdefault(artifact_digest(normalized), (origin, normalized))
    return list(unique.values())


def discover_sources(archive: Path) -> list[tuple[str, bytes]]:
    """Compatibility view of artifact discovery."""
    return [(origin, files["main.py"]) for origin, files in discover_artifacts(archive)]


def prepare_artifact_files(store: Store, files: dict[str, bytes]) -> dict[str, bytes]:
    """Compile a statically recovered C++ bundle when its notebook omitted agent.so."""
    prepared = dict(files)
    main = prepared.get("main.py", b"")
    cpp = [name for name in prepared if name.endswith(".cpp")]
    needs_shared_library = (b"agent.so" in main or b"ctypes.CDLL" in main
                            or b"from ctypes" in main)
    if not needs_shared_library:
        return prepared
    if "agent.so" not in prepared:
        if not cpp:
            return prepared
        ensure_public_league_docker_image()
        with tempfile.TemporaryDirectory(prefix="linux-build-", dir=store.state) as tmp_name:
            work = Path(tmp_name)
            for name, payload in prepared.items():
                target = work / safe_relative_path(name)
                target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(payload)
            parents = {str(Path(name).parent).replace("\\", "/") for name in cpp}
            build_parent = next(iter(parents)) if len(parents) == 1 else "."
            sources = [Path(name).name if build_parent != "." else name for name in cpp]
            include_dirs = sorted({str(Path(name).parent).replace("\\", "/")
                                   for name in prepared if name.endswith((".h", ".hpp"))})
            include_args = [value for directory in include_dirs
                            for value in ("-I", "/build/" + directory)]
            command = ["docker", "run", "--rm", "-v", f"{work.resolve()}:/build",
                       "-w", "/build" + ("/" + build_parent if build_parent != "." else ""),
                       PUBLIC_LEAGUE_DOCKER_IMAGE, "g++", "-O3", "-std=c++17", "-shared",
                       "-fPIC", "-I.", *include_args, "-o", "/build/agent.so", *sources]
            proc = subprocess.run(command, capture_output=True, text=True, timeout=600,
                                  creationflags=subprocess_no_window_flags())
            output = work / "agent.so"
            if proc.returncode or not output.exists():
                raise RuntimeError((proc.stderr or proc.stdout or "agent.so build failed")[-2000:])
            prepared["agent.so"] = output.read_bytes()
    # Public C++ submissions execute main.py + the compiled shared library.
    # Notebook-only build inputs are provenance, not runtime identity.
    return {name: payload for name, payload in prepared.items()
            if not name.lower().endswith((".cpp", ".hpp", ".h", ".inc"))}


def save_artifact(store: Store, files: dict[str, bytes]) -> tuple[str, Path, str, list[str], str]:
    files = prepare_artifact_files(store, files)
    source_data = canonical_source(files["main.py"])
    files = {**files, "main.py": source_data}
    source_digest = sha256(source_data)
    digest = artifact_digest(files)
    if set(files) == {"main.py"}:
        source = store.state / "sources" / f"{source_digest}.py"
        if not source.exists(): source.write_bytes(source_data)
    else:
        folder = store.state / "artifacts" / digest
        for name, payload in files.items():
            target = folder / safe_relative_path(name)
            if target.exists() and target.read_bytes() != payload:
                raise ValueError(f"artifact collision: {digest}/{name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists(): target.write_bytes(payload)
        source = folder / "main.py"
    platform = "linux" if any(name.endswith((".so", ".dylib")) for name in files) else "host"
    return digest, source, source_digest, sorted(files), platform


def _docker_path(path: Path) -> str:
    return "/workspace/" + path.resolve().relative_to(ROOT.resolve()).as_posix()


def ensure_public_league_docker_image() -> None:
    probe = subprocess.run(["docker", "image", "inspect", PUBLIC_LEAGUE_DOCKER_IMAGE],
                           capture_output=True, text=True,
                           creationflags=subprocess_no_window_flags())
    if probe.returncode == 0:
        return
    dockerfile = ROOT / "tools" / "public-league.Dockerfile"
    proc = subprocess.run(["docker", "build", "-f", str(dockerfile), "-t",
                           PUBLIC_LEAGUE_DOCKER_IMAGE, str(ROOT)], capture_output=True,
                          text=True, timeout=1800, creationflags=subprocess_no_window_flags())
    if proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout or "docker image build failed")[-2000:])


def qa_source(source: Path, timeout=60, execution_platform="host") -> dict:
    result = source.with_suffix(".qa.json")
    result.unlink(missing_ok=True)
    if execution_platform == "linux":
        ensure_public_league_docker_image()
        command = ["docker", "run", "--rm", "-v", f"{ROOT.resolve()}:/workspace",
                   "-w", _docker_path(source.parent), "-e", "PYTHONPATH=/workspace/src",
                   PUBLIC_LEAGUE_DOCKER_IMAGE, "python", "-m", "kaggriculture_meta.public_league",
                   "_qa", "--source", _docker_path(source), "--result", _docker_path(result)]
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout,
                              creationflags=subprocess_no_window_flags())
    else:
        proc = subprocess.run(
            [sys.executable, "-m", "kaggriculture_meta.public_league", "_qa",
             "--source", str(source), "--result", str(result)],
            cwd=source.parent, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
            env={**os.environ, "PYTHONPATH": str(ROOT / "src") + os.pathsep + os.environ.get("PYTHONPATH", "")},
        )
    if proc.returncode or not result.exists():
        return {"ok": False, "error": (proc.stderr or proc.stdout or "qa failed")[-1000:]}
    return json.loads(result.read_text(encoding="utf-8"))


def extract(store: Store, limit=100) -> dict:
    versions = store.db.execute("""
      SELECT v.*,n.title,n.url,n.author,n.ref,n.current_version_key
      FROM notebook_versions v JOIN notebooks n ON n.id=v.notebook_id
      WHERE v.status='pulled' ORDER BY v.id LIMIT ?
    """, (limit,)).fetchall()
    extracted = duplicate = quarantined = empty = 0
    for row in versions:
        try:
            archive_path = Path(row["archive_path"])
            dataset_summary = ensure_notebook_datasets(archive_path)
            if dataset_summary["failed"] or dataset_summary["skipped"]:
                store.event("dataset", f"dataset attachment partial: {row['ref']}",
                            dataset_summary, "warning")
            output_summary = ({"downloaded": [], "failed": []}
                              if row["version_key"] != row["current_version_key"]
                              else ensure_notebook_outputs(archive_path, row["ref"]))
            if output_summary["failed"]:
                store.event("notebook_output", f"published output partial: {row['ref']}",
                            output_summary, "warning")
            candidates = discover_artifacts(archive_path)
        except Exception as exc:
            # One malformed public notebook must never starve every newer item
            # in the extraction queue.  Preserve the failure for inspection and
            # continue with the remaining immutable notebook versions.
            error = f"extractor {type(exc).__name__}: {exc}"
            with store.db:
                store.db.execute(
                    "UPDATE notebook_versions SET status='quarantine',error=? WHERE id=?",
                    (error[:5000], row["id"]),
                )
            quarantined += 1
            continue
        winner = None
        errors = []
        for origin, files in candidates:
            try:
                digest, source, source_digest, artifact_files, platform = save_artifact(store, files)
                compile(source.read_bytes(), str(source), "exec")
            except Exception as exc:
                errors.append(f"{origin}: compile {type(exc).__name__}: {exc}")
                continue
            qa = qa_source(source, execution_platform=platform)
            if qa.get("ok"):
                winner = (digest, source, source_digest, artifact_files, platform, qa, origin)
                break
            errors.append(f"{origin}: {qa.get('error', 'loader failed')}")
        if not winner:
            status = "no_source" if not candidates else "quarantine"
            if status == "no_source" and output_summary["failed"]:
                errors.extend("published output unavailable: " + item["error"]
                              for item in output_summary["failed"])
            if status == "no_source" and dataset_summary["failed"]:
                errors.extend("dataset unavailable: " + item["error"]
                              for item in dataset_summary["failed"])
            with store.db:
                store.db.execute("UPDATE notebook_versions SET status=?,error=? WHERE id=?",
                                 (status, "\n".join(errors)[:5000] or "no agent source found", row["id"]))
            empty += status == "no_source"
            quarantined += status == "quarantine"
            continue
        digest, source, source_digest, artifact_files, platform, qa, origin = winner
        now = utcnow()
        is_current = int(row["version_key"] == row["current_version_key"])
        with store.db:
            prior = store.db.execute("SELECT id FROM agents WHERE sha256=?", (digest,)).fetchone()
            store.db.execute("""
              INSERT INTO agents(sha256,source_path,source_sha256,artifact_files_json,execution_platform,
                qa_status,entrypoint,created_at,status)
              VALUES(?,?,?,?,?,?,?,?,'candidate') ON CONFLICT(sha256) DO NOTHING
            """, (digest, str(source), source_digest, json.dumps(artifact_files), platform,
                  "pass", qa.get("entrypoint"), now))
            agent_id = store.db.execute("SELECT id FROM agents WHERE sha256=?", (digest,)).fetchone()[0]
            if is_current:
                store.db.execute("UPDATE aliases SET is_current=0 WHERE ref=?", (row["ref"],))
            store.db.execute("""
              INSERT OR IGNORE INTO aliases(agent_id,version_id,notebook_title,notebook_url,author,ref,is_current,discovered_at)
              VALUES(?,?,?,?,?,?,?,?)
            """, (agent_id, row["id"], row["title"], row["url"], row["author"], row["ref"],
                  is_current, row["first_seen"] or now))
            store.db.execute("UPDATE aliases SET is_current=? WHERE agent_id=? AND version_id=?",
                             (is_current, agent_id, row["id"]))
            store.db.execute("UPDATE notebook_versions SET status='extracted',error=? WHERE id=?",
                             (f"origin={origin}; agent={digest}", row["id"]))
        if prior:
            duplicate += 1
        else:
            extracted += 1
    summary = {"versions": len(versions), "new_agents": extracted, "duplicate_aliases": duplicate,
               "quarantined": quarantined, "no_source": empty}
    store.set_meta("last_extract", {"at": utcnow(), **summary})
    store.event("extract", f"new agents {extracted}, duplicate aliases {duplicate}", summary,
                "warning" if quarantined else "info")
    return summary


def engine_sha() -> str:
    from .championship_league import engine_identity
    dockerfile = ROOT / "tools" / "public-league.Dockerfile"
    contract = {
        "engine": engine_identity(), "rules": RULES_VERSION, "configuration": ENGINE_CONFIG,
        "public_league_runner": sha256(Path(__file__).read_bytes()),
        "native_runner": sha256((ROOT / "src/kaggriculture_meta/championship_league.py").read_bytes()),
        "linux_runtime": {
            "image": PUBLIC_LEAGUE_DOCKER_IMAGE,
            "dockerfile_sha256": sha256(dockerfile.read_bytes()),
            "wall_timeout_seconds": PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS,
        },
    }
    return sha256(json.dumps(contract, sort_keys=True, separators=(",", ":")).encode())


def deterministic_seeds(a_sha: str, b_sha: str, count: int, offset=0) -> list[int]:
    pair = "|".join(sorted((a_sha, b_sha)))
    rng = random.Random(int(sha256(pair.encode())[:16], 16))
    values = []
    while len(values) < count + offset:
        value = rng.randrange(1, 2**31 - 1)
        if value not in values:
            values.append(value)
    return values[offset:offset + count]


def match_key(eng: str, a_sha: str, b_sha: str, seed: int, seat_a: int) -> str:
    return sha256(f"{eng}|{a_sha}|{b_sha}|{seed}|{seat_a}".encode())


def eligible_agents(store: Store):
    return store.db.execute("""
      SELECT a.*,MAX(n.public_score) AS public_score,MAX(n.last_run) AS last_run,
        MAX(CASE WHEN n.origin='local' THEN 1 ELSE 0 END) AS is_local
      FROM agents a JOIN aliases x ON x.agent_id=a.id JOIN notebook_versions v ON v.id=x.version_id
      JOIN notebooks n ON n.id=v.notebook_id WHERE a.qa_status='pass'
      GROUP BY a.id ORDER BY a.rating DESC,a.id DESC
    """).fetchall()


def schedule_matches(store: Store, top_k=DEFAULT_TOP_K, seeds_per_pair=1, max_matches=240,
                     newcomer_priority_games=NEWCOMER_PRIORITY_GAMES,
                     focus_agent_id=None) -> list[dict]:
    agents = eligible_agents(store)
    if len(agents) < 2:
        return []
    # Keep a bounded challenger pool. Existing active policies remain, then current
    # candidates and high public-score/new policies enter. Public score is only a
    # scheduling prior; it never enters the local rating.
    active = [x for x in agents if x["status"] == "active"]
    newcomers = [x for x in agents if x["status"] == "candidate"]
    key = lambda x: (x["public_score"] if x["public_score"] is not None else -1, x["id"])
    # Reserve challenger slots even after the top-K fills, so newly published
    # notebooks are never permanently starved by incumbents.
    challenger_slots = min(10, top_k)
    pool_map = {x["id"]: x for x in active[:max(0, top_k-challenger_slots)]}

    # A policy remains in catch-up rotation across refresh cycles until its game
    # count reaches the established field's median.  This is intentionally based
    # on evidence count rather than status: update_rankings may archive a weak
    # newcomer after its first batch, but that must not stop the promised sample
    # catch-up.  Zero-game candidates lead the queue; local controls break equal
    # deficits because they are explicitly requested comparison baselines.
    active_games = sorted(int(x["games"]) for x in active)
    field_median = active_games[len(active_games) // 2] if active_games else 0
    catchup_target = min(field_median, newcomer_priority_games)
    catchup = [x for x in agents if x["id"] not in pool_map and
               ((x["status"] == "candidate" and int(x["games"]) < newcomer_priority_games)
                or int(x["games"]) < catchup_target)]
    catchup.sort(key=lambda x: (int(x["games"]), -int(x["is_local"]),
                                -(x["public_score"] if x["public_score"] is not None else -1),
                                x["sha256"]))
    for row in catchup[:top_k-len(pool_map)]:
        pool_map[row["id"]] = row
    priority_ids = {row["id"] for row in catchup if row["id"] in pool_map}

    # Fill any unused challenger places by the normal strength/newness prior.
    ordered_newcomers = sorted(newcomers, key=lambda x: (x["is_local"], *key(x)), reverse=True)
    for row in ordered_newcomers:
        if len(pool_map) >= min(top_k, len(agents)):
            break
        pool_map[row["id"]] = row
    if len(pool_map) < min(top_k, len(agents)):
        for row in sorted(agents, key=lambda x: x["rating"], reverse=True):
            pool_map[row["id"]] = row
            if len(pool_map) >= min(top_k, len(agents)):
                break
    if focus_agent_id is not None:
        focus_row = next((x for x in agents if x["id"] == int(focus_agent_id)), None)
        if focus_row is None:
            raise ValueError(f"focus agent is not eligible: {focus_agent_id}")
        if focus_row["id"] not in pool_map and len(pool_map) >= min(top_k, len(agents)):
            removable = min(pool_map.values(), key=lambda x: (x["rating"], x["games"], x["id"]))
            del pool_map[removable["id"]]
        pool_map[focus_row["id"]] = focus_row
    pool = list(pool_map.values())
    by_id = {x["id"]: x for x in pool}
    projected = {x["id"]: int(x["games"]) for x in pool}
    pair_games = {}
    for i, a in enumerate(pool):
        for b in pool[i + 1:]:
            pair = tuple(sorted((a["id"], b["id"])))
            pair_games[pair] = store.db.execute("""SELECT COUNT(*) FROM matches WHERE status='complete'
                AND ((agent_a=? AND agent_b=?) OR (agent_a=? AND agent_b=?))""",
                (a["id"], b["id"], b["id"], a["id"])).fetchone()[0]
    eng = engine_sha()
    jobs = []
    scheduled = set()
    if focus_agent_id is not None:
        focus = by_id[int(focus_agent_id)]
        opponents = [x for x in pool if x["id"] != focus["id"]]
        while opponents and len(jobs) + 2 <= max_matches:
            opponent = min(opponents, key=lambda x: (
                pair_games[tuple(sorted((focus["id"], x["id"])))],
                abs(float(x["rating"]) - float(focus["rating"])),
                projected[x["id"]], -x["rating"], x["sha256"]))
            a, b = sorted((focus, opponent), key=lambda x: x["sha256"])
            pair = tuple(sorted((a["id"], b["id"])))
            offset = pair_games[pair] // 2
            while True:
                seed = deterministic_seeds(a["sha256"], b["sha256"], 1, offset)[0]
                keys = [match_key(eng, a["sha256"], b["sha256"], seed, seat) for seat in (0, 1)]
                if not any(key_id in scheduled or store.db.execute(
                        "SELECT 1 FROM matches WHERE match_key=?", (key_id,)).fetchone() for key_id in keys):
                    break
                offset += 1
            for seat, key_id in zip((0, 1), keys):
                scheduled.add(key_id)
                jobs.append({"match_key": key_id, "engine_sha": eng,
                    "agent_a": a["id"], "agent_b": b["id"], "seed": seed, "seat_a": seat,
                    "a_sha": a["sha256"], "b_sha": b["sha256"],
                    "a_source_sha": a["source_sha256"] or a["sha256"],
                    "b_source_sha": b["source_sha256"] or b["sha256"],
                    "a_platform": a["execution_platform"], "b_platform": b["execution_platform"],
                    "a_path": a["source_path"], "b_path": b["source_path"],
                    "state_path": str(store.state.resolve())})
            projected[a["id"]] += 2
            projected[b["id"]] += 2
            pair_games[pair] += 2
        return jobs
    # Deficit balancing: the least-tested agent is selected first. It meets the
    # least-played pair among the strongest available opponents. Once its game
    # count catches the field, its priority naturally falls back to normal.
    while len(jobs) + 2 <= max_matches:
        focus_pool = [x for x in pool if not (x["id"] in priority_ids and
                                               projected[x["id"]] >= newcomer_priority_games)]
        if not focus_pool:
            focus_pool = pool
        focus = min(focus_pool, key=lambda x: (projected[x["id"]], -x["is_local"],
                                                -x["rating"], x["sha256"]))
        opponents = [x for x in pool if x["id"] != focus["id"]]
        catching_up = projected[focus["id"]] < max(projected.values())
        anchor_round = catching_up and (projected[focus["id"]] // 2) % 3 == 2
        if anchor_round:
            experienced = [x for x in opponents if projected[x["id"]] > projected[focus["id"]]]
            if experienced:
                opponents = experienced
            opponent = min(opponents, key=lambda x: (
                pair_games[tuple(sorted((focus["id"], x["id"])))],
                abs(float(x["rating"]) - float(focus["rating"])),
                -x["rating"], projected[x["id"]], x["sha256"]))
        else:
            opponent = min(opponents, key=lambda x: (
                x["id"] in priority_ids and projected[x["id"]] >= newcomer_priority_games,
                projected[x["id"]],
                pair_games[tuple(sorted((focus["id"], x["id"])))],
                abs(float(x["rating"]) - float(focus["rating"])),
                -x["rating"], x["sha256"]))
        a, b = sorted((focus, opponent), key=lambda x: x["sha256"])
        pair = tuple(sorted((a["id"], b["id"])))
        offset = pair_games[pair] // 2
        while True:
            seed = deterministic_seeds(a["sha256"], b["sha256"], 1, offset)[0]
            keys = [match_key(eng, a["sha256"], b["sha256"], seed, seat) for seat in (0, 1)]
            if not any(key_id in scheduled or store.db.execute(
                    "SELECT 1 FROM matches WHERE match_key=?", (key_id,)).fetchone() for key_id in keys):
                break
            offset += 1
        for seat, key_id in zip((0, 1), keys):
            scheduled.add(key_id)
            jobs.append({"match_key": key_id, "engine_sha": eng,
                "agent_a": a["id"], "agent_b": b["id"], "seed": seed, "seat_a": seat,
                "a_sha": a["sha256"], "b_sha": b["sha256"],
                "a_source_sha": a["source_sha256"] or a["sha256"],
                "b_source_sha": b["source_sha256"] or b["sha256"],
                "a_platform": a["execution_platform"], "b_platform": b["execution_platform"],
                "a_path": a["source_path"], "b_path": b["source_path"],
                "state_path": str(store.state.resolve())})
        projected[a["id"]] += 2
        projected[b["id"]] += 2
        pair_games[pair] += 2
    return jobs


def quarantine_runtime_failures(store: Store, threshold=None) -> dict:
    code_threshold = PUBLIC_LEAGUE_CODE_FAILURE_THRESHOLD if threshold is None else int(threshold)
    counts = {}
    examples = {}
    watermarks = {}

    def is_new_failure(agent_id: int, match_id: int) -> bool:
        if agent_id not in watermarks:
            watermarks[agent_id] = int(store.get_meta(
                f"runtime_failure_watermark:{agent_id}", 0) or 0)
        return match_id > watermarks[agent_id]

    rows = store.db.execute("SELECT * FROM matches WHERE status='invalid' AND result_json IS NOT NULL").fetchall()
    for row in rows:
        with contextlib.suppress(Exception):
            result = json.loads(row["result_json"])
            for seat, errors in enumerate(result.get("errors") or []):
                if not errors:
                    continue
                agent_id = row["agent_a"] if seat == row["seat_a"] else row["agent_b"]
                if not is_new_failure(agent_id, row["id"]):
                    continue
                counts[agent_id] = counts.get(agent_id, 0) + 1
                examples.setdefault(agent_id, errors[0])
    quarantined = []
    with store.db:
        for agent_id in counts:
            code_count = counts.get(agent_id, 0)
            if code_count < code_threshold:
                continue
            prior = store.db.execute("SELECT qa_status FROM agents WHERE id=?", (agent_id,)).fetchone()
            if prior and prior[0] == "runtime_failed":
                continue
            detail = json.dumps(examples[agent_id], ensure_ascii=False)[:1200]
            store.db.execute("""UPDATE agents SET qa_status='runtime_failed',status='quarantine',qa_error=?
                                WHERE id=?""", (f"{code_count} invalid runtime matches; {detail}", agent_id))
            quarantined.append(agent_id)
    if quarantined:
        store.event("quarantine", f"runtime-quarantined {len(quarantined)} agents",
                    {"agent_ids": quarantined, "code_threshold": code_threshold}, "warning")
    return {"quarantined": len(quarantined), "agent_ids": quarantined}


def restore_runtime_quarantine(store: Store, agent_sha: str, reason: str) -> dict:
    """Restore a runtime-quarantined agent after an external clean revalidation.

    Historical invalid matches remain immutable.  A per-agent match-id watermark
    prevents those already-reviewed failures from quarantining the agent again;
    any later failures still count under the normal threshold.
    """
    if not reason.strip():
        raise ValueError("a revalidation reason is required")
    row = store.db.execute(
        "SELECT id,sha256,qa_status,status FROM agents WHERE sha256=?", (agent_sha,)).fetchone()
    if not row:
        raise ValueError(f"unknown agent sha256: {agent_sha}")
    if row["qa_status"] != "runtime_failed" or row["status"] != "quarantine":
        raise ValueError("agent is not runtime-quarantined")
    watermark = store.db.execute(
        "SELECT COALESCE(MAX(id),0) FROM matches WHERE agent_a=? OR agent_b=?",
        (row["id"], row["id"])).fetchone()[0]
    store.set_meta(f"runtime_failure_watermark:{row['id']}", int(watermark))
    with store.db:
        store.db.execute(
            "UPDATE agents SET qa_status='pass',qa_error=NULL,status='candidate' WHERE id=?",
            (row["id"],))
    detail = {"agent_id": row["id"], "sha256": row["sha256"],
              "failure_watermark_match_id": int(watermark), "reason": reason.strip()}
    store.event("quarantine_restore", "runtime quarantine cleared after clean revalidation", detail)
    return detail


def _league_job(job: dict) -> dict:
    from .championship_league import engine_identity, run_match
    if not job.get("containerized") and "linux" in (job.get("a_platform"), job.get("b_platform")):
        ensure_public_league_docker_image()
        token = job["match_key"][:24]
        state_path = Path(job.get("state_path") or DEFAULT_STATE).resolve()
        jobs_path = state_path / "jobs"
        jobs_path.mkdir(parents=True, exist_ok=True)
        job_path = jobs_path / f"docker-{token}.json"
        result_path = jobs_path / f"docker-{token}.result.json"

        def container_path(value: str | Path) -> str:
            resolved = Path(value).resolve()
            with contextlib.suppress(ValueError):
                return "/league-state/" + resolved.relative_to(state_path).as_posix()
            return _docker_path(resolved)

        container_job = dict(job, containerized=True,
                             a_path=container_path(job["a_path"]),
                             b_path=container_path(job["b_path"]))
        job_path.write_text(json.dumps(container_job), encoding="utf-8")
        result_path.unlink(missing_ok=True)
        container_name = _league_container_name(job)
        command = ["docker", "run", "--rm", "--name", container_name,
                   "-v", f"{ROOT.resolve()}:/workspace",
                   "-v", f"{state_path}:/league-state",
                   "-w", "/workspace", "-e", "PYTHONPATH=/workspace/src",
                   PUBLIC_LEAGUE_DOCKER_IMAGE, "python", "-m", "kaggriculture_meta.public_league",
                   "_worker", "--job", f"/league-state/jobs/{job_path.name}",
                   "--result", f"/league-state/jobs/{result_path.name}"]
        proc = subprocess.run(command, capture_output=True, text=True,
                              timeout=PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS,
                              creationflags=subprocess_no_window_flags())
        if proc.returncode or not result_path.exists():
            return {"valid": False, "error": "docker_worker_failed",
                    "stderr": (proc.stderr or proc.stdout or "")[-1200:]}
        return json.loads(result_path.read_text(encoding="utf-8"))
    payload = {
        "match_id": job["match_key"][:24], "mode": "native_reacting", "stage": "public_league",
        "engine": engine_identity(), "seed": job["seed"], "candidate_seat": job["seat_a"],
        "candidate": {"path": job["a_path"], "sha256": job.get("a_source_sha", job["a_sha"])},
        "opponent": {"path": job["b_path"], "sha256": job.get("b_source_sha", job["b_sha"]),
                     "name": job["b_sha"][:12], "family": "public_notebook"},
        "configuration": ENGINE_CONFIG,
    }
    return normalize_public_league_result(run_match(payload))


def _league_container_name(job: dict) -> str:
    """Stable Docker name so a cancelled Windows worker cannot orphan its game."""
    token = re.sub(r"[^a-z0-9_.-]", "-", str(job["match_key"]).lower())[:48]
    return f"kaggriculture-public-league-{token}"


def _terminate_league_worker(proc, job: dict) -> None:
    """Terminate a worker tree and remove any Docker game it started.

    The Windows venv launcher starts a base-Python child, which may in turn run
    Docker. Killing only the launcher leaves descendants consuming CPU. Docker
    containers also outlive a killed CLI, so Linux-artifact jobs get an
    explicit deterministic container cleanup.
    """
    if proc.poll() is None:
        if os.name == "nt":
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=flags, check=False)
        else:
            with contextlib.suppress(ProcessLookupError):
                proc.terminate()
    with contextlib.suppress(Exception):
        proc.wait(timeout=5)
    if proc.poll() is None:
        with contextlib.suppress(Exception):
            proc.kill()
        with contextlib.suppress(Exception):
            proc.wait(timeout=5)
    if "linux" in (job.get("a_platform"), job.get("b_platform")):
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
        subprocess.run(["docker", "rm", "-f", _league_container_name(job)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=flags, check=False)


def normalize_public_league_result(result: dict) -> dict:
    """Use the official engine outcome; local timing/telemetry remain warnings."""
    failures = list(result.get("health_failures") or [])
    ignored, fatal = [], []
    engine_done = (result.get("statuses") == ["DONE", "DONE"]
                   and not any(result.get("errors") or []))
    for failure in failures:
        text = str(failure)
        if (engine_done and ("_over_one_second" in text or "_over_1_5_seconds" in text
                             or "_internal_error:" in text)
                or text.rsplit(":", 1)[-1] in NONFATAL_TELEMETRY_FAILURES):
            ignored.append(failure)
            continue
        fatal.append(failure)
    result["health_failures"] = fatal
    if ignored:
        result["public_league_warnings"] = ignored
    rewards = result.get("rewards") or []
    healthy = (result.get("statuses") == ["DONE", "DONE"] and result.get("states") == 720
               and len(rewards) == 2 and all(isinstance(v, (int, float)) for v in rewards)
               and not any(result.get("errors") or [])
               and result.get("candidate_timing", {}).get("calls") == 719
               and result.get("opponent_timing", {}).get("calls") == 719
               and not fatal)
    if healthy:
        margin = result.get("margin")
        result["valid"] = True
        result["outcome"] = "win" if margin > 0 else "loss" if margin < 0 else "tie"
    return result


def repair_nonfatal_telemetry_matches(store: Store) -> dict:
    """Recover stored matches rejected solely by an allowed diagnostic counter."""
    repaired, touched = 0, set()
    rows = store.db.execute(
        "SELECT * FROM matches WHERE status='invalid' AND result_json IS NOT NULL").fetchall()
    with store.db:
        for row in rows:
            with contextlib.suppress(Exception):
                result = normalize_public_league_result(json.loads(row["result_json"]))
                if not result.get("valid"):
                    continue
                rewards, seat = result["rewards"], row["seat_a"]
                ra, rb = float(rewards[seat]), float(rewards[1-seat])
                score = 1.0 if ra > rb else 0.0 if ra < rb else .5
                store.db.execute("""UPDATE matches SET status='complete',outcome_a=?,reward_a=?,reward_b=?,
                    margin_a=?,runtime=?,error=NULL,result_json=? WHERE id=?""",
                    (score, ra, rb, ra-rb, result.get("seconds"),
                     json.dumps(result, ensure_ascii=False), row["id"]))
                touched.update((row["agent_a"], row["agent_b"])); repaired += 1
        for agent_id in touched:
            row = store.db.execute("SELECT qa_status,qa_error FROM agents WHERE id=?", (agent_id,)).fetchone()
            if row and row["qa_status"] == "runtime_failed" and "overflow_contract_errors" in (row["qa_error"] or ""):
                store.db.execute("UPDATE agents SET qa_status='pass',qa_error=NULL,status='candidate' WHERE id=?",
                                 (agent_id,))
    if repaired:
        store.event("repair", f"recovered {repaired} diagnostic-only matches",
                    {"matches": repaired, "agents": sorted(touched)})
    return {"matches": repaired, "agents": len(touched)}


def run_league(store: Store, workers=8, top_k=DEFAULT_TOP_K, seeds_per_pair=1,
               max_matches=240, timeout=PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS,
               stop_event=None, focus_agent_id=None) -> dict:
    with process_lock(store.state / "league.lock") as acquired:
        if not acquired:
            return {"busy": True, "message": "another league cycle is already running"}
        return _run_league_unlocked(store, workers, top_k, seeds_per_pair,
                                    max_matches, timeout, stop_event, focus_agent_id)


def _run_league_unlocked(store: Store, workers=8, top_k=DEFAULT_TOP_K, seeds_per_pair=1,
                         max_matches=240, timeout=PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS, stop_event=None,
                         focus_agent_id=None) -> dict:
    if workers not in range(1, 13):
        raise ValueError("workers must be 1..12")
    if stop_event is not None and stop_event.is_set():
        return {"scheduled": 0, "completed": 0, "invalid": 0,
                "cancelled": 0, "stopped": True}
    stale = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)).isoformat(timespec="seconds")
    with store.db:
        store.db.execute("""UPDATE matches SET status='invalid',error='stale interrupted coordinator',completed_at=?
            WHERE status='running' AND created_at<?""", (utcnow(), stale))
    jobs = schedule_matches(store, top_k, seeds_per_pair, max_matches,
                            focus_agent_id=focus_agent_id)
    if not jobs:
        update_rankings(store, top_k=top_k)
        return {"scheduled": 0, "completed": 0, "invalid": 0}
    now = utcnow()
    with store.db:
        for job in jobs:
            store.db.execute("""INSERT INTO matches(match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,created_at)
                                VALUES(?,?,?,?,?,?,'running',?)""",
                             (job["match_key"], job["engine_sha"], job["agent_a"], job["agent_b"],
                              job["seed"], job["seat_a"], now))
    pending = list(jobs)
    active = []
    completed = invalid = cancelled = 0
    stopped = False
    try:
        while pending or active:
            if stop_event is not None and stop_event.is_set():
                stopped = True
                cancelled = len(pending) + len(active)
                with store.db:
                    for job in pending:
                        store.db.execute("DELETE FROM matches WHERE match_key=? AND status='running'",
                                         (job["match_key"],))
                pending.clear()
                for proc, _, job, _, log in list(active):
                    _terminate_league_worker(proc, job)
                    log.close()
                    with store.db:
                        store.db.execute("DELETE FROM matches WHERE match_key=? AND status='running'",
                                         (job["match_key"],))
                active.clear()
                break
            while pending and len(active) < workers:
                job = pending.pop(0)
                path = store.state / "jobs" / f"{job['match_key']}.json"
                result = path.with_suffix(".result.json")
                path.write_text(json.dumps(job), encoding="utf-8")
                result.unlink(missing_ok=True)
                log = path.with_suffix(".log").open("w", encoding="utf-8")
                env = {**os.environ, "PYTHONPATH": str(ROOT / "src") + os.pathsep + os.environ.get("PYTHONPATH", "")}
                process = subprocess.Popen(
                    [sys.executable, "-m", "kaggriculture_meta.public_league", "_worker",
                     "--job", str(path), "--result", str(result)], cwd=ROOT,
                    stdout=log, stderr=log, env=env)
                active.append((process, time.monotonic(), job, result, log))
            progressed = False
            for item in list(active):
                proc, started, job, result_path, log = item
                timed_out = time.monotonic() - started > timeout
                if proc.poll() is None and not timed_out:
                    continue
                if proc.poll() is None:
                    _terminate_league_worker(proc, job)
                else:
                    proc.wait()
                log.close(); progressed = True
                result = None
                if proc.returncode == 0 and result_path.exists() and not timed_out:
                    with contextlib.suppress(Exception):
                        result = json.loads(result_path.read_text(encoding="utf-8"))
                valid = bool(result and result.get("valid"))
                if valid:
                    rewards = result["rewards"]
                    seat = job["seat_a"]
                    ra, rb = float(rewards[seat]), float(rewards[1-seat])
                    score = 1.0 if ra > rb else 0.0 if ra < rb else .5
                    values = ("complete", score, ra, rb, ra-rb, result.get("seconds"), None,
                              json.dumps(result, ensure_ascii=False), utcnow(), job["match_key"])
                    completed += 1
                else:
                    detail = None
                    if result:
                        detail = result.get("health_failures") or result.get("errors") or result.get("error")
                    err = "timeout" if timed_out else (detail or f"worker exit {proc.returncode}")
                    values = ("invalid", None, None, None, None, None, str(err)[:1000],
                              json.dumps(result, ensure_ascii=False) if result else None, utcnow(), job["match_key"])
                    invalid += 1
                with store.db:
                    store.db.execute("""UPDATE matches SET status=?,outcome_a=?,reward_a=?,reward_b=?,margin_a=?,
                        runtime=?,error=?,result_json=?,completed_at=? WHERE match_key=?""", values)
                active.remove(item)
            if active and not progressed:
                time.sleep(.1)
    finally:
        for proc, _, job, _, log in active:
            _terminate_league_worker(proc, job)
            log.close()
            with store.db:
                store.db.execute("UPDATE matches SET status='invalid',error='runner interrupted',completed_at=? WHERE match_key=?",
                                 (utcnow(), job["match_key"]))
    quarantine = quarantine_runtime_failures(store)
    update_rankings(store, top_k=top_k)
    summary = {"scheduled": len(jobs), "completed": completed, "invalid": invalid,
               "cancelled": cancelled, "stopped": stopped, "workers": workers,
               "top_k": top_k, "runtime_quarantine": quarantine["quarantined"],
               "focus_agent_id": focus_agent_id}
    store.set_meta("last_league", {"at": utcnow(), **summary})
    verb = "stopped" if stopped else "completed"
    store.event("league", f"{verb} {completed}/{len(jobs)}, invalid {invalid}, cancelled {cancelled}", summary,
                "warning" if invalid else "info")
    return summary


def wilson(wins: float, games: int, z=1.96):
    if games <= 0:
        return None, None
    p = wins / games
    d = 1 + z*z/games
    centre = (p + z*z/(2*games))/d
    half = z * math.sqrt((p*(1-p) + z*z/(4*games))/games)/d
    return max(0, centre-half), min(1, centre+half)


def bradley_terry_ratings(agent_ids, rows, regularization=1.0) -> dict[int, float]:
    """Regularized batch Bradley-Terry fit, with ties contributing half a win."""
    ids = list(agent_ids)
    ability = {key: 0.0 for key in ids}
    relevant = [(row["agent_a"], row["agent_b"], float(row["outcome_a"])) for row in rows
                if row["agent_a"] in ability and row["agent_b"] in ability]
    if not relevant:
        return {key: 1500.0 for key in ids}
    for _ in range(300):
        gradient = {key: -regularization * ability[key] for key in ids}
        curvature = {key: regularization for key in ids}
        for a, b, outcome in relevant:
            delta = max(-30.0, min(30.0, ability[a] - ability[b]))
            probability = 1.0 / (1.0 + math.exp(-delta))
            residual = outcome - probability
            weight = probability * (1.0 - probability)
            gradient[a] += residual; gradient[b] -= residual
            curvature[a] += weight; curvature[b] += weight
        changes = {key: 0.5 * gradient[key] / curvature[key] for key in ids}
        maximum = max(abs(value) for value in changes.values())
        for key, value in changes.items(): ability[key] += value
        mean = sum(ability.values()) / len(ability)
        for key in ids: ability[key] -= mean
        if maximum < 1e-9:
            break
    scale = 400.0 / math.log(10.0)
    return {key: 1500.0 + scale * ability[key] for key in ids}


def update_rankings(store: Store, top_k=DEFAULT_TOP_K, min_games=8):
    agents = eligible_agents(store)
    rows = store.db.execute("SELECT * FROM matches WHERE status='complete' ORDER BY id").fetchall()
    ratings = bradley_terry_ratings((x["id"] for x in agents), rows)
    stats = {x["id"]: [0, 0, 0, 0, None] for x in agents}
    for row in rows:
        for ident, score in ((row["agent_a"], row["outcome_a"]),
                             (row["agent_b"], 1-row["outcome_a"])):
            if ident not in stats: continue
            stats[ident][0] += 1
            if score == 1: stats[ident][1] += 1
            elif score == 0: stats[ident][2] += 1
            else: stats[ident][3] += 1
            stats[ident][4] = row["completed_at"]
    ranked = sorted(agents, key=lambda x: (ratings[x["id"]], stats[x["id"]][0]), reverse=True)
    sufficiently_tested = [x for x in ranked if stats[x["id"]][0] >= min_games]
    active_ids = {x["id"] for x in sufficiently_tested[:top_k]}
    with store.db:
        for agent in ranked:
            games, wins, losses, ties, last = stats[agent["id"]]
            low, high = wilson(wins + .5*ties, games)
            if agent["id"] in active_ids:
                status = "active"
            elif games < min_games:
                status = "candidate"
            else:
                status = "archived"
            store.db.execute("""UPDATE agents SET rating=?,games=?,wins=?,losses=?,ties=?,score_low=?,score_high=?,
                status=?,last_played=? WHERE id=?""",
                (ratings[agent["id"]], games, wins, losses, ties, low, high, status, last, agent["id"]))


def dashboard_snapshot(store: Store) -> dict:
    new_cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=12)).isoformat(timespec="seconds")
    new_baseline = store.get_meta("new_badge_baseline", "") or ""
    agents = []
    for row in store.db.execute("""SELECT * FROM agents
                                  WHERE qa_status!='superseded'
                                  ORDER BY rating DESC,games DESC,id"""):
        aliases = [dict(x) for x in store.db.execute("""SELECT x.notebook_title,x.notebook_url,x.author,x.ref,x.is_current,x.discovered_at,
            n.public_score,n.best_public_score,n.public_votes,n.score_checked_at,n.last_run FROM aliases x JOIN notebook_versions v ON v.id=x.version_id
            JOIN notebooks n ON n.id=v.notebook_id WHERE x.agent_id=?
            ORDER BY x.is_current DESC,COALESCE(n.public_score,-1) DESC,n.last_run DESC,x.id DESC""", (row["id"],))]
        primary = next((x for x in aliases if x["is_current"]), aliases[0] if aliases else {})
        current_scores = [x["public_score"] for x in aliases if x["public_score"] is not None]
        best_scores = [x["best_public_score"] for x in aliases if x["best_public_score"] is not None]
        agents.append({**dict(row), "display_name": primary.get("notebook_title", row["sha256"][:12]),
                       "notebook_url": primary.get("notebook_url"), "author": primary.get("author"),
                       "published_at": primary.get("last_run"),
                       "public_score": max(current_scores) if current_scores else None,
                       "best_public_score": max(best_scores) if best_scores else None,
                       "is_new": any((x.get("discovered_at") or "") > new_baseline and
                                     (x.get("discovered_at") or "") >= new_cutoff for x in aliases),
                       "aliases": aliases})
    matches = [dict(x) for x in store.db.execute("""SELECT m.*,aa.sha256 AS a_sha,bb.sha256 AS b_sha
        FROM matches m JOIN agents aa ON aa.id=m.agent_a JOIN agents bb ON bb.id=m.agent_b
        ORDER BY m.id DESC LIMIT 200""")]
    unplayable = [dict(x) for x in store.db.execute("""SELECT n.ref,n.title,n.author,n.url,n.public_score,
        n.best_public_score,n.last_run,n.last_seen,v.status AS extraction_status,v.error
        FROM notebooks n JOIN notebook_versions v ON v.notebook_id=n.id AND v.version_key=n.current_version_key
        WHERE NOT EXISTS (SELECT 1 FROM aliases x WHERE x.version_id=v.id)
        ORDER BY n.last_run DESC,n.id DESC LIMIT 100""")]
    events = [dict(x) for x in store.db.execute("SELECT * FROM events ORDER BY id DESC LIMIT 100")]
    notebooks = store.db.execute("SELECT COUNT(*) FROM notebooks").fetchone()[0]
    versions = store.db.execute("SELECT COUNT(*) FROM notebook_versions").fetchone()[0]
    valid_total = store.db.execute("SELECT COUNT(*) FROM matches WHERE status='complete'").fetchone()[0]
    return {"generated_at": utcnow(), "state": str(store.state),
            "summary": {"notebooks": notebooks, "versions": versions, "agents": len(agents),
                        "active": sum(x["status"] == "active" for x in agents),
                        "valid_matches": valid_total},
            "last_crawl": store.get_meta("last_crawl"), "last_extract": store.get_meta("last_extract"),
            "last_league": store.get_meta("last_league"), "settings": runtime_settings(store), "agents": agents,
            "matches": matches, "events": events, "unplayable_notebooks": unplayable}


def agent_match_history(store: Store, agent_id: int, limit=500, offset=0) -> dict:
    limit = max(1, min(int(limit), 1000))
    offset = max(0, int(offset))
    agent = store.db.execute(
        "SELECT id,sha256,rating,games,wins,losses,ties,status FROM agents WHERE id=?",
        (int(agent_id),)).fetchone()
    if not agent:
        raise ValueError(f"unknown agent id: {agent_id}")
    alias = store.db.execute("""SELECT notebook_title,notebook_url FROM aliases WHERE agent_id=?
        ORDER BY is_current DESC,id DESC LIMIT 1""", (agent["id"],)).fetchone()
    rows = store.db.execute("""SELECT m.*,aa.sha256 AS a_sha,bb.sha256 AS b_sha,
        COALESCE((SELECT notebook_title FROM aliases WHERE agent_id=m.agent_a
                  ORDER BY is_current DESC,id DESC LIMIT 1),aa.sha256) AS a_name,
        COALESCE((SELECT notebook_title FROM aliases WHERE agent_id=m.agent_b
                  ORDER BY is_current DESC,id DESC LIMIT 1),bb.sha256) AS b_name
        FROM matches m JOIN agents aa ON aa.id=m.agent_a JOIN agents bb ON bb.id=m.agent_b
        WHERE m.agent_a=? OR m.agent_b=? ORDER BY m.id DESC LIMIT ? OFFSET ?""",
        (agent["id"], agent["id"], limit, offset)).fetchall()
    matches = []
    for row in rows:
        is_a = row["agent_a"] == agent["id"]
        outcome = row["outcome_a"] if is_a else (
            None if row["outcome_a"] is None else 1-float(row["outcome_a"]))
        matches.append({
            "id": row["id"], "opponent_id": row["agent_b"] if is_a else row["agent_a"],
            "opponent_name": row["b_name"] if is_a else row["a_name"],
            "opponent_sha": row["b_sha"] if is_a else row["a_sha"],
            "seed": row["seed"], "seat": row["seat_a"] if is_a else 1-row["seat_a"],
            "status": row["status"], "outcome": outcome,
            "own_reward": row["reward_a"] if is_a else row["reward_b"],
            "opponent_reward": row["reward_b"] if is_a else row["reward_a"],
            "margin": row["margin_a"] if is_a else (
                None if row["margin_a"] is None else -row["margin_a"]),
            "runtime": row["runtime"], "error": row["error"],
            "created_at": row["created_at"], "completed_at": row["completed_at"],
        })
    total = store.db.execute(
        "SELECT COUNT(*) FROM matches WHERE agent_a=? OR agent_b=?",
        (agent["id"], agent["id"])).fetchone()[0]
    return {"agent": {**dict(agent),
                      "display_name": alias["notebook_title"] if alias else agent["sha256"][:12],
                      "notebook_url": alias["notebook_url"] if alias else ""},
            "matches": matches, "total": total, "limit": limit, "offset": offset}


def league_progress(store: Store) -> dict:
    latest = store.db.execute(
        "SELECT created_at FROM matches WHERE status='running' ORDER BY id DESC LIMIT 1").fetchone()
    if not latest:
        return {"running": False, "cycle": None}
    row = store.db.execute("""SELECT COUNT(*) AS total,
        SUM(CASE WHEN status='complete' THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN status='invalid' THEN 1 ELSE 0 END) AS invalid,
        SUM(CASE WHEN status='running' THEN 1 ELSE 0 END) AS remaining
        FROM matches WHERE created_at=?""", (latest["created_at"],)).fetchone()
    cycle = {"started_at": latest["created_at"], **dict(row)}
    cycle["done"] = cycle["completed"] + cycle["invalid"]
    cycle["percent"] = round(100 * cycle["done"] / cycle["total"], 1) if cycle["total"] else 0
    return {"running": True, "cycle": cycle}


class BattleController:
    """Runs league batches continuously until the dashboard asks it to stop."""
    def __init__(self, state=DEFAULT_STATE):
        self.state_path = Path(state)
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.thread = None
        self.phase = "stopped"
        self.cycles = 0
        self.last_result = None
        self.last_error = None
        self.focus_agent_id = None
        self.focus_target_games = None
        self.focus_completed_games = 0

    def snapshot(self):
        with self.lock:
            return {"phase": self.phase, "cycles": self.cycles,
                    "last_result": self.last_result, "last_error": self.last_error,
                    "focus_agent_id": self.focus_agent_id,
                    "focus_target_games": self.focus_target_games,
                    "focus_completed_games": self.focus_completed_games}

    def _start_unlocked(self, focus_agent_id=None, focus_target_games=None):
        self.stop_event = threading.Event()
        self.phase = "running"
        self.cycles = 0
        self.last_result = None
        self.last_error = None
        self.focus_agent_id = focus_agent_id
        self.focus_target_games = focus_target_games
        self.focus_completed_games = 0
        self.thread = threading.Thread(target=self._loop, name="public-league-battle", daemon=True)
        self.thread.start()
        return {**self.snapshot_unlocked(), "action": "started"}

    def toggle(self):
        with self.lock:
            alive = bool(self.thread and self.thread.is_alive())
            if alive:
                self.phase = "stopping"
                self.stop_event.set()
                return {**self.snapshot_unlocked(), "action": "stop_requested"}
            return self._start_unlocked()

    def focus(self, agent_id, games=500):
        agent_id = int(agent_id)
        games = int(games)
        if games < 2 or games > 10000 or games % 2:
            raise ValueError("focus games must be an even number from 2 to 10000")
        with self.lock:
            alive = bool(self.thread and self.thread.is_alive())
            if alive and self.focus_agent_id == agent_id:
                self.phase = "stopping"
                self.stop_event.set()
                return {**self.snapshot_unlocked(), "action": "stop_requested"}
        if alive:
            self.stop(wait=True, timeout=15)
        with self.lock:
            if self.thread and self.thread.is_alive():
                raise RuntimeError("current battle did not stop in time")
            return self._start_unlocked(agent_id, games)

    def snapshot_unlocked(self):
        return {"phase": self.phase, "cycles": self.cycles,
                "last_result": self.last_result, "last_error": self.last_error,
                "focus_agent_id": self.focus_agent_id,
                "focus_target_games": self.focus_target_games,
                "focus_completed_games": self.focus_completed_games}

    def stop(self, wait=False, timeout=10):
        with self.lock:
            thread = self.thread
            if thread and thread.is_alive():
                self.phase = "stopping"
                self.stop_event.set()
        if wait and thread and thread.is_alive():
            thread.join(timeout)
        return self.snapshot()

    def _loop(self):
        try:
            while not self.stop_event.is_set():
                store = Store(self.state_path)
                try:
                    settings = runtime_settings(store)
                    with self.lock:
                        focus_agent_id = self.focus_agent_id
                        focus_target_games = self.focus_target_games
                        focus_completed_games = self.focus_completed_games
                    max_matches = int(settings["max_matches"])
                    if focus_agent_id is not None and focus_target_games is not None:
                        remaining = focus_target_games - focus_completed_games
                        if remaining <= 0:
                            break
                        max_matches = min(max_matches, remaining + remaining % 2)
                    result = run_league(store, workers=int(settings["workers"]),
                                        max_matches=max_matches,
                                        stop_event=self.stop_event,
                                        focus_agent_id=focus_agent_id)
                finally:
                    store.close()
                with self.lock:
                    self.last_result = result
                    if not result.get("busy") and not result.get("stopped"):
                        self.cycles += 1
                        if focus_agent_id is not None:
                            self.focus_completed_games += int(result.get("completed", 0))
                            if (self.focus_target_games is not None and
                                    self.focus_completed_games >= self.focus_target_games):
                                break
                if result.get("stopped") or self.stop_event.wait(1 if result.get("busy") else .25):
                    break
        except Exception as exc:
            with self.lock:
                self.last_error = f"{type(exc).__name__}: {exc}"
            with contextlib.suppress(Exception):
                store = Store(self.state_path)
                try:
                    store.event("battle", "continuous battle failed", {"error": self.last_error}, "error")
                finally:
                    store.close()
        finally:
            with self.lock:
                self.phase = "stopped"
                self.focus_agent_id = None


class BrowserSessionTracker:
    def __init__(self):
        self.started = self.last_seen = time.monotonic()
        self.had_session = False
        self.sessions = {}
        self.last_explicit_close = None
        self.lock = threading.Lock()

    def touch(self, session_id: str, now=None):
        if not session_id or len(session_id) > 200:
            raise ValueError("invalid browser session")
        now = time.monotonic() if now is None else now
        with self.lock:
            self.sessions[session_id] = now
            self.last_seen = now
            self.had_session = True
            self.last_explicit_close = None

    def close(self, session_id: str, now=None):
        now = time.monotonic() if now is None else now
        with self.lock:
            self.sessions.pop(session_id, None)
            if not self.sessions:
                self.last_explicit_close = now

    def should_exit(self, idle_seconds=BROWSER_HEARTBEAT_TTL_SECONDS,
                    startup_grace=45, close_grace=BROWSER_CLOSE_GRACE_SECONDS,
                    now=None) -> bool:
        now = time.monotonic() if now is None else now
        with self.lock:
            self.sessions = {key: seen for key, seen in self.sessions.items()
                             if now - seen <= idle_seconds}
            if self.sessions:
                return False
            # pagehide/sendBeacon is an explicit close.  Keep a short grace so
            # reload/navigation can establish its replacement session, while a
            # closed browser still tears the hidden server down promptly.
            if self.last_explicit_close is not None:
                return now - self.last_explicit_close > close_grace
            if self.had_session:
                return now - self.last_seen > idle_seconds
            return now - self.started > startup_grace


DASHBOARD = r'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Kaggriculture Public League</title>
<style>
:root{color-scheme:dark;--bg:#09110d;--card:#111d17;--line:#284034;--text:#e9f3ec;--muted:#9db0a4;--green:#56d489;--gold:#efc464;--red:#ef7b74}*{box-sizing:border-box}body{margin:0;font:14px system-ui;background:var(--bg);color:var(--text)}main{width:100%;max-width:1800px;margin:auto;padding:16px}h1{margin:0 0 4px;font-size:28px}.muted{color:var(--muted)}.bar,.cards,.settings,.legend{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;align-items:center}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 13px}.metric{font-size:22px;font-weight:700;color:var(--green)}button{background:#1f6c42;color:white;border:0;border-radius:7px;padding:8px 11px;cursor:pointer}button.stop,button.toggle-off{background:#8b3434}button:disabled{opacity:.5}input{width:90px;background:#09110d;color:var(--text);border:1px solid var(--line);border-radius:6px;padding:7px}table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line)}th,td{padding:7px 6px;border-bottom:1px solid var(--line);text-align:left}th{position:sticky;top:0;background:#16251d}a{color:#76c8ff}.active{color:var(--green)}.candidate{color:var(--gold)}.archived{color:var(--muted)}.quarantine{color:var(--red)}.new{display:inline-block;margin-left:5px;padding:2px 5px;border-radius:999px;background:#efc464;color:#182017;font-size:10px;font-weight:800;vertical-align:middle}details{max-width:100%}code{font-size:11px}.tabs button{background:#17281f}.tabs button.on{background:#276a46}.panel{display:none}.panel.on{display:block}.scroll{max-height:72vh;overflow:auto}.legend .card{flex:1 1 0;max-width:none;min-width:220px;align-self:stretch}.legend b{display:block;margin-bottom:4px}#rank table{table-layout:fixed;min-width:1280px}#rank th:nth-child(1){width:3.5%}#rank th:nth-child(2){width:20%}#rank th:nth-child(3){width:8%}#rank th:nth-child(4){width:6%}#rank th:nth-child(5){width:6%}#rank th:nth-child(6){width:5%}#rank th:nth-child(7){width:8%}#rank th:nth-child(8){width:8%}#rank th:nth-child(9){width:8%}#rank th:nth-child(10){width:7%}#rank th:nth-child(11){width:12.5%}#rank th:nth-child(12){width:8%}#rank td{overflow-wrap:anywhere}.rowactions{display:flex;gap:3px;flex-wrap:nowrap}.rowactions button{white-space:nowrap;padding:6px 7px;font-size:11px}.focusbtn{min-width:72px}</style></head><body><main>
<h1>Kaggriculture Public League</h1><div class="muted" id="stamp">불러오는 중…</div>
<div class="muted">표의 순위는 로컬 native 리그의 정규화 Bradley–Terry(BT) 점수입니다. Kaggle 현재/최고 점수는 시점 의존 참고값으로 별도 표시됩니다. NEW는 기준선 이후 새 노트북 버전이 편입된 뒤 12시간 동안 표시됩니다.</div>
<div class="bar"><button id="collectButton" onclick="collectNow()">지금 수집</button><button id="battleButton" onclick="toggleBattle()">연속 대결 OFF · 시작</button><span class="muted">ON이면 수동 중지까지 계속 대결</span><button onclick="load()">화면 새로고침</button><span id="action"></span></div>
<div class="card settings"><b>자동 수집·대결 설정</b><button id="autoCollectButton" onclick="toggleAutoCollect()">자동 수집 확인 중…</button><label>수집 주기(시간) <input id="intervalHours" type="number" min="0.25" max="168" step="0.25"></label><label>대결 워커 수 <input id="workers" type="number" min="1" max="12" step="1"></label><button onclick="saveSettings()">설정 저장</button><span class="muted" id="settingsResult">수집은 예약 실행, 대결 워커는 다음 배치부터 적용</span></div>
<div class="card settings"><b>노트북 검색·직접 추가</b><input id="searchQuery" style="width:min(520px,70vw)" placeholder="제목 검색 또는 https://www.kaggle.com/code/author/slug"><button onclick="searchNotebooks()">검색</button><label>집중 추가 유효 경기 수 <input id="focusGames" type="number" min="2" max="10000" step="2" value="500"></label><span class="muted" id="searchResultText">기존 누적 경기와 별도로 추가 측정 · 양 좌석 묶음 때문에 최대 1경기 초과 가능</span></div>
<div id="searchResults" class="card" style="display:none"></div>
<details class="card"><summary><b>현재 매칭 방식</b></summary><p>일반 대결은 QA-pass agent 중 상위 active와 신규 challenger를 최대 100개 풀로 잡습니다. 표본이 부족한 모델을 먼저 고르고, 경기 수와 상대 전적이 비슷하면 BT 점수가 가까운 상대를 우선합니다. 신규 모델은 32경기까지 catch-up하며 세 번째 대진마다 경험 많은 강자를 섞습니다. 집중 측정은 선택한 agent를 모든 경기에 고정합니다. 같은 결정적 seed를 양 좌석으로 실행하며 동일 계약·두 artifact·seed·좌석은 다시 돌리지 않습니다. 240경기는 내부 재편성 묶음이고 유효 경기만 BT·승점률에 반영합니다. main.py와 모든 제출 부속파일이 같은 artifact만 별칭으로 묶습니다.</p></details>
<div class="cards" id="cards"></div><div class="tabs"><button class="on" onclick="tab('rank',this)">랭킹</button> <button id="agentMatchTab" onclick="tab('agentmatches',this)">선택 agent 전적</button> <button onclick="tab('unplayable',this)">수집됨·대전 불가</button> <button onclick="tab('events',this)">수집 기록</button> <button onclick="tab('matches',this)">최근 경기</button></div>
<div class="legend"><div class="card"><b class="active">active</b>최소 8개 유효 경기를 마치고 현재 상위 100에 든 agent.</div><div class="card"><b class="candidate">candidate</b>실제 첫 행동 QA를 통과했지만 아직 표본이 부족하거나 도전자 대기열에 있는 agent.</div><div class="card"><b class="archived">archived</b>검증은 끝났지만 현재 상위 100 밖인 agent. 파일과 전적은 보존된다.</div><div class="card"><b class="quarantine">quarantine</b>컴파일·loader·첫 행동 QA 실패 또는 반복 코드 예외가 확인된 agent. 공식 DONE 경기의 로컬 시간 경고만으로 격리하지 않는다.</div></div>
<section id="rank" class="panel on scroll"><table><thead><tr><th>로컬 #</th><th>공유 노트북</th><th>작성자</th><th>게시/갱신</th><th>상태</th><th>로컬 BT</th><th>Kaggle 현재/최고</th><th>W-L-T</th><th>승점률 95% CI</th><th>artifact</th><th>측정·전적</th><th>동일 artifact 별칭</th></tr></thead><tbody id="agents"></tbody></table></section>
<section id="agentmatches" class="panel scroll"><div class="card" id="agentmatchsummary">순위표에서 <b>전적 보기</b>를 누르세요.</div><table><thead><tr><th>시각 (KST)</th><th>상대</th><th>시드·좌석</th><th>결과</th><th>우리/상대 현금</th><th>마진</th><th>상태·오류</th></tr></thead><tbody id="agentmatchrows"></tbody></table></section>
<section id="unplayable" class="panel scroll"><p class="muted">목록과 파일은 수집했지만 실행 가능한 agent 소스를 찾지 못했거나 추출을 완료하지 못한 최신 버전입니다. 로컬 대전에는 넣지 않습니다.</p><table><thead><tr><th>공유 노트북</th><th>작성자</th><th>게시/갱신</th><th>Kaggle 현재/최고</th><th>수집 상태</th><th>이유</th></tr></thead><tbody id="unplayablerows"></tbody></table></section>
<section id="events" class="panel scroll"><table><thead><tr><th>시각 (KST)</th><th>종류</th><th>내용</th></tr></thead><tbody id="eventrows"></tbody></table></section>
<section id="matches" class="panel scroll"><table><thead><tr><th>시각 (KST)</th><th>A/B</th><th>시드·좌석</th><th>상태</th><th>마진 A</th></tr></thead><tbody id="matchrows"></tbody></table></section>
</main><script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtTime=s=>{if(!s)return '—';let d=new Date(s);if(Number.isNaN(d.getTime()))return String(s);return new Intl.DateTimeFormat('ko-KR',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).format(d)};
let lastGeneratedAt='—',agentNames={};
const browserSession=sessionStorage.getItem('publicLeagueSession')||crypto.randomUUID();sessionStorage.setItem('publicLeagueSession',browserSession);
const pulse=()=>fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:browserSession}),keepalive:true}).catch(()=>{});pulse();setInterval(pulse,5000);addEventListener('pagehide',()=>navigator.sendBeacon('/api/session/close',JSON.stringify({id:browserSession})));
function tab(id,b){document.querySelectorAll('.panel').forEach(x=>x.classList.remove('on'));document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));document.getElementById(id).classList.add('on');b.classList.add('on')}
async function load(){let d=await fetch('/api/status').then(r=>r.json());agentNames=Object.fromEntries(d.agents.map(a=>[a.id,a.display_name]));lastGeneratedAt=fmtTime(d.generated_at);document.getElementById('stamp').textContent='갱신 '+lastGeneratedAt+' · 상태 확인 중';let s=d.summary;document.getElementById('cards').innerHTML=`<div class=card id=cyclecard><div class=metric>—</div>현재 대전 확인 중</div><div class=card><div class=metric>${s.notebooks}</div>노트북</div><div class=card><div class=metric>${s.agents}</div>고유 agent</div><div class=card><div class=metric>${s.active}</div>활성 리그</div><div class=card><div class=metric>${s.valid_matches}</div>누적 유효 경기</div>`;if(document.activeElement.id!=='intervalHours')document.getElementById('intervalHours').value=d.settings.interval_hours;if(document.activeElement.id!=='workers')document.getElementById('workers').value=d.settings.workers;
document.getElementById('agents').innerHTML=d.agents.map((a,i)=>{let rate=a.games?((a.wins+.5*a.ties)/a.games*100).toFixed(1):'—';let ci=a.score_low==null?'—':`${(a.score_low*100).toFixed(1)}–${(a.score_high*100).toFixed(1)}%`;let ps=a.public_score==null?'—':a.public_score.toFixed(1),bs=a.best_public_score==null?'—':a.best_public_score.toFixed(1),date=a.published_at?String(a.published_at).slice(0,10):'—';let als=a.aliases.map(x=>`<div><a target=_blank href="${esc(x.notebook_url)}">${esc(x.notebook_title)}</a> · ${esc(x.author)} · ${esc((x.last_run||'—').slice(0,10))} · Kaggle ${x.public_score==null?'—':Number(x.public_score).toFixed(1)}</div>`).join('');let files=(()=>{try{return JSON.parse(a.artifact_files_json||'[]').length}catch(_){return 1}})();return `<tr><td>${i+1}</td><td><a target=_blank href="${esc(a.notebook_url)}">${esc(a.display_name)}</a>${a.is_new?'<span class=new>NEW</span>':''}</td><td>${esc(a.author)}</td><td>${esc(date)}</td><td class=${esc(a.status)}>${esc(a.status)}</td><td>${a.rating.toFixed(0)}</td><td>${ps} / ${bs}</td><td>${a.wins}-${a.losses}-${a.ties} (${rate}%)</td><td>${ci}</td><td><code>${a.sha256.slice(0,12)}</code><div class=muted>${esc(a.execution_platform)} · ${files}파일</div></td><td><div class="rowactions"><button class="focusbtn" data-focus-agent="${a.id}" onclick="focusAgent(${a.id})">집중 측정</button><button onclick="showAgentMatches(${a.id})">전적 보기</button></div></td><td><details><summary>동일 artifact ${a.aliases.length}개</summary>${als}</details></td></tr>`}).join('');
document.getElementById('unplayablerows').innerHTML=(d.unplayable_notebooks||[]).map(x=>`<tr><td><a target=_blank href="${esc(x.url)}">${esc(x.title)}</a></td><td>${esc(x.author)}</td><td>${esc(fmtTime(x.last_run))}</td><td>${x.public_score==null?'—':Number(x.public_score).toFixed(1)} / ${x.best_public_score==null?'—':Number(x.best_public_score).toFixed(1)}</td><td>${esc(x.extraction_status)}</td><td>${esc(x.error||'실행 가능한 agent 소스 없음')}</td></tr>`).join('');
document.getElementById('eventrows').innerHTML=d.events.map(x=>`<tr><td>${esc(fmtTime(x.created_at))}</td><td>${esc(x.kind)}</td><td>${esc(x.message)}</td></tr>`).join('');document.getElementById('matchrows').innerHTML=d.matches.map(x=>`<tr><td>${esc(fmtTime(x.completed_at||x.created_at))}</td><td><code>${x.a_sha.slice(0,8)} / ${x.b_sha.slice(0,8)}</code></td><td>${x.seed} · ${x.seat_a}</td><td>${esc(x.status)}</td><td>${x.margin_a??'—'}</td></tr>`).join('');loadProgress()}
async function loadProgress(){let box=document.getElementById('cyclecard'),stamp=document.getElementById('stamp'),battle=document.getElementById('battleButton'),collect=document.getElementById('collectButton'),auto=document.getElementById('autoCollectButton');if(!box)return;try{let d=await fetch('/api/progress',{cache:'no-store'}).then(r=>r.json()),b=d.battle||{phase:'stopped'},autoOn=!!d.auto_collect_enabled,focus=b.focus_agent_id,focusTarget=b.focus_target_games,focusDone=b.focus_completed_games||0,focusName=focus?(agentNames[focus]||`agent ${focus}`):'';collect.disabled=!!d.collecting;collect.textContent=d.collecting?'수집 중…':'지금 수집';auto.textContent=autoOn?'자동 수집 ON · 끄기':'자동 수집 OFF · 켜기';auto.classList.toggle('toggle-off',!autoOn);document.querySelectorAll('[data-focus-agent]').forEach(x=>{let on=b.phase!=='stopped'&&Number(x.dataset.focusAgent)===Number(focus);x.textContent=on?'집중 중지':'집중 측정';x.classList.toggle('stop',on);x.disabled=b.phase==='stopping'});battle.textContent=b.phase==='stopped'?'연속 대결 OFF · 시작':b.phase==='stopping'?'대결 중지 중…':focus?`${focusName} 집중 측정 ON · 중지`:'연속 대결 ON · 중지';battle.classList.toggle('stop',b.phase!=='stopped');battle.disabled=b.phase==='stopping';if(!d.cycle){if(b.phase==='running'){box.innerHTML=`<div class=metric>준비</div>${focus?esc(focusName)+` 집중 추가 ${focusDone}/${focusTarget}`:'다음 처리 묶음 편성'} · 완료 묶음 ${b.cycles}`;stamp.textContent=`갱신 ${lastGeneratedAt} · ${focus?esc(focusName)+` 집중 추가 ${focusDone}/${focusTarget}`:'수동 중지까지 연속 대결 중'}`}else if(b.phase==='stopping'){box.innerHTML='<div class=metric>중지</div>대전 프로세스 정리 중';stamp.textContent=`갱신 ${lastGeneratedAt} · 대전 중지 중`}else{box.innerHTML='<div class=metric>0</div>현재 대전 대기';stamp.textContent=`갱신 ${lastGeneratedAt} · 대기`}return}let c=d.cycle,focusLiveDone=focus?focusDone+(c.completed||0):focusDone;box.innerHTML=`<div class=metric>${c.done}/${c.total}</div>${focus?esc(focusName)+` 집중 추가 ${focusLiveDone}/${focusTarget}`:'현재 처리 묶음'} ${c.percent.toFixed(1)}% · 남음 ${c.remaining}<div class=muted>수동 중지까지 계속 · KST ${esc(fmtTime(c.started_at))}</div>`;stamp.textContent=`갱신 ${lastGeneratedAt} · ${b.phase==='stopping'?'대전 중지 중':focus?esc(focusName)+` 집중 추가 ${focusLiveDone}/${focusTarget}`:'연속 대결 중'} (${c.done}/${c.total})`}catch(_){box.innerHTML='<div class=metric>?</div>진행 상태 확인 실패';stamp.textContent=`갱신 ${lastGeneratedAt} · 상태 확인 실패`}}
async function collectNow(){let e=document.getElementById('action');e.textContent='수집 시작 요청 중…';let r=await fetch('/api/collect',{method:'POST'}),d=await r.json();e.textContent=d.message||JSON.stringify(d);loadProgress()}
async function toggleBattle(){let e=document.getElementById('action');e.textContent='대결 상태 변경 중…';let r=await fetch('/api/battle/toggle',{method:'POST'}),d=await r.json();e.textContent=d.message||JSON.stringify(d);loadProgress()}
async function focusAgent(id){let e=document.getElementById('action'),games=Number(document.getElementById('focusGames').value)||500;e.textContent='집중 측정 상태 변경 중…';let r=await fetch('/api/focus',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({agent_id:id,games})}),d=await r.json();e.textContent=d.message||d.error||JSON.stringify(d);loadProgress()}
async function showAgentMatches(id){let e=document.getElementById('action');e.textContent='전적 불러오는 중…';let r=await fetch(`/api/agent-matches?agent_id=${id}&limit=500`),d=await r.json();if(!r.ok){e.textContent=d.error||'전적 조회 실패';return}let a=d.agent,rate=a.games?((a.wins+.5*a.ties)/a.games*100).toFixed(1):'—';document.getElementById('agentmatchsummary').innerHTML=`<b>${esc(a.display_name)}</b> · BT ${Number(a.rating).toFixed(0)} · ${a.wins}-${a.losses}-${a.ties} (${rate}%) · 저장된 경기 ${d.total}개${d.total>d.matches.length?` · 최근 ${d.matches.length}개 표시`:''}`;document.getElementById('agentmatchrows').innerHTML=d.matches.map(x=>{let result=x.status!=='complete'?'무효':x.outcome===1?'승':x.outcome===0?'패':'무';let cash=x.own_reward==null?'—':`${Number(x.own_reward).toFixed(0)} / ${Number(x.opponent_reward).toFixed(0)}`;let margin=x.margin==null?'—':Number(x.margin).toFixed(0);return `<tr><td>${esc(fmtTime(x.completed_at||x.created_at))}</td><td>${esc(x.opponent_name)} <code>${esc(x.opponent_sha.slice(0,8))}</code></td><td>${x.seed} · ${x.seat}</td><td>${result}</td><td>${cash}</td><td>${margin}</td><td>${esc(x.status)}${x.error?` · ${esc(x.error)}`:''}</td></tr>`}).join('');tab('agentmatches',document.getElementById('agentMatchTab'));e.textContent=`${a.display_name} 전적을 불러왔습니다.`}
async function searchNotebooks(){let q=document.getElementById('searchQuery').value.trim(),e=document.getElementById('searchResultText'),box=document.getElementById('searchResults');if(!q){e.textContent='검색어 또는 URL을 입력하세요.';return}e.textContent='검색 중…';let r=await fetch('/api/search?q='+encodeURIComponent(q)),d=await r.json();if(!r.ok){e.textContent=d.error||'검색 실패';return}box.style.display='block';box.innerHTML=d.results.length?d.results.map(x=>{let dup=x.duplicate_type?`<span class=muted>${esc(x.duplicate_type)} · ${esc(x.duplicate_detail||'')}</span>`:'<span class=muted>아직 수집되지 않음</span>';return `<div style=margin:8px 0><a target=_blank href="${esc(x.url)}"><b>${esc(x.title)}</b></a> · ${esc(x.author)} · ${dup} <button onclick="addNotebook('${esc(x.ref)}',false)">추가</button> <button onclick="addNotebook('${esc(x.ref)}',true)">추가+집중</button></div>`}).join(''):'검색 결과 없음';e.textContent=`검색 결과 ${d.results.length}개`}
async function addNotebook(ref,focus){let e=document.getElementById('searchResultText'),games=Number(document.getElementById('focusGames').value)||500;e.textContent='노트북 내려받기·추출 중…';let r=await fetch('/api/add-notebook',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ref,focus,games})}),d=await r.json();e.textContent=r.ok?`${d.title}: ${d.duplicate_type} · ${d.duplicate_detail}`:(d.error||'추가 실패');if(r.ok){await load();if(d.agent_id)await showAgentMatches(d.agent_id)}}
async function toggleAutoCollect(){let e=document.getElementById('settingsResult'),b=document.getElementById('autoCollectButton');e.textContent='자동 수집 상태 변경 중…';b.disabled=true;let r=await fetch('/api/auto-collect/toggle',{method:'POST'}),d=await r.json();e.textContent=r.ok?(d.settings.auto_collect_enabled?'자동 수집을 켰습니다.':'자동 수집을 껐습니다.'):(d.error||'상태 변경 실패');b.disabled=false;loadProgress()}
load();setInterval(load,30000);setInterval(loadProgress,5000);
async function saveSettings(){let e=document.getElementById('settingsResult');e.textContent='저장 중…';let body={interval_hours:Number(document.getElementById('intervalHours').value),workers:Number(document.getElementById('workers').value)};let r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});let d=await r.json();e.textContent=r.ok?`저장됨: ${d.settings.interval_hours}시간마다, 워커 ${d.settings.workers}`:(d.error||'저장 실패');if(r.ok)load()}
</script></body></html>'''


def serve(state=DEFAULT_STATE, host="127.0.0.1", port=8791, exit_with_browser=False):
    collect_lock = threading.Lock()
    sessions = BrowserSessionTracker()
    battle = BattleController(state)

    class Handler(BaseHTTPRequestHandler):
        def send(self, code, data, content_type="application/json; charset=utf-8"):
            body = data if isinstance(data, bytes) else data.encode("utf-8")
            self.send_response(code); self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path in ("/", "/index.html"):
                self.send(200, DASHBOARD, "text/html; charset=utf-8")
            elif parsed.path == "/api/status":
                local = Store(state)
                try:
                    payload = dashboard_snapshot(local)
                finally:
                    local.close()
                self.send(200, json.dumps(payload, ensure_ascii=False))
            elif parsed.path == "/api/agent-matches":
                try:
                    query = urllib.parse.parse_qs(parsed.query)
                    agent_id = int(query.get("agent_id", [""])[0])
                    limit = int(query.get("limit", ["500"])[0])
                    offset = int(query.get("offset", ["0"])[0])
                    local = Store(state)
                    try:
                        payload = agent_match_history(local, agent_id, limit, offset)
                    finally:
                        local.close()
                    self.send(200, json.dumps(payload, ensure_ascii=False))
                except Exception as exc:
                    self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            elif parsed.path == "/api/search":
                try:
                    query = urllib.parse.parse_qs(parsed.query).get("q", [""])[0]
                    local = Store(state)
                    try:
                        payload = search_public_notebooks(local, query)
                    finally:
                        local.close()
                    self.send(200, json.dumps(payload, ensure_ascii=False))
                except Exception as exc:
                    self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            elif parsed.path == "/api/progress":
                local = Store(state)
                try:
                    payload = league_progress(local)
                    payload["auto_collect_enabled"] = bool(runtime_settings(local)["auto_collect_enabled"])
                finally:
                    local.close()
                payload["battle"] = battle.snapshot()
                payload["collecting"] = collect_lock.locked()
                self.send(200, json.dumps(payload, ensure_ascii=False))
            else:
                self.send(404, json.dumps({"error": "not found"}))

        def do_POST(self):
            if self.path in ("/api/session", "/api/session/close"):
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    if self.path.endswith("/close"):
                        sessions.close(payload.get("id", ""))
                    else:
                        sessions.touch(payload.get("id", ""))
                    return self.send(204, b"")
                except Exception as exc:
                    return self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            if self.path == "/api/settings":
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    local = Store(state)
                    try:
                        settings = update_runtime_settings(local, payload.get("interval_hours"), payload.get("workers"))
                    finally:
                        local.close()
                    return self.send(200, json.dumps({"settings": settings}, ensure_ascii=False))
                except Exception as exc:
                    return self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            if self.path == "/api/battle/toggle":
                status = battle.toggle()
                message = "연속 대결을 시작했습니다." if status["action"] == "started" else "대결 중지를 요청했습니다."
                return self.send(202, json.dumps({"message": message, "battle": status}, ensure_ascii=False))
            if self.path == "/api/focus":
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    agent_id = int(payload.get("agent_id"))
                    focus_games = int(payload.get("games", 500))
                    local = Store(state)
                    try:
                        agent = local.db.execute(
                            "SELECT id,sha256,qa_status,status FROM agents WHERE id=?", (agent_id,)).fetchone()
                    finally:
                        local.close()
                    if not agent or agent["qa_status"] != "pass" or agent["status"] == "quarantine":
                        raise ValueError("집중 측정할 수 있는 QA-pass agent가 아닙니다.")
                    status = battle.focus(agent_id, focus_games)
                    if status["action"] == "started":
                        message = f"agent {agent_id} 집중 측정 {focus_games}경기를 시작했습니다."
                    else:
                        message = f"agent {agent_id} 집중 측정 중지를 요청했습니다."
                    return self.send(202, json.dumps({"message": message, "battle": status}, ensure_ascii=False))
                except Exception as exc:
                    return self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            if self.path == "/api/add-notebook":
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    local = Store(state)
                    try:
                        result = add_public_notebook(local, payload.get("ref") or payload.get("url") or "")
                    finally:
                        local.close()
                    focus = bool(payload.get("focus"))
                    if focus and result.get("agent_id"):
                        focus_games = int(payload.get("games", 500))
                        result["battle"] = battle.focus(result["agent_id"], focus_games)
                    return self.send(200, json.dumps(result, ensure_ascii=False))
                except Exception as exc:
                    return self.send(400, json.dumps({"error": str(exc)}, ensure_ascii=False))
            if self.path == "/api/auto-collect/toggle":
                try:
                    local = Store(state)
                    try:
                        settings = toggle_auto_collection(local)
                    finally:
                        local.close()
                    return self.send(200, json.dumps({"settings": settings}, ensure_ascii=False))
                except Exception as exc:
                    return self.send(500, json.dumps({"error": str(exc)}, ensure_ascii=False))
            if self.path != "/api/collect":
                return self.send(404, json.dumps({"error": "not found"}))
            if not collect_lock.acquire(blocking=False):
                return self.send(409, json.dumps({"message": "이미 수집 중입니다."}, ensure_ascii=False))
            def task():
                try:
                    local = Store(state)
                    try:
                        collect_cycle(local)
                    finally:
                        local.close()
                finally:
                    collect_lock.release()
            threading.Thread(target=task, daemon=True).start()
            self.send(202, json.dumps({"message": "백그라운드 수집을 시작했습니다."}, ensure_ascii=False))

        def log_message(self, fmt, *args):
            pass

    print(f"Public league dashboard: http://{host}:{port}", flush=True)
    server = ThreadingHTTPServer((host, port), Handler)
    if exit_with_browser:
        def browser_watch():
            while not sessions.should_exit():
                time.sleep(2)
            battle.stop(wait=True)
            server.shutdown()
        threading.Thread(target=browser_watch, daemon=True).start()
    try:
        server.serve_forever()
    finally:
        battle.stop(wait=True)
        server.server_close()


def collect_cycle(store: Store, limit=200, pull_limit=40) -> dict:
    with process_lock(store.state / "refresh.lock") as acquired:
        if not acquired:
            return {"busy": True, "message": "another collection cycle is already running"}
        return _collect_cycle_unlocked(store, limit, pull_limit)


def _collect_cycle_unlocked(store: Store, limit=200, pull_limit=40) -> dict:
    result = {}
    try:
        result["crawl"] = collect(store, limit=limit, pull_limit=pull_limit)
    except Exception as exc:
        store.event("crawl", "crawl failed; preserved prior database", {"error": str(exc)}, "error")
        result["crawl"] = {"error": str(exc)}
    result["extract"] = extract(store)
    result["local_agents"] = import_local_agents(store)
    result["repair"] = repair_nonfatal_telemetry_matches(store)
    return result


def refresh(store: Store, workers=8, limit=200, pull_limit=40, top_k=DEFAULT_TOP_K,
            seeds_per_pair=1, max_matches=240) -> dict:
    """Legacy one-shot command: collect once, then run one league batch."""
    with process_lock(store.state / "refresh.lock") as acquired:
        if not acquired:
            return {"busy": True, "message": "another collection cycle is already running"}
        result = _collect_cycle_unlocked(store, limit, pull_limit)
    result["league"] = run_league(store, workers=workers, top_k=top_k,
                                  seeds_per_pair=seeds_per_pair, max_matches=max_matches)
    return result


def _qa_main(source: Path, result: Path):
    payload = {"ok": False}
    try:
        from kaggle_environments.agent import get_last_callable
        code = source.read_text(encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            entry = get_last_callable(code, path=str(source))
        if not callable(entry):
            raise TypeError("last object is not callable")
        from kaggle_environments import make
        env = make("kaggriculture", configuration={"episodeSteps": 2, "seed": 1}, debug=False)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            steps = env.run([str(source), "starter"])
        if len(steps) < 2 or str(steps[-1][0].status) != "DONE":
            error = "official runner did not complete first action"
            if getattr(env, "logs", None):
                error += f": {env.logs[0][-1:]!r}"
            raise RuntimeError(error)
        action = steps[1][0].action
        if not isinstance(action, dict):
            raise TypeError(f"first action is {type(action).__name__}, expected dict")
        payload = {"ok": True, "entrypoint": getattr(entry, "__name__", type(entry).__name__),
                   "first_action": "dict"}
    except Exception as exc:
        payload = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    result.write_text(json.dumps(payload), encoding="utf-8")


def _worker_main(job_path: Path, result_path: Path):
    job = json.loads(job_path.read_text(encoding="utf-8"))
    result_path.write_text(json.dumps(_league_job(job), ensure_ascii=False), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    crawl = sub.add_parser("crawl"); crawl.add_argument("--limit", type=int, default=200); crawl.add_argument("--pull-limit", type=int, default=40)
    ext = sub.add_parser("extract"); ext.add_argument("--limit", type=int, default=100)
    imp = sub.add_parser("import-existing"); imp.add_argument("paths", nargs="+", type=Path)
    sub.add_parser("import-local")
    restore = sub.add_parser("restore-runtime-quarantine")
    restore.add_argument("--sha256", required=True)
    restore.add_argument("--reason", required=True)
    collect_cmd = sub.add_parser("collect"); collect_cmd.add_argument("--limit", type=int, default=200); collect_cmd.add_argument("--pull-limit", type=int, default=40)
    run = sub.add_parser("run"); run.add_argument("--workers", type=int, default=8, choices=range(1,13)); run.add_argument("--top-k", type=int, default=DEFAULT_TOP_K); run.add_argument("--seeds-per-pair", type=int, default=1); run.add_argument("--max-matches", type=int, default=240); run.add_argument("--timeout", type=float, default=PUBLIC_LEAGUE_MATCH_TIMEOUT_SECONDS)
    ref = sub.add_parser("refresh"); ref.add_argument("--workers", type=int, default=8, choices=range(1,13)); ref.add_argument("--limit", type=int, default=200); ref.add_argument("--pull-limit", type=int, default=40); ref.add_argument("--top-k", type=int, default=DEFAULT_TOP_K); ref.add_argument("--seeds-per-pair", type=int, default=1); ref.add_argument("--max-matches", type=int, default=240)
    status = sub.add_parser("status"); status.add_argument("--json", action="store_true")
    web = sub.add_parser("serve"); web.add_argument("--host", default="127.0.0.1"); web.add_argument("--port", type=int, default=8791); web.add_argument("--exit-with-browser", action="store_true")
    qa = sub.add_parser("_qa"); qa.add_argument("--source", type=Path, required=True); qa.add_argument("--result", type=Path, required=True)
    worker = sub.add_parser("_worker"); worker.add_argument("--job", type=Path, required=True); worker.add_argument("--result", type=Path, required=True)
    args = ap.parse_args(argv)
    if args.command == "_qa": return _qa_main(args.source, args.result)
    if args.command == "_worker": return _worker_main(args.job, args.result)
    if args.command == "serve": return serve(args.state, args.host, args.port, args.exit_with_browser)
    store = Store(args.state)
    if args.command == "init": result = {"database": str(store.db_path), "schema": SCHEMA_VERSION}
    elif args.command == "crawl": result = collect(store, args.limit, args.pull_limit)
    elif args.command == "extract": result = extract(store, args.limit)
    elif args.command == "import-existing": result = import_existing(store, args.paths)
    elif args.command == "import-local": result = import_local_agents(store)
    elif args.command == "restore-runtime-quarantine":
        result = restore_runtime_quarantine(store, args.sha256, args.reason)
    elif args.command == "collect": result = collect_cycle(store, args.limit, args.pull_limit)
    elif args.command == "run": result = run_league(store, args.workers, args.top_k, args.seeds_per_pair, args.max_matches, args.timeout)
    elif args.command == "refresh": result = refresh(store, args.workers, args.limit, args.pull_limit, args.top_k, args.seeds_per_pair, args.max_matches)
    else: result = dashboard_snapshot(store)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
