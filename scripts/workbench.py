#!/usr/bin/env python3
"""Open Combine's terminal views and run its isolated, reviewed guide tools."""
import argparse
import base64
import hashlib
import os
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = "Jpatching/combine"


def run(*args, capture=False, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          capture_output=capture)


def identity():
    run("git", "status", "--short", "--branch")
    run("git", "rev-parse", "HEAD")


def view(name):
    identity()
    if name == "behaviour":
        run("less", str(ROOT / "docs/WORKBENCH.md"))
        return
    if name == "checks":
        print("Source gate only; runtime and owner acceptance are separate.", flush=True)
        if input("Run python3 scripts/verify.py? [y/N] ").lower() == "y":
            run(sys.executable, "scripts/verify.py")
        input("Press Enter to return to the shell.")
        return
    while True:
        run("gh", "issue", "list", "--repo", REPO, "--state", "open", "--limit", "100")
        choice = input("Issue number to read, Enter to refresh, q to return: ").strip()
        if choice == "q":
            return
        if choice.isdecimal():
            run("gh", "issue", "view", choice, "--repo", REPO, "--comments")
        elif choice:
            print("Enter an issue number or q.")


def open_views(session):
    if session is None:
        session = run("tmux", "display-message", "-p", "#{session_name}", capture=True).stdout.strip()
    # Exact session targeting avoids prefix matches; no send-keys or pane replacement.
    target = "=" + session
    run("tmux", "has-session", "-t", target)
    existing = set(run("tmux", "list-windows", "-t", target, "-F", "#{window_name}",
                       capture=True).stdout.splitlines())
    for name in ("git", "issues", "behaviour", "checks"):
        window = "combine-" + name
        if window in existing:
            print(f"Preserved existing window: {window}")
            continue
        command = ["lazygit"] if name == "git" else [sys.executable, str(Path(__file__).resolve()), "view", name]
        # tmux's shell command is quoted once; the final shell retains the result.
        shell_command = shlex.join(command) + "; exec bash"
        run("tmux", "new-window", "-d", "-t", target + ":", "-n", window, "-c", str(ROOT), shell_command)
        print(f"Created {window}")
    print("Existing Codex/editor panes and selected window were preserved.")


def guide(tool, args):
    import json
    pins = json.loads((ROOT / "research/tool-guides.json").read_text())
    snapshot = ROOT / ".private/tool-guides" / tool
    actual = run("git", "rev-parse", "HEAD", cwd=snapshot, capture=True).stdout.strip()
    if actual != pins[tool]["revision"] or run("git", "status", "--porcelain", cwd=snapshot, capture=True).stdout:
        raise ValueError("Guide checkout changed; review it and update the recorded revision before use.")
    if tool == "universal-modder":
        # Isolate its user state; importing the CLI does not call remote asset services.
        import os
        import shutil
        knowledge = ROOT / ".private/tooling/um-knowledge"
        if not knowledge.exists():
            shutil.copytree(snapshot / "knowledge", knowledge)
        if len(args) >= 2 and args[0] == "kb" and args[1] in {"search", "show", "new", "check", "index"}:
            if not any(arg == "--root" or arg.startswith("--root=") for arg in args):
                args = [*args, "--root", str(knowledge)]
        env = dict(os.environ, PYTHONPATH=str(snapshot), UM_HOME=str(ROOT / ".private/tooling/um-state"),
                   UM_KB=str(knowledge))
        subprocess.run([sys.executable, "-m", "um", *args], cwd=ROOT, env=env, check=True)
    else:
        node = ROOT / ".private/tooling/rea/node-v24.11.0-linux-x64/bin/node"
        cli = ROOT / ".private/tooling/rea/package/node_modules/rea-agents/scripts/rea.mjs"
        package = json.loads(cli.parents[1].joinpath("package.json").read_text())
        if package["version"] != pins[tool]["package_version"]:
            raise ValueError("REA package version differs from the reviewed version.")
        if installation_digest(cli.parents[2]) != pins[tool]["installed_tree_sha256"]:
            raise ValueError("REA installation changed; review the installation before refreshing its fingerprint.")
        if hashlib.sha256(node.read_bytes()).hexdigest() != pins[tool]["node_sha256"]:
            raise ValueError("REA Node runtime changed from the checksum-verified installation.")
        run(str(node), str(cli), *args)


def installation_digest(directory):
    digest = hashlib.sha256()
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            content = b"link:" + path.readlink().as_posix().encode()
        elif path.is_file():
            with path.open("rb") as stream:
                file_hash = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    file_hash.update(chunk)
                content = file_hash.digest()
        else:
            continue
        digest.update(path.relative_to(directory).as_posix().encode() + b"\0" + content + b"\0")
    return digest.hexdigest()


def open_evidence(paths, print_only=False):
    files = [Path(path).expanduser().resolve() for path in paths]
    if not files:
        files = [ROOT / "tools/workbench/evidence.html"]
    for path in files:
        if not path.is_file():
            raise ValueError(f"Evidence file does not exist: {path}")
        if path.suffix.lower() not in {".html", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".mov"}:
            raise ValueError(f"Unsupported evidence format: {path.suffix}")
    for path in files:
        print(path.as_uri(), flush=True)
        if print_only:
            continue
        if os.name == "nt":
            os.startfile(str(path))
        elif os.environ.get("WSL_DISTRO_NAME"):
            windows_path = run("wslpath", "-w", str(path), capture=True).stdout.strip()
            # Encode a PowerShell literal, never interpolate the path as executable code.
            command = "$ErrorActionPreference='Stop'; Start-Process -FilePath '" + windows_path.replace("'", "''") + "'"
            encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
            run("powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded)
        else:
            run("open" if sys.platform == "darwin" else "xdg-open", str(path))
    if not print_only:
        print("Requested local viewers. Owner confirmation is still pending.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    opening = commands.add_parser("open", help="Add views without replacing existing panes")
    opening.add_argument("--session", help="Existing tmux session; default is current")
    viewing = commands.add_parser("view", help="Open an individual text view")
    viewing.add_argument("name", choices=["issues", "behaviour", "checks"])
    upstream = commands.add_parser("guide", help="Run an installed, pinned guide tool")
    upstream.add_argument("tool", choices=["rea", "universal-modder"])
    upstream.add_argument("args", nargs=argparse.REMAINDER)
    evidence = commands.add_parser("evidence", help="Open local evidence, or the comparison page when no files are supplied")
    evidence.add_argument("paths", nargs="*", help="Local clips or screenshots to open")
    evidence.add_argument("--print-only", action="store_true", help="Print locations without opening viewers")
    args = parser.parse_args()
    try:
        if args.command == "open":
            open_views(args.session)
        elif args.command == "view":
            view(args.name)
        elif args.command == "evidence":
            open_evidence(args.paths, args.print_only)
        else:
            guide(args.tool, args.args)
    except (subprocess.CalledProcessError, OSError, ValueError) as error:
        print(f"Workbench unavailable: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
