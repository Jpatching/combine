"""Exercise the documentation gate against real Git inventories."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_recipe import ValidationError
from verify import check_links


class DocumentationLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.git("init", "--quiet")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True,
                       capture_output=True)

    def tracked(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        self.git("add", "--", name)

    def test_nested_agent_and_research_links_are_checked(self):
        for name in ("docs/agents/work.md", "research/results/result.md"):
            with self.subTest(name=name):
                self.tracked(name, "[missing](absent.md)")
                with self.assertRaisesRegex(ValidationError, "Broken local link"):
                    check_links(self.root)
                self.tracked(name, "# Repaired\n")

    def test_relative_links_fragments_and_spaces_are_accepted(self):
        self.tracked("README.md", "[guide](docs/guide.md#steps)")
        self.tracked("docs/guide.md", "[home](../README.md) [remote](https://example.com)")
        self.tracked("docs/with spaces.md", "[section](#heading)")
        self.assertEqual(check_links(self.root), 3)

    def test_angle_bracket_relative_links_with_spaces_and_fragments_are_accepted(self):
        self.tracked("README.md", "[guide](<docs/with spaces.md>)")
        self.tracked("docs/with spaces.md", "[home](<../README.md#heading>)")
        self.assertEqual(check_links(self.root), 2)

    def test_angle_bracket_destination_with_parentheses_is_accepted(self):
        self.tracked("README.md", "[guide](<docs/guide (draft).md#steps>)")
        self.tracked("docs/guide (draft).md", "# Steps\n")
        self.assertEqual(check_links(self.root), 2)

    def test_remote_and_anchor_links_are_excluded_with_or_without_brackets(self):
        for target in ("https://example.com/guide", "http://example.com/guide",
                       "mailto:owner@example.com", "#heading"):
            for destination in (target, f"<{target}>"):
                with self.subTest(destination=destination):
                    self.tracked("README.md", f"[excluded]({destination})")
                    self.assertEqual(check_links(self.root), 1)

    def test_missing_angle_bracket_local_target_is_rejected(self):
        self.tracked("README.md", "[missing](<docs/missing guide.md#steps>)")
        with self.assertRaisesRegex(ValidationError, "Broken local link"):
            check_links(self.root)

    def test_angle_bracket_links_to_existing_external_targets_are_rejected(self):
        outside = tempfile.TemporaryDirectory(dir=self.root.parent)
        self.addCleanup(outside.cleanup)
        target = Path(outside.name) / "outside guide.md"
        target.write_text("# Outside\n", encoding="utf-8")
        for destination in (f"../{target.parent.name}/{target.name}", str(target)):
            with self.subTest(destination=destination):
                self.tracked("README.md", f"[outside](<{destination}#heading>)")
                with self.assertRaisesRegex(ValidationError, "Broken local link"):
                    check_links(self.root)

    def test_untracked_private_markdown_is_not_read(self):
        self.tracked(".gitignore", ".private/\n")
        self.tracked("README.md", "# Public\n")
        private = self.root / ".private/other-worktree"
        private.mkdir(parents=True)
        (private / "README.md").write_text("[missing](absent.md)")
        (self.root / "scratch.md").write_text("[missing](absent.md)")
        self.assertEqual(check_links(self.root), 1)

    def test_untracked_public_context_is_rejected_until_staged(self):
        self.tracked("README.md", "# Public\n")
        for name in ("GLOSSARY.md", "docs/adr/decision.md", "research/results/note.md"):
            with self.subTest(name=name):
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Reviewed context\n", encoding="utf-8")
                with self.assertRaisesRegex(ValidationError, "Untracked public context"):
                    check_links(self.root)
                self.git("add", "--", name)
                check_links(self.root)

    def test_ignored_markdown_under_public_docs_is_not_read(self):
        self.tracked(".gitignore", "docs/private/\n")
        self.tracked("README.md", "# Public\n")
        private = self.root / "docs/private"
        private.mkdir(parents=True)
        (private / "note.md").write_text("[missing](absent.md)", encoding="utf-8")
        self.assertEqual(check_links(self.root), 1)

    def test_link_outside_repository_is_rejected(self):
        self.tracked("README.md", "[outside](../outside.md)")
        with self.assertRaisesRegex(ValidationError, "Broken local link"):
            check_links(self.root)


if __name__ == "__main__":
    unittest.main()
