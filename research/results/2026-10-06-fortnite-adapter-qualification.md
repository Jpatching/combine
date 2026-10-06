# Full Fortnite island + Skate: adapter qualification — 2026-10-06

Current objective: reuse existing export/map tools to prove a repeatable Fortnite
area with Skate movement, then deliver the complete selected island. This file
owns the qualification/specification; source inspection alone does not prove play. Destination: the full selected Windows Fortnite island,
`Release-3.1-CL-3917250`, with Skate movement only. Smaller areas are validation
cases, not a replacement destination. D-022 supersedes older building-only scope.
Actual Synergy and hit radius remain separate and incomplete.

Resume update (2026-10-06, owner-supplied reuse plan): assess existing exporters
and Skate map tools before extending the custom adapter. Qualification must end
with an evidenced route or a precise blocker. Existing eight tickets are retained;
route-dependent implementation is parked until a real terrain/building witness.
PR #1 rail repair remains required before merge. Local metadata now identifies the
selected 3.1 input, but recorded parser attempts mount no containers and find no
worlds. The bounded discovery below is historical. See [current handoff](../../docs/HANDOFF.md)
for fresh publication/input evidence and D-023 for authorized version choice.

## Agreed observable outcomes

1. Recognizable Fortnite scenery with Skate controls, camera and movement.
2. Solid ground, walls and stairs, plus suitable grind paths.
3. Fall recovery and return to a safe location.
4. Exit and relaunch the same isolated setup.
5. Complete selected island after the real-area checkpoint.
6. Clear preparation errors identifying missing prerequisites.
7. Original installations and earlier trials preserved.
8. Pinned tools, exact input/output identities and reproducible commands.
9. Existing implementations assessed before new conversion code.
10. Source-safe tests/diagnostics with no distributed game data.
11. Each supported experience declares inputs, adapter, checks and limitations.
12. Shared interfaces derived from working integrations; no arbitrary compatibility promise.
13. One active outcome and an exact next actor/action.

The first area's acceptance requires prepare/load/control/recover/close, jump,
collision, a representative grind and relaunch. Full-island acceptance adds
content coverage, regional travel, safe loading and measured performance on
identified Windows hardware. Malformed geometry, unsupported versions, missing
dependencies and excessive inputs must fail before a partial session is
installed. Existing public validation regressions remain required. Synthetic
tests/builds/process launch do not satisfy physical gameplay or owner acceptance.

## Reuse qualification result — 2026-10-06

**Precise blocker; no route selected.** The recorded 3.1 parser runs mounted
0/10 containers and found zero worlds. All ten version-4 footers carry an
encrypted-index flag; the inspected parser skips mounting them. These are
[reproduced prior observations](2026-10-06-fortnite-input-diagnosis.md), not new
export attempts here. No accessible replacement, terrain/building export or
collision witness was established. This does not prove every exporter fails.
It prevents any candidate from meeting the owner's real-data qualification gate.

Qualification inputs: current board/specification, recorded input diagnosis,
pinned runtime and public tool source. Output: comparison below and an explicit
open input prerequisite. No tool/plugin was installed or run against game data,
no input/key was changed, and no private assets or logs were uploaded.

### Existing runtime reuse, source-inspected

The runtime already includes a [SKATE01–15 reader](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-data/src/skate_map.rs).
It parses visual geometry, materials/textures, separate collision and rails;
newer versions fail explicitly. The [world adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/skate_world.rs)
rejects absent collision, authored doors and external texture placeholders,
and rejects unsupported required extensions. Some retained lighting/material
features have explicit limitations. The [public bridge](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs)
constructs a collision-only in-memory SkateMap from triangles/rails and loads
stock assets/graphs/physics. Its public constructor does not load a `.skate`
render package or own a standalone display session.

Thus a compatible existing map pipeline could reuse parsing and physics; it
still needs qualified presentation/session wiring in Combine. A matching suffix
or supported version is insufficient. Source inspected via `git show` at the
exact pin; remote HEAD/v0.4.0 refreshed and still match. No runtime changed.

### Conditional comparison

