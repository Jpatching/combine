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

    def test_complete_snapshot_and_explicit_absence_of_pr_are_accepted(self):
        self.check(HANDOFF)
        self.check(HANDOFF.replace("[PR](https://github.com/Jpatching/combine/pull/23) remains blocked.",
                                  "No PR exists; preserved experiment."))

    def test_missing_empty_or_duplicate_section_is_rejected(self):
        for text in (HANDOFF.replace("## Next step", "## Other"),
                     HANDOFF.replace("Reproduce the recorded blocker.", ""),
                     HANDOFF + "\n## Next step\nAnother instruction.\n"):
            with self.subTest(text=text), self.assertRaisesRegex(ValidationError, "Next step"):
                self.check(text)

    def test_missing_empty_or_duplicate_disposition_is_rejected(self):
        for text in (HANDOFF.replace("Disposition:", "Other:"),
                     HANDOFF.replace("Disposition: pushed; [PR](https://github.com/Jpatching/combine/pull/23) remains blocked.",
                                     "Disposition: "),
                     HANDOFF + "\nDisposition: merged\n"):
            with self.subTest(text=text), self.assertRaisesRegex(ValidationError, "Disposition"):
                self.check(text)

    def test_short_revision_and_missing_tracker_links_are_rejected(self):
        for old, new, message in (
            ("b" * 40, "b403377", "full source revision"),
            ("https://github.com/Jpatching/combine/issues/20", "historical.txt", "current issue"),
            ("https://github.com/Jpatching/combine/pull/23", "historical.txt", "link the PR"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(ValidationError, message):
                self.check(HANDOFF.replace(old, new))


if __name__ == "__main__":
    unittest.main()
