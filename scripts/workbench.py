#!/usr/bin/env python3
"""Open Combine's terminal views and run its isolated, reviewed guide tools."""
import argparse
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
        env = dict(os.environ, PYTHONPATH=str(snapshot), UM_HOME=str(ROOT / ".private/tooling/um-state"))
        subprocess.run([sys.executable, "-m", "um", *args], cwd=ROOT, env=env, check=True)
    else:
        node = ROOT / ".private/tooling/rea/node-v24.11.0-linux-x64/bin/node"
        cli = ROOT / ".private/tooling/rea/package/node_modules/rea-agents/scripts/rea.mjs"
        package = json.loads(cli.parents[1].joinpath("package.json").read_text())
        if package["version"] != pins[tool]["package_version"]:
            raise ValueError("REA package version differs from the reviewed version.")
        run(str(node), str(cli), *args)


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
    commands.add_parser("evidence", help="Print the local clip/screenshot comparison page location")
    args = parser.parse_args()
    try:
        if args.command == "open":
            open_views(args.session)
        elif args.command == "view":
            view(args.name)
        elif args.command == "evidence":
            print((ROOT / "tools/workbench/evidence.html").as_uri())
            print("Open this file in your local browser; select media there without uploading it.")
        else:
            guide(args.tool, args.args)
    except (subprocess.CalledProcessError, OSError, ValueError) as error:
        print(f"Workbench unavailable: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
