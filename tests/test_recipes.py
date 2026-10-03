"""Boundary tests for configuration that must never turn into executable input."""

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_recipe import MAX_JSON_BYTES, ValidationError, read_json, validate_recipe


class RecipeTests(unittest.TestCase):
    def setUp(self):
        self.lock = read_json(ROOT / "research/upstream.lock.json")
        self.recipe = read_json(ROOT / "recipes/mw2-skate.json")

    def assert_rejected(self, change):
        recipe = deepcopy(self.recipe)
        change(recipe)
        with self.assertRaises(ValidationError):
            validate_recipe(recipe, self.lock)

    def test_both_candidates_are_accepted(self):
        for path in sorted((ROOT / "recipes").glob("*.json")):
            with self.subTest(recipe=path.name):
                validate_recipe(read_json(path), self.lock)

    def test_stale_runtime_commit_is_rejected(self):
        self.assert_rejected(lambda r: r["runtime"].update(commit="0" * 40))

    def test_wrong_runtime_identity_is_rejected(self):
        self.assert_rejected(lambda r: r["runtime"].update(id="arbitrary-game"))

    def test_execution_and_private_path_fields_are_rejected(self):
        for field in ("command", "hook", "download_url", "game_path"):
            with self.subTest(field=field):
                self.assert_rejected(lambda r: r.update({field: "untrusted-value"}))

    def test_nested_extra_fields_are_rejected(self):
        self.assert_rejected(lambda r: r["runtime"].update(command="untrusted-value"))

    def test_missing_fields_are_rejected(self):
        self.assert_rejected(lambda r: r.pop("required_content"))

    def test_non_object_roots_are_rejected(self):
        for value in ([], None, True, "recipe", 1):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_recipe(value, self.lock)

    def test_schema_version_requires_integer_one(self):
        for value in (True, 1.0, "1", 0, 2, None):
            with self.subTest(value=value):
                self.assert_rejected(lambda r: r.update(schema_version=value))

    def test_invalid_worlds_do_not_crash_validator(self):
        for value in ("unknown:world", [], {}, None):
            with self.subTest(value=value):
                self.assert_rejected(lambda r: r.update(world=value))

    def test_world_cannot_omit_additional_content(self):
        self.assert_rejected(lambda r: r.update(world="minecraft:overworld"))

    def test_unsupported_modes_are_rejected(self):
        self.assert_rejected(lambda r: r.update(movement=["flight"]))
        self.assert_rejected(lambda r: r.update(combat="custom-script"))

    def test_display_control_characters_and_unsafe_ids_are_rejected(self):
        for value in ("", "../private", "two--hyphens", "UPPER", "a" * 65):
            self.assert_rejected(lambda r: r.update(id=value))
        for value in (" ", "title\ncommand", "\x1b[31m", "\u202esecret", "x" * 121):
            self.assert_rejected(lambda r: r.update(title=value))

    def test_malformed_duplicate_and_non_finite_json_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recipe.json"
            for content in (b'{', b'{"x":1,"x":2}', b'{"x":NaN}',
                            b'{"x":Infinity}', b'{"x":1e999}', b'\xff',
                            b'[' * 2000 + b']' * 2000):
                with self.subTest(content=content[:20]):
                    path.write_bytes(content)
                    with self.assertRaises(ValidationError):
                        read_json(path)

    def test_size_limit_and_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recipe.json"
            with self.assertRaises(ValidationError):
                read_json(path)
            path.write_bytes(b'{}' + b' ' * (MAX_JSON_BYTES - 2))
            self.assertEqual(read_json(path), {})
            path.write_bytes(b'{}' + b' ' * (MAX_JSON_BYTES - 1))
            with self.assertRaises(ValidationError):
                read_json(path)

    def test_cli_failure_does_not_echo_untrusted_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"secret":"DO-NOT-ECHO"}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/check_recipe.py"), str(path)],
                capture_output=True, text=True, check=False, cwd=directory,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("error:", result.stderr)
            self.assertNotIn("DO-NOT-ECHO", result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_cli_runs_outside_repo_without_mutating_recipe(self):
        path = ROOT / "recipes/mw2-skate.json"
        before = path.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/check_recipe.py"), str(path)],
                capture_output=True, text=True, check=False, cwd=directory,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unverified", result.stdout)
        self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
