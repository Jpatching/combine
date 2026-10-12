"""Check that a fresh session receives a usable context entry point."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_recipe import ValidationError
from verify import check_handoff


HANDOFF = """# Current context

## Current task
Reviewed: 2026-10-09
Task: [task](https://github.com/Jpatching/combine/issues/20)
Source branch: `integration/example`
Source revision: `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`
Disposition: pushed; [PR](https://github.com/Jpatching/combine/pull/23) remains blocked.
## Evidence
Latest runtime evidence: not run.
## Next step
Reproduce the recorded blocker.
## Session close
Preserve evidence and report disposition.
## Historical reference
Earlier work is parked.
"""


class HandoffTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "docs").mkdir()

    def check(self, text):
        (self.root / "docs/HANDOFF.md").write_text(text, encoding="utf-8")
        check_handoff(self.root)

    def test_complete_snapshot_is_still_accepted(self):
        self.check(HANDOFF)

    def test_short_issue_pointer_without_snapshot_fields_is_accepted(self):
        self.check("Resume [ground support](https://github.com/Jpatching/combine/issues/39).\n")

    def test_empty_handoff_is_rejected(self):
        for text in ("", " \n"):
            with self.subTest(text=text), self.assertRaisesRegex(ValidationError, "empty"):
                self.check(text)

    def test_missing_current_issue_is_rejected(self):
        for text in ("Resume a task.\n", "https://github.com/Jpatching/combine/pull/23"):
            with self.subTest(text=text), self.assertRaisesRegex(ValidationError, "current issue"):
                self.check(text)


if __name__ == "__main__":
    unittest.main()
