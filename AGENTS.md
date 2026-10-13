# Combine

Work from the owner's current request; historical plans do not authorize work.
Preserve existing implementation, local changes and original game installations.
Use Matt Pocock's original skills; `ask-matt` selects the flow.

Before edits, after handoff and before commit/push, run
`git rev-parse --show-toplevel`, `git branch --show-current`, `git rev-parse HEAD` and
`git status --short --branch` in the selected worktree. Match its exact directory
and task branch. Reuse an existing task worktree automatically with explicit
command working directories and file paths; a different chat attachment or UI
branch label does not block work. Stop writes if the actual target is wrong,
`main` or detached. Preserve unrelated changes; never force-switch or reset them.

- Start/resume: read [handoff](docs/HANDOFF.md), current issue requirements and
  relevant latest evidence. Fetch older comments only to resolve a specific uncertainty.
- Tracker/publication operations: read [slice conventions](docs/agents/issue-tracker.md).
- Triage: read [label mapping](docs/agents/triage-labels.md).
- Exploration: read [domain rules](docs/agents/domain.md).
- Runtime trials: read the [adapter guide](tools/gtaiv-skate/README.md) and
  [workbench guide](docs/WORKBENCH.md); recovery uses the [Windows runbook](docs/WINDOWS_BASELINE.md).
- Task boundary: follow [context maintenance](docs/agents/current-context.md).

Run `python3 scripts/verify.py` (`py -3 scripts/verify.py` on Windows).
Runtime changes also need relevant runtime checks. Preparation, launch, gameplay,
owner acceptance, merge and release are separate evidence claims.
Keep GTA IV windowed; verify this before input and after every restart. Retain
foreground and input-ownership safeguards.

Keep assets, converted data, identities, secrets, recordings, private logs and
settings outside Git and AI uploads. Isolate runtime copies/caches/profiles;
review plugins/scripts before use. No DRM/anti-cheat bypass. Source licences do
not establish asset/publisher rights. Recipes are strict data, never executable
commands, paths or download URLs. No universal merger, new engine, marketplace
or production launcher is authorized. Spending, outreach, redistribution,
launch, deployment and release need task authority.
