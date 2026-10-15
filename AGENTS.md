# Combine

Work from the owner's current request. The previous workflow and backlog are
retired; historical plans do not select or authorize new work.
Preserve the existing implementation and local changes.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues (Jpatching/combine). See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `GLOSSARY.md` and `docs/adr/`. See `docs/agents/domain.md`.

## Project reference

- Start/resume: the selected issue; for GTA, [#61 current summary](https://github.com/Jpatching/combine/issues/61) and [#20 acceptance](https://github.com/Jpatching/combine/issues/20).
- Fortnite + Skate requirements: [interactive-world contract](docs/FORTNITE_SKATE.md).
- Purpose and entry points: [README](README.md).
- Parked Synergy: [menu guide](docs/TRICKSHOT_MENU.md); actual pinned GSC.
- Baseline recovery: [Windows runbook](docs/WINDOWS_BASELINE.md).
- Decisions: [host rationale](docs/adr/0001-preserve-offline-gta-gameplay.md); consult `docs/adr/` for the affected experience.
- Source/release identities: [pins](research/upstream.lock.json); refresh does not move pins.

Repository gate: `python3 scripts/verify.py` (`py -3 scripts/verify.py` on Windows).
Runtime changes need relevant runtime checks. Preparation, launch, gameplay,
verification, owner acceptance and release are distinct evidence claims.

Keep GTA IV in windowed mode throughout runtime testing. Confirm window mode
during preflight and after each restart; retain foreground and input-ownership
safeguards.

Keep game assets, converted data, identities, secrets, recordings, private logs
and settings outside Git and AI uploads. Preserve original installs and builds;
isolate runtime copies/caches/profiles. Review plugins/scripts before use.
No DRM/anti-cheat bypass. Source licences do not establish asset/publisher rights.
Recipes remain strict data, never executable commands, paths or download URLs.
No universal merger, new engine, marketplace or production launcher is authorized.
Spending, outreach, redistribution, launch, deployment and release need task authority.
