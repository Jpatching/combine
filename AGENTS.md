# Combine

Combine puts the existing Skate simulation into offline GTA IV: mount where you
stand, ride on GTA's own ground, dismount back to ordinary GTA. Start from the
selected open GitHub issue.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues (Jpatching/combine). See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.

## Working loop

- Tight loop: `python3 tools/gtaiv-skate/check.py` (seconds, no game). Build
  behaviour test-first in its harness; run the game once per slice, at the end.
- Cut each new branch from a freshly fetched `origin/main`.
- Gate before every PR: `python3 scripts/verify.py`.
- Report source checks, runtime observation and owner acceptance as separate claims.

## Guardrails

- Game assets, converted data, recordings, private logs and settings stay local,
  outside Git and AI uploads.
- Original installs and builds stay untouched; run from isolated copies.
- Use locally owned, unprotected setups; DRM and anti-cheat stay intact.
- Spending, outreach, redistribution, deployment and release need explicit owner authority.
