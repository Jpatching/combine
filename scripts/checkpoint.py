"""Prepare private checkpoint data; never installs, launches or moves a player."""
import json
import math
from pathlib import Path
import re
import uuid


def prepare(point, output):
    value = json.loads(Path(point).read_text())
    if set(value) != {'label', 'position'} or not isinstance(value['label'], str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,40}', value['label']):
        raise ValueError('Invalid checkpoint data')
    position = value['position']
    if not isinstance(position, list) or len(position) != 3 or any(type(x) not in (int,float) or not math.isfinite(x) or abs(x)>100000 for x in position):
        raise ValueError('Invalid checkpoint position')
    value['token'] = uuid.uuid4().hex
    source = Path(__file__).resolve().parents[1] / 'tools/workbench/checkpoint.js'
    script = source.read_text().replace('__CONFIG__', json.dumps(value, allow_nan=False))
    with Path(output).open('x', encoding='utf-8') as file: file.write(script)
    return {'token': value['token'], 'label': value['label'], 'scope': 'preparation only; no runtime action'}
