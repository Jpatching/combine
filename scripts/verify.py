"""Repository gate: validate research metadata, recipes, local links and input tests."""

from pathlib import PurePosixPath
import re
import subprocess
import sys

from check_recipe import LOCK_PATH, ROOT, ValidationError, read_json, require, validate_recipe


def check_lock(lock):
    require(type(lock.get("schema_version")) is int and lock["schema_version"] == 1,
            "lock schema_version must be integer 1")
    runtime = lock["runtime"]
    require(re.fullmatch(r"[0-9a-f]{40}", runtime["commit"]) is not None,
            "lock needs a full source commit")
    require(runtime["repository"] == "https://github.com/chasmlol/2010-rust-rewrite-mashup",
            "unexpected baseline repository")
    require(runtime["platform"] == "windows-x64", "baseline platform must be windows-x64")
    release_url = runtime["repository"] + "/releases/tag/" + runtime["tag"]
    require(runtime["release_url"] == release_url, "release URL does not match the tag")
    asset = runtime["asset"]
    require(re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]) is not None,
            "archive needs a full SHA-256")
    require(type(asset["size_bytes"]) is int and asset["size_bytes"] > 0,
            "archive size must be a positive integer")
    require(asset["url"] == runtime["repository"] + "/releases/download/"
            + runtime["tag"] + "/" + asset["name"], "archive URL does not match the release")
    require(bool(lock["source_files"]), "source evidence index is empty")
    seen = set()
    for source in lock["source_files"]:
        path = PurePosixPath(source["path"])
        require(not path.is_absolute() and ".." not in path.parts and str(path) not in seen,
                "source evidence paths must be unique and relative")
        seen.add(str(path))
        require(re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is not None,
                "source evidence needs a full SHA-256")


def check_links(root=ROOT):
    root = root.resolve()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--",
         "GLOSSARY.md", "docs/", "research/results/"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    require(untracked.returncode == 0, "Cannot inspect public context inventory")
    pending = [name for name in untracked.stdout.split("\0") if name.endswith(".md")]
    require(not pending,
            "Untracked public context: " + ", ".join(pending)
            + ". Review and stage intended public files; keep private material outside these paths.")
    inventory = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    require(inventory.returncode == 0, "Cannot list tracked Markdown documents")
    docs = [root / name for name in inventory.stdout.split("\0") if name]
    for doc in docs:
        require(doc.resolve().is_relative_to(root) and doc.is_file(),
                f"Missing or external Markdown document: {doc.relative_to(root)}")
        for target in re.findall(r"\[[^\]]+\]\((<[^<>\n]*>|[^)]+)\)", doc.read_text(encoding="utf-8")):
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target.startswith(("https://", "http://", "#", "mailto:")):
                continue
            path = (doc.parent / target.split("#", 1)[0]).resolve()
            require(path.is_relative_to(root) and path.is_file(),
                    f"Broken local link in {doc.relative_to(root)}")
    return len(docs)


def check_handoff(root=ROOT):
    text = (root / "docs/HANDOFF.md").read_text(encoding="utf-8")
    for section in ("Current task", "Evidence", "Next step", "Session close", "Historical reference"):
        matches = re.findall(r"^## " + re.escape(section) + r"\n(.*?)(?=^## |\Z)",
                             text, flags=re.MULTILINE | re.DOTALL)
        require(len(matches) == 1 and bool(matches[0].strip()),
                f"HANDOFF needs one nonempty '{section}' section")
    for field in ("Reviewed", "Task", "Source branch", "Source revision", "Disposition",
                  "Latest runtime evidence"):
        values = re.findall(r"^" + re.escape(field) + r":[ \t]*(.*)$", text, flags=re.MULTILINE)
        require(len(values) == 1 and bool(values[0].strip()), f"HANDOFF needs one '{field}' value")
    require(re.search(r"^Reviewed: \d{4}-\d{2}-\d{2}$", text, flags=re.MULTILINE),
            "HANDOFF Reviewed must use YYYY-MM-DD")
    require(re.search(r"^Source revision: `[0-9a-f]{40}`$", text, flags=re.MULTILINE),
            "HANDOFF needs a full source revision")
    require(re.search(r"^Task: .*https://github.com/Jpatching/combine/issues/\d+", text, flags=re.MULTILINE),
            "HANDOFF Task must link the current issue")
    require("https://github.com/Jpatching/combine/pull/" in text or "No PR exists" in text,
            "HANDOFF must link the PR or state 'No PR exists'")


def main():
    try:
        lock = read_json(LOCK_PATH)
        check_lock(lock)
        recipes = sorted((ROOT / "recipes").glob("*.json"))
        require(len(recipes) == 2, "the research catalogue must contain two candidates")
        seen_ids = set()
        for path in recipes:
            recipe = read_json(path)
            validate_recipe(recipe, lock)
            require(recipe["id"] not in seen_ids, "recipe ids must be unique")
            seen_ids.add(recipe["id"])
        doc_count = check_links()
        check_handoff()
    except (ValidationError, KeyError, TypeError, OSError) as error:
        message = str(error) if isinstance(error, ValidationError) else "Invalid repository metadata"
        print(f"FAIL: {message}", file=sys.stderr)
        return 1
    print(f"PASS: lock structure, {len(recipes)} recipes, local links in {doc_count} documents, "
          "public context inventory and HANDOFF structure", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT,
        check=False,
    )
    if result.returncode:
        return result.returncode
    print("PASS: repository gate. Windows gameplay and business validation are NOT covered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
