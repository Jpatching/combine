# Combine

Combine is an investigation into making supported game mashups easy to configure,
play and share. The first candidate is the existing MW2/Skate 3/Minecraft runtime.
The business hypothesis is that reliable compatibility and shareable configurations
can remove enough friction to bring players back and attract creators.

**Current status: research foundation and offline recipe validation implemented.**
There is no Combine launcher or website yet. No upstream gameplay has been tested
here, no participants have been interviewed, and distribution rights are unresolved.

```text
Discover example -> choose supported configuration -> check compatibility
                                                       | invalid
                                                       +-> explain missing requirement
                                                       | valid
                                                       v
                                    prepare isolated profile -> launch locally
                                                       |
                                                 share recipe
```

The intended hub handles discovery and sharing; a future local companion handles
files and launch. Only recipe/metadata checks are implemented now. Recipes describe
already integrated capabilities; they do not merge arbitrary games.

## Start here

1. Read [research and limitations](docs/RESEARCH.md).
2. Follow the [Windows baseline runbook](docs/WINDOWS_BASELINE.md).
3. Work from the [local backlog](BACKLOG.md); use the [handoff](docs/HANDOFF.md) to resume.
4. Use the [player/creator study](docs/VALIDATION.md) after a usable baseline exists.

Python 3.10+ is needed only for this research tooling. It needs no extra packages,
network access, game files or accounts. Players using the upstream release do not
need Python or Rust.

```sh
python3 scripts/verify.py
python3 scripts/check_recipe.py recipes/mw2-skate.json
python3 scripts/check_recipe.py recipes/minecraft-skate.json
```

On Windows, replace `python3` with `py -3`. Success means the research recipe matches
the pinned catalogue, not that games are installed, licensed, safe or playable.
Invalid input produces a short error and nonzero exit status. These commands do
not download, prepare, modify or execute game files.

## Project map

| Artifact | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Project instructions layered over global Codex defaults |
| [Agent roles](docs/AGENT_ROLES.md) | Bounded research, runtime and review responsibilities |
| [Decisions](docs/DECISIONS.md) | Scope, effort budget and continue/change/stop decision |
| [Recipe contract](docs/RECIPE.md) | Minimal configuration interface and two candidates |
| [Upstream lock](research/upstream.lock.json) | Source/release pin, publisher hash and evidence status |
| [Baseline result template](templates/baseline-result.md) | Hardware, timings, outcomes and failure evidence |

## Boundaries

Keep private runtime files and participant records in ignored `.private/` or outside
this repository. `.gitignore` reduces accidental staging; it does not authorize
redistribution or prevent deliberate force-adds. Share only redacted observations
and recipes. Do not upload game assets or private paths in support reports.

The target is a solo, small-budget, Windows-first study with a ten-working-day effort
budget, plus time for participant responses. No paid infrastructure, public services,
multiplayer hosting, payments or arbitrary game imports are part of this milestone.
This repository does not grant rights to upstream projects or game content.
