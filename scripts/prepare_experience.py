"""Create separate local workspaces. Never install, copy assets or launch a game."""

import argparse
import json
from pathlib import Path
import sys

from check_recipe import ROOT, ValidationError, require


# These are workspace identities, not supported recipes or ready runtime builds.
EXPERIENCES = {
    "mw2-skate-minecraft": {"world": "existing-mashup", "combat": "mw2-default"},
    "fortnite-skate": {"world": "Release-3.1-CL-3917250", "combat": "none"},
}
DIRECTORIES = ("runtime", "profile", "build", "reviews")


def prepare(experience, root):
    require(experience in EXPERIENCES, "Unknown experience; use a listed workspace identity")
    root = Path(root).resolve()
    # Game files must never enter tracked source. External local roots are allowed.
    require(not root.is_relative_to(ROOT) or root.is_relative_to(ROOT / ".private"),
            "Use .private or a local directory outside the source repository")
    destination = root / experience
    require(not destination.exists() and not destination.is_symlink(),
            "Experience workspace already exists; refusing to overwrite")
    root.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Exclusive creation also protects against competing runs.
    for directory in DIRECTORIES:
        (destination / directory).mkdir()
    manifest = {
        "schema_version": 1,
        "experience": experience,
        **EXPERIENCES[experience],
        "state": "scaffolded",
        "build": None,
        "acceptance": "unaccepted",
    }
    (destination / "workspace.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8",
    )
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experience", choices=EXPERIENCES)
    parser.add_argument("--root", type=Path, default=ROOT / ".private" / "experiences")
    args = parser.parse_args(argv)
    try:
        manifest = prepare(args.experience, args.root)
    except (ValidationError, OSError, ValueError) as error:
        message = str(error) if isinstance(error, ValidationError) else (
            "Cannot create workspace; check access. Any partial workspace is retained."
        )
        print("FAIL: " + message, file=sys.stderr)
        return 1
    print(json.dumps(manifest))
    print("Workspace only: no runtime, assets, executable, launch or gameplay qualification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