| Candidate route | Existing capability / evidence | Work and qualification still required |
| --- | --- | --- |
| CUE4Parse/FModel world export → existing Blender/map tools → pinned host | Pinned CUE4Parse WorldExporter walks actors, landscapes and streaming levels into USDA; instance transforms/material overrides are represented | Real legacy-build decode, all required sublayers, no dummy meshes, authoritative collision, Blender import/material conversion and exact `.skate` compatibility; Combine render/session bridge |
| FortnitePorting → Blender → existing Skate map exporter | Candidate map/asset import path; tool assessment below | Selected-build support and terrain/building witness, shader conversion, collision semantics, transform/axes measurements and compatible exporter output; same Combine session gap |
| Complete Combine custom export adapter → native world/host | Existing native validation/preparation patch and host triangle/rail API; source tests only | Export prerequisite remains identical; additional format decoding, material/instance conversion and rendering/lifecycle work; no custom serialization justified yet |
| Another Skate map runtime | Existing tooling may target a different host | Exact feature/performance/access comparison and explicit owner runtime decision; not selected or executed |

CUE4Parse pin is `e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc`.
Its [world exporter](https://github.com/FabianFG/CUE4Parse/blob/e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc/CUE4Parse-Conversion/Exporters/WorldExporter.cs)
and [USD writer](https://github.com/FabianFG/CUE4Parse/blob/e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc/CUE4Parse-Conversion/Formats/World/UsdWorldFormat.cs)
include dummy-cube fallbacks and streaming-level handling; successful export
status alone does not establish complete island content. No collision export
witness exists. FModel/Blender tools are alternatives to qualify, not locally
verified substitutions.

### Public tool pins and online reuse leads

Public refs recorded October 6 with `git ls-remote`; selected runtime unchanged.
Source/documentation downloaded only to temporary local inspection files, not
installed or executed:

| Tool | Exact observed reference | Source assessment |
| --- | --- | --- |
| SK8-Engine Blender map exporter | preview.15 tag object `98bef0c339f1761c7c9900901dd522f5e087fa7e`, commit `59614c8a0039395f1575e8bf08ed7ad82a554fa4` | Existing `.blend` adoption, embedded materials/textures, independent collision, named grind paths and spawn; v15 candidate |
| FortnitePorting | v4.3.3/main `4c13c7907ad1f7804b7affc6c86a737e8e70285d` | Installed/custom/on-demand asset access, Blender extension; pinned map source sets actor/foliage/landscape export flags |
| BlenderUmap2 | better-materials `87ae84e70f706356945c8152a407108262a41897` | UE4/5 `.umap` and Fortnite replay actor import; Blender 3+, .NET 6, PSK/PSA importer dependencies |

The pinned [SK8 exporter guide](https://github.com/SK8-ENGINE/SK8-Engine/blob/59614c8a0039395f1575e8bf08ed7ad82a554fa4/tools/blender_owned_map/README.md)
can adopt visible meshes as presentation plus collision and convert/bake selected
shader inputs. That default does not preserve Fortnite's source solid-surface
semantics automatically. Complex materials, foliage/decals and collider groups
need inspection. Use existing authored rails/edge algorithms, then test actual
grinds; generated paths are candidates. Its optional agent-assisted classification
workflow must not receive private game images/assets. Manual local classification
is available. A failed exact format-spec URL was not used as compatibility proof.

Pinned FortnitePorting [README](https://github.com/h4lfheart/FortnitePorting/blob/4c13c7907ad1f7804b7affc6c86a737e8e70285d/README.md)
requires Windows x64 and Blender 4.2+ for live import. Search-cached moving
documentation says Blender 5.0+; use exact-version compatibility evidence, not
that contradictory cache. Its [map code](https://github.com/h4lfheart/FortnitePorting/blob/4c13c7907ad1f7804b7affc6c86a737e8e70285d/src/FortnitePorting/Models/Map/WorldPartitionMap.cs)
exports selected grid worlds with actor/landscape flags but skips a null world
without establishing completeness. Collision fidelity remains unverified.
Its [provider](https://github.com/h4lfheart/FortnitePorting/blob/4c13c7907ad1f7804b7affc6c86a737e8e70285d/src/FortnitePorting/Services/CUE4ParseService.cs)
uses manifest-backed on-demand downloads and key submission; this is an access
lead requiring review under the existing no-bypass boundary, not permission
to fetch keys or run it. Logged-in exports can submit map-path identifiers;
keep account/export sharing disabled for a private trial. No such requests made.
The pinned [BlenderUmap2 README](https://github.com/MinshuG/BlenderUmap2/blob/87ae84e70f706356945c8152a407108262a41897/README.md)
does not establish collision or `.skate` preservation.

Owner follow-up requests online/downloadable examples rather than depending
only on supplied input. Bounded searches found:

- [Sxlar3d's map-import tutorial](https://www.youtube.com/watch?v=Ne6YgsB7Rjo)
  (2022-10-22) documents replay/map import through BlenderUmap, FModel and PSK/PSA
  tools, including position and texture repairs. Only its published description
  was inspected; no independent viewing/reproduction or Skate play is claimed.
- [Minshu's whole-map release post](https://www.patreon.com/minshug/posts/beta-with-lights-75676254)
  documents Asteria_Terrain WorldPartition import (2022-12-08). Historical
  Blender-world support does not qualify the selected build or collision.
- [HeightLayerMaps](https://github.com/jasn7135/HeightLayerMaps) offers extracted
  3.6/9.10 terrain height/layer maps and import metadata. It supplies no building
  placement/collision witness, so downloading terrain alone cannot close C-024.
  Author claims of source accuracy and usage permission were not independently
  verified; no game data downloaded.
- [Skate 3 University in Fortnite](https://www.fortnite.com/@chillsam2/3105-1199-7249)
  is an island listing for the reverse scenery direction. It provides neither
  the selected Fortnite island nor a downloadable Skate-runtime package.

No inspected source supplies a ready full Fortnite-island `.skate` package or
a reproduced end-to-end Fortnite→Combine session. Best candidate to test first
**(recommendation, not route selection)**: FortnitePorting → Blender → pinned
SK8 map exporter → pinned Combine reader/host. Reusing the exporter does not
require adopting its separate C++/Skate3Recomp runtime. The decision-changing
unknowns are accessible supported input, collision preservation and complete
terrain/building export—not whether a new generic decoder can be designed.

### What seamless Fortnite scenery with Skate movement requires

Fortnite supplies the scene: terrain/buildings, exact instance transforms,
material bindings/textures and lighting. Skate supplies controls, movement,
animations, board contact/grinds and camera. Map preparation connects them
through correct units/axes, solid collision, rails and safe spawn/recovery.
Session ownership connects input, rendering, loading, recovery and teardown.
Visual import alone proves none of the movement/collision/lifecycle behavior.
Some original shader/lighting effects may need baking or adaptation; exact
pixel parity is unverified. Original Fortnite gameplay is excluded.

### Qualification exit and next action

```text
Identified accessible input or existing private export
  -> reviewed pinned exporter -> terrain + building + collision witness
       | missing/unsupported -> explicit blocker, preserve prior setup
       v
Compare actual Blender/map output with pinned reader/host
  -> select route and revise C-025/C-027 -> prepare/load/control/recover/close
  -> real-area physical checks -> measured full-island implementation
```

Next actor: Codex qualifies an accessible input/export for the recommended
pinned toolchain under the existing access boundaries; the owner explicitly
requested online sources rather than depending only on supplied input. No
qualified download was established. Local location/build/tool identity and
private game files remain separate from source. Required
witness records root/sublevel identity, terrain plus a building, placements,
materials, source collision/missing content, hashes and commands. Then measure
landmark scale/axes/winding, instances, terrain seams and playable collision/grind
behavior. Until then C-024 stays open, and route-dependent C-025–C-030 work is
parked. No new decoder, output schema, alternate runtime or universal interface
is selected. Full residency/streaming waits for census and Windows measurements.

### Preserved work and repair obligation

The four inherited exporter files were reviewed and preserved unchanged in a
separate local source checkpoint after the owner requested a clean Git worktree.
They remain unfinished research scaffolding, not the chosen conversion route.
Default .NET bin/obj output is ignored; no private reports/assets were staged. SHA-256 at this qualification:

- FortniteExport.csproj: `4b6849a56dd41bea271059cfa99c687dd2fc85cce490e4fefc76616665b841a2`
- Program.cs: `94ef40797e3f24cf2c400e433f0e3dd1fa1033bf4d9f5e815ac70570f7f67fcf`
- check_runner.py: `50ea295a7151421c78d5a263351cbddb916a4dd835ff7c798e346324ef603f91`
- packages.lock.json: `3b16ccc3e8d3eec25573cb5d7718384ae893b755ca55c1e41960d61edd9c39cc`

No exporter rebuild is claimed; inherited missing NuGet/analyzer cache remains.
PR #1's [reproduced rail defect](2026-10-06-pr1-review.md) remains unfixed and
blocks merge. Parked does not waive its regression/fix obligation. Synergy and
other trials/commits remain preserved; global router retirement is separate.

## Evidence and reproducibility

Runtime source inspected with `git show f608f85:<path>` in the existing ignored
checkout; full pin `f608f85e407ff1b7689d54a9aafdd16e95711ac4`. This avoids confusing
local Synergy patches with upstream. October 6 `git ls-remote` reports HEAD and
v0.4.0 still at that pin. No pin moved. A bounded read-only helper traced runtime
source; the lead inspected the principal structs and host bridge directly.

Public CUE4Parse source downloaded for inspection, without building or executing:
`git clone --depth 1 https://github.com/FabianFG/CUE4Parse.git .private/fortnite-qualification/CUE4Parse`.
Observed revision `e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc`, clean checkout.
This is a research-tool witness, not the selected export tool or a dependency added
to Combine. Source licences/dependencies need review before incorporating code.
No Fortnite game data, private logs or settings were uploaded or converted.

Local discovery checked the project private directory to depth three for Fortnite
folders and the default Windows Epic Games installation directory: no selected
build found there. This is a bounded check, not a full machine inventory. No local
path or manifest proving selected-build identity has been supplied. No package
contents, island object counts, export output or runtime performance were observed.

The owner additionally requested a GitHub search/download. The public
[manifest archive](https://github.com/VastBlast/FortniteManifestArchive) lists the
exact Windows CL, while [another build list](https://github.com/n6617x/Fortnitebuilds)
is only a third-party archive lead. These establish listings, not authentic local
bytes, authorized redistribution or successful decoding. Epic's
[installation instructions](https://www.epicgames.com/help/en-US/c-Category_SaveTheWorld/a000084906)
describe the current launcher route, not the selected legacy build. No verified
publisher-authorized legacy download was established; no game archive downloaded.
The owner now permits a suitable accessible version (D-023); record the actual
selected build and identity before substitution. No alternative is selected.

## Reusable runtime interfaces and required changes

All links in this section resolve to the runtime pin above. Observed facts:

| Stage | Source-backed behavior | Required Fortnite change (proposed) |
| --- | --- | --- |
| Request/load | [`approve_map_load`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/match_load.rs#L189) resolves a zone and requires `common_mp`; [`walk_prepared_match`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/session_load/match_walk.rs#L121) uses game lanes | Add an explicit standalone Skate session route before the MW match loader; no proxy Rust zone or common_mp fallback |
| World contract | [`LoadedWorld`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/lane/mod.rs#L32) contains world, materials, collision, spawns and gaps; [`PreparedWorld`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/session_load/mod.rs#L94) carries static meshes/placements, bounds, lighting and policy | Reuse render structures through a world-only preparation boundary; do not make scripts/weapons prerequisites |
| Geometry | [`build_world_draw`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/asset_world/src/world_draw.rs#L679) decodes resident vertices/indices/surfaces from MW zones | Supply validated imported meshes/material bindings/instances without pretending exported data is a fastfile |
| Collision | [`ClipCollision`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/asset_world/src/clip_collision.rs#L36) holds brushes, mesh tables, BSP, materials and placed models | Either correctly build every table required by retained queries or feed a narrow validated triangle/rail boundary directly to Skate; empty BSP tables must not be assumed sufficient |
| Skate conversion | [`collision::extract`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs#L20) extracts solid mesh/brush/static-model surfaces and inferred rails | Factor reusable rail extraction/coordinate conversion from MW collision ingestion; retain solid semantics and instance transforms |
| Host | [`Session::new`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs#L32) accepts asset root, triangle vectors, rails, spawn, heading; host loads Skate assets/graphs/physics | Reuse host API; missing Skate assets fail before session publication. Fortnite input alone does not supply Skate rigs/animations |
| Entry/presentation | [`skate::update`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs#L326) requires authority, in-game screen and living presented MW player; `present` writes its origin | Introduce standalone session identity, spawn, input and pose/camera ownership; remove dependency on MW alive/player/authority state for this route |
| Exit | [`stop`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs#L284) suspends input and retains the map session; update compares collision Arc identity | Distinguish temporary skating suspension from full session disposal; cancel workers, reject stale replies, drop world/physics/render ownership on exit and failed load |

The Minecraft precedent uses an IW4 proxy and scripts; it is not a Skate-only
startup recipe. `PreparedMatch` contains weapons/FPV/body/world-weapon catalogs.
[`match_apply`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/session/src/match_apply.rs#L826)
installs combat resources and later script resolver/gametype entry points.
[`admission`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/session/src/admission.rs#L62)
and [`HUD menus`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/hud/src/menus/mod.rs#L173)
retain class/weapon assumptions. No inspected configuration establishes independent
Skate-only startup. This is a concrete implementation gap, not a new owner decision.

Proposed session composition: register world rendering, Skate host, its input,
camera, pause/recovery and exit lifecycle. Do not enter MW sign-on/class selection,
run gametype/GSC/Synergy, publish weapon catalogs, spawn combat entities, simulate
fire/damage, or render weapon/crosshair/ammo/score/class HUD. Gate actual systems,
not just their visibility. Walking/dismount transitions must use Skate's supported
movement or a separately qualified neutral controller; never restore an armed MW
player by default. Audit Combine's Synergy/audio patches when composing plugins:
upstream-only inspection does not prove patched systems are excluded.

```text
Identified private export + Skate assets
  -> bounded validation -> world-only preparation -> standalone session
       | failure: report missing/invalid data        | render + collision + pose
       +-> retain prior session; no partial install  v
                                        Skate movement / recovery
                                                  |
                            exit -> cancel + clear + drop -> relaunch
MW common_mp / combat / class / GSC / proxy world have no entry in this path.
```

## Exporter assessment and actual island evidence gap

[CUE4Parse WorldExporter at the downloaded revision](https://github.com/FabianFG/CUE4Parse/blob/e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc/CUE4Parse-Conversion/Exporters/WorldExporter.cs)
walks `WorldDto.StreamingLevels`, actors/root components, `MeshPtr`, material
overrides, attached actors and landscape components; current extension is `usda`.
Its [dispatch](https://github.com/FabianFG/CUE4Parse/blob/e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc/CUE4Parse-Conversion/ExportSession.cs)
recognizes `UWorld`. This is the strongest inspected component lead, not proof of
3.1 parsing. Streaming-level filtering makes export completeness an explicit check.

[FModel](https://github.com/4sval/FModel/releases) documents world export, including
instances, landscapes and streaming levels, with USD output. Its
[viewer collision code](https://github.com/4sval/FModel/blob/dev/FModel/Views/Snooper/Models/StaticModel.cs)
reads BodySetup/AggGeom; collision preview does not prove collision export.
[BlenderUmap2](https://github.com/MinshuG/BlenderUmap2/blob/better-materials/README.md)
is a map-import component candidate. [FortnitePorting](https://github.com/h4lfheart/FortnitePorting)
documents asset export to Blender/Unreal/folders; that is insufficient evidence of
complete legacy-island export. [UEViewer](https://github.com/gildor2/UEViewer/blob/master/Docs/FAQ.md)
is an individual-mesh/material fallback, with no complete island witness in the
reviewed material. None was run against the selected game build. Moving source
links were observed October 6; pin any selected tool before execution.

A genuine selected-build census must establish each row, not assume a modern
Unreal layout applies to this legacy island:

| Required island content | Missing evidence / required output |
| --- | --- |
| Root world and all sublevels | Actual package identity, dependency graph, loaded/exported/missing counts; no filter silently omitting regions |
| Terrain | Landscape component coverage, height/holes, transform, LOD and material-layer mapping; seams across component borders |
| Buildings and objects | Unique meshes and instance counts; actor/component hierarchy, rotation/scale/translation, repeated instances and attachments |
| Materials | Material slots/overrides, texture references and decoded sizes; explicit unsupported shader effects, no silent missing textures |
| Collision | Terrain and building source collision representation; convex/simple/complex semantics, solid surfaces and transformed instances; render mesh is not automatically collision |
| Spawn and extent | Full bounds, source units/axes, measured recognizable landmarks and a collision-clear spawn/recovery point |

Exact input prerequisite: owner-identified legitimate local selected-build root,
private manifest/build identity and hashes, chosen island package, complete package
dependencies, reviewed/pinned parser settings, and a private reproducible export
witness. Record redacted success/failure, missing classes/references and counts.
If required packages cannot be decoded without an unsupported/bypass route, stop
that input path and report it. No DRM/anti-cheat bypass or unreviewed plugin run.

## Adapter contract: settle semantics now, serialization after a witness

This specifies responsibilities, not an invented on-disk schema. CUE4Parse USD is
a candidate because actual source emits it; no Rust USD decoder or collision
sidecar is selected until an inspected export establishes fields and semantics.

Input: identified map content plus exporter/tool revision and explicit coordinate
metadata; private local assets only. Processing: resolve dependencies inside the
selected root, validate before allocation, apply transforms once, preserve mesh
instancing/material bindings, derive world bounds and movement collision, then
construct reusable runtime render/host products. Output: prepared render world,
materials/placements, solid triangles and rails (or fully valid ClipCollision if
needed by retained queries), spawn/heading and a completeness/error report.

Proposed internal separation: decoder owns format/version quirks; validator owns
resource limits/reference closure/geometry checks; world preparer owns GPU-ready
render structures and collision; session owns lifecycle/input/pose. No format
parser may start scripts, issue downloads or choose a shell command. New Rust
modules should live at assets/world preparation and session/render boundaries;
Skate physics remains in the existing host, not a Python runtime imitation.

Reject truncated/malformed input, unsupported format versions, missing required
sublevels/collision, invalid indices/material references, NaN/infinite coordinates,
degenerate solid triangles, singular transforms and unsafe spawns. Require checked
size arithmetic, limits on decompressed bytes/texture dimensions/vertices/instances/
references and recursion depth before allocation; cancellation must preserve the
previous session. Canonicalize references beneath the chosen root; reject absolute,
parent-traversal, symlink escape and network paths. Return redacted asset identifiers
and actionable errors, not private paths or raw logs. Exact budgets must be chosen
from the census and target hardware, then covered by boundary tests; they are not
unlimited until performance work. Optional cosmetic omissions need an explicit
report and do not permit a claim of complete visual parity.

## Full-island loading decision

Current static extraction supplies the entire triangle/rail vectors to the host.
[`BoardWorld::new`](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-core/src/physics/board_world.rs#L104)
retains triangles and bounds. Existing
[rail extraction](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rails.rs#L32)
caps rails at `u16::MAX`; silently truncating full-island rails is unacceptable.
The Minecraft bridge rebuilds nearby block collision (40-block horizontal radius,
20 depth, recentre at 14, 250 ms change interval), not arbitrary island streaming.
The host's `collision_builder`/`install_collision` is a possible swap seam; it does
not itself provide paging, safe ground coverage or a render-streaming manager.

**Decision remains open:** full residency versus spatial streaming cannot be
selected responsibly without island counts and measured memory/frame/load costs.
Measure unique/placed triangles, collision/rail counts, materials/textures and
bounds; estimate peak memory including decoded data, transformed collision,
acceleration structures, staging/upload duplication and GPU textures. Then measure
load time, peak RAM/VRAM, frame-time distribution and stalls on the named Windows
hardware over representative regional travel. Compare to recorded budgets.
If residency fails, qualify aligned render/collision regions, keep ground loaded
before entry, handle teleport/recovery destination prefetch, cancel stale jobs and
ensure rail continuity across boundaries. Collision swaps must be synchronized
with physics. Failure must pause/recover safely, never remove ground beneath a
moving player. No full-map performance promise or invented object count is made.

## Ordered implementation ticket and acceptance evidence

Track this work in existing C-019 under C-020, with named dependency edges in the
body. This list is implementation order, not a second status tracker.

1. **Standalone Skate session tracer (route-dependent work parked during reuse qualification).** Depends on this source specification and
   reviewed Skate asset setup, not on Fortnite files. Separate world/session entry
   from MW match boot; render a clearly labelled synthetic fixture and use the
   existing host. Verify no common_mp/gametype/GSC/weapon/class dependencies, input
   and pose ownership, recovery, failed load, cancellation, full exit/relaunch and
   ordinary MW/Minecraft regression isolation. Synthetic success proves only the
   session seam, never Fortnite compatibility. Capture Rust changes as patches.
2. **Selected-build decoder witness.** Depends on identified private input and
   reviewed pinned export tool. Census the entire island graph; use terrain,
   building and instance test cases to inspect actual fields/collision. Publish
   only redacted identity/tool/count/error evidence. Freeze the interchange
   contract only after this passes; record exact incompatibilities otherwise.
3. **Real-area integration through the qualified route.** Depends on 1 and 2
plus recorded route selection. Reuse existing map parsing/preparation where
compatible; custom Rust conversion addresses only witnessed gaps. Translate map data
   through bounded validation to render/collision/placements/spawn. Verify known
   axis/scale distances, transform round trips/winding, rotated/scaled instances,
   terrain holes/seams, building interiors/roofs/stairs, solid walls and grindable
   lips. Test malformed/truncated input, out-of-range indices, NaNs, oversized
   allocations and unsafe paths. Fail without partial session installation.
4. **Full-island load and travel.** Depends on 3 and measured census/budgets.
   Qualify residency or implement the required spatial streaming. Test travel
   across multiple map regions, terrain/building transitions, sustained grinds,
   fall/recovery/teleport, dismount/remount, exit/relaunch and retained memory.
   Count missing/duplicate placements and prove no proxy geometry or MW combat/UI.
5. **Exact Windows owner trial.** Depends on 4 and required gates. Record source,
   parser/export revision, private input/output hashes, executable hash, hardware,
   measured performance and representative locations/routes. Prepare isolated
   launch/files/checklist shortcuts. Owner verdict remains separate from source
   checks, synthetic tests, launch, merge and release.

Qualification completion: source findings and interface changes are recorded;
input identity/export/census and no-MW2 startup are precisely blocked/unimplemented.
The repository gate validates documents/metadata and existing Python tests only.
No adapter build, exporter compatibility run, full-island performance measurement,
gameplay or owner acceptance was performed in this slice.

## Published specification and implementation tickets

The full user-story specification is published on the existing C-019 private
Project draft. Linked implementation tickets use the same session-level test
boundary and retain explicit input and sizing dependencies. The first preparation
check uses the host native geometry interface; it does not invent an export format.

Specification and ticket bodies were published and read back on October 6.
Private draft items lack labels/native blocking edges, so readiness and named
dependencies are recorded in each body; no repository issue labels were invented.

- [C-023 · Prepare a validated standalone Skate world](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192627)
- [C-024 · Identify and export the selected island privately](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192669)
- [C-025 · Render and control an isolated Skate session](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192734)
- [C-026 · Recover and relaunch standalone skating](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192780)
- [C-027 · Skate a real island terrain and building test case](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192822)
- [C-028 · Measure full-island loading and choose residency](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192863)
- [C-029 · Travel safely across the complete island](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192926)
- [C-030 · Prepare the exact full-island owner trial](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192995)

The first preparation sub-slice has subsequent [implementation evidence](2026-10-06-standalone-world.md).
The qualification observations above describe the pre-implementation boundary.
