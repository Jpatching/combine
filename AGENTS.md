# Combine

## Objective and current milestone

Validate whether ordinary Windows players can configure, launch and share
supported game mashups without editing code. The owner is working solo with
Codex on a small budget. Start with the existing MW2/Skate/Minecraft ecosystem.
The current milestone is research and baseline reproduction, not a universal
merger, new engine, marketplace or production launcher.

Read README.md and BACKLOG.md first. BACKLOG.md is the authoritative local issue
tracker until a remote tracker is deliberately adopted. Record consequential
decisions and milestone outcomes in docs/DECISIONS.md. Git is the code source
of truth; do not claim a commit or remote exists without checking.

## Evidence

- Record URLs, observation dates, exact source revisions and reproduction steps.
- Distinguish documented, source-inspected, reproduced and unverified behaviour.
- A successful build or matching archive hash does not establish playable behaviour.
- Keep upstream claims separate from our measurements. Record contradictory docs.
- Pin supported versions in research/upstream.lock.json. Refresh upstream refs at
  handoff, but never silently replace the selected baseline with the newest build.

## Boundaries

- Keep game assets, converted data, secrets and participant identities out of Git.
- Preserve original installations; keep runtime copies, caches and profiles separate.
- Review code licences, asset rights and publisher terms separately. An open-source
  licence or user-owned game is not blanket distribution or commercial clearance.
- Do not implement DRM/anti-cheat bypasses or run unreviewed plugins/scripts.
- Do not publish, redistribute, spend money or contact others without task-specific
  authorization. Read-only research and reversible local work are authorized.
- Never upload game files or private logs to AI services. Redact shared diagnostics.

## Engineering and validation

- Deliver end-to-end vertical slices: one player outcome, the minimum supporting
  layers, explicit failure handling, and observed acceptance evidence. The research
  foundation is preparation, not a completed playable slice.
- Reuse verified upstream capabilities before replacing them. Recipes select
  implemented features; a new game requires a separately tested integration.
- Recipes are strict configuration data, never shell commands, paths or download URLs.
- Separate compatibility checking, preparation and launching. Current tooling only
  checks research data; it does not install or launch a runtime.
- Full local gate: `python3 scripts/verify.py` (Windows: `py -3 scripts/verify.py`).
- Focused checks: `python3 -m unittest discover -s tests -v`.
- Windows gameplay acceptance: follow docs/WINDOWS_BASELINE.md and record results
  using templates/baseline-result.md. Synthetic fixtures do not prove gameplay.
- Do not run an upstream build until that task needs it; record exact toolchain and
  dependencies if building. The selected upstream currently uses moving `stable`.
- Run the full local gate once at handoff; rerun only after relevant changes/failures.

## Coordination and handoff

Use one lead agent by default. docs/AGENT_ROLES.md defines bounded work packages;
it does not configure or automatically spawn agents. Delegate only when requested.
Give each task an output, evidence requirement and completion check; avoid shared
file ownership. Agent research cannot declare legal clearance.

Keep explanations proportional to the task. Handoff must distinguish local tooling
verification, upstream gameplay verification, owner acceptance and release status.
State the next concrete step, prerequisites, exact checks and unresolved limits.
