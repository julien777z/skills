import importlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

HOOK = Path(__file__).resolve().parents[1] / "main.py"
sys.path.insert(0, str(HOOK.parent))
ledgers = importlib.import_module("ledgers")
REPLY_PROMPT = (HOOK.parent / "prompts" / "reply.md").read_text(encoding="utf-8").strip()
BLOCK_EXIT = 2


class LedgerHookTest(unittest.TestCase):
    """Test the turn-end hook against a private state directory and session transcript."""

    def setUp(self):
        """Give each test an empty state directory and a transcript that records a start."""

        state_home = tempfile.TemporaryDirectory()

        self.addCleanup(state_home.cleanup)
        self.state_home = Path(state_home.name)
        self.directory = self.state_home / "agent-ledgers"
        self.session_id = str(uuid.uuid4())
        self.transcript = self.state_home / "transcript.jsonl"
        self.transcript.write_text(json.dumps({"timestamp": "2000-01-01T00:00:00Z"}) + "\n")

    def run_hook(self, **payload):
        """Run the hook as the harness does, with this test's session in its input."""

        payload = {"session_id": self.session_id, "transcript_path": str(self.transcript)} | payload

        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=os.environ | {"XDG_STATE_HOME": str(self.state_home)},
            check=False,
        )

    def ledger_files(self):
        """List the file names in the ledger directory."""

        if not self.directory.exists():
            return []

        return sorted(path.name for path in self.directory.iterdir())

    def test_creates_private_session_file_once(self):
        """Test that a session no ledger lists gets one private file, named to it only once."""

        ledger = self.directory / f"session-{self.session_id}.yaml"
        mentioning = self.directory / "mentioning-task.yaml"
        observation = {"event": "handoff", "evidence": self.session_id, "data": {}}
        review = {"id": "review-1", "kind": "review", "summary": "s", "data": {}}
        entries = [review | {"observations": [observation]}]

        self.directory.mkdir()
        mentioning.write_text(json.dumps({"session_ledger": {"sessions": [], "entries": entries}}))

        first = self.run_hook()

        self.assertEqual(first.returncode, BLOCK_EXIT)
        self.assertIn(str(ledger), first.stderr)

        self.assertEqual(stat.S_IMODE(ledger.stat().st_mode), 0o600)
        self.assertIn(f'- "{self.session_id}"', ledger.read_text())

        second = self.run_hook()

        self.assertEqual((second.returncode, second.stderr), (0, ""))
        self.assertEqual(self.ledger_files(), [mentioning.name, ledger.name])

    def test_keeps_existing_session_file_the_scan_misses(self):
        """Test that a session file with records, older than the session and naming no ID, stays."""

        ledger = self.directory / f"session-{self.session_id}.yaml"
        plan = {"id": "plan-1", "kind": "plan", "summary": "s", "data": {"status": "shown"}}
        text = json.dumps({"session_ledger": {"sessions": [], "entries": [plan]}})

        self.directory.mkdir()
        ledger.write_text(text)
        os.utime(ledger, (0, 0))

        result = self.run_hook()

        self.assertEqual(result.returncode, BLOCK_EXIT)
        self.assertIn(f"{ledger} has entries missing", result.stderr)
        self.assertEqual(ledger.read_text(), text)

        with mock.patch.dict(os.environ, {"XDG_STATE_HOME": str(self.state_home)}):
            self.assertIsNone(ledgers.create_session_ledger(self.session_id))

        self.assertEqual(ledger.read_text(), text)

    def test_followup_message_names_created_file(self):
        """Test that Cursor's conversation ID keys a private file its follow-up message names."""

        result = self.run_hook(
            session_id=None, conversation_id=self.session_id, hook_event_name="stop"
        )

        message = json.loads(result.stdout)["followup_message"]

        self.assertEqual(result.returncode, 0)
        self.assertIn(f"session-{self.session_id}.yaml", message)
        self.assertTrue(message.endswith(REPLY_PROMPT))
        self.assertEqual(stat.S_IMODE(self.directory.stat().st_mode), 0o700)

    def test_skips_unusable_id_and_continuation(self):
        """Test that a missing or unsafe session ID, or a reopened turn, creates nothing."""

        for case in (
            {"session_id": None},
            {"session_id": "../outside"},
            {"stop_hook_active": True},
        ):
            with self.subTest(case=case):
                result = self.run_hook(**case)

                self.assertEqual((result.returncode, result.stderr), (0, ""))
                self.assertEqual(self.ledger_files(), [])

    def test_checks_recorded_files_without_creating(self):
        """Test that files the transcript names, list the session or fail to parse are checked."""

        self.directory.mkdir()
        plan = {"id": "plan-1", "kind": "plan", "summary": "s", "data": {"status": "shown"}}
        named = self.directory / "named-task.yaml"
        recording = self.directory / "recording-task.yaml"
        broken = self.directory / "broken-task.yaml"
        repeated = self.directory / "repeated-task.yaml"

        named.write_text(json.dumps({"session_ledger": {"entries": [plan]}}))
        recording.write_text(
            json.dumps({"session_ledger": {"sessions": [self.session_id], "entries": [plan]}})
        )

        broken.write_text(f"session_ledger: [{self.session_id}\n")
        repeated.write_text(
            f"session_ledger:\n  entries: [{{id: kept}}]\n  entries: []\n"
            f"  sessions: [{self.session_id}]\n"
        )

        self.transcript.write_text(
            self.transcript.read_text() + json.dumps({"path": str(named)}) + "\n"
        )

        result = self.run_hook()

        self.assertEqual(result.returncode, BLOCK_EXIT)
        self.assertIn(f"{named} has entries missing", result.stderr)
        self.assertIn(f"{recording} has entries missing", result.stderr)
        self.assertIn(f"{broken} could not be read", result.stderr)
        self.assertIn(f"{repeated} could not be read", result.stderr)
        self.assertEqual(result.stderr.count(REPLY_PROMPT), 1)
        self.assertTrue(result.stderr.rstrip().endswith(REPLY_PROMPT))
        self.assertEqual(
            self.ledger_files(), [broken.name, named.name, recording.name, repeated.name]
        )

    def test_session_end_removes_only_untouched_file(self):
        """Test that session end deletes the hook's file only while nothing is recorded in it."""

        ledger = self.directory / f"session-{self.session_id}.yaml"
        task = self.directory / "task.yaml"
        rewritten = f"session_ledger:\n  entries: []\n  sessions: [{self.session_id}]\n"
        joined = rewritten.replace(f"{self.session_id}]", f"{self.session_id}, {uuid.uuid4()}]")
        claude = {"hook_event_name": "SessionEnd"}
        cursor = {"session_id": None, "conversation_id": self.session_id}
        cursor |= {"hook_event_name": "sessionEnd"}

        for payload, text, kept, returncode in (
            (claude, None, False, 0),
            (cursor, None, False, 0),
            (claude, rewritten, False, 0),
            (claude, joined, True, 0),
            (claude, rewritten.replace("entries: []", "entries: [{id: kept}]"), True, 0),
            (claude, rewritten.replace(f"[{self.session_id}]", "[]"), True, 0),
            (claude, rewritten + "  notes: [kept]\n", True, 0),
            (claude, "session_ledger:\n  entries: [{id: kept}]\n" + rewritten[16:], True, 1),
            (claude, f"session_ledger: [{self.session_id}\n", True, 1),
        ):
            with self.subTest(payload=payload, text=text):
                if ledger.exists():
                    ledger.unlink()

                self.run_hook()

                if text is not None:
                    ledger.write_text(text)

                result = self.run_hook(**payload)

                self.assertEqual(result.returncode, returncode)
                self.assertEqual(ledger.exists(), kept)

        task.write_text(rewritten)
        ledger.unlink()

        self.run_hook(**claude)

        self.assertTrue(task.exists())


if __name__ == "__main__":
    unittest.main()
