import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.kaggriculture_meta import public_league as league


AGENT = '''def agent(obs, config):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''


class PublicLeagueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.root = Path(self.tmp.name)
        self.store = league.Store(self.root / "state")

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def add_version(self, ref, title, archive, version="v1"):
        author, slug = ref.split("/", 1)
        now = league.utcnow()
        with self.store.db:
            self.store.db.execute("""INSERT INTO notebooks
              (ref,title,author,slug,url,first_seen,last_seen,current_version_key)
              VALUES(?,?,?,?,?,?,?,?)""", (ref, title, author, slug,
                f"https://www.kaggle.com/code/{ref}", now, now, version))
            nid = self.store.db.execute("SELECT id FROM notebooks WHERE ref=?", (ref,)).fetchone()[0]
            cur = self.store.db.execute("""INSERT INTO notebook_versions
              (notebook_id,version_key,metadata_json,archive_path,status,first_seen,pulled_at)
              VALUES(?,?,?,?,'pulled',?,?)""", (nid, version, "{}", str(archive), now, now))
        return cur.lastrowid

    def notebook(self, directory, source=AGENT):
        directory.mkdir(parents=True)
        doc = {"cells": [{"cell_type": "code", "source": "%%writefile main.py\n" + source}]}
        (directory / "agent.ipynb").write_text(json.dumps(doc), encoding="utf-8")

    def test_listing_preserves_exact_title_and_builds_original_link(self):
        row = league.normalize_listing_item({"ref": "alice/great-bot", "title": "Great Bot 🌾",
                                             "lastRunTime": "2026-09-20", "totalVotes": 9})
        self.assertEqual(row["title"], "Great Bot 🌾")
        self.assertEqual(row["url"], "https://www.kaggle.com/code/alice/great-bot")
        self.assertEqual(row["public_votes"], 9)
        self.assertIsNone(row["public_score"])

    def test_public_score_comes_from_linked_submission_not_votes(self):
        row = league.normalize_listing_item({"ref": "alice/great-bot", "title": "Great Bot",
                                             "lastRunTime": "2026-09-20", "totalVotes": 99})
        response = io.BytesIO(json.dumps({
            "kernel": {"upvoteCount": 99, "bestPublicScore": 2801},
            "submission": {"scoreFormatted": "2755.4"},
            "bestSubmissionScore": {"scoreFormatted": "2801.2"},
        }).encode())
        with patch.object(league.urllib.request, "urlopen", return_value=response):
            score = league.fetch_public_score(row)
        self.assertEqual(score["public_score"], 2755.4)
        self.assertEqual(score["best_public_score"], 2801.2)
        self.assertEqual(score["public_votes"], 99)

    def test_extract_writefile_main_tar_and_literal(self):
        nb = self.root / "n.ipynb"
        nb.write_text(json.dumps({"cells": [
            {"cell_type": "code", "source": "%%writefile main.py\n" + AGENT},
            {"cell_type": "code", "source": "BOT = " + repr(AGENT * 10)},
        ]}), encoding="utf-8")
        found = league.sources_from_notebook(nb)
        self.assertTrue(any(origin.endswith("writefile") for origin, _ in found))
        tar_path = self.root / "submission.tar.gz"
        payload = AGENT.encode()
        with tarfile.open(tar_path, "w:gz") as tf:
            info = tarfile.TarInfo("main.py"); info.size = len(payload)
            tf.addfile(info, io.BytesIO(payload))
        self.assertEqual(league.sources_from_archive(tar_path)[0][1], payload)

    def test_artifact_paths_reject_traversal_and_absolute_members(self):
        for value in ("../evil.py", "a/../../evil.py", "/tmp/evil.py",
                      r"C:\\tmp\\evil.py", r"..\\evil.py"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                league.safe_relative_path(value)
        self.assertEqual(league.safe_relative_path("./bundle/main.py"), "bundle/main.py")

    def test_multifile_tar_identity_includes_runtime_sidecars(self):
        def write_bundle(path, sidecar):
            with tarfile.open(path, "w:gz") as tf:
                for name, payload in (("main.py", AGENT.encode()), ("actions.json", sidecar)):
                    info = tarfile.TarInfo(name); info.size = len(payload)
                    tf.addfile(info, io.BytesIO(payload))
        first = self.root / "one.tar.gz"; second = self.root / "two.tar.gz"
        write_bundle(first, b"[1]"); write_bundle(second, b"[2]")
        files_a = league.artifacts_from_archive(first)[0][1]
        files_b = league.artifacts_from_archive(second)[0][1]
        self.assertEqual(set(files_a), {"main.py", "actions.json"})
        self.assertNotEqual(league.artifact_digest(files_a), league.artifact_digest(files_b))

    def test_compiled_cpp_build_inputs_are_excluded_from_runtime_identity(self):
        files = {"main.py": AGENT.encode() + b"\n# agent.so\n",
                 "agent.cpp": b"extern \"C\" int x(){return 1;}",
                 "agent.hpp": b"int x();", "detail.inc": b"#define X 1"}

        def fake_run(command, **kwargs):
            mount = command[command.index("-v") + 1].split(":/build", 1)[0]
            Path(mount, "agent.so").write_bytes(b"compiled-library")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(league, "ensure_public_league_docker_image"), patch.object(
                league.subprocess, "run", side_effect=fake_run):
            prepared = league.prepare_artifact_files(self.store, files)
        self.assertEqual(set(prepared), {"main.py", "agent.so"})
        self.assertEqual(prepared["agent.so"], b"compiled-library")

    def test_windows_worker_cleanup_kills_tree_and_removes_named_container(self):
        proc = SimpleNamespace(pid=321, poll=lambda: None,
                               wait=lambda timeout=None: None, kill=lambda: None)
        job = {"match_key": "ABC/unsafe" + "f" * 80,
               "a_platform": "linux", "b_platform": "host"}
        with patch.object(league.os, "name", "nt"), patch.object(
                league.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run:
            league._terminate_league_worker(proc, job)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(commands[0][:2], ["taskkill", "/PID"])
        self.assertIn("/T", commands[0])
        self.assertEqual(commands[1][:3], ["docker", "rm", "-f"])
        self.assertEqual(commands[1][3], league._league_container_name(job))
        self.assertNotIn("/", commands[1][3])

    def test_linux_worker_docker_run_has_stable_cleanup_name(self):
        job = {"match_key": "a" * 64, "a_platform": "linux", "b_platform": "host",
               "a_path": str(self.root / "a.py"), "b_path": str(self.root / "b.py"),
               "a_sha": "a" * 64, "b_sha": "b" * 64, "seed": 1, "seat_a": 0,
               "state_path": str(self.store.state)}
        result_path = self.store.state / "jobs" / ("docker-" + "a" * 24 + ".result.json")
        result_path.parent.mkdir(parents=True, exist_ok=True)

        commands = []
        call_kwargs = []
        def fake_run(command, **kwargs):
            commands.append(command)
            call_kwargs.append(kwargs)
            if "--name" in command:
                result_path.write_text(json.dumps({"valid": True}), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(league, "ensure_public_league_docker_image"), patch.object(
                league.subprocess, "run", side_effect=fake_run):
            league._league_job(job)
        docker_run = next(command for command in commands if "--name" in command)
        docker_index = commands.index(docker_run)
        self.assertEqual(docker_run[docker_run.index("--name") + 1],
                         league._league_container_name(job))
        self.assertEqual(call_kwargs[docker_index]["creationflags"],
                         league.subprocess_no_window_flags())

    def test_dataset_helper_is_not_promoted_as_standalone_agent(self):
        dataset = self.root / "_datasets" / "bundle"
        dataset.mkdir(parents=True)
        (dataset / "observation.py").write_text(AGENT, encoding="utf-8")
        self.assertEqual(league.discover_artifacts(self.root), [])

    def test_dataset_csv_preamble_does_not_bypass_size_limit(self):
        listing = ("Next Page Token = next-token\n"
                   "name,size,creationDate\n"
                   f"episodes.zip,{league.PUBLIC_LEAGUE_MAX_DATASET_BYTES + 1},today\n")
        calls = []

        def fake_kaggle(args, timeout=180):
            calls.append(args)
            return listing

        with patch.object(league, "run_kaggle", side_effect=fake_kaggle):
            result = league.download_notebook_datasets(
                self.root, {"dataset_sources": ["alice/huge"]})
        self.assertEqual(result["downloaded"], [])
        self.assertEqual(result["skipped"][0]["reason"], "size_limit")
        self.assertFalse(any(args[:2] == ["datasets", "download"] for args in calls))

    def test_published_output_listing_requires_submission_primary(self):
        listing = json.dumps([
            {"name": "analysis.json", "size": 10},
            {"name": "weights.npz", "size": 10},
        ])
        self.assertEqual(league._published_output_names(listing), [])
        listing = json.dumps([
            {"name": "main.py", "size": 10},
            {"name": "weights.npz", "size": 10},
            {"name": "movie.mp4", "size": 10},
        ])
        self.assertEqual(league._published_output_names(listing),
                         ["main.py", "weights.npz"])

    def test_published_notebook_output_is_downloaded_without_running_cells(self):
        archive = self.root / "published"; archive.mkdir()

        def fake_kaggle(args, timeout=180):
            if args[:2] == ["kernels", "files"]:
                return json.dumps([{"name": "submission.py", "size": 1},
                                   {"name": "weights.npz", "size": 1},
                                   {"name": "plot.png", "size": 1}])
            destination = Path(args[args.index("-p") + 1])
            (destination / "submission.py").write_text(AGENT, encoding="utf-8")
            (destination / "weights.npz").write_bytes(b"weights")
            (destination / "ignored.log").write_text("log", encoding="utf-8")
            return ""

        with patch.object(league, "run_kaggle", side_effect=fake_kaggle):
            result = league.ensure_notebook_outputs(archive, "alice/bot")
        self.assertEqual(result["downloaded"], ["submission.py", "weights.npz"])
        output = archive / "_published_output"
        self.assertTrue((output / "submission.py").exists())
        self.assertTrue((output / "weights.npz").exists())
        self.assertFalse((output / "ignored.log").exists())
        artifact = league.discover_artifacts(archive)[0][1]
        self.assertEqual(artifact["main.py"], AGENT.encode())
        self.assertNotIn(".public-league-output-complete.json", artifact)

    def test_compressed_builder_cell_can_reconstruct_main(self):
        import base64, zlib
        encoded = base64.b85encode(zlib.compress(AGENT.encode())).decode()
        nb = self.root / "packed.ipynb"
        cell = ("import base64,zlib\nEXPECTED_MAIN_SHA256='pinned'\n"
                f"SUBMISSION_B85={encoded!r}\n"
                "Path('main.py').write_bytes(zlib.decompress(base64.b85decode(SUBMISSION_B85)))")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}), encoding="utf-8")
        found = league.sources_from_builder_cells(nb)
        self.assertEqual(found[0][1], AGENT.encode())

    def test_self_contained_direct_agent_cell_is_an_artifact_candidate(self):
        nb = self.root / "direct.ipynb"
        nb.write_text(json.dumps({"cells": [
            {"cell_type": "code", "source": AGENT},
        ]}), encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_named_baseline_agent_cell_is_an_artifact_candidate(self):
        source = AGENT.replace("def agent(", "def greedy_farmer_agent(")
        nb = self.root / "named-direct.ipynb"
        nb.write_text(json.dumps({"cells": [
            {"cell_type": "code", "source": source},
        ]}), encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": source.encode()})

    def test_absolute_kaggle_working_main_writefile_is_collected(self):
        nb = self.root / "absolute-main.ipynb"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code",
            "source": "%%writefile /kaggle/working/main.py\n" + AGENT}]}), encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_single_named_agent_writefile_is_promoted_to_main(self):
        nb = self.root / "named-agent.ipynb"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code",
            "source": "%%writefile submission.py\n" + AGENT}]}), encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_agentfile_magic_without_name_is_main(self):
        nb = self.root / "agentfile.ipynb"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code",
            "source": "%%agentfile\n" + AGENT}]}), encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_literal_lzma_base85_agent_source_is_recovered_without_execution(self):
        import base64, lzma
        encoded = base64.b85encode(lzma.compress(AGENT.encode())).decode()
        nb = self.root / "lzma-source.ipynb"
        cell = ("import base64,lzma\n"
                f"AGENT_SOURCE=lzma.decompress(base64.b85decode({encoded!r})).decode()\n"
                "raise RuntimeError('must not execute notebook cell')")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_literal_zlib_base85_name_and_split_parts_are_recovered(self):
        import base64, zlib
        encoded = base64.b85encode(zlib.compress(AGENT.encode())).decode()
        parts = [encoded[index:index + 31] for index in range(0, len(encoded), 31)]
        nb = self.root / "zlib-parts.ipynb"
        cell = (f"AGENT_SHA256={league.sha256(AGENT.encode())!r}\n"
                f"PARTS={parts!r}\n"
                "agent_bytes=zlib.decompress(base64.b85decode(''.join(PARTS).encode('ascii')))\n"
                "raise RuntimeError('must not execute notebook cell')")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertTrue(any(files == {"main.py": AGENT.encode()} for _, files in found))

    def test_literal_gzip_source_and_written_sidecars_are_recovered(self):
        import base64, gzip
        source = base64.b85encode(gzip.compress(AGENT.encode())).decode()
        notice = base64.b85encode(gzip.compress(b"notice")).decode()
        nb = self.root / "gzip-sidecars.ipynb"
        cell = (f"SOURCE_B85={source!r}\nNOTICE_B85={notice!r}\n"
                "source=gzip.decompress(base64.b85decode(SOURCE_B85))\n"
                "notice=gzip.decompress(base64.b85decode(NOTICE_B85))\n"
                "main=WORK/'main.py'\nnotice_path=WORK/'NOTICE.txt'\n"
                "main.write_bytes(source)\nnotice_path.write_bytes(notice)\n")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        files = next(files for _, files in league.artifacts_from_notebook(nb)
                     if set(files) == {"main.py", "NOTICE.txt"})
        self.assertEqual(files, {"main.py": AGENT.encode(), "NOTICE.txt": b"notice"})

    def test_literal_base64_tar_archive_is_recovered(self):
        import base64, io, tarfile
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w:gz") as bundle:
            info = tarfile.TarInfo("main.py"); info.size = len(AGENT.encode())
            bundle.addfile(info, io.BytesIO(AGENT.encode()))
        encoded = base64.b64encode(raw.getvalue()).decode()
        nb = self.root / "literal-archive.ipynb"
        cell = f"Path('submission.tar.gz').write_bytes(base64.b64decode({encoded!r}))\n"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertTrue(any(files == {"main.py": AGENT.encode()} for _, files in found))

    def test_nested_payload_map_and_raw_source_map_are_recovered(self):
        import base64, zlib
        encoded = base64.b85encode(zlib.compress(AGENT.encode())).decode()
        digest = league.sha256(AGENT.encode())
        for name, expression in (
            ("nested", f"FILES={{'main.py':{{'size':{len(AGENT)},'sha256':{digest!r},'payload':({encoded!r},)}}}}"),
            ("raw", f"TOP_AGENT_FILES={{'main.py':{AGENT!r}}}"),
        ):
            nb = self.root / f"{name}.ipynb"
            nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": expression}]}),
                          encoding="utf-8")
            found = league.artifacts_from_notebook(nb)
            self.assertTrue(any(files == {"main.py": AGENT.encode()} for _, files in found), name)

    def test_literal_assignment_survives_unrelated_malformed_output_line(self):
        source = AGENT.encode().replace(b"\n", b"\r\n")
        chunks = tuple(source[index:index + 17] for index in range(0, len(source), 17))
        digest = league.sha256(source)
        cell = (f"EXPECTED_MAIN_SHA256={digest!r}\nSOURCE_BYTES=b''.join({chunks!r})\n"
                "Copied display output that is not Python\n")
        nb = self.root / "malformed-output.ipynb"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        found = league.artifacts_from_notebook(nb)
        self.assertTrue(any(files == {"main.py": AGENT.encode()} for _, files in found))

    def test_pinned_remote_archive_is_hash_checked_before_collection(self):
        import hashlib
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w:gz") as bundle:
            info = tarfile.TarInfo("main.py"); info.size = len(AGENT.encode())
            bundle.addfile(info, io.BytesIO(AGENT.encode()))
        payload = raw.getvalue(); digest = hashlib.sha256(payload).hexdigest()
        nb = self.root / "remote.ipynb"
        cell = (f"COMMIT='{'a' * 40}'\nEXPECTED={digest!r}\n"
                "URL=f'https://raw.githubusercontent.com/user/repo/{COMMIT}/agent.tar.gz'\n")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}),
                      encoding="utf-8")
        response = io.BytesIO(payload)
        with patch.object(league.urllib.request, "urlopen", return_value=response):
            found = league.artifacts_from_notebook(nb)
        self.assertTrue(any(files == {"main.py": AGENT.encode()} for _, files in found))

    def test_discover_artifacts_wraps_builder_source_as_single_file_artifact(self):
        import base64, zlib
        encoded = base64.b85encode(zlib.compress(AGENT.encode())).decode()
        nb = self.root / "packed-discovery.ipynb"
        cell = ("import base64,zlib\nEXPECTED_MAIN_SHA256='pinned'\n"
                f"SUBMISSION_B85={encoded!r}\n"
                "Path('main.py').write_bytes(zlib.decompress(base64.b85decode(SUBMISSION_B85)))")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}), encoding="utf-8")
        found = league.discover_artifacts(self.root)
        self.assertEqual(found[0][1], {"main.py": AGENT.encode()})

    def test_literal_files_dictionary_recovers_packed_main_without_execution(self):
        import base64, hashlib, zlib
        encoded = base64.b85encode(zlib.compress(AGENT.encode())).decode()
        digest = hashlib.sha256(AGENT.encode()).hexdigest()
        nb = self.root / "files-dict.ipynb"
        cell = (f"FILES={{'main.py': {encoded!r}, 'NOTICE.txt': 'ignored'}}\n"
                f"EXPECTED={{'main.py': {digest!r}}}\n"
                "raise RuntimeError('this public cell must not be executed')")
        nb.write_text(json.dumps({"cells": [{"cell_type": "code", "source": cell}]}), encoding="utf-8")
        found = league.sources_from_notebook(nb)
        self.assertEqual(found[0][1], AGENT.encode())

    def test_extracting_historical_version_does_not_replace_current_alias(self):
        old_dir = self.root / "old"; self.notebook(old_dir, AGENT)
        new_source = AGENT + "# new version\n"
        new_dir = self.root / "new"; self.notebook(new_dir, new_source)
        old_id = self.add_version("alice/versioned", "Versioned", old_dir, "old")
        with self.store.db:
            nid = self.store.db.execute("SELECT id FROM notebooks WHERE ref='alice/versioned'").fetchone()[0]
            now = league.utcnow()
            cur = self.store.db.execute("""INSERT INTO notebook_versions
              (notebook_id,version_key,metadata_json,archive_path,status,first_seen,pulled_at)
              VALUES(?,?,?,?,'pulled',?,?)""", (nid, "new", "{}", str(new_dir), now, now))
            self.store.db.execute("UPDATE notebooks SET current_version_key='new' WHERE id=?", (nid,))
        league.extract(self.store)
        aliases = [dict(x) for x in self.store.db.execute(
            "SELECT version_id,is_current FROM aliases ORDER BY version_id")]
        self.assertEqual(aliases, [{"version_id": old_id, "is_current": 0},
                                   {"version_id": cur.lastrowid, "is_current": 1}])

    def test_extractor_exception_does_not_starve_later_versions(self):
        broken = self.root / "broken"; self.notebook(broken, AGENT)
        healthy = self.root / "healthy"; self.notebook(healthy, AGENT + "# healthy\n")
        broken_id = self.add_version("alice/broken", "Broken", broken, "v1")
        healthy_id = self.add_version("alice/healthy", "Healthy", healthy, "v1")
        real_discover = league.discover_artifacts

        def discover(path):
            if Path(path) == broken:
                raise AttributeError("malformed recovered artifact")
            return real_discover(path)

        with patch.object(league, "discover_artifacts", side_effect=discover):
            result = league.extract(self.store)
        broken_row = self.store.db.execute(
            "SELECT status,error FROM notebook_versions WHERE id=?", (broken_id,)).fetchone()
        healthy_row = self.store.db.execute(
            "SELECT status FROM notebook_versions WHERE id=?", (healthy_id,)).fetchone()
        self.assertEqual(broken_row["status"], "quarantine")
        self.assertIn("extractor AttributeError", broken_row["error"])
        self.assertEqual(healthy_row["status"], "extracted")
        self.assertEqual(result["quarantined"], 1)

    def test_exact_source_duplicate_becomes_one_agent_with_two_named_links(self):
        for ref, title in (("alice/one", "Notebook One"), ("bob/two", "Notebook Two")):
            directory = self.root / ref.replace("/", "-")
            self.notebook(directory)
            self.add_version(ref, title, directory)
        result = league.extract(self.store)
        self.assertEqual(result["new_agents"], 1)
        self.assertEqual(result["duplicate_aliases"], 1)
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM agents").fetchone()[0], 1)
        snapshot = league.dashboard_snapshot(self.store)
        self.assertEqual({x["notebook_title"] for x in snapshot["agents"][0]["aliases"]},
                         {"Notebook One", "Notebook Two"})
        self.assertTrue(all(x["notebook_url"].startswith("https://www.kaggle.com/code/")
                            for x in snapshot["agents"][0]["aliases"]))
        self.assertTrue(snapshot["agents"][0]["is_new"])

    def test_new_badge_expires_after_12_hours(self):
        directory = self.root / "old"; self.notebook(directory)
        self.add_version("alice/old", "Old Notebook", directory)
        league.extract(self.store)
        old = (league.dt.datetime.now(league.dt.timezone.utc) - league.dt.timedelta(hours=13)).isoformat(timespec="seconds")
        with self.store.db:
            self.store.db.execute("UPDATE aliases SET discovered_at=?", (old,))
        self.assertFalse(league.dashboard_snapshot(self.store)["agents"][0]["is_new"])

    def test_new_badge_baseline_excludes_existing_aliases(self):
        directory = self.root / "baseline"; self.notebook(directory)
        self.add_version("alice/baseline", "Baseline Notebook", directory)
        league.extract(self.store)
        self.store.set_meta("new_badge_baseline", league.utcnow())
        self.assertFalse(league.dashboard_snapshot(self.store)["agents"][0]["is_new"])

    def test_new_version_is_preserved_instead_of_overwriting(self):
        directory = self.root / "nb"; self.notebook(directory)
        self.add_version("alice/one", "One", directory, "v1")
        now = league.utcnow()
        nid = self.store.db.execute("SELECT id FROM notebooks").fetchone()[0]
        with self.store.db:
            self.store.db.execute("""INSERT INTO notebook_versions
              (notebook_id,version_key,metadata_json,archive_path,status,first_seen,pulled_at)
              VALUES(?,?,'{}',?,'pulled',?,?)""", (nid, "v2", str(directory), now, now))
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM notebook_versions").fetchone()[0], 2)

    def test_compile_or_loader_failure_is_quarantined(self):
        directory = self.root / "bad"; self.notebook(directory, "def broken(:\n")
        self.add_version("alice/bad", "Bad", directory)
        result = league.extract(self.store)
        self.assertEqual(result["quarantined"], 1)
        self.assertEqual(self.store.db.execute("SELECT status FROM notebook_versions").fetchone()[0], "quarantine")

    def seed_agent(self, digest, title):
        now = league.utcnow(); path = self.root / f"{digest}.py"; path.write_text(AGENT)
        with self.store.db:
            aid = self.store.db.execute("""INSERT INTO agents
              (sha256,source_path,qa_status,created_at,status) VALUES(?,?,'pass',?,'candidate')""",
              (digest, str(path), now)).lastrowid
            nid = self.store.db.execute("""INSERT INTO notebooks
              (ref,title,author,slug,url,first_seen,last_seen,current_version_key)
              VALUES(?,?,?,?,?,?,?,?)""", (f"a/{digest}", title, "a", digest,
              f"https://www.kaggle.com/code/a/{digest}", now, now, "v1")).lastrowid
            vid = self.store.db.execute("""INSERT INTO notebook_versions
              (notebook_id,version_key,metadata_json,status,first_seen) VALUES(?,'v1','{}','extracted',?)""",
              (nid, now)).lastrowid
            self.store.db.execute("""INSERT INTO aliases
              (agent_id,version_id,notebook_title,notebook_url,author,ref,discovered_at)
              VALUES(?,?,?,?,?,?,?)""", (aid, vid, title, f"https://www.kaggle.com/code/a/{digest}",
              "a", f"a/{digest}", now))
        return aid

    def test_match_cache_does_not_schedule_identical_game_twice(self):
        self.seed_agent("a" * 64, "A"); self.seed_agent("b" * 64, "B")
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, seeds_per_pair=1, max_matches=2)
            self.assertEqual(len(jobs), 2)
            with self.store.db:
                for j in jobs:
                    self.store.db.execute("""INSERT INTO matches
                      (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,created_at)
                      VALUES(?,?,?,?,?,?,'complete',?)""", (j["match_key"], "engine", j["agent_a"],
                      j["agent_b"], j["seed"], j["seat_a"], league.utcnow()))
            again = league.schedule_matches(self.store, seeds_per_pair=1, max_matches=2)
            self.assertEqual(len(again), 2)
            self.assertTrue({j["match_key"] for j in jobs}.isdisjoint(
                {j["match_key"] for j in again}))

    def test_scheduled_job_carries_custom_state_path(self):
        self.seed_agent("a" * 64, "A"); self.seed_agent("b" * 64, "B")
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, max_matches=2)
        self.assertEqual({job["state_path"] for job in jobs}, {str(self.store.state.resolve())})

    def test_linux_job_uses_custom_state_for_docker_exchange(self):
        source = self.store.state / "artifacts" / "x" / "main.py"
        source.parent.mkdir(parents=True); source.write_text(AGENT, encoding="utf-8")
        job = {"match_key": "a" * 64, "state_path": str(self.store.state),
               "a_platform": "linux", "b_platform": "host",
               "a_path": str(source), "b_path": str(source), "containerized": False}

        def fake_run(command, **kwargs):
            result = self.store.state / "jobs" / ("docker-" + "a" * 24 + ".result.json")
            result.write_text(json.dumps({"valid": True, "marker": "custom-state"}), encoding="utf-8")
            self.assertIn(f"{self.store.state.resolve()}:/league-state", command)
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with patch.object(league, "ensure_public_league_docker_image"), patch.object(
                league.subprocess, "run", side_effect=fake_run):
            result = league._league_job(job)
        self.assertEqual(result["marker"], "custom-state")

    def test_engine_hash_includes_linux_execution_contract(self):
        first = league.engine_sha()
        with patch.object(league, "PUBLIC_LEAGUE_DOCKER_IMAGE", "different:image"):
            second = league.engine_sha()
        self.assertNotEqual(first, second)

    def test_round_robin_batch_distributes_matches(self):
        for ch in "abcdef": self.seed_agent(ch * 64, ch.upper())
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, top_k=6, seeds_per_pair=1, max_matches=12)
        counts = {}
        for j in jobs:
            counts[j["agent_a"]] = counts.get(j["agent_a"], 0) + 1
            counts[j["agent_b"]] = counts.get(j["agent_b"], 0) + 1
        self.assertEqual(len(counts), 6)
        self.assertLessEqual(max(counts.values()) - min(counts.values()), 2)

    def test_focus_batch_only_schedules_selected_agent_and_balances_opponents(self):
        aids = [self.seed_agent(ch * 64, ch.upper()) for ch in "abcdef"]
        with self.store.db:
            for rank, aid in enumerate(aids):
                self.store.db.execute(
                    "UPDATE agents SET status='active',games=40,rating=? WHERE id=?",
                    (1800-rank, aid))
        focus = aids[-1]
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(
                self.store, top_k=6, max_matches=20, focus_agent_id=focus)
        self.assertEqual(len(jobs), 20)
        self.assertTrue(all(focus in (job["agent_a"], job["agent_b"]) for job in jobs))
        opponents = {job["agent_b"] if job["agent_a"] == focus else job["agent_a"] for job in jobs}
        self.assertEqual(opponents, set(aids[:-1]))
        for seed in {job["seed"] for job in jobs}:
            self.assertEqual(sum(job["seed"] == seed for job in jobs), 2)

    def test_notebook_url_parser_and_agent_match_history(self):
        self.assertEqual(league.parse_notebook_ref(
            "https://www.kaggle.com/code/alice/my-notebook?scriptVersionId=3"),
            "alice/my-notebook")
        self.assertEqual(league.parse_notebook_ref("alice/my-notebook"), "alice/my-notebook")
        self.assertIsNone(league.parse_notebook_ref("not a notebook"))
        a = self.seed_agent("a" * 64, "A")
        b = self.seed_agent("b" * 64, "B")
        now = league.utcnow()
        with self.store.db:
            self.store.db.execute("""INSERT INTO matches
              (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,outcome_a,
               reward_a,reward_b,margin_a,created_at,completed_at)
              VALUES('history','engine',?,?,9,0,'complete',1,110,90,20,?,?)""",
              (a, b, now, now))
        history = league.agent_match_history(self.store, b)
        self.assertEqual(history["total"], 1)
        self.assertEqual(history["matches"][0]["opponent_name"], "A")
        self.assertEqual(history["matches"][0]["outcome"], 0)
        self.assertEqual(history["matches"][0]["margin"], -20)

    def test_new_agent_gets_catch_up_matches_until_game_deficit_closes(self):
        veterans = [self.seed_agent(ch * 64, ch.upper()) for ch in "abc"]
        newcomer = self.seed_agent("d" * 64, "New")
        with self.store.db:
            for aid in veterans:
                self.store.db.execute("UPDATE agents SET status='active',games=30,rating=1700 WHERE id=?", (aid,))
            self.store.db.execute("UPDATE agents SET status='candidate',games=0 WHERE id=?", (newcomer,))
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, top_k=12, seeds_per_pair=1, max_matches=12)
        self.assertEqual(len(jobs), 12)
        self.assertTrue(all(newcomer in (job["agent_a"], job["agent_b"]) for job in jobs))

    def test_archived_new_agent_keeps_catch_up_priority_across_cycles(self):
        veterans = [self.seed_agent(f"{i:064x}", f"Veteran {i}") for i in range(1, 13)]
        newcomer = self.seed_agent("f" * 64, "New but initially weak")
        with self.store.db:
            for rank, aid in enumerate(veterans):
                self.store.db.execute(
                    "UPDATE agents SET status='active',games=40,rating=? WHERE id=?",
                    (1800-rank, aid))
            # A completed first batch can mark the newcomer archived.  Its sample
            # is still far below the incumbent median, so it must stay in rotation.
            self.store.db.execute(
                "UPDATE agents SET status='archived',games=10,rating=1200 WHERE id=?",
                (newcomer,))
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, top_k=12, seeds_per_pair=1,
                                           max_matches=12)
        self.assertEqual(len(jobs), 12)
        self.assertTrue(all(newcomer in (job["agent_a"], job["agent_b"]) for job in jobs))

    def test_newcomer_priority_ends_after_fixed_game_threshold(self):
        veterans = [self.seed_agent(f"{i:064x}", f"Veteran {i}") for i in range(1, 13)]
        newcomer = self.seed_agent("f" * 64, "Enough evidence")
        with self.store.db:
            for rank, aid in enumerate(veterans):
                self.store.db.execute(
                    "UPDATE agents SET status='active',games=80,rating=? WHERE id=?",
                    (1800-rank, aid))
            self.store.db.execute(
                "UPDATE agents SET status='archived',games=?,rating=900 WHERE id=?",
                (league.NEWCOMER_PRIORITY_GAMES, newcomer))
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, top_k=12, max_matches=12)
        self.assertFalse(any(newcomer in (job["agent_a"], job["agent_b"]) for job in jobs))

    def test_newcomer_priority_drops_mid_batch_at_threshold(self):
        veterans = [self.seed_agent(f"{i:064x}", f"Veteran {i}") for i in range(1, 13)]
        newcomer = self.seed_agent("f" * 64, "Almost enough evidence")
        with self.store.db:
            for rank, aid in enumerate(veterans):
                self.store.db.execute(
                    "UPDATE agents SET status='active',games=80,rating=? WHERE id=?",
                    (1800-rank, aid))
            self.store.db.execute(
                "UPDATE agents SET status='archived',games=30,rating=900 WHERE id=?",
                (newcomer,))
        with patch.object(league, "engine_sha", return_value="engine"):
            jobs = league.schedule_matches(self.store, top_k=12, max_matches=24)
        appearances = sum(newcomer in (job["agent_a"], job["agent_b"]) for job in jobs)
        self.assertEqual(appearances, 2)

    def test_battle_controller_starts_stopped(self):
        controller = league.BattleController(self.root / "battle-state")
        self.assertEqual(controller.snapshot()["phase"], "stopped")

    def test_pre_stopped_league_does_not_schedule_matches(self):
        stopped = __import__("threading").Event(); stopped.set()
        result = league.run_league(self.store, stop_event=stopped)
        self.assertTrue(result["stopped"])
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM matches").fetchone()[0], 0)

    def test_known_diagnostic_counter_is_warning_not_invalid_match(self):
        result = {"valid": False, "statuses": ["DONE", "DONE"], "states": 720,
                  "rewards": [100, 90], "margin": 10, "errors": [[], []],
                  "candidate_timing": {"calls": 719}, "opponent_timing": {"calls": 719},
                  "health_failures": ["opponent_internal_error:overflow_contract_errors"]}
        normalized = league.normalize_public_league_result(result)
        self.assertTrue(normalized["valid"])
        self.assertEqual(normalized["health_failures"], [])
        self.assertEqual(normalized["public_league_warnings"],
                         ["opponent_internal_error:overflow_contract_errors"])

    def test_wall_timeout_is_not_attributed_to_either_agent(self):
        slow = self.seed_agent("d" * 64, "Slow")
        good_a = self.seed_agent("e" * 64, "Good A")
        good_b = self.seed_agent("f" * 64, "Good B")
        now = league.utcnow()
        with self.store.db:
            for i, opponent in enumerate((good_a, good_b)):
                for seat in (0, 1):
                    self.store.db.execute("""INSERT INTO matches
                      (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,error,created_at)
                      VALUES(?,?,?,?,?,?,'invalid','timeout',?)""",
                      (f"timeout-{i}-{seat}", "engine", slow, opponent, i, seat, now))
            self.store.db.execute("""INSERT INTO matches
              (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,outcome_a,created_at)
              VALUES('good-complete','engine',?,?,1,0,'complete',.5,?)""",
              (good_a, good_b, now))
        result = league.quarantine_runtime_failures(self.store)
        self.assertNotIn(slow, result["agent_ids"])
        self.assertEqual(self.store.db.execute(
            "SELECT qa_status FROM agents WHERE id=?", (slow,)).fetchone()[0], "pass")
        self.assertEqual(self.store.db.execute(
            "SELECT qa_status FROM agents WHERE id=?", (good_a,)).fetchone()[0], "pass")

    def test_local_import_skips_exact_duplicate_source(self):
        source = self.root / "ours.py"
        source.write_text(AGENT, encoding="utf-8")
        config = self.root / "locals.json"
        config.write_text(json.dumps({"agents": [{"name": "ours", "path": "ours.py"}]}), encoding="utf-8")
        with patch.object(league, "ROOT", self.root), patch.object(
                league, "qa_source", return_value={"ok": True, "entrypoint": "agent"}):
            first = league.import_local_agents(self.store, config)
            second = league.import_local_agents(self.store, config)
        self.assertEqual(first["imported"], 1)
        self.assertEqual(second["duplicates_skipped"], 1)
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM agents").fetchone()[0], 1)

    def test_browser_session_tracker_exits_after_last_heartbeat_expires(self):
        tracker = league.BrowserSessionTracker()
        start = tracker.started
        self.assertFalse(tracker.should_exit(now=start + 10))
        tracker.touch("tab-1", now=start + 11)
        self.assertFalse(tracker.should_exit(now=start + 20))
        # A background tab may be throttled to one timer per minute.  It must
        # survive that gap instead of stopping a running league batch.
        self.assertFalse(tracker.should_exit(now=start + 130))
        tracker.touch("tab-1", now=start + 131)
        self.assertFalse(tracker.should_exit(now=start + 250))
        self.assertTrue(tracker.should_exit(now=start + 312))

    def test_browser_session_tracker_explicit_close_keeps_reload_grace(self):
        tracker = league.BrowserSessionTracker()
        start = tracker.started
        tracker.touch("tab-1", now=start + 1)
        tracker.close("tab-1", now=start + 2)
        self.assertFalse(tracker.should_exit(now=start + 6))
        tracker.touch("tab-2", now=start + 6)
        self.assertFalse(tracker.should_exit(now=start + 170))
        tracker.close("tab-2", now=start + 171)
        self.assertTrue(tracker.should_exit(now=start + 177))

    def test_current_cycle_progress_counts_only_latest_running_batch(self):
        a = self.seed_agent("a" * 64, "A")
        b = self.seed_agent("b" * 64, "B")
        with self.store.db:
            self.store.db.execute("""INSERT INTO matches
              (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,created_at)
              VALUES('old','engine',?,?,1,0,'complete','2026-09-20T00:00:00+00:00')""", (a, b))
            for key, status in (("done", "complete"), ("bad", "invalid"),
                                ("left-1", "running"), ("left-2", "running")):
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,created_at)
                  VALUES(?,'engine',?,?,2,0,?,'2026-09-20T01:00:00+00:00')""",
                  (key, a, b, status))
        progress = league.league_progress(self.store)
        self.assertTrue(progress["running"])
        self.assertEqual(progress["cycle"]["total"], 4)
        self.assertEqual(progress["cycle"]["done"], 2)
        self.assertEqual(progress["cycle"]["remaining"], 2)
        self.assertEqual(progress["cycle"]["percent"], 50.0)

    def test_repeated_runtime_error_quarantines_agent(self):
        bad = self.seed_agent("a" * 64, "Bad"); good = self.seed_agent("b" * 64, "Good")
        now = league.utcnow()
        with self.store.db:
            for i, seat in enumerate((0, 1)):
                result = {"errors": [[{"type": "FileNotFoundError"}], []] if seat == 0 else [[], [{"type": "FileNotFoundError"}]]}
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,result_json,created_at)
                  VALUES(?,?,?,?,?,?,'invalid',?,?)""", (f"bad{i}", "e", bad, good, i, seat,
                  json.dumps(result), now))
        out = league.quarantine_runtime_failures(self.store)
        self.assertEqual(out["quarantined"], 1)
        row = self.store.db.execute("SELECT qa_status,status FROM agents WHERE id=?", (bad,)).fetchone()
        self.assertEqual(tuple(row), ("runtime_failed", "quarantine"))

    def test_repeated_local_timing_warning_does_not_quarantine_agent(self):
        bad = self.seed_agent("c" * 64, "Slow"); good = self.seed_agent("d" * 64, "Good")
        other = self.seed_agent("e" * 64, "Other")
        now = league.utcnow()
        with self.store.db:
            for i in range(4):
                opponent = good if i < 2 else other
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,result_json,created_at)
                  VALUES(?,?,?,?,?,0,'invalid',?,?)""", (f"slow{i}", "e", bad, opponent, i,
                  json.dumps({"errors": [[], []], "candidate_timing": {"max": 1.6},
                              "health_failures": ["candidate_over_1_5_seconds"]}), now))
        league.quarantine_runtime_failures(self.store)
        self.assertEqual(self.store.db.execute("SELECT status FROM agents WHERE id=?", (bad,)).fetchone()[0],
                         "candidate")

    def test_sub_1_5_second_health_warning_is_accepted(self):
        result = {"statuses": ["DONE", "DONE"], "states": 720, "rewards": [10, 9],
                  "errors": [[], []], "candidate_timing": {"calls": 719, "max": 2.0},
                  "opponent_timing": {"calls": 719, "max": .2},
                  "health_failures": ["candidate_over_one_second"], "margin": 1}
        normalized = league.normalize_public_league_result(result)
        self.assertTrue(normalized["valid"])
        self.assertEqual(normalized["health_failures"], [])
        self.assertEqual(normalized["public_league_warnings"], ["candidate_over_one_second"])

    def test_multifile_artifact_identity_includes_sidecar_bytes(self):
        main = AGENT.encode()
        first = league.artifact_digest({"main.py": main, "actions.json": b"[1]"})
        second = league.artifact_digest({"actions.json": b"[2]", "main.py": main})
        self.assertNotEqual(first, second)
        self.assertEqual(league.artifact_digest({"main.py": main}),
                         league.sha256(league.canonical_source(main)))

    def test_notebook_gzip_json_map_recovers_all_files(self):
        import base64, gzip
        payload = base64.b64encode(gzip.compress(json.dumps(
            {"main.py": AGENT, "actions.json": "[]"}).encode())).decode()
        nb = self.root / "packed-map.ipynb"
        nb.write_text(json.dumps({"cells": [{"cell_type": "code",
            "source": f"data_payload={payload!r}\nimport base64,gzip,json\n"}]}), encoding="utf-8")
        artifacts = league.artifacts_from_notebook(nb)
        files = next(files for _, files in artifacts if "actions.json" in files)
        self.assertEqual(set(files), {"main.py", "actions.json"})

    def test_qa_rejects_callable_submission_builder_object(self):
        source = self.root / "builder.py"
        source.write_text("from pathlib import Path\nPath\n", encoding="utf-8")
        qa = league.qa_source(source)
        self.assertFalse(qa["ok"])

    def test_qa_uses_official_runner_signature_adaptation(self):
        source = self.root / "one-argument-agent.py"
        source.write_text('''def agent(obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}
