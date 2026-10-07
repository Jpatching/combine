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

    def test_untracked_private_markdown_is_not_read(self):
        self.tracked(".gitignore", ".private/\n")
        self.tracked("README.md", "# Public\n")
        private = self.root / ".private/other-worktree"
        private.mkdir(parents=True)
        (private / "README.md").write_text("[missing](absent.md)")
        (self.root / "scratch.md").write_text("[missing](absent.md)")
        self.assertEqual(check_links(self.root), 1)

    def test_link_outside_repository_is_rejected(self):
        self.tracked("README.md", "[outside](../outside.md)")
        with self.assertRaisesRegex(ValidationError, "Broken local link"):
            check_links(self.root)


if __name__ == "__main__":
    unittest.main()
