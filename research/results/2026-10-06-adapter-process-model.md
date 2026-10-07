# Adapter process model and source publication — 2026-10-06

## Result and selected method

The owner selects same-process Skate reuse first; test methods per game and add
IPC only after an observed constraint requires it. This is a preference for the
Fortnite experiment, not a claim that a Fortnite extension has been qualified.
The existing [Fortnite specification](2026-10-06-fortnite-adapter-qualification.md)
owns acceptance. No live Fortnite bridge or gameplay was demonstrated here.

## Existing MW2 / Skate / Minecraft runtime: one process

Source inspected at `f608f85e407ff1b7689d54a9aafdd16e95711ac4` in
[2010-rust-rewrite-mashup](https://github.com/chasmlol/2010-rust-rewrite-mashup/tree/f608f85e407ff1b7689d54a9aafdd16e95711ac4).
The local source checkout was read with `git show` and targeted `git grep` at that
revision; private game data and logs were not inputs. This is source inspection,
not a fresh gameplay trial.

```text
iw4l.exe — one Bevy application
  MW2 world / input / camera / rendering
    <-> local Skate adapter <-> worker thread + Skate Session
    <-> local Minecraft runtime / voxel collision / mesh extraction
```

- [Launcher](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/launcher/src/main.rs#L11-L31)
  calls bootstrap. [Bootstrap](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/bootstrap/src/launch.rs#L450-L560)
  constructs the Bevy application, registers plugins and runs it.
- [Skate adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs#L121-L180)
  creates a worker thread and Rust `mpsc` Job/Reply channels, then constructs
  `skate_host::Session`. These channels are between threads within the same
  process; they are not shared-memory IPC between running games.
- The adapter reads local player state and gamepad input, extracts triangle/rail
  geometry from MW2 collision, and publishes Skate pose/camera to IW4L. Its
  existing host dependencies are MW2 authority/presentation, collision and Bevy
  resources; those dependencies are not a Fortnite interface.
- [Minecraft systems](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/minecraft_world.rs#L197-L215)
  own an in-process runtime resource. The same file's block-update path writes
  changed shapes into `sim::voxel`; Bevy render extraction handles the meshes.
  A separate `iw4l-master` network service is not a local guest/host game bridge.

The reusable part is Skate's simulation/session API and associated pose/collision
adapters. Existing success does not mean the original Fortnite executable can be
loaded by IW4L or that Fortnite behavior may be replaced with static geometry.

## Public Minecraft crossover: two processes, shared-memory IPC

The matching reference is
[minecraft-crossover-bridge](https://github.com/justbustin/minecraft-crossover-bridge/tree/d1723873ec8f370389cf19f74fac455b9e581321),
not Universal Modder itself. `git ls-remote ... refs/heads/main` resolved
`d1723873ec8f370389cf19f74fac455b9e581321`; the lead read the README and architecture
documentation at that exact revision after the scout inspected moving-branch
pages. This is pinned documentation evidence; no code was installed or run.

The [README](https://github.com/justbustin/minecraft-crossover-bridge/blob/d1723873ec8f370389cf19f74fac455b9e581321/README.md)
describes Minecraft Java/Fabric running natively on macOS alongside a Windows
host under CrossOver. Supported hosts are Monster Hunter: World 15.23.00 and
Elden Ring 1.17.1, not Fortnite.

The [architecture document](https://github.com/justbustin/minecraft-crossover-bridge/blob/d1723873ec8f370389cf19f74fac455b9e581321/docs/how-it-works.md)
describes file-backed shared memory for state, camera, collision queries and
entity/damage messages, with sequence counters. A separate triple-buffered frame
mapping carries guest color/depth for host composition. Its native host module
performs game-thread queries; the Fabric guest converts ray hits to terrain.
Exact-version signatures disable unsupported features. Each new host still
needs its own camera, collision, player and rendering access. This supplies an
IPC reference, not a Fortnite adapter or proof that ray sampling meets Skate's
triangle collision and rail requirements.

## Fortnite next slice

1. Retain the existing 3.1 CL3917250 candidate unless a tested prerequisite
   justifies another accessible build. Pin the client and extension source.
2. Establish a permitted host extension and game-thread callback. Read one real
   player/camera value and show it changing with host movement; a synthetic
   message or successful process launch does not pass.
3. Check whether that extension can host the existing Skate Session and provide
   live geometry/rails, build/edit/destroy lifecycle, input, pose/camera and render
   access. Prefer direct calls and internal threads. Record an actual constraint
   before selecting a second process or transport.
4. Advance to the existing live ramp acceptance seam only after those gates.

Inspected Reboot and Instigator normal launch paths manipulate EAC processes;
they remain unqualified under the project boundary. Stock and direct executable
startup results do not establish a permitted host adapter. No universal framework,
Fortnite gameplay recreation, protection bypass or static substitution is selected.

## Git cleanup and publication evidence

At the start, the active branch was 15 commits ahead of remote main and zero
behind; eleven commits were unpushed. Local main was nine behind and was safely
fast-forwarded. PR #1 contains four published commits and remains blocked by its
reproduced rail-validation defect, independently of GitHub's conflict status.

Reviewed all newly reachable blob types, sizes, extensions and credential/path
patterns. No binary/game assets or credential-pattern matches were found; seven
historical blob instances contained a machine-specific documentation path.
A publication copy redacts it to `/path/to/combine`. Original branch tip
`be8d3b8e08259f39f93dcdaa5d06eeb877dcfd10` remains local and preserved.

The owner then requested removing obsolete workflow work. The focused branch
omits interview-only commits `cdaa4a7` and `86a2c6e`, their obsolete interview
record, and its handoff pointer. Mixed commits containing game evidence remain.
The nine remaining publication-copy commits end at
`76a03831e562ddc7e31304c5d8018b456ddab8c0`; their game source trees are unchanged.
A separate specification/evidence commit follows. No published history was
rewritten. Original local recovery history must not be pushed wholesale.

Actual local audit commands: `python3 /tmp/audit-combine-publication.py`,
`python3 /tmp/prepare-combine-publication.py` and
`python3 /tmp/focus-combine-history.py`. These are temporary source-only tools;
new trees were checked against their predecessors. The final source scan,
repository gate is recorded in the handoff. Branch publication and remote-SHA
read-back are pending until the reviewed commit exists, then recorded on the
private board. Preservation copies explain why all-local-ref counts can still
show unpublished historical commits after the active branch is synchronized.

Use short-lived topic branches and explicit remote tracking, consistent with
[Git's branching guidance](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows).
Push reviewed authorized source at slice completion, then verify its remote SHA.
Gameplay acceptance, merge and release remain separate. Remove merged branch
names only after ancestry/worktree checks; never rewrite shared main to tidy it.

Completed workflow worktree removed after clean/ignored-file inspection; stale
worktree metadata pruned. Local `chore/workflow-routing` and
`chore/visual-workflow-guide` names deleted after confirming their commit is in
main. Game branches and PR #1 retained.
