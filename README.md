# Combine — reproducible game mashup experiments in Rust

For one approved coding task in an isolated Docker worker, use the
[Sandcastle operating guide](tools/sandcastle/README.md).

Combine explores separate mashup experiences in the existing MW2 / Skate 3 /
Minecraft runtime. Each experience needs its own preparation and gameplay evidence;
The long-term ambition is a substantial open-source project with reproducible,
separate experiences and contributor-friendly source. Today this is experimental
source, with no game files, playable download or installer. Each new world needs
an independently evidenced integration; the ambition is not a universal merger.

**Current outcome: Fortnite + Skate.** No playable integration exists. The
[current experiment](https://github.com/Jpatching/combine/issues/4) owns the next
native one-surface proof and its prerequisites. Other work,
including Synergy's unaccepted trial and unimplemented hit radius, is parked.
See the [current handoff](docs/HANDOFF.md) for retained evidence and the fresh-start status.

Start with the [reproduction guide](docs/REPRODUCING.md) for source checks,
the pinned Rust/Synergy build and private-trial prerequisites. Rust is the runtime
implementation language; original GSC remains Synergy's menu source. Python and
PowerShell support validation and Windows trial preparation.

| Experience | What exists | Player route |
| --- | --- | --- |
| Skate on MW2 Rust with MW2 combat | Owner reports skating worked; baseline recovery/replay incomplete | [Windows baseline](docs/WINDOWS_BASELINE.md) |
| Minecraft world with MW2 combat and skating | Owner reports Minecraft worked; skating on changed terrain and replay unverified | [Windows baseline](docs/WINDOWS_BASELINE.md) |
| Actual Synergy trickshot menu in the existing mashup | Original GSC menu integrated; Intervention/input checks recorded; exact-build physical trial unaccepted | [Menu guide](docs/TRICKSHOT_MENU.md), [trial evidence](docs/HANDOFF.md) |
| Interactive Fortnite island + Skate | Gameplay base/client/bridge qualification; building/editing/destruction required; no playable integration | [Contract](docs/FORTNITE_SKATE.md) |

Recipes are strict research metadata. The Python checker does not prepare or
launch these experiences. Unfinished preparation scaffolding is not playable progress.

## Parked Synergy trial

Use the versioned review folder and shortcuts identified in the
[archived trial handoff](docs/archive/HANDOFF-2026-10-07.md): **Test Synergy**, **Open trial files** and
**Read checklist**. Players need a separately prepared lawful local Windows
runtime and game data; preserve original installations and use isolated copies.
The [actual Synergy checklist](templates/synergy-checklist.txt) owns this trial's
controls and physical input checks (default bindings below; prompts reflect remaps).

| Action | DualSense | Keyboard / mouse |
| --- | --- | --- |
| Open | Hold L2 + press R3 (Aim + Melee) | Hold right mouse + press V |
| Up / down | L2 / R2 (Aim / Fire) | Right / left mouse |
| Select | Square (Use) | E |
| Back; close at root | R3 (Melee) | V |
| Sliders | L1 / R1 (Tactical / Frag) | G / F |

Release the opening chord before navigating. Choose Weapon Options → Give
Weapons → Sniper Rifles → Intervention. Menu capture should block gameplay;
after closing, return all controls to neutral before freshly firing on foot.
Physical close/reopen, focus/reconnect and quit/relaunch still require the owner
trial. Other original sections are visible; their effects are not verified.

The destination is actual pinned Synergy plus the agreed sniper near-pass hit
radius, without Combine practice additions. **Hit radius was selected first for the menu**, per [D-019](docs/DECISIONS.md#d-019-hit-radius-first-and-resume-reconciliation--2026-10-05).
The later request starts Fortnite-with-Skate wayfinding: Fortnite’s interactive world and
Skate movement, tricks and grinds, with no MW2 combat or Synergy in that experience. Hit radius is not implemented: Off by default, first enable 0.25 metres, steps to 5 metres,
Normal/One-shot damage after ordinary cover/reach qualification. The
[menu guide](docs/TRICKSHOT_MENU.md) owns the complete contract.
Rainy remains a research candidate with IW4x/Bot Warfare and function-replacement
compatibility gaps reported by the preceding investigation; it has not been
installed, launched or gameplay-tested and does not replace Synergy.

## Source, checks and history

The existing implementation is retained. PRs #1 and #2 are closed, and the
previous workflow and backlog are retired. New work starts from the owner's
request. The [current handoff](docs/HANDOFF.md) records the retained evidence.
The [workspace tour](research/results/2026-10-06-workspace-orientation.md)
explains source, scripts and private trials.

```sh
python3 scripts/verify.py
python3 scripts/check_recipe.py recipes/mw2-skate.json
```

Use `py -3` on Windows. These are offline research/input checks, not gameplay.
Developer pins, patches, build and review procedures are in the
[menu guide](docs/TRICKSHOT_MENU.md) and [patch guide](patches/README.md).
Synergy by SyndiShanX is pinned in [source metadata](research/upstream.lock.json),
with its M203 / Xeirh and Apparition Structure Team credits and
[GPLv3 attribution](licenses/Synergy-GPL-3.0.md).

The earlier native practice controls and previews are preserved in the menu
guide's historical appendix and [October 3 evidence](research/results/2026-10-03-synergy-menu.md).
Audio work and private highlight exports are recorded in
[the audio evidence](research/results/2026-10-03-skate-audio-highlights.md).
They are separate earlier trials and are not current Synergy instructions.

No universal merger, marketplace, production launcher, public-match assistance
or firing while skating is authorized. Keep game assets, converted data, settings,
recordings and private logs outside Git. Source licences do not settle asset
rights or publisher terms. Owner acceptance, source publication, merge and release
remain separate.
