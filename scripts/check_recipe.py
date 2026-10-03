"""Check research recipes offline. Never download, prepare or launch game files."""

import argparse
import json
import math
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "research" / "upstream.lock.json"
MAX_JSON_BYTES = 64 * 1024
BASE_CONTENT = ["mw2-2009-steam-multiplayer", "skate3-xbox360-extracted"]
CONTENT_BY_WORLD = {
    "iw4:mp_rust": BASE_CONTENT,
    "minecraft:overworld": BASE_CONTENT + ["minecraft-26.3-runtime-data"],
}


class ValidationError(ValueError):
    """An actionable input error whose message does not echo private input."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def exact_keys(value, expected, label):
    require(type(value) is dict, f"{label} must be an object")
    require(set(value) == set(expected), f"{label} has missing or unsupported fields")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON contains a duplicate field")
        result[key] = value
    return result


def reject_constant(_value):
    raise ValidationError("JSON must not contain non-finite numbers")


def finite_float(value):
    parsed = float(value)
    require(math.isfinite(parsed), "JSON must not contain non-finite numbers")
    return parsed


def check_depth(value):
    pending = [(value, 0)]
    while pending:
        item, depth = pending.pop()
        require(depth <= 16, "JSON nesting exceeds 16 levels")
        if isinstance(item, dict):
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)


def read_json(path):
    try:
        with Path(path).open("rb") as handle:
            data = handle.read(MAX_JSON_BYTES + 1)
        require(len(data) <= MAX_JSON_BYTES, "JSON exceeds the 64 KiB limit")
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
        check_depth(value)
        return value
    except (OSError, UnicodeError) as error:
        raise ValidationError("Cannot read a UTF-8 JSON file; check the file and access") from error
    except (json.JSONDecodeError, RecursionError, ValueError) as error:
        if isinstance(error, ValidationError):
            raise
        raise ValidationError("Malformed or excessively nested JSON") from error


def validate_recipe(recipe, lock):
    exact_keys(recipe, {
        "schema_version", "id", "title", "runtime", "world", "movement",
        "combat", "required_content",
    }, "recipe")
    require(type(recipe["schema_version"]) is int and recipe["schema_version"] == 1,
            "schema_version must be integer 1")
    recipe_id = recipe["id"]
    require(type(recipe_id) is str and len(recipe_id) <= 64
            and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", recipe_id) is not None,
            "id must use lowercase letters/digits and single separating hyphens (1–64 characters)")
    title = recipe["title"]
    require(type(title) is str and 1 <= len(title) <= 120 and bool(title.strip())
            and not any(unicodedata.category(char).startswith("C") for char in title),
            "title must be 1–120 characters with no control characters")
    exact_keys(recipe["runtime"], {"id", "commit"}, "runtime")
    expected_runtime = {key: lock["runtime"][key] for key in ("id", "commit")}
    require(recipe["runtime"] == expected_runtime, "runtime must match the pinned catalogue revision")
    world = recipe["world"]
    require(type(world) is str and world in CONTENT_BY_WORLD, "world is not in the candidate catalogue")
    require(recipe["movement"] == ["on-foot", "skate"], "movement must be on-foot followed by skate")
    require(recipe["combat"] == "mw2-default", "combat must use mw2-default")
    require(recipe["required_content"] == CONTENT_BY_WORLD[world],
            "required_content must match the world's ordered prerequisite identifiers")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe", type=Path, help="candidate recipe JSON file")
    args = parser.parse_args(argv)
    try:
        lock = read_json(LOCK_PATH)
        validate_recipe(read_json(args.recipe), lock)
    except (ValidationError, KeyError, TypeError) as error:
        message = str(error) if isinstance(error, ValidationError) else "Catalogue lock is invalid"
        print(f"error: {message}", file=sys.stderr)
        return 1
    print("Recipe metadata accepted. Gameplay, local prerequisites and rights remain unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
