"""Independent proof checks against source in a credential-free container."""
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path.cwd() / "scripts"))
from check_recipe import ValidationError
from verify import check_links


with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "docs").mkdir()
    (root / "docs/with spaces.md").write_text("# Steps\n")
    (root / "README.md").write_text(
        "[guide](<docs/with spaces.md#steps>) [normal](docs/with spaces.md) "
        "[anchor](<#section>) [web](<https://example.com>)\n"
    )
    subprocess.run(["git", "-C", str(root), "add", "README.md", "docs/with spaces.md"], check=True)
    assert check_links(root) == 2, "Valid local/remote/anchor links rejected"
    for destination in ("<docs/missing.md>", "<../outside.md>"):
        (root / "README.md").write_text(f"[bad]({destination})")
        try:
            check_links(root)
        except ValidationError:
            pass
        else:
            raise AssertionError(f"Invalid target accepted: {destination}")
print("PASS: external Markdown-link acceptance checks")
