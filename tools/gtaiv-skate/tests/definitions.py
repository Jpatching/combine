"""Generated native contracts; pass the exact pinned public definition JSON."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

module_path = Path(__file__).resolve().parents[1] / "prepare_definitions.py"
spec = importlib.util.spec_from_file_location("prepare_definitions", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = Path(sys.argv[1])

with tempfile.TemporaryDirectory() as directory:
    for evaluation in (False, True):
        target = Path(directory) / ("evaluation.json" if evaluation else "normal.json")
        module.prepare(source, target, evaluation)
        commands = {command["name"]: command
                    for extension in json.loads(target.read_text())["extensions"]
                    for command in extension["commands"]}
        assert commands["DESTROY_CAM"]["input"][0].get("source", "any") == "any", \
            "DESTROY_CAM must receive the camera handle by value, not its address"
        assert commands["GET_GROUND_Z_FOR_3D_COORD"]["attrs"]["is_condition"] is True
        assert commands["GET_GROUND_Z_FOR_3D_COORD"]["output"][0]["type"] == "float"
        assert ("COMBINE_SKATE_EVAL_INPUT" in commands) is evaluation
        assert ("COMBINE_SKATE_EVAL_KEY" in commands) is evaluation
    invalid = Path(directory) / "changed-pin.json"
    invalid.write_bytes(source.read_bytes() + b" ")
    try:
        module.prepare(invalid, Path(directory) / "invalid-output.json")
    except ValueError:
        pass
    else:
        raise AssertionError("Modified upstream definition pin was accepted")

print("PASS: generated native return/argument contracts, evaluation opt-in and pin refusal")
print("LIMIT: definition contracts do not establish native execution or gameplay")
