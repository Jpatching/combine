"""Evidence presentation must request a viewer without executing path contents."""
import base64
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import workbench


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.clip = Path(temp.name) / "owner's $(example) clip.mp4"
        self.clip.write_bytes(b"synthetic test placeholder")

    def test_wsl_opens_explicit_media_as_literal_windows_path(self):
        windows_path = "C:\\Evidence\\owner's $(example) clip.mp4"
        with patch.dict(os.environ, {"WSL_DISTRO_NAME": "Ubuntu"}), \
                patch.object(workbench, "run") as run:
            run.return_value.stdout = windows_path + "\n"
            workbench.open_evidence([self.clip])
        self.assertEqual(run.call_args_list[0].args,
                         ("wslpath", "-w", str(self.clip)))
        invocation = run.call_args_list[1].args
        self.assertEqual(invocation[:4], ("powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand"))
        self.assertEqual(base64.b64decode(invocation[4]).decode("utf-16-le"),
                         "$ErrorActionPreference='Stop'; Start-Process -FilePath 'C:\\Evidence\\owner''s $(example) clip.mp4'")

    def test_default_opens_comparison_and_print_only_opens_nothing(self):
        with patch.dict(os.environ, {}, clear=True), \
                patch.object(workbench, "run") as run:
            workbench.open_evidence([])
            run.assert_called_once_with("open" if sys.platform == "darwin" else "xdg-open",
                                        str(workbench.ROOT / "tools/workbench/evidence.html"))
            run.reset_mock()
            workbench.open_evidence([self.clip], print_only=True)
            run.assert_not_called()

    def test_invalid_batch_opens_nothing(self):
        executable = self.clip.with_suffix(".exe")
        executable.write_bytes(b"not executable")
        for invalid in (self.clip.with_name("absent.mp4"), executable):
            with self.subTest(path=invalid), patch.object(workbench, "run") as run:
                with self.assertRaises(ValueError):
                    workbench.open_evidence([self.clip, invalid])
                run.assert_not_called()

    def test_viewer_failure_returns_nonzero(self):
        with patch.object(sys, "argv", ["workbench.py", "evidence", str(self.clip)]), \
                patch.object(workbench, "run", side_effect=subprocess.CalledProcessError(1, "viewer")):
            self.assertEqual(workbench.main(), 1)


if __name__ == "__main__":
    unittest.main()
