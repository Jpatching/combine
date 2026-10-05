# Combine issue tracker

The private [Combine Project](https://github.com/users/Jpatching/projects/5/views/4)
is the sole active status authority, verified and migrated October 4, 2026.
BACKLOG.md is a frozen historical record and pointer. Git owns source; there is
a public source remote at https://github.com/Jpatching/combine. Verify the remote
branch SHA before claiming a source revision was pushed. Private draft items do not publish source.

- Open Now, read the active draft, phase, current skill, phase exit, next action
  and evidence checklist. Refresh before handoff. Milestones and Needs you give
  the wider outcome and owner decisions. Keep one Codex implementation slice active;
  a wayfinding map/current decision and pending owner trials may also be visible in Now.
- Preserve C-identifiers. The 17 migrated drafts retain open/deferred outcomes;
  C-018 names the earlier pending full-library inventory request. Completed old
  C-001/C-002/C-004 and the earlier workflow setup remain historical evidence.
- `to-spec` updates docs/TRICKSHOT_MENU.md for menu requirements and links the
  draft. `to-tickets` finalises independently demonstrable slices with explicit
  dependencies. Drafts lack native issue dependency/subissue links, so their
  bodies use named draft links for Blocked by and parent relationships.
- Read the current card alongside requirements, latest owner corrections and exact
  evidence. Reconcile stale ordering before choosing one missing decision/check.
  Historical native mechanisms never supersede D-015 actual-GSC execution.
  Preserve pending trials and incomplete requirements when reprioritizing work.
- Update the board at meaningful phase changes and read back changes. If unavailable,
  report sync pending and preserve intended changes in docs/HANDOFF.md. Do not
  maintain a second local status list or claim failed writes landed.
- The global router's GitHub reference and helper live under
  `~/.codex/skills/matt-workflow/` and `~/.codex/workflows/solo-development/`.
  Local requirements, decisions and technical evidence stay in their existing docs.
- The extra roadmap view (View 5) is preserved. The shared helper validates the
  three required views while allowing extras; use its `update --body-file` with
  read-back for routine updates. Start/Target date fields exist; starts are stamped
  once on implementation. Targets remain blank. Roadmap date mapping needs a UI
  check; the available API exposes no start/target mapping fields.
- Tests/builds establish only their coverage. Owner acceptance is explicit;
  reviewed source-branch publication to Jpatching/combine is authorized by D-016/D-017
  before acceptance; merge and release remain separate.
  Check current task-specific commit/push authority and the branch workflow in
  docs/WORKFLOW.md; October 6 owner steering resumes local checkpoints. Board maintenance does
  not authorize source publication, assets/logs,
  spending, outreach or CI/CD. Use one lead/writer and the bounded helper policy
  recorded in D-017 and docs/AGENT_ROLES.md.

## Wayfinding operations

Use private draft items on this same Project. A map uses Kind Milestone and a
`wayfinder:map` marker in its body; decision children use Kind Decision and
`wayfinder:research`, `wayfinder:grilling` or `wayfinder:task` in their bodies.
Drafts lack labels/native subissue or blocking relationships, so bodies carry
named Parent / Blocked by links. These markers are conventions, not GitHub labels.
The lead is the sole writer; claim with `Claimed by: Codex lead` before work.
Query drafts by their Parent link to find open children, then check named blockers
and claim. Record resolution in the child body (drafts have no issue comments),
set Status Done and add a named context pointer to the map. No copied task list
in BACKLOG. Pending decisions stay Todo/In Progress, not silently answered.
Preserve views/fields; the live Needs you filter and additional visible columns
may differ from the helper's installation template. Validate live configuration
and read back writes without resetting it to defaults.
