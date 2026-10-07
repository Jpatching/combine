# Combine

Work from the owner's current request. The previous workflow and backlog are
retired; historical plans do not select or authorize new work.
Preserve the existing implementation and local changes.

## Agent skills

Use Matt Pocock's original skills; `ask-matt` selects the appropriate flow.

### Issue tracker

New specs and tickets use Jpatching/combine GitHub Issues. Before repository edits
(including documentation), resuming work or tracker operations, read
[workspace and slice conventions](docs/agents/issue-tracker.md).

### Triage labels

Use Matt's five default labels. Before triage, read the [label mapping](docs/agents/triage-labels.md).

### Domain docs

Use a root glossary and `docs/adr/`, created when needed. Before exploration,
read the [domain documentation rules](docs/agents/domain.md).

## Project reference

- Current status and evidence: [handoff](docs/HANDOFF.md); fetch the linked live issue before resuming its task.
- Fortnite + Skate requirements: [interactive-world contract](docs/FORTNITE_SKATE.md).
- Player overview/controls: [README](README.md).
- Parked Synergy: [menu guide](docs/TRICKSHOT_MENU.md); actual pinned GSC.
- Baseline recovery: [Windows runbook](docs/WINDOWS_BASELINE.md).
- Historical technical decisions: [decision log](docs/DECISIONS.md).
- Source/release identities: [pins](research/upstream.lock.json); refresh does not move pins.

Repository gate: `python3 scripts/verify.py` (`py -3 scripts/verify.py` on Windows).
Runtime changes need relevant runtime checks. Preparation, launch, gameplay,
verification, owner acceptance and release are distinct evidence claims.

Keep game assets, converted data, identities, secrets, recordings, private logs
and settings outside Git and AI uploads. Preserve original installs and builds;
isolate runtime copies/caches/profiles. Review plugins/scripts before use.
No DRM/anti-cheat bypass. Source licences do not establish asset/publisher rights.
Recipes remain strict data, never executable commands, paths or download URLs.
No universal merger, new engine, marketplace or production launcher is authorized.
Spending, outreach, redistribution, launch, deployment and release need task authority.
