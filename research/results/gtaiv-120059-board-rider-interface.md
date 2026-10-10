# GTA IV 1.2.0.59 board and solved rider presentation

Source-only decision input for [issue #46](https://github.com/Jpatching/combine/issues/46), 2026-10-10. **Verdict: requires-local-proof; runtimeVerified=false.** The strongest bounded first candidate is a GTA native object driven by a solved board transform through the existing CLEO Redux entry route. Public source also provides a D3D9 geometry-rendering reference in LibertyCraft, but that plugin explicitly excludes Complete Edition 1.2.0.59. None of the inspected interfaces establishes arbitrary solved-pose injection into a GTA ped, or an exact-version-qualified separate Skate skater renderer. There is therefore no source-supported claim that one ready-made public interface already delivers the complete board, rider and cleanup requirement on this build.

This report recommends proof order, not a runtime architecture, implementation spec, appearance choice or gameplay acceptance. Version, placement, mounting guard, source pins and retained candidates stay unchanged. The host coordinates fresh Standards and Spec review and links findings afterward; existing implementation issues remain open.

## Verified source facts

### Provenance and riding observations

The worker checkout started clean on `research/gtaiv-board-rider-interface` at `82d35ad1e43620389abb69fa6bcb591cca1d6279`. Candidate files were explicitly downloaded as public text from `fd9f8c4933d3aed193273a2ce5d78fb076886972`; their presence in committed main was not assumed. The [candidate adapter README](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/README.md) describes the mount/move/dismount adapter and optional worker, rather than a complete presentation renderer. Upstream comparison used the requested `f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Public GitHub commit/tree metadata resolved the other complete revisions cited below. Downloaded source was read, never executed.

The [requested riding comment](https://github.com/Jpatching/combine/issues/20#issuecomment-6098478199) was fetched through the public GitHub API. It reports a sustained mount until explicit cleanup, zero observer-start markers, a later guard refusal and owner-reported partial forward movement without a board or Skate animation. Its integration-source and installed-runtime identities differ; the runtime is still `b403377481a33e407aeb81b78b8d38984aac4735`. These are attributed observations, not this researcher's real run. They do not qualify the later source snapshot or prove a complete ride. No private timeline, coordinate, asset or diagnostic was accessed.

This process follows the supplied Matt research steps: inspect primary sources, write one cited result in the existing results directory, report its location. It is the delegated researcher; no nested agents were created. Universal Modder's pinned [mashup skill](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/mashup-mods/SKILL.md), [route note](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/choosing-a-mashup-route.md), [collision/lifecycle guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/collision-and-combat-bridging.md) and [evidence levels](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/evidence-levels-for-mashup-claims.md) were inspected as method references. They distinguish rebuilt guest simulation in a real host from conversion or two-game picture transport and require per-host proofs. They are not compatibility evidence.

### Where the actual solved pose stops

The pinned [Session bridge](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs) exposes `Session::activate`, `tick`, and `pose`. `Pose` contains a root matrix, `bones: Vec<Mat4>`, bone names, camera, deck velocity, tick and state. `pose()` converts the skater's `render_pose` matrices with `native_matrix` and returns evaluator bone names. This is the solved presentation output to consume, rather than a new animation selected from input buttons. The returned root is the animated skeleton's `animation_to_world`; deck velocity alone is not a deck orientation.

The candidate [in-process adapter](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/in_process.rs) reduces that pose to `[x,y,z,heading]`. Heading comes from root forward; `combine_value` exposes four floats. It does not export bone matrices, full root rotation, board-joint transforms or mesh data. The [worker](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/bin/worker.rs) validates root, velocity and all bone matrices as finite, then likewise publishes only four movement floats plus period. The [wire contract](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/wire.rs) has a fixed 48-byte response with ride, sequence, collision revision, four-float pose and period. Thus neither branch currently transports the solved rider skeleton or a board skinning palette across the GTA boundary.

The [main script](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate.js) disables player control, freezes the existing ped, sets its coordinates and heading and updates an owned chase camera. It neither creates a board nor applies Skate animations. Its restoration makes independent best-effort calls to stop the adapter, deactivate/destroy the owned camera, unfreeze the saved ped and restore player control. The [watchdog](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate_watchdog.js) separately attempts those operations after rescue. Neither currently owns an object handle, ped visibility change or custom GPU resources to clean up. The [accepted-pose cache](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/accepted_pose.rs) rejects mismatched ride/revision/epoch, invalid surface and outputs older than 250 ms without renewing their original update time. This is reusable freshness policy, not proof of future board deletion or render-thread retirement.

### What the pinned MW2 path actually supplies

The [Skate converter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/converter/iw4l_skate_convert.py) prepares animation/physics data and `private/skater.glb` from the owner's files. The [board exporter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/skate_board.rs) derives `rig.json` and `board.json` from that GLB: joint names, bind/inverse-bind matrices, surfaces whose material names contain `Skate`, indexed vertices with four joints/weights, normals, UVs and textures. It changes winding and limits texture dimensions to 512. Its rig binds remove the GLB/Blender basis; board inverse binds remain as written. These files are intermediate data, not GTA-native models or a GTA renderer.

The upstream [presentation adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs) copies complete bones/names/tick into `SkateMode`, converts the root and clears bones on exit. Its [basis conversion](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs) uses Skate metres versus MW2 inches (`0.0254`) and axes `(x,z,-y)`. That MW2 scale must not become a GTA constant; the current GTA metre assumption is still unqualified.

The [rig code](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rig.rs) has two different consumers:

- `board()` matches board joints by name, constructs palettes as `solved_bone * rb * inverse_bind`, weights transformed positions/normals over four influences, converts into MW2 axes/units and appends packed vertices/indices/material surfaces to CPU body geometry. Board tilt/flip therefore comes from solved joints; it is not a prop attached rigidly to a foot or copied from root yaw.
- `pose()` maps MW2 soldier joints to Skate names, aligns reference bind segments and computes `posed * inverse(reference_bind) * fit`, finally multiplying the soldier bind. Unmapped helpers inherit ancestor effects; upper spine/neck/head have explicit special handling; attached models use attachment handling. This is a host-specific retargeter, not a general skeleton converter.

The [remote-body consumer](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/occupancy/remote_body.rs) invokes the retargeter for the active living local skater, supplies its matrices to body skinning, removes the gun/attachments for that job and appends the board through `rig::board`. Consequently MW2 visibly combines simulation, full-pose publication, rig mapping, CPU skinning and its existing geometry submission. Asset conversion alone supplies only an earlier part of this chain.

### Public GTA interfaces and their version limits

| Candidate | Source-supported boundary | Exact 1.2.0.59 status |
| --- | --- | --- |
| CLEO Redux plus GTA native object commands | Existing script/plugin entry, model request/load, object creation, position/rotation, deletion and model release | Loader explicitly documents this version; each new native call, model import and lifecycle still needs local proof |
| GTA native animation tasks | Clip playback, normalized clip time and speed; ped-bone position query | Native definitions are source data, not exact-build qualification or an arbitrary bone-palette setter |
| LibertyCraft D3D9 custom geometry | Concrete render-thread enqueue, frame camera/depth handling, mesh submission and state restoration reference | Explicitly older-version-only; no CE support can be inferred from pattern scanning or use of D3D9 |
| IV-SDK and its entity/ped classes | Older-build plugin/class reference | README limits support to 1.0.7.0/1.0.8.0 EFIGS; unsuitable as a drop-in CE skeleton API |

CLEO Redux's [supported-game documentation](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md) explicitly lists GTA IV Complete Edition 1.2.0.43/1.2.0.59. Its [public SDK header](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h) exposes command registration, parameter exchange, before/after-script callbacks and runtime-init callbacks. It exposes no arbitrary mesh draw, D3D device, scene-depth or ped-bone palette interface. A script callback must not be assumed to be a render-thread callback.

The exact [Sanny Builder GTA IV definition file](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json) declares `REQUEST_MODEL`, `HAS_MODEL_LOADED`, `CREATE_OBJECT`, `SET_OBJECT_COORDINATES`, `SET_OBJECT_ROTATION`, `FREEZE_OBJECT_POSITION`, `SET_OBJECT_COLLISION`, `DELETE_OBJECT` (pointer argument), and `MARK_MODEL_AS_NO_LONGER_NEEDED`. This supplies a concrete native-prop hypothesis. The same file declares `TASK_PLAY_ANIM`, `SET_CHAR_ANIM_CURRENT_TIME`, `SET_CHAR_ANIM_SPEED`, `GET_PED_BONE_POSITION`, `ATTACH_OBJECT_TO_PED` and `SET_CHAR_VISIBLE`. A bone-position read or attachment command is not a bone-matrix write. No inspected entry here accepts the Session's complete named matrix array. Sprite drawing is not skinned world-model drawing. These are community-owned primary API definitions, not Rockstar's exact-build guarantee.

LibertyCraft's [ASI README](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/README.md) targets 1.0.8.0 and considers 1.0.7.0 likely; its [startup source](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/dllmain.cpp) reports all other versions inactive and registers IV-SDK drawing callbacks only through the supported startup. Its [render integration](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/Render.cpp) captures a frame snapshot, enqueues a draw command, accesses the D3D9 device on the render thread, skips lost devices, obtains matching render/depth targets and restores a state block after drawing. Its [world renderer](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/render/World.cpp) consumes avatar/scene geometry and draws vertex batches, including `DrawPrimitiveUP`. This is a useful reference for drawing already-skinned Skate vertices, not a library that accepts Skate rig data unchanged. Its copied viewport layouts and hooks require independent CE support; its Minecraft lighting/shadows do not automatically give Skate native GTA materials.

The [IV-SDK README](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md) expressly limits supported versions and says other versions differ substantially in classes/functions. Downgrading or treating older offsets as CE addresses is outside this decision.

### Conversion/import and Universal Modder helpers

Alexander Blade's first-party [GTA IV OFIO documentation](https://www.dev-c.com/gtaiv/ofio) describes 3ds Max import/export of drawables, bounds and animations through OpenIV text openFormats, including skinned-mesh export fixes. This identifies an existing offline authoring boundary. It does not document loading a GLB directly into GTA or streaming a solved Session pose at runtime. OpenIV's linked format page was inaccessible in this attempt; no format-schema or exact-version claim is based on it. Importing a board or ped can make content available to a host model hash, once packaging/registration is proved locally. It cannot alone implement simulation transport, mounting ownership, pose updates or cleanup.

Universal Modder's pinned [README tool inventory](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/README.md) supplies `um kb` discovery, `um scan` inventory, GLB-to-sprite `um render3d`, generation/rigging helpers, Windows input/capture, backup and publication checks. The inspected [CLI dispatcher](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/um/cli.py) is tool orchestration, not a GTA drawing/model or ped skeleton API. `render3d` produces offline sprite frames; generic auto-rigging neither maps GTA bones nor writes its runtime palette. Generation would also substitute content rather than preserve the converted Skate asset and is not required here. No helper was installed or run, no paid service used and no game media uploaded. `um kb search` was unavailable in this worker; source/manual discovery was used instead. Its [geometry-transfer note](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/geometry-transfer-host-draws-guest-meshes.md) usefully specifies wall occlusion, host lighting and state restoration proofs. Available helpers reduce research/authoring/evidence work; they do not fill the missing CE render hook or live skeleton interface.

## Source inference

**Native board candidate:** use the existing CE script entry with one native object whose transform follows the solved deck, after locally proving model registration/load and object calls. This is the smallest visible-board question because GTA owns drawing and model lifetime. A rigid board can demonstrate deck position/orientation and cleanup, but cannot claim the pinned weighted board's full truck/wheel deformation. If reproducing that skinning matters, separate rigid parts or custom CPU-skinned drawing require a later boundary. Attachment to a GTA foot is an optional presentation approximation, not evidence of actual solved board motion.

**GTA-character rider:** keeping the current ped avoids selecting another appearance. Native clip tasks could provide a temporary skating-looking animation, or imported baked clips could be retargeted offline. Neither is the actual Session solution, which includes state blending, IK and current physics adjustments. Faithful live presentation needs GTA bone identifiers/hierarchy, bind frames and proportions, a Skate-to-GTA retargeter, and a proven write phase after GTA animation evaluation but before skinning, with restoration of native animation authority. The MW2 rig algorithm is a reference for the mathematics; its bone names, fits and special cases cannot be copied as GTA mappings. No inspected exact-build interface establishes the required live write phase.

**Separately rendered Skate skater:** consume the GLB geometry/weights and the Session's solved matrices with its own bind palette, retaining the source rig instead of retargeting onto GTA. That avoids the GTA-ped skeleton write requirement, but still needs a CE-qualified draw callback/device, camera/depth, GPU upload/materials, culling and lifecycle. Host lighting/shadows remain additional proofs. Hide the host ped only if this route is selected later and restore its prior visibility on every exit; keep the host gameplay actor as the existing ownership contract requires. Separate rendering inside GTA is different from replacing the player model, compositing an image or running a second real game. Appearance and scope remain owner decisions.

The shared missing transport boundary is a bounded, versioned snapshot carrying full root/board orientation and, for a rider, names or a stable skeleton identity plus full solved matrices and tick. Preserve ride/sequence/collision revision/epoch, original freshness deadline and finite checks; cap lengths and publish atomically. Establish matrix storage, local/world spaces, bind order and GTA axes/scale explicitly to avoid double-applying root transforms. A same-process path still needs a synchronized full-pose publication boundary even without IPC. A renderer must accept one coherent snapshot and retire queued old-ride draws on dismount. Those requirements are derived from the inspected interfaces, not an approved protocol spec.

## Unknowns

- Exact 1.2.0.59 behavior/signatures of the new object and animation commands, availability of a suitable private imported board model, streaming failure behavior and safe placement pivot/orientation. Native definitions and asset presence cannot qualify these.
- Which solved named joints define the converted board components and whether a single rigid transform is an acceptable first scope; actual asset contents were not read. Full board skinning parity is unproved.
- GTA skeleton hierarchy/binds, retarget quality, feet/deck contact and an exact-build live bone write interface. No universal negative claim about all public mods follows from this bounded source set.
- CE custom draw scheduling, device/reset behavior, depth convention, viewport layout, materials, occlusion, lighting/shadows and compatibility with the retained loaders/camera. LibertyCraft's older-build implementation proves none of these for CE.
- End-to-end freshness/latency and cleanup for new handles, visibility changes and render queues under cancellation, exceptions, worker exit/stall, invalid pose, loss of input/surface, script termination, load/respawn and device loss. Current cleanup cannot recover resources it does not yet track.
- Owner's appearance and initial scope preferences remain unresolved. This report selects neither a GTA character identity nor a replacement Skate body.

Access limitations: [LuaModLoader's first-party site](https://zalgo-dev.github.io/LuaModLoader/) advertises CE 1.2.0.59 native calls and text/rectangle drawing, but its linked `https://github.com/Zalgo-Dev/LuaModLoader` source returned 404. Treat these as creator documentation only; a 2D `Draw` namespace does not establish mesh/skinning support. OpenIV's OFIO-linked `https://openiv.com/?page_id=384` timed out; an exploratory category page returned 502. Two guessed CLEO doc paths (`docs/en/intro.md`, `docs/en/gtaiv.md`) returned 404, resolved by inspecting its public tree and reading `docs/en/introduction.md`; they are not compatibility blockers. Owned binaries/assets and Windows runtime were intentionally outside scope. No native binary analysis, dependency installation, game launch/control, push, merge or release occurred.

## Next local proof

Recommendation only, requiring separately authorized local implementation/runtime work:

1. **Qualify one native object before rider work.** Keep exact version, candidates, placement and guard. In an isolated local copy, verify the model-load/create/rotate/delete/release sequence and an ownership record shared with rescue. Start with a permitted placeholder if private conversion is unavailable, then the owner's privately converted board. A placeholder proves the interface only; asset-import success is a separate claim. Bound model-load wait and retain native control if preparation fails. Do not modify original archives or infer registration from a file existing.
2. **Make that board consume the actual solved board output.** Preserve the Session; expose enough of its solved palette to derive the deck transform with documented pivot, axes, scale and bind conventions. Demonstrate tilt/orientation that four-float root movement cannot express, at the unchanged qualified patch. Measure snapshot tick/age and feet/deck relationship. A rigid first board is explicitly a restricted proof, not MW2 skinning parity or complete rider acceptance.
3. **Prove visible lifetime and recovery together.** On normal dismount and each bounded fault, discard old snapshots/queued draws, delete only the owned board, release only the model reference requested by this ride, clear ownership, and preserve the existing camera/control/unfreeze recovery. Cleanup must be repeatable and reachable from the independent rescue path, including when a preceding cleanup call throws. Confirm no board survives refusal, cancellation, worker stall/exit, stale/invalid pose or script failure, and remount creates only one board. For a custom draw route also prove reset/resource retirement, no post-dismount render and restored GPU state. Source checks cannot establish these behaviors.
4. **Then compare rider mappings without choosing appearance.** Use solved-pose debug markers first to validate named joints, frames and foot contacts. Compare a GTA bind-based retarget with a separately skinned Skate rig. For the GTA route prove a CE bone write phase; for the separate route first prove one world-space triangle/board, wall occlusion, camera alignment and draw-state restoration on CE. Only then evaluate animated push/turn/contact snapshots and restoring native ped animation/visibility. Failed interface proofs should stop that route, rather than silently downgrade the game or approximate a solved pose with canned clips.

Real-game proof must name exact source and installed build, distinguish preparation from launch and visible behavior, and keep captures/assets/private diagnostics local. This container established source reading only. Validation before commit: `python3 scripts/verify.py` passed 62 tests and local-link/context checks across 60 documents; `python3 tools/sandcastle/acceptance/research_report.py research/results/gtaiv-120059-board-rider-interface.md` passed; `python3 tools/sandcastle/acceptance/markdown_links.py` passed. These ran repository-owned checks only, not downloaded source. The host's fresh Standards/Spec reviews assess citation support separately. Their approval would still be research acceptance, not Windows qualification, gameplay acceptance or permission to close #20/#21/#22.

<research>
{
  "verdict": "requires-local-proof",
  "runtimeVerified": false,
  "sources": [
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/README.md",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/mashup-mods/SKILL.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/choosing-a-mashup-route.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/collision-and-combat-bridging.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/evidence-levels-for-mashup-claims.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/in_process.rs",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/bin/worker.rs",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/wire.rs",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate.js",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate_watchdog.js",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/accepted_pose.rs",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/converter/iw4l_skate_convert.py",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/skate_board.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rig.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/occupancy/remote_body.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json",
      "revision": "34bedee0be2f57047ed8f0705c81f137ede3d3ce"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/README.md",
      "revision": "83dcdfe2dd710d1b51d65dd7f3644f82b365e406"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/dllmain.cpp",
      "revision": "83dcdfe2dd710d1b51d65dd7f3644f82b365e406"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/Render.cpp",
      "revision": "83dcdfe2dd710d1b51d65dd7f3644f82b365e406"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/render/World.cpp",
      "revision": "83dcdfe2dd710d1b51d65dd7f3644f82b365e406"
    },
    {
      "url": "https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md",
      "revision": "dddbd3f54b146bdb3a9852809e48e5cb169af3cd"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/README.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/um/cli.py",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/geometry-transfer-host-draws-guest-meshes.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    }
  ],
  "unknowns": [
    "Exact CE object native/model-loading behavior and reliable owned-object cleanup.",
    "Solved board pivot/joint conventions and full-pose transport are not implemented in the inspected GTA boundary.",
    "GTA bind-based retargeting and a CE live bone write phase remain unqualified.",
    "CE D3D9 draw scheduling, depth/camera integration and renderer lifecycle remain unqualified.",
    "Owner appearance/scope preferences and all new Windows runtime evidence remain pending."
  ],
  "inaccessibleSources": [
    "Universal Modder CLI/kb search unavailable; inspected pinned public source instead.",
    "LuaModLoader linked public source https://github.com/Zalgo-Dev/LuaModLoader returned 404; site claims not upgraded to source qualification.",
    "OpenIV https://openiv.com/?page_id=384 timed out; exploratory https://openiv.com/?cat=24 returned 502.",
    "Guessed CLEO docs intro.md/gtaiv.md returned 404; actual introduction.md resolved and inspected.",
    "Owned assets, native binary/provider and Windows runtime intentionally not accessed under source-only scope."
  ]
}
</research>
