# Fortnite–Skate route qualification with Universal Modder — 2026-10-06

**Result: no candidate qualifies for live execution.** Reboot remains the first
candidate, but the reviewed launch path does not meet our no-protection-bypass
boundary. Rift and Era evidence does not close that gap. Preserve the existing
Skate simulation and same-process preference; no observed constraint justifies IPC.
This completes the requested bounded investigation with a precise prerequisite
blocker, not a playable integration or a claim that every possible route fails.

The [existing contract](2026-10-06-fortnite-adapter-qualification.md) owns requirements.
Any qualified interactive island is acceptable. Building, editing and destruction
remain essential; static scenery and a replacement Skate implementation are excluded.

## Evidence levels and inputs

- **Documented:** upstream guidance/README claims, explicitly identified below.
- **Source-inspected:** pinned public text read this session; code was not run.
- **Experimentally verified this session:** source retrieval, hashes and repository
  checks only. No Fortnite launch, live host-value read or gameplay test occurred.
- **Inherited experiment:** existing 3.1 / CL-3917250 isolated client was prepared
  and hash-checked; stock BattlEye startup stalled, and direct unmodified shipping
  EXE exited within 20 seconds for an unknown reason. See the
  [original trial record](2026-10-06-fortnite-adapter-qualification.md#isolated-windows-startup-trial--owner-directed-follow-up).
  These observations neither establish playable access nor diagnose the exit.

Inspection inputs were public source and existing redacted reports. No game data,
private logs, settings or recordings were uploaded. No new client was acquired,
plugin installed, launcher run, paid service used or runtime API introduced.

## Pinned guidance and its limited role

Universal Modder `main`/`HEAD` resolved to
`76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70`. A bounded read-only research helper
inspected the following; the lead read the Unreal/mashup text and verified hashes.
These are references, not installed skills or authority to execute their tools.

| Reference at that revision | Useful application here | Limit |
| --- | --- | --- |
| [Reconnaissance](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/skills/game-recon/SKILL.md) | Record exact game/engine identity, protection, loader and supported version before choosing a route | Its description of `um scan` as file-reading is not an implementation audit; we did not run it |
| [Unreal guidance](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/skills/mod-any-game/references/engines/unreal.md) | Identify build-specific object, game-thread and rendering seams only after host access qualifies | Explicitly excludes EAC/BattlEye titles including Fortnite; generic UE4SS/C++ suggestions do not qualify this client |
| [Mashup guidance](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/skills/mashup-mods/SKILL.md) | Its IW4L example fits existing in-process Skate/collision reuse; plan observable checks first | Its separate two-process pattern is not a Fortnite prerequisite or evidence of compatibility; reimplementation patterns are outside this task |
| [Safety](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/skills/mod-any-game/references/safety.md), [tool overview](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/README.md), [MCP configuration](https://github.com/rehan-remade/universal-modder/blob/76b9c7e77ead5fd2d5f1b7613c6a7ed591b01c70/.mcp.json) | Review execution, input automation and external-service boundaries before use | No `um`, UE4SS, fal or bundled hooks installed/executed; no tool implementation declared audited |

Adopt the investigation method, not a universal framework. No repetitive operation
has demonstrated a reusable integration method here: temporary read-only retrieval
snippets stay temporary. Extract scripts only after demonstrated repetition, and
create a reusable skill only after the method succeeds on a second case. Shared
workflow material belongs in global Codex storage, not this repository.

## Candidate qualification

Reboot was inspected first. Alternative checks were limited to whether primary
sources supply the missing launch/extension prerequisite; no broad replacement
ranking or binary downloads were performed.

| Candidate / exact source | Client, acquisition and launch requirements | Extension evidence and unresolved blocker |
| --- | --- | --- |
| [Reboot 3.0](https://github.com/Milxnor/Project-Reboot-3.0/blob/3f6417ee6b07063bb6f83902ad3971f998888bab/README.md), `3f6417ee6b07063bb6f83902ad3971f998888bab`; [launcher](https://github.com/Milxnor/Reboot-Launcher/tree/64dc971da499f1856f40af992d0068c5801e344b), `64dc971da499f1856f40af992d0068c5801e344b` | README documents S3–S15, Visual Studio 2022 and Reboot Launcher, not a known-good exact client patch. Existing 3.1 CL-3917250 is the initial candidate; lawful supported acquisition/provenance and successful compatible launch remain unresolved. No new archive acquired | Server build/edit handlers exist; launcher starts/suspends EAC. Reviewed route fails project boundary; no permitted rendering-client/native extension established |
| [Rift Mods](https://github.com/RiftFN/Mods/tree/ac40fc160a29b3304679b90a7e6940ea36ded876), `ac40fc160a29b3304679b90a7e6940ea36ded876` | First-party archived catalogue; exact compatible client CL, supported acquisition, launcher revision and dependencies are **not established** by inspected docs | README describes `.rift` package submission; [NaxMenu description](https://github.com/RiftFN/Mods/blob/ac40fc160a29b3304679b90a7e6940ea36ded876/MenuMods/NaxMenu/readme.md) documents a menu. Neither supplies a reviewed native simulation extension, permitted launch or collision lifecycle interface. No candidate client selected |
| [Era launcher](https://github.com/EraFNOrg/Era-Launcher/tree/e7d48de4ba652df3efef50c25698ef43549d5d10), `e7d48de4ba652df3efef50c25698ef43549d5d10` | Pinned WPF project targets .NET Framework 4.8; user-selected local client directory. Exact supported client CL and lawful acquisition are **not established** by inspected source | `StartFortnite` requests protection-disabling options, then injects `EraV2.dll`. DLL source/build identity and native extension contract unqualified. Do not execute this route; no claim about unrelated current Era distributions |

Reboot's freshly inspected
[controller](https://github.com/Milxnor/Project-Reboot-3.0/blob/3f6417ee6b07063bb6f83902ad3971f998888bab/Project%20Reboot%203.0/FortPlayerController.cpp#L846)
contains `ServerCreateBuildingActorHook` and `ServerEditBuildingActorHook`
(line 1742); editing invokes `ReplaceBuildingActor`. Its
[DLL source](https://github.com/Milxnor/Project-Reboot-3.0/blob/3f6417ee6b07063bb6f83902ad3971f998888bab/Project%20Reboot%203.0/dllmain.cpp)
registers server hooks. This proves source paths exist, not that client rendering,
destruction or current Skate collision works. The
[launcher entry](https://github.com/Milxnor/Reboot-Launcher/blob/64dc971da499f1856f40af992d0068c5801e344b/gui/lib/src/widget/game/game_start_button.dart#L211)
calls a helper that suspends the EAC process; its
[dependency code](https://github.com/Milxnor/Reboot-Launcher/blob/64dc971da499f1856f40af992d0068c5801e344b/common/lib/src/util/dll.dart)
uses downloads rather than a complete reviewed dependency pin set. No loader
binary was downloaded. Injection alone is not the reason for rejection; the
observed protection manipulation and missing supported route are.

Era's [launch source](https://github.com/EraFNOrg/Era-Launcher/blob/e7d48de4ba652df3efef50c25698ef43549d5d10/EraLauncher/Home.xaml.cs#L292)
and [project file](https://github.com/EraFNOrg/Era-Launcher/blob/e7d48de4ba652df3efef50c25698ef43549d5d10/EraLauncher/EraLauncher.csproj#L11)
are the basis of that bounded assessment. No effectiveness of its launch flags
was tested. Rift's [README](https://github.com/RiftFN/Mods/blob/ac40fc160a29b3304679b90a7e6940ea36ded876/README.md)
establishes packaging only. “Offline,” “single-player” and “anti-cheat removed”
are not evidence that an acquired client or launch path meets project boundaries.

## Comparison with the existing Skate Session

The authoritative guest-side source remains
[`physics/bridge.rs` at `f608f85e407ff1b7689d54a9aafdd16e95711ac4`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs).
Fresh reads confirm these interfaces; the existing
[process-model report](2026-10-06-adapter-process-model.md) distinguishes worker
threads from cross-process transport. This table is a gap analysis, not a new API.

| Concern | Existing Skate input/output | Fortnite evidence still needed |
| --- | --- | --- |
| Controls and timing | `collect(InputFrame, dt)`, `advance`, `period`; raw diagnostic `tick(Controls)` | Reviewed client input/tick callback, on-foot/skating ownership and neutral transitions without duplicate movement |
| Player and camera | `activate(spawn, heading)`; `pose()` returns root/bones, camera, velocity, tick/state | Read live player/camera values, measure axes/units, then establish authority to apply pose/camera without host correction |
| Rendering | Pose exposes bone names/transforms and camera parameters; it is not a Fortnite renderer | Host skater/board meshes, skeleton binding, depth/lighting and game-thread lifetime rules |
| Changing collision | `collision_builder().build(triangles, rails)` then `install_collision`; rebinds grind world | Actual terrain/structure collider geometry, transforms and authoritative create/edit/destroy notifications; no inspected client bridge supplies these |
| Failure and recovery | Fallible construction/activation/ticks, `suspend_input`; requires private Skate assets | Reject stale collision work after edit/destroy, stop skating if current collision cannot install; reset on world replacement and detach cleanly |

**Inference:** a thin in-process host adapter could reuse these seams, but Rust
Session availability does not prove a stable native ABI or Unreal interoperability.
No bridge library, generic IPC protocol or rendering substitute is selected.

## First live experiment — defined, blocked, not run

**Question:** can a permitted extension observe a real player or camera value
changing with movement in the identified Fortnite client?

```text
Exact client + reviewed dependencies + permitted launch/extension
  | missing or protection manipulation required -> STOP, record prerequisite
  v
Load interactive island -> read host player/camera through reviewed callback
  -> stand still -> move forward/back -> turn 90 degrees -> stop
  | absent/stale/non-finite/wrong-world sample -> FAIL, no pose writes
  v
Correlate timestamped host samples with movement -> live-read evidence
  -> later: qualify same-process Session input/pose/render/collision
```

1. Before execution, record exact Windows client CL/executable hash, launcher,
   backend and extension source/build hashes, supported acquisition evidence and
   reviewed dependency behavior. Preserve original installation; use an isolated
   profile. A missing permitted extension is a blocker, not a reason to try injection.
2. Select any qualified interactive island; record island/world identity and
   Windows hardware. Through its reviewed callback, sample one real position or
   camera transform plus monotonic time/world identity. Use existing diagnostics
   if available; do not build a general runtime API for this experiment.
3. Record stillness, forward movement, reverse movement and a 90-degree turn.
   A changing position correlated with translation or camera orientation correlated
   with turning must appear in consecutive fresh samples. Describe expected
   non-changes (e.g. position during an in-place turn); measure axes/scale separately
   before attempting pose control. A moving timer, startup log or synthetic value fails.
4. Repeat after clean exit/relaunch. Pass requires responsive, attributable live
   values from the same recorded build; stale values, missing callbacks, wrong-world
   objects or protection changes fail. Keep raw diagnostics private; share redacted
   values/results only. No Skate pose writes or collision changes in this first read.

The next acceptance sequence remains: **build ramp on foot → switch to Skate →
skate/jump/grind → edit and verify changed collision → destroy and verify removal
of collision/grind support → recover/exit/relaunch**. A successful live read would
qualify observation only, not this sequence or full-island performance/acceptance.

## Reproduction and checks

Public text retrieval used Python standard-library `urllib.request`/`json` and
SHA-256, without importing/executing downloaded code. Temporary commands were
`python3 /tmp/qualify-public.py` and `python3 /tmp/qualify-alternatives.py`.
The initial sandbox attempt failed DNS and then a missing-pin lookup; approved
network retry completed. No partial result was treated as qualification.

To reproduce without those temporary scripts:

1. Resolve each repository's default branch with GitHub REST
   `GET /repos/{owner}/{repo}`, then `GET /repos/{owner}/{repo}/commits/{branch}`.
   Read `GET /repos/{owner}/{repo}/git/trees/{recorded-pin}?recursive=1`.
2. Fetch only the linked files at the recorded pins from
   `https://raw.githubusercontent.com/{owner}/{repo}/{pin}/{path}` into a
   temporary directory; URL-encode spaces. Compute `sha256sum` and compare below.
3. Search Reboot for `ServerCreateBuildingActorHook`, `ServerEditBuildingActorHook`,
   `ReplaceBuildingActor`; launcher for `_startGameProcesses`, `_createPausedProcess`,
   `suspend`; Era for `StartFortnite`, `PreInject`; Skate for `pub fn` and `Pose`.
   Read surrounding implementations, not only matches. Inspect Rift README/menu
   metadata as documentation, without acquiring `.rift` packages.
4. Compare host evidence with the table and the live-read prerequisite. Missing
   exact client/dependency identity or permission evidence remains unknown; never
   fill it from a season-level support claim.

Fresh remote refs: Reboot default branch
`10c659028ad9d6816f78226483f11a884bf81f57` (inspection pin intentionally unchanged);
launcher, Rift and Era defaults matched the revisions above. Runtime remote HEAD
remained `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; project lock unchanged.
Rift's repository API reported archived; Era's tree was not truncated. Exact
revision and file scope matter: these reads are not an audit of all forks/releases.

| File | SHA-256 |
| --- | --- |
| Universal Modder game-recon | `77a7c20e74e5add09824433d8181d30e9dbca2c96c2c271e22afdadc7af0adca` |
| Universal Modder Unreal reference | `34e897880500a737c3df34e948211b76fac919b582236388db135b053a5f3bcc` |
| Universal Modder mashup-mods | `13c74bb1452b57b603166c9fcda2c955a931cad0d27f574b5270e27e7988d175` |
| Reboot FortPlayerController.cpp | `1cfe6bb2ddcf2bf5fa225995767eed156b9b6a4f1f1ea7f16f873b16c871e56e` |
| Reboot launcher game_start_button.dart | `8d8b04393eb408609da6d3066c8142d489261a9223479834df833c48501cf6b6` |
| Skate physics/bridge.rs | `7b47702ca1dd3067ff17fb1bb170c289cc692d8892a7a4d4ca410254a47a4b57` |
| Rift README.md | `09da31edfb65ceab900fc3bde04a62916a2229b9aa55dfa9d944fcbb1ddbc96a` |
| Era Home.xaml.cs | `43db0594268858df93883217950e5e0a7283afea5e46abb49b6605e592ca9eed` |

Repository checks and review outcome are recorded in [the handoff](../../docs/HANDOFF.md).
They do not establish gameplay. This research changes documentation only; inherited
exporter/native test debts remain separate. The prior rail correction is already
in the starting Git revision and is not a new result of this investigation.

**Next actor: Codex, when new host-access evidence exists.** Require a documented,
reviewable client launch and extension route compatible with project boundaries,
then perform the live-value experiment above. Re-running the rejected launchers,
adding a universal framework or switching to IPC does not resolve that prerequisite.