def _kaggle_submission_entrypoint(obs):
    return agent(obs)
''', encoding="utf-8")
        qa = league.qa_source(source)
        self.assertTrue(qa["ok"], qa)
        self.assertEqual(qa["entrypoint"], "_kaggle_submission_entrypoint")

    def test_bradley_terry_orders_clear_winner(self):
        rows = [{"agent_a": 1, "agent_b": 2, "outcome_a": 1.0} for _ in range(8)]
        ratings = league.bradley_terry_ratings([1, 2], rows)
        self.assertGreater(ratings[1], ratings[2])

    def test_restored_runtime_quarantine_ignores_reviewed_failures_only(self):
        bad = self.seed_agent("e" * 64, "Recovered"); good = self.seed_agent("f" * 64, "Good")
        now = league.utcnow()
        with self.store.db:
            for i in range(2):
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,result_json,created_at)
                  VALUES(?,?,?,?,?,0,'invalid',?,?)""", (f"old-slow{i}", "e", bad, good, i,
                  json.dumps({"errors": [[{"type": "RuntimeError"}], []],
                              "health_failures": []}), now))
        league.quarantine_runtime_failures(self.store)
        restored = league.restore_runtime_quarantine(self.store, "e" * 64, "8-worker clean QA")
        self.assertEqual(restored["failure_watermark_match_id"], 2)
        self.assertEqual(tuple(self.store.db.execute(
            "SELECT qa_status,status FROM agents WHERE id=?", (bad,)).fetchone()), ("pass", "candidate"))
        self.assertEqual(league.quarantine_runtime_failures(self.store)["quarantined"], 0)
        with self.store.db:
            for i in range(2, 4):
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,result_json,created_at)
                  VALUES(?,?,?,?,?,0,'invalid',?,?)""", (f"new-slow{i}", "e", bad, good, i,
                  json.dumps({"errors": [[{"type": "RuntimeError"}], []],
                              "health_failures": []}), now))
        self.assertEqual(league.quarantine_runtime_failures(self.store)["quarantined"], 1)

    def test_invalid_match_never_counts_and_top_k_archives_without_deleting(self):
        aids = [self.seed_agent(ch * 64, ch.upper()) for ch in "abc"]
        now = league.utcnow()
        with self.store.db:
            for i in range(8):
                self.store.db.execute("""INSERT INTO matches
                  (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,outcome_a,created_at,completed_at)
                  VALUES(?,?,?,?,?,0,'complete',1,?,?)""",
                  (f"good{i}", "e", aids[0], aids[1], i, now, now))
            self.store.db.execute("""INSERT INTO matches
              (match_key,engine_sha,agent_a,agent_b,seed,seat_a,status,outcome_a,created_at)
              VALUES('bad','e',?,?,99,0,'invalid',1,?)""", (aids[2], aids[0], now))
        league.update_rankings(self.store, top_k=1, min_games=8)
        rows = self.store.db.execute("SELECT id,status,games FROM agents ORDER BY id").fetchall()
        self.assertEqual(sum(x["status"] == "active" for x in rows), 1)
        self.assertEqual(next(x["games"] for x in rows if x["id"] == aids[2]), 0)
        self.assertTrue(all(Path(self.store.db.execute("SELECT source_path FROM agents WHERE id=?", (x["id"],)).fetchone()[0]).exists() for x in rows))

    def test_collector_failure_preserves_existing_database(self):
        self.seed_agent("a" * 64, "A")
        with patch.object(league, "run_kaggle", side_effect=RuntimeError("offline")):
            with self.assertRaisesRegex(RuntimeError, "offline"):
                league.collect(self.store)
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM agents").fetchone()[0], 1)

    def test_deferred_collection_is_resumed_on_next_cycle(self):
        listing = json.dumps([{"ref": "alice/new", "title": "New", "lastRunTime": "now"}])
        calls = []
        def fake(args, timeout=180):
            calls.append(args)
            return listing if args[:2] == ["kernels", "list"] else ""
        with patch.object(league, "run_kaggle", side_effect=fake), patch.object(
                league, "enrich_public_scores", return_value={"checked": 0, "failed": 0}):
            first = league.collect(self.store, limit=5, pull_limit=0)
            self.assertEqual(first["deferred"], 1)
            second = league.collect(self.store, limit=5, pull_limit=1)
        self.assertEqual(second["new_versions"], 0)
        self.assertEqual(second["pulled"], 1)
        self.assertTrue(any(x[:2] == ["kernels", "pull"] for x in calls))

    def test_refresh_lock_prevents_overlapping_cycle(self):
        lock = self.store.state / "refresh.lock"
        with league.process_lock(lock) as acquired:
            self.assertTrue(acquired)
            with patch.object(league, "collect") as collect_mock:
                result = league.refresh(self.store, max_matches=0)
            self.assertTrue(result["busy"])
            collect_mock.assert_not_called()

    def test_runtime_settings_validate_and_update_scheduler(self):
        with patch.object(league.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout="", stderr="")) as run:
            settings = league.update_runtime_settings(self.store, 2.5, 10)
        self.assertEqual(settings["interval_hours"], 2.5)
        self.assertEqual(settings["workers"], 10)
        command = " ".join(map(str, run.call_args.args[0]))
        self.assertIn("configure-public-league-task.ps1", command)
        self.assertIn("-State Enabled", command)
        with self.assertRaises(ValueError):
            league.update_runtime_settings(self.store, 0, 10)
        with self.assertRaises(ValueError):
            league.update_runtime_settings(self.store, 1, 13)

    def test_auto_collection_toggle_updates_task_and_setting(self):
        with patch.object(league.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout="", stderr="")) as run:
            settings = league.toggle_auto_collection(self.store)
        self.assertFalse(settings["auto_collect_enabled"])
        self.assertFalse(league.runtime_settings(self.store)["auto_collect_enabled"])
        command = " ".join(map(str, run.call_args.args[0]))
        self.assertIn("set-public-league-collection.ps1", command)
        self.assertIn("-State Disabled", command)


if __name__ == "__main__":
    unittest.main()
