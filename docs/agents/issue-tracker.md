# Combine tracker

The private [Combine Project](https://github.com/users/Jpatching/projects/5/views/8) owns
current status; Git owns source. BACKLOG.md is history and is not startup reading.

The sole default view is **Fortnite + Skate**, grouped by **Work status** in order:
**Ready → Doing → Blocked → Done**. Doing permits one task at most; check its count
before moving a card there. The current destination is C-019 and the sole current
task is C-024. Both are Blocked until matching input is established. The destination
is context, not a second implementation task. Done means the card's stated check
passed; gameplay/owner acceptance need their own explicit evidence.

Read and update the Project directly with GitHub's UI or Projects API (`gh api`).
Do not run the custom seven-phase `projects.py` helper for Combine: its validation
and configuration would restore retired process fields/views. Existing global tools
and Matt's original skills are unchanged.

Each active card has only intended result, acceptance check, current evidence/blocker,
next action and relevant links. Preserve C-identifiers, draft/item IDs and evidence
links. Update after meaningful results, then read back. Keep routine publication SHA
and verification results with the card's evidence or PR instead of another commit.
If GitHub is unavailable, record the failed operation and intended update as sync
pending in the current handoff; do not claim a successful write or revive BACKLOG.

The October 7 reset privately snapshots all 29 items, fields and six prior views
in ignored `.private/workflow-reset/before.json`. It archives 27 items without changing
their bodies, historical statuses or acceptance claims. Synergy/trial, hit radius
and static-world work are inactive, not accepted or completed. Restore an archived
item only when selected. Work status is separate so every old Status/Phase/skill and
other process value remains intact; those fields are hidden and no longer maintained.
Previous view configurations are retained in the snapshot, not as active process views.

Board maintenance is authorized. Source publication follows [workflow](../WORKFLOW.md);
assets/private logs, spending, outreach, launch, CI deployment, merge and release
retain their separate boundaries.
