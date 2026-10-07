# Matt-only setup and accumulated branch cleanup

Observed 2026-10-07. Owner approved using Matt's original skills globally,
installing triage, retaining private Project tracking and reconciling accumulated
work. No game/runtime changes, launches or backlog merges belong to this cleanup.
Source base: `3a8763ddbe265def5b82886dd77a3efe4d940336`.

## Setup

Global AGENTS.md now contains communication preferences and original-skill routing,
without the custom engineering sequence or mandatory source/handoff closure rules.
Original triage installed from `mattpocock/skills`, path `skills/engineering/triage`,
revision `6fd947921b935b7e1e69293a200400f0fdd5c15f`, including its two references and
Codex metadata. Installation used the system skill installer; existing skills were
unchanged. Fresh-turn discovery is distinct from successful file installation.

Combine's previous workflow/agent briefs are historical archives. D-034 supersedes
the process rules while preserving requirements and execution boundaries. Project
routing follows setup-matt-pocock-skills: private draft tracker, lazy single-context
domain docs, five default triage states. The board also has bug/enhancement category
metadata as required by original triage. Both new single-select fields and the
corrected Project description were read back. Existing game cards were not triaged.

## Local work preservation and disposition

Before removal, all Git refs were captured in a complete private bundle, verified
with `git bundle verify`. All tracked/untracked files from the dirty reconciliation
worktree were archived and compared byte-for-byte with the archive; its ignored-file
inventory was empty. The clean rail worktree contained only disposable Python caches
outside tracked files. Both were checked again immediately before removal.

Backups and comparison manifests are ignored under `.private/matt-only/`:
`before-cleanup.bundle`, `refs.txt`, `reconciliation-worktree.tar.gz`,
`reconciliation.patch`, `worktree-comparison.json`, `alternate-comparisons.json`,
`deleted-local-branches.json` and the previous global instructions. They stay local,
not in source publication. To recover a historical branch, inspect
`git bundle list-heads .private/matt-only/before-cleanup.bundle`, then fetch its
specific original ref into a new recovery branch. Extract the worktree archive
into a separate recovery directory, never over an active checkout.

The dirty worktree largely duplicated published documents. Remaining differences
were older process text, missing later metadata/patch documentation and two historical
archives. The process interview and reset handoff are retained under docs/archive;
the interview's original 81-line body matches commit `86a2c6e` exactly. No runtime
implementation was taken from the dirty checkout.

Seven historical branches contained 22 overlapping unpublished ancestry commits.
Tree comparisons against published counterparts confirmed the previously recorded
alternate-history differences: machine-specific example paths, the historical
interview and its handoff pointer. These commits remain recoverable in the bundle;
they were not merged or republished. Full prior analysis remains in
[branch reconciliation](2026-10-07-branch-reconciliation.md).

Removed 22 local branch names and both auxiliary worktrees. Retained:

| Local branch | Reason |
| --- | --- |
| main | Matches origin/main at `a5593d671142f31653d45caeaad7b926d40ff855` |
| slice/separate-mashup-qualification | PR #1; local pointer advanced to published `b45d878ae6770e686f323014488a925becf0e119` |
| slice/fortnite-workflow-reset | PR #2; contains this cleanup and accumulated source |

All 10 remote branches remain available, preserving published references pending
backlog disposition. Three active local branches does not mean their source has
merged: both PRs remain unmerged. The 22 historical commits are private recovery
history, not outstanding feature work on an active branch.

## Verification boundary

Review and final gate results belong on PR #2 and the private tracker with the exact
cleanup commit. Documentation changes cannot approve the inherited runtime diff.
Review PR #1 first, then PR #2's remaining changes; inherited missing native-test,
exporter rebuild and analyzer limitations remain until separately resolved.
Owner authorization is required before either backlog merge. Current game cards
retain the input-integrity blocker; no gameplay acceptance is inferred.
