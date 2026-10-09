# Next proof for Skate interacting with GTA IV's world

Preparatory public-source assessment for [#28](https://github.com/Jpatching/combine/issues/28), 2026-10-09. The owner selected Universal Modder's rebuilt guest engine in a real host route. **The next decision is whether the retained GTA IV 1.2.0.59 baseline can supply trustworthy nearby collision to the pinned Skate Session.** A refusal by the existing flat-patch candidate does not answer that question.

## What the guide recommends and what can be reused

Universal Modder separates acquisition of host geometry, conversion for the consuming simulation and freshness as the world moves. Its GTA IV example uses incremental line probes and nearby-object sampling; its rebuilt-engine examples include physical collision volumes and a separate moving-prop layer. These are host-specific implementations, not a supplied GTA/Skate adapter. Creator demonstrations remain reports. [Collision guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/collision-and-combat-bridging.md), [rebuilt-host guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/rebuilt-guest-engine-inside-a-host.md).

LibertyCraft supplies a useful **source model**: game-thread `CWorld::ProcessLineOfSight` calls, explicit static-building flags, finite-hit and segment-consistency checks, floor/ceiling/wall reconstruction, triangle winding and separate object probes. Its synthetic tests exercise an awning, room, overpass and stairs. The tests demonstrate intended checks in source; they were not run in this assessment. Its Minecraft voxel representation should not be copied indiscriminately: our pinned Skate Session accepts triangles and rails, with collision replacement interfaces already audited. [Rays](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h), [geometry builder](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Geometry.h), [synthetic cases](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/tests/collision_test.cpp), [existing interface audit](2026-10-09-repository-interface-audit.md).

## Exact-version gap

LibertyCraft's boot code accepts only 1070/1080. Its ray header explicitly attributes result offsets, flags, one-sided hits and near-face inconsistencies to measurements on **1.0.8.0**. Neither those addresses nor that structure layout is qualified for 1.2.0.59. Reusing its plugin unchanged or copying offsets is unsupported. [Version gate](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/dllmain.cpp), [ray contract](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h).

CLEO Redux documents 1.2.0.59 and provides registered commands, typed parameters and runtime callbacks. That is an integration entry point; its inspected SDK does not establish a qualified line-query collision interface. The retained adapter's `GET_GROUND_Z_FOR_3D_COORD` height samples and flatness guard provide no evidence for vertical walls, multiple surface layers or moving objects. [CLEO supported versions](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md), [SDK](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h), [retained adapter](https://github.com/Jpatching/combine/blob/c87e59471c34aff6ffcae5f23b8afc320ca6bd09/tools/gtaiv-skate/combine_skate.js).

## Alternatives and order

| Approach | What it could answer | Work still required |
| --- | --- | --- |
| Exact-version live line queries, then local triangle reconstruction | Can streamed host surfaces become collision usable by Skate? | Qualify calling interface, flags, result interpretation, main-thread scheduling, sampling coverage and timing on 1.2.0.59. Thin geometry and unsampled space remain hazards. |
| Extract physical collision from owned game data or traverse loaded collision structures | Can existing physical meshes avoid sampling approximation? | Establish formats/layouts, instance transforms, winding, streaming/lifetime and moving-entity handling. Static exports alone cannot describe traffic or current doors. No compatible extraction implementation was established here. |

**Recommendation:** investigate an exact-version query contract first, because the cited GTA example supplies a bounded public implementation to compare. This is a test-order inference, not a final architecture choice. If no trustworthy interface can be established, evaluate extraction against the same scene tests. LibertyCraft's `dump_collision.py` only reads its live bridge's already-produced triangles/voxels; it is not a GTA asset extractor. [Tool source](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/tools/dump_collision.py).

## Smallest decisive probe

First complete the existing research prerequisite and identify a reviewed, exact-version query interface. Then prepare one observation-only probe on the retained baseline, with no Skate ownership transfer. Its command should classify a known floor, a wall and an overhang with space underneath, plus a clear miss. Cast both relevant directions to expose one-sided behavior; repeat from separated start positions to expose near-face artifacts. Keep raw positions and owned geometry local. Publish only bounded validity, classification, repeatability and timing summaries.

Proposed pass: all intended hits/misses are repeatable across three batches; hit positions and normals are finite, segment fractions agree with positions, normals have a declared orientation, floor and ceiling remain distinct, and each bounded batch meets an explicitly chosen main-thread budget. Tolerances and budget must be recorded before execution, justified by the baseline and expected skating speed. Missing or stale regions must report unavailable, never empty.

Proposed stop: unknown call/layout, inconsistent results, unbounded work, unavailable surface represented as empty, or host instability. A pass establishes an acquisition candidate only. The next proof then converts that small scene into correctly transformed/wound triangles for the **real pinned Session**, tests a slope, wall and underside, and validates replacement freshness. Moving traffic, rails, materials and broad-city streaming remain separate follow-up requirements. Hand-over and failure recovery from the [existing proof contract](2026-10-09-guide-driven-proof.md) remain necessary for playable riding.

## Evidence and blocker

Inspected clean public-source snapshots at the revisions cited above and the retained adapter Git object; attempted web access to exact source pages returned cache misses, so local exact-revision source supplied those observations. No builds, runtime probes, extraction, private-data reads, installs, configuration changes or pin changes were performed.

**#20's separate collision-feasibility research prerequisite remains unmet.** No connected research/native analysis tools were available to this assessment. This note prepares that investigation and its experiment; it does not satisfy the required separate research-capable Sandcastle session or claim GTA 1.2.0.59 collision compatibility.
