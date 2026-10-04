# Combine project instructions

Global collaboration defaults apply. Read README.md and BACKLOG.md first.
The private Combine GitHub Project is the status authority; Git is the source
authority. BACKLOG.md is the historical record and board pointer. Do not
claim a commit, remote, gameplay result, acceptance or release without evidence.
Record consequential decisions in docs/DECISIONS.md.

## Agent skills

Use the globally installed `$matt-workflow` for substantial work, resuming the
current phase. Small fixes stay lightweight. Read [workflow guidance](docs/WORKFLOW.md).
The selected plan and existing contracts satisfy settled setup/design choices;
do not restart settled discussions. D-015 records the owner's correction:
execute the actual pinned Synergy GSC menu through the existing runtime engine,
with its own presentation and options. A native imitation is not the replacement.
The destination also includes the agreed trickshot hit radius, without Combine
practice additions. The menu guide owns requirements; its earlier native C-016
mechanism is historical where superseded by D-015. Resume the same board item's
next missing integration/check.

### Issue tracker

Private [Combine Project](https://github.com/users/Jpatching/projects/5/views/4),
using draft items and explicit dependencies. See [tracker configuration](docs/agents/issue-tracker.md).
Board maintenance is authorized; source publication and CI/CD remain separate.

### Domain docs

Use the existing player/menu guides and `docs/DECISIONS.md`. See
[domain configuration](docs/agents/domain.md); do not create parallel authorities.

## Current slice and references

Validate ordinary Windows players configuring, launching and sharing supported
MW2/Skate/Minecraft mashups. The current slice integrates Synergy itself;
automated Intervention navigation/equip is observed, with input, presentation
and owner gameplay evidence still required. Hide HUD
is deferred and blocks no active work. Baseline reproduction remains incomplete.
No universal merger, new engine, marketplace or production launcher is authorized.

- README.md owns the player overview, controls and limitations.
- docs/TRICKSHOT_MENU.md owns menu build, trial and acceptance procedures.
- docs/WINDOWS_BASELINE.md owns baseline gameplay/recovery checks.
- research/results/ owns redacted evidence; docs/HANDOFF.md points to the latest.
- research/upstream.lock.json pins the supported source/release and menu source.

## Project-specific boundaries

Keep game assets, converted data, secrets, identities, OBS/recordings, private logs
and local settings outside Git. Never upload game files or private logs to AI
services. Preserve original installations; isolate runtime copies, caches and
profiles. Redact shared diagnostics.

Review source licences, asset rights and publisher terms separately. Open source
or ownership of a game does not grant blanket distribution/commercial clearance.
Do not implement DRM/anti-cheat bypasses or run unreviewed plugins/scripts.
Publishing, redistribution, spending and outreach need task-specific authority.
D-016/D-017 record reviewed source-branch publication to Jpatching/combine before
menu acceptance. Keep assets/private data excluded; verify remote commit and board
read-back. Owner acceptance, merge and release remain separate. Reversible local
work on the selected menu-then-Fortnite plan is authorized.

Recipes remain strict data, never shell commands, paths or download URLs. Reuse
verified upstream capabilities; each new integration needs its own evidence.
Separate checking, preparation, launch, gameplay and owner acceptance. The Python
recipe checker performs research validation only.

## Verification and coordination

Record observation date, source URL/revision, commands, results and reproduction.
Distinguish documented, source-inspected, reproduced and unverified behavior;
archive hashes/builds/synthetic fixtures do not prove play. Record contradictory
upstream documentation. Refresh upstream refs at handoff without moving the pin.

Full repository gate: `python3 scripts/verify.py` (Windows: `py -3 scripts/verify.py`).
Focused Python checks: `python3 -m unittest discover -s tests -v`.
Run the full gate once at handoff; repeat only after relevant changes/failures.
Menu Rust/native-render checks are in docs/TRICKSHOT_MENU.md. Windows gameplay
uses the baseline runbook and templates/baseline-result.md. Build upstream only
when needed, recording exact tools; upstream's moving `stable` is not a pin.

Use one lead/writer. D-017 authorizes bounded read-only helpers selected through
the shared routing policy; docs/AGENT_ROLES.md supplies project task briefs. Use at
most two helpers when independent work justifies them; follow stricter session
restrictions. Research agents cannot declare legal clearance. Finish with evidence, remaining limitations and
one concrete next step, distinguishing implementation, verification, acceptance
and release. Preserve unrelated work and keep explanations proportional.
