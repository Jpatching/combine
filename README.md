# Combine — GTA IV with Skate

Combine connects offline GTA IV's world and ordinary gameplay to the existing
Skate simulation. The intended path is:

```text
GTA world → correctly placed collision → Skate movement and solved pose
                                              ↓
                                   GTA character and board
```

GTA supplies the supporting floor. The adapter supplies qualified collision and
riding input to Skate, then applies the resulting position and heading in GTA.
Solved board presentation and GTA-character animation are further requirements;
the current character is a visual placeholder. Dismounting must restore ordinary
GTA movement, camera and vehicle use. Correct collision at one location does not
establish coverage elsewhere.

For the active candidate, verified behavior, blocker and next experiment, read
[the handoff](docs/HANDOFF.md). This is experimental source, with no game files,
playable download or installer. Source checks, runtime evidence and owner
acceptance are separate claims.

## Controls and local trials

The adapter defaults to keyboard/mouse: **F6** mounts/dismounts, **W** pushes,
**A/D** steer and the mouse orbits the chase camera. While dismounted and idle,
**F5** selects keyboard/mouse or controller mode; controller riding uses A/X push
and left-stick steering. See the [adapter guide](tools/gtaiv-skate/README.md)
for prerequisites, limits and runtime checks.

Use the [workbench guide](docs/WORKBENCH.md) for private visual evidence and
runtime monitoring, and the [reproduction guide](docs/REPRODUCING.md) for source
checks and private-trial preparation. Preserve original installations and use
isolated runtime copies with lawfully available local data.

## Parked experiences

- MW2 Rust and Minecraft mashups: [Windows baseline/recovery](docs/WINDOWS_BASELINE.md).
- Original Synergy trickshot menu: [menu guide](docs/TRICKSHOT_MENU.md) and
  [controls/checklist](templates/synergy-checklist.txt).
- Interactive Fortnite island with Skate: [requirements](docs/FORTNITE_SKATE.md).

## Source and checks

```sh
python3 scripts/verify.py
python3 tools/gtaiv-skate/check.py
```

Use `py -3` on Windows. These checks do not establish gameplay acceptance.
For an authorized isolated coding task, see the [Sandcastle guide](tools/sandcastle/README.md).
Source identities live in [pins](research/upstream.lock.json); retained decisions
are in [the decision log](docs/DECISIONS.md) and [ADRs](docs/adr/0001-preserve-offline-gta-gameplay.md).
Build/patch procedures remain in the [patch guide](patches/README.md).
Synergy attribution and credits remain in its [GPLv3 record](licenses/Synergy-GPL-3.0.md).
Keep assets, converted data, settings, recordings and private logs outside Git.
Source licences do not settle asset rights or publisher terms.
