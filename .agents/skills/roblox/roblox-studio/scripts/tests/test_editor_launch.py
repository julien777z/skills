import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio_mcp.client import editor_launch_refusal, held_editor_slots, member_receipt  # noqa: E402
from studio_mcp.models import AgentLockReceipt, EditorSlot, RunnerConfig  # noqa: E402

SLOTS = [EditorSlot(number=number, lock_key=f"game-vm/editor-{number}", project=f"editor-{number}")
         for number in (1, 2, 3)]
CONFIG = RunnerConfig(ROBLOX_STUDIO_GAME="sample-game", ROBLOX_STUDIO_TART="tart", ROBLOX_STUDIO_VM="game-vm",
                      ROBLOX_STUDIO_SSH_USER="runner", ROBLOX_STUDIO_SSH_KEY="runner-key",
                      ROBLOX_STUDIO_KNOWN_HOSTS="known-hosts", ROBLOX_STUDIO_EDITORS=3)


class EditorLaunchTest(unittest.TestCase):
    def test_a_lease_on_the_vm_alone_launches_no_editor(self) -> None:
        """Test that a lease holding only the VM's own lock, as tooling from before the pool takes, launches no
        editor, whatever runs."""

        refusal = editor_launch_refusal("legacy", [], False, 3, 0)

        self.assertIsNotNone(refusal)
        self.assertIn("predates the pool", refusal or "")

    def test_an_editor_lock_launches_only_in_its_own_project(self) -> None:
        """Test that one editor's lock launches an editor in its own project folder or a published place, and in no
        other project."""

        self.assertIsNone(editor_launch_refusal("editor-2", [SLOTS[1]], False, 3, 2))
        self.assertIsNone(editor_launch_refusal(None, [SLOTS[1]], False, 3, 2))
        self.assertIsNotNone(editor_launch_refusal("legacy", [SLOTS[1]], False, 3, 2))

    def test_the_whole_vm_launches_in_any_project(self) -> None:
        """Test that the whole VM launches an editor in a project of its choosing."""

        self.assertIsNone(editor_launch_refusal("a-game", SLOTS, True, 3, 0))

    def test_no_launch_goes_past_the_pool_size(self) -> None:
        """Test that a launch is refused once the VM runs as many editors as its pool has, whatever the lease."""

        for held, whole_vm in (([SLOTS[0]], False), (SLOTS, True)):
            with self.subTest(whole_vm=whole_vm):
                self.assertIsNone(editor_launch_refusal("editor-1", held, whole_vm, 3, 2))
                self.assertIsNotNone(editor_launch_refusal("editor-1", held, whole_vm, 3, 3))

    def test_the_whole_vm_is_held_only_with_every_editor_receipt(self) -> None:
        """Test that a receipt for one editor holds that editor, and one for the VM's own lock counts as the whole VM
        only beside a receipt for every editor."""

        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / "vm.json"
            one = Path(folder) / "editor.json"

            receipt.write_text(json.dumps(AgentLockReceipt(key="game-vm", lock_file="vm.lock", token="vm-token")))
            one.write_text(json.dumps(AgentLockReceipt(key="game-vm/editor-3", lock_file="editor.lock",
                                                       token="editor-token")))

            self.assertEqual(held_editor_slots(receipt, CONFIG), ([], False))
            self.assertEqual(held_editor_slots(one, CONFIG), ([SLOTS[2]], False))

            for slot in SLOTS:
                member_receipt(receipt, slot).write_text("{}")

            self.assertEqual(held_editor_slots(receipt, CONFIG), (SLOTS, True))

if __name__ == "__main__":
    unittest.main()
