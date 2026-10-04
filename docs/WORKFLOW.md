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
