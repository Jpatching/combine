"""Workspace separation protects predecessor trials and keeps assets private."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_recipe import ROOT, ValidationError
from prepare_experience import prepare


class ExperienceTests(unittest.TestCase):
    def test_separate_workspaces_do_not_migrate_or_claim_a_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("mw2-skate-minecraft", "fortnite-skate"):
                manifest = prepare(name, root)
                self.assertEqual(manifest["state"], "scaffolded")
                self.assertIsNone(manifest["build"])
                self.assertEqual(manifest["acceptance"], "unaccepted")
                for directory in ("runtime", "profile", "build", "reviews"):
                    self.assertEqual(list((root / name / directory).iterdir()), [])
            self.assertEqual(json.loads((root / "fortnite-skate/workspace.json").read_text())["combat"], "none")

    def test_repeated_preparation_preserves_local_work(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepare("fortnite-skate", root)
            prior = root / "fortnite-skate/profile/settings"
            prior.write_text("preserve")
            with self.assertRaises(ValidationError):
                prepare("fortnite-skate", root)
            self.assertEqual(prior.read_text(), "preserve")

    def test_unknown_id_and_tracked_destination_fail_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "untouched"
            for name in ("../other", "fortnite-skate-mw2", "https://example.com", "$(command)"):
                with self.assertRaises(ValidationError):
                    prepare(name, root)
            self.assertFalse(root.exists())
        with self.assertRaises(ValidationError):
            prepare("fortnite-skate", ROOT / "assets")

    def test_existing_symlink_is_never_followed_or_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "fortnite-skate").symlink_to(root / "missing", target_is_directory=True)
            with self.assertRaises(ValidationError):
                prepare("fortnite-skate", root)
            self.assertFalse((root / "missing").exists())
