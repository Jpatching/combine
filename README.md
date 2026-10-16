# Combine

Combine puts the existing Skate simulation into offline GTA IV: mount where you
stand, ride on GTA's own ground, dismount back to ordinary GTA. Game data and
private trials stay local.

```sh
python3 tools/gtaiv-skate/check.py   # tight loop: riding checks, no game
python3 scripts/verify.py            # gate before every PR
```

- Riding source: [`tools/gtaiv-skate/`](tools/gtaiv-skate/README.md).
- [Agent instructions](AGENTS.md), [glossary](GLOSSARY.md) and [surface decision](docs/adr/0004-live-host-queries-supply-riding-surfaces.md).
- Current work: open GitHub issues.

[Source pins](research/upstream.lock.json), [patches](patches/README.md) and
[licences](licenses/Synergy-GPL-3.0.md) identify retained third-party sources.
Source licences do not grant game-asset or publisher rights.
