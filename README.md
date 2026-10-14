# Combine

Combine connects an existing game's world and ordinary gameplay with the existing
Skate simulation. This repository contains experimental source and reproduction
tools; game data and private trials stay local.

- [Reproduce source checks and builds](docs/REPRODUCING.md).
- [Windows baseline recovery](docs/WINDOWS_BASELINE.md).
- [Synergy controls and requirements](docs/TRICKSHOT_MENU.md).
- [Investigation tools and local evidence viewing](docs/WORKBENCH.md).
- [Agent instructions](AGENTS.md), [glossary](GLOSSARY.md) and
  [host decision](docs/adr/0001-preserve-offline-gta-gameplay.md).

```sh
python3 scripts/verify.py
```

Use `py -3` on Windows. This checks source metadata, recipes, tracked links and
tests; gameplay needs separate runtime evidence and explicit owner acceptance.

Current GTA candidate, evidence, blocker and next action live in
[workflow #61](https://github.com/Jpatching/combine/issues/61).
[Ride #20](https://github.com/Jpatching/combine/issues/20) owns ride acceptance;
[spec #64](https://github.com/Jpatching/combine/issues/64) owns wider GTA riding.
[Fortnite proof #4](https://github.com/Jpatching/combine/issues/4) and the
[interactive-world contract](docs/FORTNITE_SKATE.md) own the separate Fortnite goal.

[Source pins](research/upstream.lock.json), [patches](patches/README.md) and
[Synergy GPLv3 attribution](licenses/Synergy-GPL-3.0.md) identify the retained
sources. Source licences do not establish game-asset or publisher rights.
