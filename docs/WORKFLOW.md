# Combine workflow configuration

Start with **Continue Combine**, or explicitly invoke `$matt-workflow`.
Codex reads [Combine — Now](https://github.com/users/Jpatching/projects/5/views/4),
the [handoff](HANDOFF.md) and current Git state, then resumes the first missing
check. The owner does not need to remember skill order or select a model for
each task. A status question alone does not authorize new execution.

The private board owns status, Git owns source, and the handoff points to current
evidence. [BACKLOG](../BACKLOG.md) is historical. Reusable resume/model/agent rules
live in `~/.codex/workflows/solo-development/ROUTING.md`, reached by the global
router; this file holds Combine's project choices. [Tracker operations](agents/issue-tracker.md)
describe updates and offline recovery. Read project-required files once, then
load only relevant sections and the skill for the current check.

## Agreed order and evidence boundaries

D-016 originally scheduled the menu then Fortnite. D-020 starts Fortnite + Skate-only
wayfinding now, while the separate menu work and owner trial remain incomplete. Preserve actual pinned Synergy, its presentation,
options and agreed trickshot hit radius; Hide HUD stays deferred.

Read the live board and latest owner correction for the current priority. D-019
supersedes D-018's hit-radius-last ordering: hit-radius qualification/implementation
comes first while the prepared Synergy physical trial remains pending independently.
The remaining batches retain their requirements: basic loadout, weapons,
presentation/adjustments, movement and killstreaks/private players. Their current
order and progress belong on the board.

```text
Live card + requirements + evidence + latest owner correction
  -> reconcile -> one missing check -> one observable outcome
  -> verify behavior + affected instructions -> board + handoff -> read back
Pending exact-build owner trial -> physical verdict (separate from Codex checks)
Fortnite input + session qualification -> adapter -> regional tests -> full-island trial
```

Opening Synergy or equipping Intervention is not full menu completion. Hit-radius
research is part of its slice; an unsupported capability needs a precise blocker.
The [menu guide](TRICKSHOT_MENU.md) owns that slice's behavior and acceptance matrix.

Check effect, reversal, important failures and related-option interactions;
retain input/lifecycle regressions. Unsupported entries remain full-menu
requirements while independent entries continue. New ideas go in the board's
Later view. Hide HUD remains deferred. Each checked trial includes a newly
working-options list and versioned Launch, Files and Checklist shortcuts.

Source publication means a reviewed branch with its remote revision verified.
A local trial means an exact checked build is available for review. A local
release additionally requires the owner's acceptance of that exact build and
preserves its predecessor. Public full-menu release requires complete coverage
and hit-radius checks, explicit build acceptance, reproducibility and applicable
distribution-permission review, then separate publication authority. Earlier
experimental source snapshots establish none of those release claims.

The Fortnite destination is the **full selected island + Skate movement only**,
currently identified as Windows `Release-3.1-CL-3917250` with the pinned Rust runtime.
The live board permits a suitable accessible replacement (D-023); record its actual
selected build/identity before substitution. No replacement is selected. Smaller areas,
including a Tilted building and surrounding ground, are test cases within that
integration, not the destination. D-022 records the latest correction.
The [adapter qualification and specification](../research/results/2026-10-06-fortnite-adapter-qualification.md)
owns the source trace, proposed interfaces, ordered implementation work and exact
input/startup blockers. Do not choose an interchange schema without an inspected
selected-build export. Full-island loading/streaming must be assessed from counts
and measurements before promising performance. No MW2 combat, class selection,
weapon HUD, Synergy or visible/collidable proxy map belongs in this session.

Fortnite qualification proceeds independently of the separate Synergy trial and
hit-radius requirements. Keep game assets and converted data private. No Fortnite
building/editing, destruction or online services; no new engine or asset
redistribution. Source specification is not adapter implementation or playability.

## Implementation language and existing setup

Gameplay, collision, damage and authoritative menu integration use the existing
Rust runtime. Synergy's original GSC remains its menu source; Rust supplies its
runtime capabilities and the hit-radius extension. Python checks research data
and local preparation metadata; PowerShell prepares and verifies Windows trials.
Neither helper layer substitutes for playable runtime implementation.

The engineering-skill setup already exists: AGENTS.md points to the private
Project tracker and existing domain/decision documents through docs/agents/.
`triage` is not installed, so no triage-label configuration is required. Reuse
this adapted setup rather than creating another tracker, glossary or ADR store.
`ask-matt` routes the settled contract to qualification within the slice, then
`implement`/behavior tests and review. No new interview is required for the
already agreed menu or hit-radius behavior.

## Checks, synchronization and delivery

- Menu requirements and trial procedure: [menu guide](TRICKSHOT_MENU.md).
  Baseline recovery: [Windows runbook](WINDOWS_BASELINE.md).
  Full repository gate: `python3 scripts/verify.py`.
- Keep one lead/writer and one implementation slice; [task briefs](AGENT_ROLES.md)
  assign bounded helpers. Saved defaults govern new supported local sessions;
  an existing session may retain its explicit model choice.
- Preserve inherited dirty work. Runtime edits in ignored checkouts must be
  captured as reviewed reproducible source patches before claiming Git contains
  them. A Combine commit alone does not checkpoint an ignored runtime checkout.
- At meaningful phase changes and handoff, update the live card's phase,
  progress, blockers, evidence and next actor, then read it back. If unavailable,
  mark sync pending in the handoff; do not revive BACKLOG as a competing tracker.
- D-016/D-017 authorize reviewed source-branch pushes to Jpatching/combine before
  owner acceptance. Review the source list and reachable history, commit only
  the slice and verify the remote branch SHA after pushing. Keep failed/missing
  checks visible. A push is not owner acceptance, merge or release.
- Before requesting an owner trial, pass required checks and prepare a fresh
  versioned review folder identifying commit, pins, patch hashes, executable hash,
  launch/files/checklist shortcuts and limitations. Preserve previous builds.
  Stop at ready for the owner's test; launch only on their instruction.

The shared Windows review helpers stay in global storage. Combine's adapter is
`scripts/prepare-trickshot-trial.ps1`. A checklist for a rejected earlier native
build cannot establish acceptance of the actual Synergy build. Raw logs, game
files, settings, recordings and local machine paths stay outside published source.

## Visible progress without extra ceremony

The owner can say **Continue Combine**; Codex selects the next skill from the
current evidence. Now shows the phase, observable outcome, evidence, blocker and
next actor/action; Milestones shows larger outcomes and Needs you shows decisions
or trials. Reuse settled decisions and requirements. Failed checks keep the slice
in Phase 5; changed assumptions reopen the affected earlier decision. Small fixes
use the lightweight path rather than creating new planning documents.

At meaningful updates, record the observation date/time and exact build/source
where available. Implementation start dates are stamped once; target dates stay
blank unless deliberately scheduled. Test, acceptance, merge and release dates
are separate verified events; never infer a merge from a passing check. Roadmap
date mapping still needs a UI check.

During active sessions, flag workflow bloat when documents duplicate an authority,
a step repeats a settled decision or an expensive check without changed evidence,
a helper has no bounded question, or process work delays the playable outcome.
State the redundant step and the simpler next action. These are session warnings,
not a background monitor. Keep one active slice and concise evidence pointers.

## Branch to main workflow

Use one `slice/<outcome>` branch for each reviewable outcome. Refresh origin and
inspect the merge base before starting; checkpoint inherited work separately,
label unfinished scaffolding honestly, and never mix private assets into commits.
Source inspection/specification can be a completed source deliverable even when
its eventual game integration is not playable.

```text
main -> slice branch -> focused commits -> review + required gate -> PR
                           ^                      | failure: revise
                           +----------------------+
PR + review + authorized merge -> main
Exact game build -> owner trial -> acceptance -> separately authorized release
```

Before proposing a merge: inspect the entire diff from current `origin/main`, not
only the newest commit; identify stacked prerequisites; resolve conflicts; run
`python3 scripts/verify.py` once on the handoff revision, plus relevant runtime
checks for runtime changes. Attach evidence and limitations to the PR. Do not
merge unfinished ancestors just to clean a worktree. A local checkpoint is cheap
and reversible; publishing, merging and release retain their own authority.
After authorized merge, read back the PR/remote main SHA and board. Create the next
slice from refreshed main. No automatic merge/CI setup is implied.

The owner challenged the accumulated dirty work on October 6 and requested a
clear branch/merge workflow. Resume local reviewable checkpoints; keep this slice
unpushed and unmerged until its complete branch diff and target are reviewed.
The earlier plan's no-commit instruction is superseded for local checkpoints by
that correction; it does not establish publication or merge completion.

For a concise live resume, run `python3 ~/.codex/workflows/solo-development/projects.py
summary 5 /path/to/combine` (one shell line). It reads Git and the board;
it does not fetch or synchronize them. D-024 reuse qualification precedes more route-dependent adapter/rendering work.
D-025 records the owner’s questions about runtime necessity and directs research
into existing hosts per experience. Combine remains the source baseline; final
Fortnite trial-host choice is open. Matching source build is required only for
a fair exporter comparison; Blender is not a gameplay-runtime requirement.
C-024 needs a real terrain/building export before route selection; stop with a
precise blocker if unavailable. C-023 rail repair remains required before PR #1
merge. C-025 asset loading/rendering remains a preserved conditional task. Planning/slicing complete does not mean integration complete.

## Session orientation

Start with what is usable, today's bounded finish line, why it matters and who
acts next. Explain any script before using it: input, processing, output and
failure behavior. Work one bounded task, then explain the result. Use chat plus
HANDOFF as the starting point; reuse this board and the Fortnite map. Create a
decision ticket only when a precise unanswered question changes the route.

At return, check whether the reminder makes usable/current/blocker/next instruction
clear. The [workspace orientation](../research/results/2026-10-06-workspace-orientation.md)
classifies existing tools; it is evidence, not a new status dashboard. Finish:
“We did __. We checked __. Next is __.” Passing checks remains separate from
owner acceptance, publication, merge and release.
