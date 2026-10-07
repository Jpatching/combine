# Combine

Use Matt Pocock's original skills for engineering work; `ask-matt` routes requests.
The [private board](https://github.com/users/Jpatching/projects/5/views/8) owns tickets
and current status. [Current context](docs/HANDOFF.md) summarizes the game blocker.

## Agent skills

### Issue tracker

Tickets and specs live as private Project draft cards. Read
[tracker operations](docs/agents/issue-tracker.md) before ticket operations.

### Triage labels

Matt's five default roles map to Project metadata. Read
[triage labels](docs/agents/triage-labels.md) when triaging incoming requests.

### Domain docs

Single-context; read [domain docs](docs/agents/domain.md) when exploring terminology
or recording decisions.

## Project reference

- Fortnite + Skate requirements: [interactive-world contract](research/results/2026-10-06-fortnite-adapter-qualification.md).
- Player overview/controls: [README](README.md).
- Parked Synergy: [menu guide](docs/TRICKSHOT_MENU.md); actual pinned GSC.
- Baseline recovery: [Windows runbook](docs/WINDOWS_BASELINE.md).
- Existing decisions and task authority: [decision log](docs/DECISIONS.md), with D-034 superseding custom process rules.
- Source/release identities: [pins](research/upstream.lock.json); refresh does not move pins.

Full gate: `python3 scripts/verify.py` (`py -3 scripts/verify.py` on Windows).
Runtime changes need relevant runtime checks. Preparation, launch, gameplay,
verification, owner acceptance and release are distinct evidence claims.

Keep game assets, converted data, identities, secrets, recordings, private logs
and settings outside Git and AI uploads. Preserve original installs and builds;
isolate runtime copies/caches/profiles. Review plugins/scripts before use.
No DRM/anti-cheat bypass. Source licences do not establish asset/publisher rights.
Recipes remain strict data, never executable commands, paths or download URLs.
No universal merger, new engine, marketplace or production launcher is authorized.
Spending, outreach, redistribution, launch, deployment and release need task authority.
Existing backlog PRs #1 and #2 still require separate owner merge authorization.
