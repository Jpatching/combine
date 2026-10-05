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

The owner's selected plan continues the same menu work, then qualifies a Fortnite
map inside the existing runtime. Preserve actual pinned Synergy, its presentation,
options and agreed trickshot hit radius; Hide HUD stays deferred.

```text
Input isolation -> first Synergy trial -> remaining menu coverage + hit radius
       | failed checks -> fix                  | incomplete -> continue
                                               v
                    Fortnite access/build/export qualification
                         | unavailable -> record exact blocker
                         v
             one building + ground -> adapter -> bounded Tilted trial
```

Opening Synergy or equipping Intervention is not full menu completion. A trial
marked ready is not owner accepted. Resume from the current card's evidence;
advance along agreed dependencies rather than inferring readiness from a
plan, a newer chat topic, a compiled binary or a synthetic fixture.

Continue menu coverage in these owner-selected batches after recording and
committing the Intervention/input result. Keep one batch active; split only for
a demonstrated integration problem:

1. Basic loadout: God Mode, infinite ammo/grenades, individual/all perk grant/removal.
2. Weapons: catalogue, take/drop, attachments and camos.
3. Presentation/adjustments: position/colours, weapon visibility, visions, camera,
   speed, gravity and timescale.
4. Movement: Frag No Clip and Forge Mode, including recovery and cleanup.
5. Killstreaks/private players: catalogue effects, host permissions, guest access
   and identity handling.
6. Trickshot hit radius: the existing geometry, damage and cover contract.

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

The Fortnite research target is Windows `Release-3.1-CL-3917250` (Chapter 1
Season 3), as selected in the owner's plan. Local legitimate access, identity,
exporter compatibility and conversion remain unverified. Start with one Tilted
building and surrounding ground before a map adapter or broader area. The route
is static geometry/materials/placements/collision/spawns into existing
`LoadedWorld`/`PreparedWorld` and `ClipCollision`, reusing grind-rail detection.
Require observed scale, axes, solid surfaces, walking/skating/jump/grind/recovery,
Intervention equip/on-foot shooting, menu isolation and exit/relaunch. No Fortnite
building/editing, destruction, full-island streaming or online services in this slice.
Keep all game assets and converted data private. Do not invent a map from absent data.

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
