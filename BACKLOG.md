# Local issue tracker

This file is the status authority. `done` means the stated deliverable exists and
was checked, not owner acceptance or release. There is no remote issue tracker.

| ID | Status | Owner | Work and completion evidence |
| --- | --- | --- | --- |
| C-001 | done | lead | Initialize Git; add project instructions, evidence records and local verification. See docs/HANDOFF.md. |
| C-002 | done | research | Pin v0.4.0 source and release metadata; inspect integration/setup and record contradictions. See research/upstream.lock.json and docs/RESEARCH.md. |
| C-003 | owner preparing prerequisites | owner + runtime | Run the incremental Windows baseline below. Owner reports MW2 downloading and does not own Skate 3. Full acceptance still needs both candidates and 30 minutes of observed gameplay. Windows execution is unavailable in this Linux workspace. |
| C-003a | pending MW2 download | owner + runtime | Verify pinned archive; launch MW2 Rust on-foot with skating declined, exercise movement/combat and restart. Record real Windows results. No IW4x needed. |
| C-003b | blocked on Skate content | owner + runtime | With legitimate extracted Xbox 360 files, enable skating on Rust; exercise transitions, collision and recovery. No suitable local files available yet. |
| C-003c | pending C-003a/b | owner + runtime | Exercise Minecraft overworld with combat/skating, changed collision and replay; finish the full baseline report. Resolve applicable content-acquisition questions first. |
| C-004 | done | lead | Define recipe v1 and two candidate examples; offline checks reject unsupported/executable input. Does not prove runtime support. |
| C-005 | pending C-003 | product | Observe baseline setup friction and compare with proposed guided configuration flow. Document at least one valuable improvement or recommend stopping. |
| C-006 | unresolved | owner + reviewer | Resolve code/converter provenance, asset access and proposed distribution/monetisation rights. Evidence checklist in docs/RESEARCH.md. Blocks public redistribution. |
| C-007 | ready to recruit | owner | Research protocol and recording sheet prepared in docs/VALIDATION.md. Recruit ten players and three creators; no outreach has occurred. |
| C-008 | pending C-003/C-005/C-006 | lead | Specify and implement only the smallest demonstrated usability improvement. Before code, record trigger, interfaces, measurable outcome and acceptance checks. |
| C-009 | pending study | owner + lead | Complete continue/change/stop decision in docs/DECISIONS.md using real results; do not fabricate missing measurements. |

## Effort allocation (budget, not delivery promise)

- Days 1–2: foundation, source inspection, release pin and provenance questions.
- Days 3–4: Windows reproduction and failure matrix; stop early if prerequisites fail.
- Days 5–6: setup observation, recipe-sharing task and smallest guided-flow proposal.
- Days 7–8: owner-run interviews and observed player sessions when prerequisites allow.
- Days 9–10: synthesise evidence and decide; seven-day return observations may finish later.

Do not claim these days were worked merely because materials exist. If a dependency
is unavailable, record the gap and use remaining effort on independent research.
Do not expand scope to make an unsuccessful experiment look successful.

## Delivery after baseline: vertical slices

These are the proposed increments for C-008 if observed friction justifies a companion.
Each crosses only the layers needed for one player outcome; do not build whole UI,
backend or catalogue layers ahead of usable behaviour.

1. **Play one combination:** choose one supported recipe → validate local prerequisites
   → prepare an isolated profile → launch → see a useful error/retry if it fails.
   Done when an eligible novice succeeds unaided and originals remain unchanged.
2. **Return to it:** save the configuration → exit → reopen that same pinned profile.
   Done when settings persist and failed preparation preserves the last good profile.
3. **Share it:** export recipe → another eligible Windows PC checks/imports it → plays
   the same world/modes. Done with no shared game assets, secrets or private paths.

Only then add another configuration or a discovery website. Reassess whether a
companion is needed after the manual baseline; metadata validation does not complete
these player-facing slices. Use the owner checkpoints in docs/AGENT_ROLES.md.
