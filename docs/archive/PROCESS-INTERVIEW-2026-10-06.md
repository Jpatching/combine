> Historical interview, preserved from `86a2c6e50e6007a2f50da97b5373cace052e950a`.
> Current decisions and workflow supersede the open questions below.

# Process interview: closing slices and repeating game integrations

Observation: 2026-10-06. Requested through ask-matt and grill-with-docs.
This is evidence and an open interview, not an adopted policy or another tracker.
Existing game requirements and decisions remain authoritative.

## Verified starting point

- Live board: Fortnite input qualification C-024 is blocked; next runtime check
  is isolated prepared-asset loading for standalone Skate C-025. Synergy's
  physical trial remains separate and pending.
- `git fetch origin` succeeded. Remote main is `a5593d6`; local main is
  `bfcb607`, nine commits behind. Current branch is
  `slice/fortnite-input-diagnosis` at
  `d4ebf876f036182cc6b19e0ff6b13941210781a4`, seven commits above remote main.
- [PR #1](https://github.com/Jpatching/combine/pull/1) is OPEN/MERGEABLE/CLEAN,
  with no attached automated checks and no review decision. Its body explicitly
  says "No merge or release requested." Head is `b399c55`, base is main.
- PR #1 contains four commits and changes 20 files, with 5,537 insertions and
  417 deletions. It includes inherited unfinished preparation scaffolding,
  requirements/documentation and a standalone runtime preparation patch.
- Three later commits continue above that unmerged PR. Four inherited exporter
  files remain untracked; they were not changed or reviewed in this interview.
- Latest handoff records 0/10 Fortnite containers mounted, no world export,
  missing exporter rebuild cache and an inherited broad runtime test blocker.
  No new game execution or runtime tests were performed for this interview.

Commands: `git status --short --branch`, `git branch -avv`,
`git log --oneline origin/main..HEAD`, `git diff --stat
origin/main...origin/slice/separate-mashup-qualification`, `gh pr view 1
--repo Jpatching/combine --json ...`, and the shared read-only Projects summary.

## Interpretation and recommendations awaiting owner answers

Observed stacking and missing merge closure create integration debt. These facts
do not establish widespread code-quality debt; that requires concrete review.
Earlier authority separated source publication, source merge, physical acceptance
and release. An open, mergeable PR is not proof that its full diff is ready.

Recommend reviewing PR #1's entire diff and identifying a coherent source slice,
including whether inherited scaffolding belongs. Resolve its disposition before
stacking more dependent work. Define source merge criteria separately from
exact-build gameplay acceptance, with explicit merge authority retained.

For additional games, reuse demonstrated world/session capabilities and qualify
each game's actual input and conversion separately. An adapter translates a
game's world data into the existing runtime's usable world representation.
Require witnessed geometry, collision, scale, materials, spawn, lifecycle and
measured performance; a format name or synthetic fixture alone is insufficient.
Do not design a universal adapter or expand active integration work yet.

## Open interview frontier

1. Which demonstrated mod/video/repository is the intended reference, and which
   observable behaviors should be reproduced?
2. Does reuse mean Skate movement in other worlds, or also carrying those games'
   gameplay systems? Existing Fortnite Skate-only scope stays settled.
3. Should reviewed source slices be eligible for merge before the complete
   experience passes physical acceptance? Recommend yes with clearly scoped
   checks and limitations; owner experience acceptance and release stay separate.

Next: owner answers this round; record settled consequential choices in
docs/DECISIONS.md and refine only the remaining questions. No merge, publication,
new integration or global workflow change is authorized by these recommendations.

## Owner follow-up: research bounds and Intervention source

The owner asks how to bound research to approximately 20 minutes and says the
Intervention detour was a waste of time but its source can be pushed/merged.
This grants task-specific source integration authority, not gameplay acceptance.
Live `git ls-remote origin` confirms main and slice/synergy-input-isolation both
at `a5593d671142f31653d45caeaad7b926d40ff855`; ancestor checks confirm both
slice/intervention-review and actual Synergy checkpoint c591086 are already
contained there. No additional push/merge is required for those revisions;
no claim about how main acquired them is made. PR #1 is separate Fortnite work.
Do not repeat the Intervention implementation merely to close its source status.

Timer guidance: a clock-checked instruction with a search cutoff and final-report
deadline is cooperative; an external CLI timeout enforces process termination
and may interrupt the final report. No hard timer or global configuration was
installed by this question. Other interview questions remain unresolved.
