"""Run authored GTA adapter checks without assets, downloads or game launch."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent


def run(label, command):
    started = time.monotonic()
    print(f"CHECK: {label}", flush=True)
    try:
        subprocess.run(command, cwd=HERE.parents[1], check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {label}: {error}", file=sys.stderr, flush=True)
        return False
    print(f"PASS: {label} ({time.monotonic() - started:.2f}s)", flush=True)
    return True


def main():
    tools = {name: shutil.which(name) for name in ("node", "rustc", "g++")}
    missing = [name for name, path in tools.items() if path is None]
    if missing:
        print(
            "FAIL: missing required tools on PATH: " + ", ".join(missing)
            + ". Supply Node.js, Rust (edition 2024) and a C++17 g++ compiler; "
            "this command does not install tools.",
            file=sys.stderr,
        )
        return 1

    started = time.monotonic()
    passed = True
    for name in ("script", "status-script", "live-evaluation"):
        if not run(f"JavaScript {name}", [tools["node"], str(HERE / "tests" / f"{name}.cjs")]):
            passed = False

    with tempfile.TemporaryDirectory(prefix="combine-gtaiv-check-") as directory:
        suffix = ".exe" if sys.platform == "win32" else ""
        for name in ("connection", "wire", "freshness"):
            executable = str(Path(directory) / (name + suffix))
            if run(f"Rust {name} compile", [tools["rustc"], "--edition=2024", "--test",
                    str(HERE / "tests" / f"{name}.rs"), "-o", executable]):
                if not run(f"Rust {name}", [executable]):
                    passed = False
            else:
                passed = False

        executable = str(Path(directory) / ("evaluation-input" + suffix))
        if run("C++ evaluation-input compile", [tools["g++"], "-std=c++17", "-Wall",
                "-Wextra", "-Werror", str(HERE / "tests" / "evaluation-input.cpp"),
                "-o", executable]):
            if not run("C++ evaluation-input", [executable]):
                passed = False
        else:
            passed = False

    print(f"{'PASS' if passed else 'FAIL'}: authored GTA adapter checks "
          f"({time.monotonic() - started:.2f}s)", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
