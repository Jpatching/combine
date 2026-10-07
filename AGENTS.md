# Combine

Start with the [current board](https://github.com/users/Jpatching/projects/5/views/8)
and [current handoff](docs/HANDOFF.md): goal, blocker, next action. Git owns source;
the private Project owns status. Read [workflow](docs/WORKFLOW.md) when implementing
or publishing/merging, and [tracker operations](docs/agents/issue-tracker.md) when updating cards.
Historical backlog and archived handoffs are optional evidence, not startup reading.

Load requirements for the selected task only:

- Fortnite + Skate: [interactive-world contract](research/results/2026-10-06-fortnite-adapter-qualification.md).
- Player overview/controls: [README](README.md).
- Parked Synergy: [menu guide](docs/TRICKSHOT_MENU.md); actual pinned GSC, not a native imitation.
- Baseline recovery: [Windows runbook](docs/WINDOWS_BASELINE.md).
- Relevant decisions: [decision log](docs/DECISIONS.md); add consequential owner decisions there.
- Source/release identities: [pins](research/upstream.lock.json); do not move pins during refresh.

Full gate: `python3 scripts/verify.py` (`py -3 scripts/verify.py` on Windows).
Use relevant runtime checks for runtime changes. Checks, preparation, launch,
gameplay, owner acceptance, publication, merge and release are distinct claims.
Record exact revisions, commands/results and redacted evidence; never infer play.

Keep game assets, converted data, identities, secrets, recordings, private logs
and settings outside Git and AI uploads. Preserve original installs and existing
builds; isolate runtime copies/caches/profiles. Review plugins/scripts before use.
No DRM/anti-cheat bypass. Source licences do not establish asset/publisher rights.
Recipes remain strict data, never executable commands, paths or download URLs.
No universal merger, new engine, marketplace or production launcher is authorized.
Spending, outreach, redistribution, launch and release need task authority.
Reviewed source publication and routine PR merges follow the workflow (D-033);
the existing backlog needs separate merge authorization. Verify remote SHA and
board read-back. Preserve unrelated work and published history.
