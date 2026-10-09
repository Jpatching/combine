# GTA IV 1.2.0.59: native collision-query feasibility

Source-only research for Issue #31, 2026-10-09. **Verdict: requires-local-proof. Native artifact investigation is still required before proposing an executable collision probe.** CLEO Redux documents this exact game's loading/scripting route; the inspected public sources do not establish an exact-version interface returning a segment hit and surface normal. LibertyCraft supplies a concrete older-version reference, explicitly excluded as an implementation for 1.2.0.59. This report establishes neither usable world collision nor gameplay acceptance.

Scope: the separately delegated researcher owns only this report on `research/gtaiv-native-collision`, starting at `1db98bdf0cd567548da3394d058c779c8be10dcc`. The host retains dispatch qualification, independent reviews and publication. Public [issue #30](https://github.com/Jpatching/combine/issues/30) is closed; the [#31 dispatch comment](https://github.com/Jpatching/combine/issues/31#issuecomment-6085527845) records the host's readiness checks. Those are attributed coordination evidence, not game evidence. The working HANDOFF still describes #30; the current assignment selects #31. No nested agents, installs, downloaded-code execution, game control, private assets, live hooks, uploads, pushes, pin changes or flatness changes occurred. Matt's supplied research steps were followed by this background researcher; an installed `ask-matt` command was not available or claimed to run.

## Verified source facts

### Context and guidance provenance

The unmerged prior [next-proof report](https://github.com/Jpatching/combine/blob/d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad/research/results/2026-10-09-world-collision-next-proof.md) recommends investigating the query contract first and preserving the existing baseline. The accompanying [repository-interface audit](https://github.com/Jpatching/combine/blob/d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad/research/results/2026-10-09-repository-interface-audit.md) distinguishes a documented CLEO loader from a compatible collision interface. Both were fetched at the full resolved revision above; neither was assumed present on main.

Universal Modder's [mashup skill](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/mashup-mods/SKILL.md) recommends selecting the route and planning an oracle before building. Its [route guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/choosing-a-mashup-route.md) classifies rebuilt Skate in a real host separately from two-real-game passthrough, and requires host-specific game-thread and collision investigation. Its [collision guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/collision-and-combat-bridging.md) describes LibertyCraft acquisition as incremental line probes plus nearby-object sampling, separates representations and directions, and warns about filling arches and treating unknown regions as empty. Its [evidence guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/evidence-levels-for-mashup-claims.md) separates creator reports, source inspection, proposals and real runs. These are methodology sources; their example descriptions were traced to LibertyCraft source below, not treated as GTA compatibility documentation.

**Provenance discrepancy:** all four raw public files at the requested revision were retrieved and read, but their byte hashes differ from the values supplied in the task. LF normalization did not reconcile them. Supplied text remains task context; public bytes are independently cited evidence. This researcher cannot attest that the host-supplied guidance bundle is byte-identical to the public pin, or diagnose why. The host should resolve that discrepancy before claiming pin-integrity qualification for this run.

| File at the cited Universal Modder revision | Supplied SHA256 | Retrieved raw-byte SHA256 |
| --- | --- | --- |
| `skills/mashup-mods/SKILL.md` | `9d881c6bee592b3b6efe1fbd0e61722d887c63df3af319ef01d4999fda2e02f8` | `abb75f8864c0e05cbf55a6beee75bf7d2accd07c1f4054c5d928a2490a856104` |
| `knowledge/techniques/choosing-a-mashup-route.md` | `bbd2bcde55001e283f85718258a2363f95941d23cd9f74d0403010360416d1e2` | `e2fd4a2d77cab5dfc1ee788245f33a4c16044131db7806cc7f7ef175809a2d98` |
| `knowledge/techniques/collision-and-combat-bridging.md` | `ac93f3e6f85b00af30dc7a1bd2537151d13b219489da08567bfd314dd9358d3b` | `26163d274bd16400123172d0a535c2be7994c4877169dd16940edaf3ec996c30` |
| `knowledge/techniques/evidence-levels-for-mashup-claims.md` | `19f164907973771f8e3de66c3e28466a93b3fa4302fb24f7e891eb18fb9e6058` | `089e4aa7b4417ed894889cd86a0845d45d0352d207031608e4580f3106104742` |

### LibertyCraft's actual query contract: reference only

The [plugin version gate](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/dllmain.cpp) accepts executable versions 1070/1080 and reports other versions inactive. It registers `Game::Tick` on `processScriptsEvent`. The [plugin README](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/README.md) names 1.0.8.0 as supported and 1.0.7.0 as expected to work. This is explicit evidence against using its supplied plugin unchanged on 1.2.0.59.

The [ray implementation](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h) zeroes its result buffer and invokes:

```cpp
CWorld::ProcessLineOfSight(&from, &to, nullptr, &result,
                          STATIC_COLLISION | BUILDINGS, 1, 0, 0, 4);
```

The SDK dependency pinned by LibertyCraft's gitlink is `Zolika1351/iv-sdk` at `dddbd3f54b146bdb3a9852809e48e5cb169af3cd`. Its [CWorld header](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/include/CWorld.h) defines a nine-argument `__cdecl` wrapper, with a `uint32_t` underlying return converted to `bool`, a `0x54`-byte result, and flags `STATIC_COLLISION=2`, `BUILDINGS=4`, `VEHICLES=8`, `PEDS_BOUNDING_BOX=32`, `PEDS_COLLISION=64`, `OBJECTS=128`. Thus the static-map mask in the reference is 6; no peds, vehicles or movable objects are requested. The see/shoot parameter is zero, disabling those exemptions; SDK comments assign bits 1/2 to see/shoot-through checks. These values and that ABI are **older-version source facts only**, not proposed CE constants.

Result fields in that header, interpreted by LibertyCraft's ray code:

| Reference byte offset | SDK storage | LibertyCraft interpretation/evidence |
| --- | --- | --- |
| `+0x00` | physics-instance pointer | Hit-instance identity; not safe to retain across streaming |
| `+0x10` | `m_vEndPosition` | Hit position |
| `+0x20`, `+0x30` | `m_vUnk`, `m_vUnk2` | Face unit normal and a copy, per creator's 1.0.8.0 measurement comment |
| `+0x40` | `m_fUnk1` | Segment fraction, per the same comment; used in validation |
| `+0x44` | `m_fUnk2` | Remaining distance, per the same comment |
| `+0x48` | `m_nUnkFlags4` | Low byte used as surface-material index, per creator measurements |

The code's comments attribute these interpretations to measurements on **1.0.8.0**: true means hit, argument `nUnk1=1` is necessary, BUILDINGS carries city collision, rays are one-sided, and starts within roughly 1–2 cm of a surface can yield inconsistent results. Those measurements were not reproduced here. `HitToMc` rejects nonfinite combined position/normal values or a discrepancy between `fraction * length` and start-to-hit distance greater than `0.05 + 0.001 * length`; rejected positions become NaN. That radial-distance test alone does not establish collinearity or signed segment bounds. The code maps GTA `(x,y,z)` to Minecraft `(x,z,-y)`; this mapping is not a Skate contract.

Object-only casts are a separate path with at most four passes, identity filtering and 2 cm skip-ahead. If the physics instance is absent, LibertyCraft counts the unknown hit as the target. That permissive behavior should not be inherited by an observation probe. Material IDs and entity layouts are unnecessary for the first static-scene proof. All these findings come from the ray implementation cited above.

The [collision scheduler](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Collision.cpp) uses a 2,500 microsecond frame deadline, reserves 800 microseconds for pending object work, probes on `Collision::Update`, and transfers completed data to a worker for geometry construction/transport. The [game tick](https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Game.cpp) calls that update. The ray header explicitly says physics queries belong on the game thread and are unsafe from another thread. This is source architecture and a creator safety assertion, not independently established CE synchronization. Time checks between queries cannot interrupt one slow native call.

### Exact-version CLEO support versus collision support

[CLEO introduction](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md) explicitly lists GTA IV Complete Edition 1.2.0.43 and **1.2.0.59**; the [changelog](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/CHANGELOG.md) records 1.2.0.59 support added in CLEO Redux 1.1.1. This is documented loader/runtime support, without a collision-query guarantee or a real run in this container.

The [SDK header](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h) supplies `RegisterCommand`, float input/output, `OnBeforeScripts`, `OnAfterScripts`, and `OnRuntimeInit`. Header comments place before/after callbacks in the main-loop script iterations and init callbacks at new-game/load/runtime initialization. `GetHostId` distinguishes IV, but does not attest the exact executable build. [script API](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/api.md) documents `CLEO.hostVersion` and native-name dispatch through Sanny definitions. The [plugin SDK guide](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-sdk.md) describes extensibility and DLL plugin loading. None of these inspected interfaces specifies a CE collision result structure or guarantees that its callback is a safe physics-query phase. Source/API checks can identify host metadata and arrange a callback; local thread/lifetime proof remains required.

The [x86 memory-call guide](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-memory.md) documents address-based calls and stack cleanup for stdcall/cdecl. This is an invocation mechanism requiring an already justified address and ABI; it does not discover or validate either. Generic `GetSymbolAddress` in the SDK is similarly not documentation of an exported collision symbol.

The [Sanny GTA IV native definitions](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json) describe `GET_GROUND_Z_FOR_3D_COORD` with three float inputs and one ground-Z output. This interface lacks a segment, wall/ceiling normal and hit fraction. `IS_POINT_OBSCURED_BY_A_MISSION_ENTITY` is a volume/vehicle condition, not a general surface query. `REQUEST_COLLISION_AT_POSN` requests collision; it does not attest availability. Searching all command names in this file for line-of-sight/raycast/shape-test/probe terms found no full segment-hit-and-normal query. This is a bounded negative catalog finding, not proof that the executable has no such routine or undocumented native. The definitions' metadata does not qualify each command specifically on 1.2.0.59.

The [IV-SDK README](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md) documents only 1.0.7.0/1.0.8.0 EFIGS and says other versions are not planned because classes/functions differ. The [IV-SDK-DotNet README](https://github.com/ClonkAndre/IV-SDK-DotNet/blob/f5f5d63f705819525fe2f5307648661fb5613124/README.md) likewise limits support to those two versions. This comparison is limited to the cited sources; no claim about every public CE mod follows. No older-version address is reproduced here as a CE candidate.

## Source inference

**Recommended route to investigate:** retain CLEO Redux as the documented 1.2.0.59 script/plugin entry route; establish an independently verified CE segment query, then expose a small observation command from a reviewed x86 plugin at a proven safe game-thread phase. The SDK offers plausible input/output and scheduling plumbing. This is a proposed interface boundary, not a compatible implementation. Reusing LibertyCraft's validation ideas and bounded scheduling is defensible; copying its call, mask, layout or version gate is not.

Proposed record: request ID, executable qualification ID, scene/load epoch, frame/time, endpoints in GTA coordinates, status (`hit`, `miss`, `unavailable`, `invalid`), hit position, normal, fraction, validated category mask and elapsed time. Store results by value and do not export/dereference native pointers. All numeric fields must have explicit units, normal orientation and endpoint convention before use. An internal surface observation should not force streaming, alter entities or move the player. This report proposes no registry name or new production API.

Ground height alone cannot pass the wall/overhang test. A finite ray sample cannot prove complete mesh coverage, watertightness, sweep/capsule support, thin-object coverage, moving-door freshness or Skate contact fidelity. A successful native probe would justify a further acquisition experiment; it would not select worker versus in-process Session, replace physical extraction research #32, or satisfy gameplay #20.

## Unknowns

1. On the owned 1.2.0.59 executable: the collision routine or native registration, calling convention, pointer/alignment requirements, complete buffer size/write bounds, argument meanings, return/miss behavior, normal orientation, fraction semantics, filtering, and safe execution phase are unknown. No CE addresses, signatures or field offsets have been established.
2. Loader support does not settle physics-thread identity, reentrancy, synchronization during loads, or whether callbacks occur while physics/streaming structures are stable. CLEO public SDK/docs do not expose enough host internals to resolve this here.
3. A miss cannot distinguish empty from unstreamed space without an independently justified availability contract. Positive neighboring controls are useful evidence but not proof that an arbitrary volume is fully loaded.
4. Exact local query latency, failure behavior, one-sidedness, near-face artifacts, GTA-to-Skate units/axes, and suitable consumer tolerances require local proof. Native source assertions and old creator tests are insufficient.
5. Supplied Universal Modder hashes and retrieved public bytes disagree. Qualification provenance needs host reconciliation; the research conclusion remains bounded to the cited public contents and supplied task text.

Access limits: only public source/docs were fetched. The private owned executable, runtime and native REA provider were neither available nor accessed. `um kb search` was unavailable; no Universal Modder tool was installed or executed. The public CLEO repository supplied SDK/docs, not an inspected GTA host implementation resolving the physics-call contract. Exploratory public repository URLs `GTAmodding/IV-SDK` and `zalgo-dev/LuaModLoader` returned HTTP 404; they are not negative evidence about similarly named projects. The actual LibertyCraft SDK was resolved and inspected from its pinned gitlink. No secondary forum claim, other GTA game's SDK or compatibility-patch package was used to supply the missing interface.

## Next local proof

Everything below is **proposed future work**, requiring a separately authorized, local-only native investigation and then runtime trial. Nothing below ran here.

### Bounded native artifact question

For a locally identified, owned **GTAIV.exe 1.2.0.59**: does a side-effect-free segment query reachable from a proven script/game-thread phase return both hit position and surface normal? Inspect one candidate routine and its immediate call sites, or one native registration and its wrapper. Establish all arguments, return semantics, result buffer size/alignment/write ranges, normal/fraction fields, category filtering, and streaming/lifetime conditions independently from this exact binary. Use LibertyCraft/IV-SDK only as hypotheses for comparison. Prefer an existing documented native if found; otherwise record a build-bound local resolution with unambiguous identity/uniqueness and rejection of every other build. Do not search for a general merger or investigate unrelated gameplay systems.

Bound the initial REA pass to **one candidate, at most three immediate call sites, and two hours**. If ABI, output bounds or safe entry cannot be justified, return unresolved and stop; do not try guessed calls. Keep executable bytes, signatures, disassembly, addresses and identifying private logs local. Public output should be a source-safe contract summary and unresolved questions. No bypass, installation, patching, live hook or launch is authorized by this report. Provider readiness is a remaining blocker.

### Smallest observation scene and directed rays

Use one locally documented, already streamed static scene with an ordinary floor, a wall and a solid overhang with open space beneath. Avoid traffic, doors and glass in this first pass. The local manifest specifies expected surfaces and their visible normals before measured acceptance; independently inspect the scene locally, rather than using the tested query itself as ground truth. Keep coordinates and recordings private.

| Group | Segment purpose | Expected decisive evidence |
| --- | --- | --- |
| Floor | Downward across a known floor and its reverse | Valid floor hit in the face-facing direction; characterize the reverse |
| Wall | Horizontal across the wall and its reverse | Valid wall hit and horizontal normal; characterize sidedness |
| Overhang top | Downward across the roof/top and its reverse | A separate upper surface, not ground-height fallback |
| Overhang underside | Upward from free space under the slab and its reverse | Valid underside hit and downward normal |
| Gap | Horizontal through the open space beneath the overhang and its reverse | Both miss in a confirmed local clear corridor; no filled arch |
| Clear miss | Short unobstructed segment away from any face and its reverse | Both miss with explicitly valid availability |

These are **12 directed rays**. Repeat the set from a second parallel segment displaced **0.25 m** tangentially while staying on the same broad faces: **24 rays per batch**. Use at most **8 m** segments, minimum **0.10 m**, with ordinary endpoints at least **0.10 m** clear of faces. Three measured batches at least **2 seconds** apart give **72 measured calls**. Reverse-direction hits are not assumed: a pilot establishes one-sided versus two-sided expectations without reclassifying an expected face-facing miss as a pass. If the scene cannot provide unambiguous endpoints/surfaces, stop and choose a new manifest before testing.

### Proposed validity tolerances and local calibration

Let `d = B - A`, `L = |d|`, `t_geom = dot(P-A,d)/L²`. Reject nonfinite endpoints; reject invalid length before entering native code. For hits, test each component of `P`, `N`, and returned `t` individually for finiteness. Check:

- Signed segment bounds: `t` and `t_geom` in `[-0.001, 1.001]`.
- Position on segment: `|P - (A + t_geom*d)| <= 0.01 + 0.001*L` metres.
- Fraction agreement: `|t - t_geom|*L <= 0.01 + 0.001*L` metres. At the 8 m cap this is 18 mm, below the existing 5 cm guard; do not alter that guard.
- Unit normal: `abs(|N|-1) <= 0.01` before any normalization. If the local contract defines outward one-sided normals, require `dot(N,d/L) <= 0.01`; otherwise establish and freeze the declared sign convention first.
- Known horizontal floor/top: `N.z >= 0.98`; underside: `N.z <= -0.98`; vertical wall: `abs(N.z) <= 0.05`, with the expected horizontal direction within **5 degrees**. These scene-specific checks assume GTA Z-up only after locally establishing that convention.
- Same-ray repeatability across measured batches: hit position spread at most **0.01 m**, normal angle spread at most **2 degrees**, and identical hit/miss classification. Parallel displaced rays compare to the known face plane, not identical positions. Misses carry no valid hit fields and must not reuse a previous hit.

These numbers are proposed gates, not GTA guarantees or measurements. First verify unit scale, axes and the scene's own dimensions/slope locally. Use up to **24 pilot calls**, one per tick, to measure quantization and establish sidedness/normal orientation under the predeclared validity bounds. Pilot disagreement rejects readiness; do not widen tolerances until results pass. A redesigned contract requires explicit review and a fresh acceptance set. Use at most **24 additional diagnostic calls** with starts **0.005, 0.02 and 0.10 m** from representative faces to characterize near-origin instability; invalid results must stay invalid. Three surfaces, forward/reverse, three distances require 18 calls, leaving six for predeclared repeat checks. No skip-ahead or silent normalization turns bad data into good geometry. Total native-call cap: **120** for the pilot, measured batches and near-face diagnostics combined.

Calibrate position/fraction limits against observed floating-point precision and independently documented broad planes; calibrate normal limits against face orientation and measured repeatability. If the local geometry cannot constrain orientation to the proposed bounds, use a better reference scene before evaluating the query. Do not equate visual proximity with exact physical geometry. Test zero-length/nonfinite requests only through rejection before native entry.

### Availability, timing and stopping

Require a build-bound qualification and safe phase before the first call. A request carries the current load epoch; cancel on load, pause, missing callback, build mismatch or epoch change. Never carry entity pointers between callbacks. A locally justified availability check is mandatory for publishing `miss`; where availability is uncertain publish `unavailable` and fail the clear-miss acceptance. Loaded neighboring positive controls cannot waive this condition. Results older than **100 ms** are stale for this observation pass; expire them rather than fill a hole with guessed collision.

Measure **600 baseline callback/frame intervals**, capped at **30 seconds**, with no query work. Calibrate clock overhead and frame-time p50/p95/p99 locally. Pilot queries run **one per tick**. Only if pilots remain within budget may measured work rise to at most **four calls per tick**, with an elapsed-work budget of **0.5 ms** and no catch-up queue, retries or worker-thread native calls. Check time before and after every call; a native call is non-preemptible. Stop issuing calls after any single-call or per-tick probe time above **1 ms**, or when the measured p95 probe work exceeds **0.5 ms**. A **60-second overall probe deadline** cancels unfinished batches. Use bounded local buffering (120 results) and drain logging outside the physics callback.

Calibrate the batch cap using pilot worst-case/p95 query cost plus callback/validation cost; choose the smaller of four and what fits 0.5 ms. If one call cannot fit, reject the route for this proposed probe. Compare measured frame-time p95 against the baseline; a regression greater than **1 ms** needs investigation before acceptance, even when query timings look good. Baseline/pilot samples provide provisional diagnostic timing, not long-run worst-case assurance. Calibrate the 100 ms freshness bound from measured callback cadence and load/streaming behavior; if cadence cannot meet it, reject this manifest. Later skating needs a speed-dependent coverage condition such as lookahead exceeding speed times worst-case acquisition age plus stopping/contact margin; no local speed/timing data exists here to claim that condition holds.

**Pass only** with independently justified exact-build ABI/thread/availability, all predeclared directed outcomes across three batches, valid finite/segment/normal results, distinct top/underside and clear gap, repeatability and timing within bounds. Publish only source-safe counts, classifications, validity residual ranges and timing summaries. Record OS/runtime and exact build qualification locally; do not claim a passed hypothetical test.

**Reject or stop** for an unknown ABI/layout, ambiguous native resolution, out-of-bounds writes/canary corruption in a later reviewed probe, wrong thread, build/epoch mismatch, stale/unavailable data represented as empty, near-face corruption leaking into accepted results, unexplained normals/fractions, a face-facing miss, filled overhang gap, unstable repeatability, budget breach, host stall/crash or unintended gameplay mutation. Do not relax the flatness guard or substitute ground height for missing walls. If native investigation remains inconclusive, preserve the negative result and let #32 evaluate extraction independently.

Remaining blockers: resolve the guidance hash discrepancy for host provenance; qualify a local native-analysis provider; justify the exact CE query contract and availability/thread conditions; obtain separate runtime-task authority; run the bounded observation proof; then investigate transform/winding and collision installation into the real pinned Skate Session. Moving traffic/doors, rails, broad-city coverage, recovery, rider presentation and owner acceptance remain later requirements. A report or documentation check completes source research only.

<research>{
  "verdict": "requires-local-proof",
  "runtimeVerified": false,
  "sources": [
    {
      "url": "https://github.com/Jpatching/combine/blob/d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad/research/results/2026-10-09-world-collision-next-proof.md",
      "revision": "d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad"
    },
    {
      "url": "https://github.com/Jpatching/combine/blob/d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad/research/results/2026-10-09-repository-interface-audit.md",
      "revision": "d6f672560b40cbf33b8ebaa6bd18d8f7fa5899ad"
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
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/dllmain.cpp",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/README.md",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/collision/Rays.h",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/include/CWorld.h",
      "revision": "dddbd3f54b146bdb3a9852809e48e5cb169af3cd"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Collision.cpp",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/mrborghini/libertycraft/blob/0fe0f2c9aae2ba974cb077e282b091a38f1ca48f/asi/src/Game.cpp",
      "revision": "0fe0f2c9aae2ba974cb077e282b091a38f1ca48f"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/CHANGELOG.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/api.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-sdk.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/using-memory.md",
      "revision": "bbf6773fe8cc1bfa95c73509a25928f97b0d8d13"
    },
    {
      "url": "https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json",
      "revision": "34bedee0be2f57047ed8f0705c81f137ede3d3ce"
    },
    {
      "url": "https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md",
      "revision": "dddbd3f54b146bdb3a9852809e48e5cb169af3cd"
    },
    {
      "url": "https://github.com/ClonkAndre/IV-SDK-DotNet/blob/f5f5d63f705819525fe2f5307648661fb5613124/README.md",
      "revision": "f5f5d63f705819525fe2f5307648661fb5613124"
    }
  ],
  "unknowns": [
    "Exact 1.2.0.59 segment-query resolution, ABI, result layout and filtering remain unestablished.",
    "Safe physics-query phase, streaming availability and lifetime rules remain unestablished.",
    "Local normal orientation, precision, repeatability, latency and Skate suitability were not measured.",
    "All four supplied Universal Modder SHA256 values differ from retrieved bytes at the requested revision; host provenance needs reconciliation."
  ],
  "inaccessibleSources": [
    "Owned GTAIV.exe 1.2.0.59 and private runtime were unavailable and not accessed.",
    "Native REA provider and um kb search were unavailable; no tools installed.",
    "CLEO GTA host collision internals were not available in the inspected public SDK/documentation scope.",
    "Exploratory public URLs GTAmodding/IV-SDK and zalgo-dev/LuaModLoader returned HTTP 404; no conclusion drawn about alternate repository locations."
  ]
}</research>
