"""Add the two diagnostic commands to exact pinned definitions, into a new file."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA256 = "ba78c1ae32ea2eb800311f4513617e75c6283ac94805db016d157745356eb21b"


def prepare(source, destination):
    content = source.read_bytes()
    if hashlib.sha256(content).hexdigest() != BASE_SHA256:
        raise ValueError("Definitions differ from the pinned source; stop")
    definitions = json.loads(content)
    fields = [("timer", "int"), ("frame", "float"), ("ped", "int"), ("onFoot", "int")]
    fields += [(name, "float") for name in (
        "x", "y", "z", "cameraX", "cameraY", "cameraZ", "rotationX", "rotationY", "rotationZ")]
    fields += [(name, "int") for name in ("leftX", "leftY", "rightX", "rightY")]
    definitions["extensions"].append({"name": "combine_diagnostic", "commands": [
        {"name": "COMBINE_IV_READY", "num_params": 1, "input": [],
         "output": [{"name": "ready", "type": "int"}]},
        {"name": "COMBINE_IV_SAMPLE", "num_params": len(fields),
         "input": [{"name": name, "type": kind} for name, kind in fields], "output": []},
    ]})
    with destination.open("x", encoding="utf-8") as output:
        json.dump(definitions, output, indent=2)
        output.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    prepare(args.source, args.destination)
