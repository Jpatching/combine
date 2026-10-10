# GTA IV Complete Edition 1.2.0.59: bounded Skate street contact route

Issue #45, source research, 2026-10-10. **Verdict: requires-local-proof; runtimeVerified=false.** Retained decoded physical collision is the smallest credible supplier of static floor, slope and curb triangles to the existing Skate Session. Host queries should first provide an independent comparison oracle. The inspected public interfaces do not establish a qualified 1.2.0.59 segment-hit/normal API, so native reconstruction is still an investigation route. A documented loader and a finite ground height cannot fill that gap. No street candidate is accepted by this report.

This delegated background researcher followed the supplied Matt research steps: primary-source reading, one cited report in the existing results directory, no nested agents. The checkout was clean at task base `82d35ad1e43620389abb69fa6bcb591cca1d6279` on `research/gtaiv-street-contact-route`. HANDOFF describes the earlier dispatch setup; its [live issue #44](https://github.com/Jpatching/combine/issues/44) records the merged setup and current research authority. Only this report is changed. No downloaded code was executed, dependencies installed, private resources accessed, game launched/controlled, binaries analyzed, or tracker mutations performed. Version, placement, mounting guard and retained candidates are preserved. The host owns fresh Standards/Spec review and linking findings; implementation issues remain open. This is a decision input, not an implementation spec or Windows/gameplay qualification.

## Verified source facts

### Retained evidence and actual adapter

The requested [latest riding observation](https://github.com/Jpatching/combine/issues/20#issuecomment-6098478199) attributes partial forward movement to the owner, with no visible board/Skate animation. It records sustained mounting followed by requested cleanup, zero observer-start markers, a later `over-0.05-metres` refusal, and a stale-status refusal. It does not establish measured push/steering or full-loop acceptance. Its 5×5 guard surveys an 8-unit square; metre scale is an assumption. These are attributed prior observations, not runs by this researcher.

The unmerged candidate was **explicitly fetched as public text** from full commit `fd9f8c4933d3aed193273a2ce5d78fb076886972`, rather than assumed to exist in this main-based clone. Its [riding script](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate.js) obtains `GET_GROUND_Z_FOR_3D_COORD`, checks finite values and plausibility against ped height, then sends 25 grid samples. It rejects sample deviations above 0.05 m. Those checks do not expose a separate query-success or collision-loaded result. Its [Surface implementation](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/connection.rs) validates grid placement and near-flatness, triangulates the 16 cells into 32 triangles, maps relative GTA coordinates to Skate `(dx, dz, -dy) * scale`, and confines riding inside the patch with ground-height checks. This representation has one height per horizontal sample, with no vertical curb face, wall, underside or multiple layers at one horizontal location. Small sampled height variations are possible; arbitrary street slopes/curbs are outside this guard's contract.

The [in-process path](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/in_process.rs) passes those Surface triangles and empty rails to Session, then checks containment before/after stepping. The [worker path](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/bin/worker.rs) also consumes Surface triangles, using the collision builder/install seam when replacing an active surface. Neither path imports the retained decoded street mesh. The [plugin](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/plugin.cpp) gates file version 1.2.0.59 and host ID, binds CLEO commands/callbacks and adapter functions; it supplies no host segment-hit/normal query. Its script-thread checks are adapter protections, not an audited GTA physics-query lifetime contract.

### Retained decoded physical geometry and placement

The candidate [bounded decoder](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-collision/inspect_resource.py) reads a bounds resource with strict magic/type/codec, span/count/pointer checks and finite coordinates. It unquantizes geometry/BVH vertices in RAGE coordinates, validates indices and nondegenerate triangles, splits quads, and supports composites containing geometry/BVH children with rigid, orientation-preserving matrices. It applies those child matrices. Nested composites, primitives, index flags, differing internal/current transforms and nonrigid transforms are refused; dictionary/model-bound association is not implemented. A successful structural result does not attest world placement or host activation. Stored polygon normals are validated but not returned as authoritative host contact normals.

The [retained resource-placement report](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-09-gtaiv-resource-placement.md) reports private provenance/count checks and exactly identity child matrices for this resource only. The later [checkpoint preparation](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md) retains R1 ordinary road, P1 paved margin, H1 lower approach and H2 upper approach. Different endpoint heights do not establish a continuous slope. The [latest tooling account at the requested revision](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-10-gtaiv-checkpoint-tooling.md) records owner location confirmation but incomplete exact surface/layer associations, including an inadequate H1 view. No paired GTA readings exist there. Those reports are attributed local evidence summaries; private data was not accessed or reproduced here.

Pinned GTA4Unity's [composite reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs) enumerates geometry and primitive children but omits child matrices and nested composites. Its [geometry reader](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundGeometry.cs) unquantizes vertices and maps to Unity `(-x,z,-y)`. Its [collision builder](https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/CollisionBuilder.cs) selects cached WBNs, merges geometry, reverses winding for Unity, creates colliders at identity and catches per-file exceptions. It ignores primitives and can announce ready despite skipped files. Identity child matrices make one omission inert for the retained input, not generally safe. The viewer is a placement-inspection helper; it does not establish currently loaded GTA collision. Do not transfer its Unity axis/winding changes blindly to Skate or apply an arbitrary WPL transform to static WBN geometry.

### Pinned Skate/MW2 comparison

At `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, the [MW2 extractor](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs) uses physical ClipCollision, including selected mesh partitions, brushes and placed static-model collision. It filters contents, handles model transforms, corrects winding, derives rail candidates and maps MW2 inches to Y-up metres with factor 0.0254. That factor is MW2-specific, not a GTA unit calibration. The [MW2 Session integration](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs) supplies extracted world triangles/rails to Session and uses off-thread preparation plus replacement for Minecraft block collision. This is source evidence of a reusable consumer, not an exact GTA adapter or a run reproduced here.

The [Session bridge](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs) accepts arbitrary triangle batches and rail polylines through `Session::new`, `collision_builder().build` and `install_collision`. Replacement takes effect from the next tick according to its source comment. It builds one material/surface mapping rather than preserving GTA material/neighbour semantics. This is a whole-world prepared replacement seam, not a per-GTA-entity mutation or host ray callback. The [collision compiler](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/skate_world.rs) derives cross-product normals, uses 1 mm welding for adjacency and treats portable faces as one-sided; winding, degeneracy and narrow geometry matter. The [physics setup](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics.rs) documents map spawn as a wheel-ground anchor in native Y-up metres. Geometry ingestion is supported in source; GTA contact fidelity, grindability and moving-body response are unproved.

### Native queries and modding interfaces

[CLEO Redux's introduction](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md) explicitly lists Complete Edition 1.2.0.59. Its [SDK header](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h) exposes command registration, numeric I/O and before/after-script/init callbacks. This documents entry and scheduling plumbing; it specifies no GTA segment result, physics lock or loaded intended-surface guarantee.

The pinned [Sanny GTA IV definitions](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json) describe `GET_GROUND_Z_FOR_3D_COORD` as three float inputs and one ground-Z output. The inspected definition does not expose an explicit success output, normal, segment endpoints or fraction. `REQUEST_COLLISION_AT_POSN` requests collision, and `LOAD_ALL_OBJECTS_NOW` is a streaming command; neither definition certifies successful loaded intended-layer contact. No general full segment-hit/normal query was identified in this catalog. This is a bounded catalog finding, not proof that the exact executable has no such routine. Per-command exact-version semantics, Z-selection rules, miss values and loaded-state guarantees remain unknown. Do not infer GTA V native behavior for IV.

LibertyCraft provides concrete older-version prior art: [boot code](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/dllmain.cpp) accepts 1070/1080; [IV-SDK README](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md) explicitly supports only those EFIGS versions and describes major differences elsewhere. Its [CWorld wrapper](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/include/CWorld.h) supplies ProcessLineOfSight, but is not a CE ABI qualification. LibertyCraft's [ray code](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h) queries static/building collision, with separate object probing. Creator comments describe 1.0.8.0 hit position, normal and fraction, one-sided hits, game-thread requirement and inconsistent fractions when starting within roughly 1–2 cm of faces. It validates distance/fraction consistency but that alone does not establish signed segment bounds or collinearity. The [scheduler](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Collision.cpp) incrementally budgets acquisition; a between-call deadline cannot interrupt a slow call. This supports design comparison, while explicitly excluding the supplied plugin as an unchanged 1.2.0.59 solution.

### Universal Modder: useful helpers, missing runtime interface

The pinned [mashup skill](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/mashup-mods/SKILL.md) and [route selection](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/choosing-a-mashup-route.md) support rebuilt Skate inside the real host and planning an oracle. Its [collision guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/collision-and-combat-bridging.md) separates geometry acquisition, representations, direction and streaming freshness. Its [evidence guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/evidence-levels-for-mashup-claims.md) separates source reading from real runs. These supplied method sources were also fetched at their immutable revision; their instructions do not widen this report's authority.

Universal Modder's [README/tool inventory](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/README.md) documents `um kb` for prior-art search, `um scan` for version/engine reconnaissance, native investigation playbooks, `um win` capture/control and `um publish check`. These helpers can aid later authorized evidence collection, provenance and research. Art/video/asset tools do not acquire contact. The listed GTA V example is another host. No exact IV 1.2.0.59 segment interface is established by this inventory or its cited LibertyCraft example. `um` is absent from PATH here; no CLI, native-analysis provider or Windows helper was installed or used. Generic orchestration cannot replace a missing, exact-build GTA collision contract.

## Source inference

**Prefer retained static physical triangles as the next supplier candidate, paired with an independently qualified host oracle.** This reuses the actual Session ingestion seam and retained resource, preserves multiple layers and vertical faces when they are decoded, and avoids inventing city geometry from a sparse height grid. It remains conditional on complete bounded coverage, world placement and host comparison. It does not select worker versus in-process architecture or rider appearance/scope.

| Route | Floor/slope/curb coverage | Placement and height layers | Streaming, normal and segment limits | Disposition on exact 1.2.0.59 |
| --- | --- | --- | --- | --- |
| Retained decoded physical bounds → Session | Decoded triangles can represent floor, slope and vertical curb; retained four heights alone do not prove all three are present/continuous. Unsupported children remain unavailable. | Preserve resource and child transforms; calibrate GTA units and axis/winding exactly once. Distinct layers remain distinct, but intended association is still pending. | Offline retained mesh does not track active host variants, traffic/doors or unloads. Cross-product normals are geometric, not host-measured. Session requires bounded installed support. | Smallest source-supported static supplier candidate; requires local proof. |
| Existing native ground grid → Surface | Sparse near-flat support only. Connecting top samples can fabricate a ramp across a curb/gap; no vertical face. | World coordinates come from host queries, but unknown Z-selection/loaded semantics can choose another layer. Finite values are insufficient. | No segment, normal, underside or completeness guarantee. Its fixed guard appropriately refuses wider variation. | Existing bounded adapter; unsupported as proof of floor/slope/curb street contact. |
| Qualified native segment probes → reconstructed triangles | Potential host-active floor/slope/curb samples; thin faces and corners can fall between probes. Reconstruction must not bridge holes. | Can discriminate layers with directed endpoints only after semantics are qualified; no universal highest-ground rule. | Needs exact CE ABI, phase, filtering, availability, sidedness, segment validation and bounded latency. Unknown must differ from empty. Old-version near-face issues are hypotheses for CE testing. | Technically plausible prior art; CE interface still unknown, not ready to implement from these sources. |
| Loaded bound traversal/modding SDK | Could preserve physical geometry and current transforms if a compatible traversal existed. | Needs exact layouts and instance/child transforms, activation and identity. | Native locks/lifetimes, unload invalidation and copying by value are unqualified. Old SDK addresses are inapplicable. | No qualified CE loaded-bound traversal found in inspected scope. |

Coverage must mean the complete floor/slope/curb envelope needed by the bounded ride, including adjacent support and clearance, not merely resource counts or overlay pixels. Keep unknown, stale and unsupported coverage distinct from validated empty space. An offline mesh might remain available after host unload, or disagree with an active scripted variant. Whole-world replacement must retain adjacent support and reject stale preparation; replacing a batch does not prove moving-body velocity/friction or collision sweeps. These are derived requirements from the inspected decoder, Session replacement and old acquisition route, not runtime measurements.

The comparison oracle must establish **query_success**, **ground_loaded** and **intended_surface** independently of numerical closeness to the decoded prediction. Filling these flags from `Number.isFinite`, a streaming request, nearby positive queries, visual flatness or the prediction itself would make the comparison circular. A finite fallback/stale/default height can coincide with the mesh and still be unavailable. Correct top-surface height likewise says nothing about a vertical curb normal. A ray is not a wheel/body sweep and cannot alone establish Skate collision response.

## Unknowns

- Exact CE ground query success/miss behavior, loaded-state evidence, Z-selection, units and intended-layer qualification. The current script/catalog do not settle these.
- Complete R1/P1/H1/H2 anchor-base surface association, especially H1; this report reads the requested immutable snapshot and public comments, not private imagery.
- Whether the retained resource provides all floor, continuous slope, curb riser/top and boundary support required by a bounded street, and which decoded faces are physically active in this CE scene.
- GTA-to-Skate scale, winding/normal orientation, seam behavior and contact correctness after Session ingestion; material and rail semantics are not preserved automatically.
- A safe exact 1.2.0.59 segment query or loaded-bound traversal, including ABI, result validity, physics phase, filters, streaming availability, lifetime and timing. Source absence in inspected interfaces is not impossibility.
- Dynamic vehicles/doors, unload/reload and failure recovery, presentation and owner riding acceptance remain separate unproved behavior.

Access record: GitHub web rendering of the requested candidate tree failed with a cache miss; direct public GitHub API tree and immutable raw files succeeded. The `gh` CLI is absent, so public issue bodies/comments were read through GitHub's unauthenticated API. No evidence source was substituted with a secondary summary. The owned executable, private resource, coordinates, settings, logs and runtime were intentionally unavailable under source-only scope. Native binary analysis and `um kb search` did not run. No inaccessible source is treated as negative proof of CE capability.

## Next local proof

The smallest next proof is a **read-only retained-point comparison**, after completing the existing surface/layer prerequisites and establishing an explicit exact-version host observation contract. Reuse the owner-confirmed location and unchanged resource; obtain clear local anchor-base evidence for every retained point, including H1, without shifting geometry or points to improve agreement. If intended layer or query success/loading cannot be established, stop as inconclusive before collecting apparent successes. This proposed next task needs its own local authority; nothing here authorizes launch, installation or native analysis.

Reuse [street qualification #39](https://github.com/Jpatching/combine/issues/39) and the candidate [comparison command](https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-collision/compare_ground.py): freeze the exact four retained points and mesh predictions; collect **three valid readings per point** at identical fixed horizontal coordinates. Every reading must be explicitly successful, loaded, finite and on the independently identified intended surface. Require maximum-minus-minimum spread **≤ 0.02 m** and **every** absolute vertical error **≤ 0.05 m**, both inclusive. No offset fitting, averaging away failure, fallback heights, point dropping or guard widening. Any stable valid point exceeding error tolerance gives **disagreement**, even if another point is unavailable; all four complete passing points give **agreement**; otherwise **inconclusive**. The command trusts supplied qualification flags; authored command checks do not certify a native collector. This gate proves **point ground agreement only**, not continuous slope, curb/wall contact, whole-resource activation or gameplay.

After that gate, the separate **floor/slope/curb contact proof** must include both geometry comparison and actual consumer response before accepting a street candidate:

1. Privately freeze one bounded static envelope from the same resource, with independently identified floor, a continuous slope including transitions, and a curb's lower approach, riser and top. Audit complete child/face coverage, placement, unsupported geometry, units and winding. Keep height layers separate. If the retained candidate lacks a necessary feature, report that limit rather than invent a curb or select a new scope silently.
2. Establish a qualified exact-CE contact oracle capable of directed vertical, slope-normal and horizontal curb segments. Freeze expected surfaces, clear misses, directions and position/normal/segment validity bounds before measurement. Compare repeated floor/slope/riser/top observations with the unchanged decoded geometry; check signed segment membership, collinearity, normal orientation, one-sided behavior, near-start behavior and clear gaps. Loaded intended-surface success is mandatory. A ground-only API cannot complete this stage. If public interfaces remain insufficient, a separately authorized bounded local exact-build interface investigation must resolve the ABI/thread/availability contract first; do not guess older SDK calls.
3. In a separately authorized isolated trial, feed the audited bounded triangle batch through the pinned Session seam and demonstrate actual support on the floor, traversal of slope/transitions and contact with the curb riser/top as appropriate to the predeclared maneuver. Check penetration, tunneling, seam snagging and unintended layer switching. A successful cast is geometry evidence, not wheel/skater response. Predeclare response and timing criteria before the trial, using independent known geometry to calibrate the oracle; this report does not invent a gameplay acceptance spec or claim a pass.
4. Prove bounded availability/coverage throughout that trial, stale/unavailable refusal, dismount and native GTA recovery, then repeat under the agreed restart/loading conditions. Include failures and refusals. Keep moving traffic/doors, grind rails and broader city coverage outside the static contact claim. Board/rider presentation, full riding-loop evidence and owner acceptance remain separate decisions.

Do not widen the existing mounting tolerance to admit slope or curb samples. That would retain the height-grid limitations while weakening refusal. A later reviewed contact-aware integration would need its own explicit safety contract; it is not authorized by this report. The competing native route becomes supportable only after exact CE segment and availability proof; the old-version SDK remains unsupported unchanged. Retained static geometry is the most economical source candidate, while its host agreement and contact response remain unverified.

Verification: only public text and repository documentation were inspected. `python3 scripts/verify.py` passed 62 tests and 60 document/context checks after the reviewed new report was staged; its initial untracked-context refusal was resolved by staging only this report. The report structural acceptance and external Markdown-link acceptance checks passed. These checks do not test game contact. Fresh source-support Standards and Spec reviews are the host's next acceptance steps. No runtime or Windows qualification is claimed.

<research>{
  "verdict": "requires-local-proof",
  "runtimeVerified": false,
  "sources": [
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/combine_skate.js",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/src/connection.rs",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
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
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-skate/plugin.cpp",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-collision/inspect_resource.py",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-09-gtaiv-resource-placement.md",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/research/results/2026-10-10-gtaiv-checkpoint-tooling.md",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    },
    {
      "url": "https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs",
      "revision": "c107e46cf8ab4e3d42f9c0bf685f80bb732a3609"
    },
    {
      "url": "https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundGeometry.cs",
      "revision": "c107e46cf8ab4e3d42f9c0bf685f80bb732a3609"
    },
    {
      "url": "https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/CollisionBuilder.cs",
      "revision": "c107e46cf8ab4e3d42f9c0bf685f80bb732a3609"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/skate_world.rs",
      "revision": "f608f85e407ff1b7689d54a9aafdd16e95711ac4"
    },
    {
      "url": "https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics.rs",
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
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/dllmain.cpp",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md",
      "revision": "dddbd3f54b146bdb3a9852809e48e5cb169af3cd"
    },
    {
      "url": "https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/include/CWorld.h",
      "revision": "dddbd3f54b146bdb3a9852809e48e5cb169af3cd"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Collision.cpp",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
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
      "url": "https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/README.md",
      "revision": "8370faa8e114baf33acdb23079aff552a7728c4b"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/fd9f8c4933d3aed193273a2ce5d78fb076886972/tools/gtaiv-collision/compare_ground.py",
      "revision": "fd9f8c4933d3aed193273a2ce5d78fb076886972"
    }
  ],
  "unknowns": [
    "Exact CE query success, loading and intended-layer semantics remain unqualified.",
    "Retained point surface association, continuous slope/curb coverage and active host geometry require local proof.",
    "Exact CE segment interface, units, normals, streaming and Session contact response remain unverified."
  ],
  "inaccessibleSources": [
    "GitHub web rendering of fd9f8c4933d3aed193273a2ce5d78fb076886972 tree failed with cache miss; public API and raw sources succeeded.",
    "gh and um CLIs unavailable; public issue API used, no tools installed.",
    "Owned executable, private resources and runtime intentionally unavailable under public-source-only scope."
  ]
}</research>
