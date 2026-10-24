import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import TypedDict

HOOK = Path(__file__).resolve().parents[2] / ".agents" / "hooks" / "ledger_backup_check.py"
COMMENT = "https://example.invalid/pull/1#issuecomment-"


class HookResult(TypedDict):
    code: int
    stderr: str


def ledger_entry(entry_id: str, kind: str, **data: object) -> dict[str, object]:
    return {"id": entry_id, "kind": kind, "summary": "synthetic", "data": data, "observations": []}


def ledger_document(entries: list[dict[str, object]]) -> dict[str, object]:
    return {"session_ledger": {"entries": entries}}


class LedgerBackupCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.state = tempfile.TemporaryDirectory()
        self.addCleanup(self.state.cleanup)

        self.ledgers = Path(self.state.name) / "agent-ledgers"
        self.ledgers.mkdir()

    def write_ledger(self, document: object, name: str = "task-one.yaml") -> Path:
        ledger = self.ledgers / name

        ledger.write_text(document if isinstance(document, str) else json.dumps(document))

        return ledger

    def run_hook(self, hook_input: dict[str, object] | None = None) -> HookResult:
        completed = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(hook_input or {}),
            capture_output=True,
            text=True,
            env={**os.environ, "XDG_STATE_HOME": self.state.name},
            check=False,
        )

        self.assertEqual(completed.stdout, "")

        return HookResult(code=completed.returncode, stderr=completed.stderr)

    def assert_clean(self, document: object) -> None:
        self.write_ledger(document)

        self.assertEqual(self.run_hook(), HookResult(code=0, stderr=""))

    def test_no_ledger_directory_passes(self) -> None:
        self.ledgers.rmdir()

        self.assertEqual(self.run_hook(), HookResult(code=0, stderr=""))

    def test_reports_each_entry_missing_its_backup(self) -> None:
        cases = {
            "pushed guidance correction": ledger_entry(
                "gc-example", "guidance_correction", status="pending", commits=["abc1234"]
            ),
            "plan": ledger_entry("plan-example", "plan", status="approved"),
            "decision entry": ledger_entry("decision-example", "decision"),
            "answered question": ledger_entry("question-example", "question", status="answered"),
        }

        for label, entry in cases.items():
            with self.subTest(label):
                self.write_ledger(ledger_document([entry]))

                result = self.run_hook()

                self.assertEqual(result["code"], 2)
                self.assertIn(f"- {entry['id']} ({entry['kind']}): ", result["stderr"])

    def test_reports_listed_decision_without_backup(self) -> None:
        document = ledger_document([])
        document["decisions"] = [{"text": "synthetic choice"}]

        self.write_ledger(document)

        result = self.run_hook()

        self.assertEqual(result["code"], 2)
        self.assertIn("- decisions[0] (decision): no recovery_comment URL", result["stderr"])

    def test_reports_shared_guidance_comment(self) -> None:
        self.write_ledger(
            ledger_document(
                [
                    ledger_entry(
                        f"gc-example-{index}",
                        "guidance_correction",
                        commits=["abc1234"],
                        recovery_comment=f"{COMMENT}1",
                    )
                    for index in (1, 2)
                ]
            )
        )

        result = self.run_hook()

        self.assertEqual(result["code"], 2)
        self.assertIn("- gc-example-1 (guidance_correction): ", result["stderr"])
        self.assertIn("is shared with gc-example-2", result["stderr"])

    def test_allows_one_comment_per_kind(self) -> None:
        document = ledger_document(
            [
                ledger_entry("plan-example-1", "plan", recovery_comment=f"{COMMENT}1"),
                ledger_entry("plan-example-2", "plan", recovery_comment=f"{COMMENT}1"),
                ledger_entry("decision-example", "decision", recovery_comment=f"{COMMENT}2"),
                ledger_entry(
                    "question-example",
                    "question",
                    status="answered",
                    recovery_comment=f"{COMMENT}3",
                ),
            ]
        )
        document["decisions"] = [{"text": "synthetic choice", "recovery_comment": f"{COMMENT}2"}]

        self.assert_clean(document)

    def test_skips_entries_that_owe_no_backup(self) -> None:
        self.assert_clean(
            ledger_document(
                [
                    ledger_entry(
                        "gc-unverified",
                        "guidance_correction",
                        status="awaiting_action_verification",
                        commits=["abc1234"],
                    ),
                    ledger_entry("gc-unpushed", "guidance_correction", status="pending"),
                    ledger_entry(
                        "gc-delivered",
                        "guidance_correction",
                        delivery="delivered",
                        commit="abc1234",
                    ),
                    ledger_entry("plan-withdrawn", "plan", status="withdrawn"),
                    ledger_entry("question-open", "question", status="open"),
                    ledger_entry(
                        "plan-before-pull-request", "plan", recovery_comment="awaiting_pull_request"
                    ),
                    ledger_entry("artifact-example", "artifact"),
                ]
            )
        )

    def test_reports_unreadable_ledger(self) -> None:
        cases = {"invalid YAML": "session_ledger: [", "wrong shape": "- just a list"}

        for label, content in cases.items():
            with self.subTest(label):
                ledger = self.write_ledger(content)

                result = self.run_hook()

                self.assertEqual(result["code"], 2)
                self.assertIn(f"{ledger} could not be read", result["stderr"])

    def test_passes_when_already_continuing_after_a_block(self) -> None:
        self.write_ledger(ledger_document([ledger_entry("plan-example", "plan")]))

        self.assertEqual(self.run_hook({"stop_hook_active": True}), HookResult(code=0, stderr=""))

    def test_skips_an_unchanged_ledger_after_a_clean_check(self) -> None:
        ledger = self.write_ledger(ledger_document([]))

        self.assertEqual(self.run_hook()["code"], 0)

        status = ledger.stat()
        broken = "!" * status.st_size

        ledger.write_text(broken)
        os.utime(ledger, ns=(status.st_atime_ns, status.st_mtime_ns))

        self.assertEqual(self.run_hook()["code"], 0)

        os.utime(ledger, ns=(status.st_atime_ns, status.st_mtime_ns + 1))

        self.assertEqual(self.run_hook()["code"], 2)

    def test_rechecks_after_a_failed_check(self) -> None:
        ledger = self.write_ledger(ledger_document([ledger_entry("plan-example", "plan")]))

        self.assertEqual(self.run_hook()["code"], 2)
        self.assertFalse(ledger.with_name(f"{ledger.name}.backup-check").exists())
        self.assertEqual(self.run_hook()["code"], 2)

    def test_removes_the_check_record_of_a_removed_ledger(self) -> None:
        ledger = self.write_ledger(ledger_document([]))

        self.run_hook()
        ledger.unlink()
        self.run_hook()

        self.assertEqual(list(self.ledgers.iterdir()), [])

    def test_checks_only_ledgers_the_session_transcript_names(self) -> None:
        self.write_ledger(ledger_document([]), "task-clean.yaml")
        self.write_ledger(ledger_document([ledger_entry("plan-example", "plan")]), "task-owed.yaml")

        transcript = Path(self.state.name) / "transcript.jsonl"
        cases = {
            "names the clean ledger": ("agent-ledgers/task-clean.yaml", 0),
            "names the ledger owing a backup": ("~/.local/state/agent-ledgers/task-owed.yaml", 2),
            "names no ledger": ("no locator", 0),
        }

        for label, (text, expected) in cases.items():
            with self.subTest(label):
                transcript.write_text(json.dumps({"text": text}))

                result = self.run_hook({"transcript_path": str(transcript)})

                self.assertEqual(result["code"], expected)


if __name__ == "__main__":
    unittest.main()
