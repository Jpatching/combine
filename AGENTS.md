# Combine project instructions

Global collaboration defaults apply. Read README.md and BACKLOG.md first.
BACKLOG.md is the local status authority; Git is the source authority. Do not
claim a commit, remote, gameplay result, acceptance or release without evidence.
Record consequential decisions in docs/DECISIONS.md.

## Current slice and references

Validate ordinary Windows players configuring, launching and sharing supported
MW2/Skate/Minecraft mashups. The active bounded slice is the Synergy-derived native
trickshot menu; broader research/baseline reproduction remains incomplete.
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
The current plan permits source publication to Jpatching/combine only after the
owner accepts the replacement menu. Read-only research and reversible local work
within the slice are authorized.

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

Use one lead agent. docs/AGENT_ROLES.md describes bounded work packages, not an
automatic delegation instruction. Delegate only when requested. Research agents
cannot declare legal clearance. Finish with evidence, remaining limitations and
one concrete next step, distinguishing implementation, verification, acceptance
and release. Preserve unrelated work and keep explanations proportional.
