# Existing branch reconciliation — 2026-10-07

## Verified snapshot and scope

Inventory before the D-033 documentation commit. Git fetch succeeded; GitHub
reported PR #1 open with head `slice/separate-mashup-qualification`.
Main: `a5593d671142f31653d45caeaad7b926d40ff855`.
Published workflow tip: `4a366cb537da2c9eb6d3be2269b0eebe5eb8d2b1`.
There are 25 local branches and 10 remote branches including main. The workflow
branch contains 25 commits beyond main across 40 files. No backlog merge or branch
deletion is performed by this inventory. This is source evidence, not a second
status board. Routine merge authority is recorded in D-033.

Commands: `git fetch origin`, `git for-each-ref`, `git worktree list`,
`git rev-list --count <branch> --not --remotes=origin`,
`git cherry origin/slice/fortnite-workflow-reset <branch>`,
`git log origin/main..HEAD`, `git diff --stat origin/main...HEAD`,
and `gh pr list --state open`. Remote refs were refreshed before comparing.

## Branch inventory

Unpublished counts overlap; do not add them. A published ancestor is not necessarily
merged into main. A cleanup candidate is not permission to discard unique history.

| Local branch | Snapshot tip | Disposition |
|---|---|---|
| `chore/original-matt-skills` | `064f65f` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `chore/resume-summary` | `ad8b793` | 1 unpublished ancestry commits; retain for reconciliation |
| `docs/branch-reconciliation` | `a5593d6` | Tip contained in published history; cleanup candidate after dependency/link checks; attached worktree |
| `docs/process-interview` | `86a2c6e` | 6 unpublished ancestry commits; retain for reconciliation |
| `docs/project-orientation` | `397f535` | 2 unpublished ancestry commits; retain for reconciliation |
| `fix/skate-rail-validation` | `b45d878` | Tip contained in published history; cleanup candidate after dependency/link checks; attached worktree |
| `main` | `a5593d6` | Matches origin/main; retain |
| `slice/core-client-qualification` | `f0d1fac` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-12-41-original-client` | `6769987` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-12-41-preparation` | `6769987` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-adapter-architecture` | `6a0ffd8` | 11 unpublished ancestry commits; retain for reconciliation |
| `slice/fortnite-guidance-qualification` | `3482d4d` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-input-diagnosis` | `d4ebf87` | 3 unpublished ancestry commits; retain for reconciliation |
| `slice/fortnite-input-export` | `b399c55` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-interactive-qualification` | `be8d3b8` | 11 unpublished ancestry commits; retain for reconciliation |
| `slice/fortnite-loading-gate` | `93f4b0c` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-reader-witness` | `93f4b0c` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-reuse-qualification` | `70f3519` | 10 unpublished ancestry commits; retain for reconciliation |
| `slice/fortnite-same-process` | `02d3b8a` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-skate-connection` | `e7642dd` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/fortnite-workflow-reset` | `4a366cb` | Current workflow branch; 25 inherited commits beyond main; retain |
| `slice/hide-hud` | `b7aed59` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/intervention-review` | `3f2e70d` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/separate-mashup-qualification` | `b399c55` | Tip contained in published history; cleanup candidate after dependency/link checks |
| `slice/synergy-input-isolation` | `a5593d6` | Tip contained in published history; cleanup candidate after dependency/link checks |

## Unpublished history accounted for

Seven branches have ancestry absent from every origin branch: 22 distinct commits
in total. Comparing patch identity and trees against matching published changes
shows alternate histories, not 22 independent unshipped features. Subject matches
were only candidate selection; tree diffs established the following differences:

- `chore/resume-summary`, `docs/project-orientation` and
  `slice/fortnite-input-diagnosis`: published counterparts replace machine-specific
  example paths with portable placeholders. No unique runtime code found.
- `docs/process-interview` and `slice/fortnite-reuse-qualification`: also retain
  an older process-interview document and its nine-line handoff pointer.
- `slice/fortnite-interactive-qualification` at `be8d3b8` versus published
  `76a0383`: four differing documents, comprising that interview/pointer and two
  path substitutions; all other tree contents match.
- `slice/fortnite-adapter-architecture` at `6a0ffd8` versus published `76a0383`:
  only the interview document and handoff pointer differ; all other tree contents
  match. The interview records earlier recommendations and owner follow-up about
  research limits and Intervention source already present in main. It is historical
  evidence, not adopted replacement requirements.

Preserve all seven branch refs for now. Proposed disposition: retain a redacted,
clearly historical copy of the interview in the documentation archive, repair its
links and review the preservation diff. Then verify coverage of each unique commit
before any deletion. Do not republish machine-specific paths or blindly merge
alternate histories merely to make ancestry counts zero.

Local `slice/fortnite-same-process` is two commits ahead of its same-named remote,
but both are already in the published workflow branch. Likewise, several branch
names have no same-named remote even though their complete ancestry is published.
These are not unpublished source. `slice/separate-mashup-qualification` locally
still points to `b399c55`; its remote/PR #1 includes the rail fix at `b45d878`.
Three worktrees are attached: the workflow branch, rail-fix branch and
branch-reconciliation branch. Inspect each before cleanup; none was removed.

## Proposed backlog merge order — separate authorization required

1. Review PR #1 at `b45d878ae6770e686f323014488a925becf0e119` against main.
   The [prior review](2026-10-06-pr1-review.md) found a rail arithmetic defect;
   the [fix evidence](2026-10-06-rail-validation-fix.md) records its correction
   and 15 passing focused native tests. Do not repeat the stale claim that the
   defect remains unfixed. Refresh the PR, review the fix and verify the exact
   candidate before proposing merge. Broader native missing-test debt remains
   explicit; these historical results are not a new full-diff approval.
2. Keep the workflow branch visible as a draft PR targeting main and depending
   on PR #1. Review its remaining diff after PR #1's disposition. It contains
   qualification research, the parked exporter, source metadata and workflow
   changes; it does not establish a playable integration. Exporter rebuild and
   analyzer debt require explicit review disposition. Review/check the final
   head/base, then request the owner's backlog merge authorization.
3. Preserve the historical interview as described above. After authorized merges,
   synchronize local main and clean up redundant local/remote refs only after
   containment, worktree and durable-reference checks. Existing global rules and
   shared skill installation are outside this correction.

The workflow policy correction is reviewed separately against `4a366cb`, not
against main's entire inherited backlog. Passing its documentation gate cannot
approve either backlog PR. Next action is exact-head backlog review, starting
with PR #1; the Fortnite input blocker is a separate gameplay prerequisite.
