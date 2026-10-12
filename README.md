# Combine — reproducible game mashup experiments in Rust

For one approved coding task in an isolated Docker worker, use the
[Sandcastle operating guide](tools/sandcastle/README.md).

Combine explores separate mashup experiences in the existing MW2 / Skate 3 /
Minecraft runtime. Each experience needs its own preparation and gameplay evidence;
The long-term ambition is a substantial open-source project with reproducible,
separate experiences and contributor-friendly source. Today this is experimental
source, with no game files, playable download or installer. Each new world needs
an independently evidenced integration; the ambition is not a universal merger.

For the selected task, current verdict and next step, start with the
[current context](docs/HANDOFF.md), then fetch its linked live issue. Source checks,
runtime observations and owner gameplay acceptance are separate evidence.

Use the [workbench guide](docs/WORKBENCH.md) for REA and Universal Modder guidance,
terminal views, and private visual evidence tied to acceptance checks.

Start with the [reproduction guide](docs/REPRODUCING.md) for source checks,
the pinned Rust/Synergy build and private-trial prerequisites. Rust is the runtime
implementation language; original GSC remains Synergy's menu source. Python and
PowerShell support validation and Windows trial preparation.

| Experience | What exists | Player route |
| --- | --- | --- |
| Skate on MW2 Rust with MW2 combat | Owner reports skating worked; baseline recovery/replay incomplete | [Windows baseline](docs/WINDOWS_BASELINE.md) |
| Minecraft world with MW2 combat and skating | Owner reports Minecraft worked; skating on changed terrain and replay unverified | [Windows baseline](docs/WINDOWS_BASELINE.md) |
| Actual Synergy trickshot menu in the existing mashup | Original GSC menu integrated; Intervention/input checks recorded; exact-build physical trial unaccepted | [Menu guide](docs/TRICKSHOT_MENU.md), [trial evidence](docs/archive/HANDOFF-2026-10-07.md) |
| GTA IV + Skate | Candidate on [PR #23](https://github.com/Jpatching/combine/pull/23); complete repeatable riding remains unaccepted | [Current context](docs/HANDOFF.md) |
| Interactive Fortnite island + Skate | Gameplay base/client/bridge qualification; building/editing/destruction required; no playable integration | [Contract](docs/FORTNITE_SKATE.md) |

Recipes are strict research metadata. The Python checker does not prepare or
launch these experiences. Unfinished preparation scaffolding is not playable progress.

## Parked Synergy trial

The [menu guide](docs/TRICKSHOT_MENU.md) contains controls and the retained
contract. The [archived trial](docs/archive/HANDOFF-2026-10-07.md) is historical
evidence. Resume this experience only when the owner selects it.

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
