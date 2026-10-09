# Current context

## Current task

Reviewed: 2026-10-10

Task: implement a focused selected-overlay visibility comparison under [spec #39](https://github.com/Jpatching/combine/issues/39) for [#20](https://github.com/Jpatching/combine/issues/20). [Viewer ticket #40](https://github.com/Jpatching/combine/issues/40) is closed with bounded qualification; [street ticket #41](https://github.com/Jpatching/combine/issues/41) is resolved as an inconclusive investigation.

Source branch: `implement/gtaiv-composite-collision`

Source revision: `2f228b4ae128090d59dde36ffe67cdd916ed5ec6`

This is the reviewed focused visibility implementation, compared with `51e258a`.
The integrated baseline viewer fixture/procedure is `b75eb037`. Decoder source
remains unchanged from `47e8a2c`. The issue owns later publication revisions.

Disposition: draft [#38](https://github.com/Jpatching/combine/pull/38) awaits owner source approval. The existing owned file decodes; provenance and a candidate map area are traced, but independent street placement remains inconclusive.

The owner authorized the bounded investigation and focused implementation with
TDD, using subagents where efficient. The broader target remains one real GTA IV
street with visible board/animation, curb/wall contact, dismount and ordinary GTA
driving. Traffic/pedestrians stay active; riding contact with moving objects is
deferred. Source integration and gameplay acceptance remain separate.

## Evidence

The owner selected the small `implement`/`tdd` route to continue inspection. The
new [visibility commands](../tools/gtaiv-viewer/README.md) hide and restore only
the selected collision-only root's renderers. They do not move meshes or the
camera, sample ground or launch GTA. The authored resource-to-scene fixture
exercises those public menu commands: it failed with the Hide command missing,
then passed after implementation, with unchanged literal geometry and an
unrelated renderer still enabled. Both runs compiled without C# errors;
the failed CLI wrapper returned 6 and the passing wrapper returned 0.
Mixed/absent-selection refusal also passed; no separate red/green cycle is
claimed for those guard checks. Earlier GUID compilation failures were setup
unavailability, not behavioral red. Explicit `-accept-apiupdate` enabled API
migration for the pinned Editor; package manifest/lock and ProjectVersion were
rechecked unchanged.

The reviewed private bootstrap now places those same selected mesh children
under a dedicated identity parent. Independent static review found no placement,
resource or map-loader change. The live trial again verified the digest and
complete counts, completed normal loading, and emitted both HIDDEN and SHOWN
markers without C# compilation errors. A fixed-camera map-only/restored pair was
captured and automatically opened locally. Independent visual review confirmed
the overlay disappears and returns while landmarks retain their positions.
Green coverage broadly follows the foreground bridge approach, parts of the yard,
a small building and roadside/verge surfaces; farther disconnected bridge spans
remain uncovered. This is visual correspondence, not named street identity or
qualified coordinate checkpoints. The updated [location verdict](../research/results/2026-10-10-gtaiv-viewer-location-verdict.md)
remains inconclusive. Independent Standards and Spec reviews found no actionable
findings. The repository gate passed 73 tests and 63-document/context checks.
The final authored rerun after expectation reuse also compiled without C# errors,
emitted PASS and completed with CLI exit 0; staged source and pins matched exactly.
The source is committed on the existing branch; draft #38 retains owner approval.

The owner approved spec #39, its two-ticket dependency chain, and the authored
resource-to-viewer scene test boundary. The existing current branch is preserved;
ticket #40 preparation used `implement/gtaiv-viewer-qualification` in its retained
implementer worktree. Its authored fixture, procedure and reviewed compile fix
are integrated at `b75eb037`; the worktree and private setup remain retained.
The first Unity run stopped at compilation: an ambiguous fixture
`CompressionLevel` reference and package GUID references. The fixture now fully
qualifies the compression enum. Independent review found no defects in that fix.
The second Unity CLI run compiled and emitted `PASS (scene geometry; pixels
unverified)` with exit 0. This is baseline qualification, not a behavioral
red-to-green implementation claim.

Pinned GTA4Unity already contains a collision debug renderer implementation,
disabled by a commented startup call. Its required Unity Editor is 6000.4.0f1 (8cf496087c8f),
and its actual scene is ECSMain. Unity is a local inspection-tool dependency,
not a selected Combine host or Skate integration engine. The official editor
installer matches release metadata size/integrity; editor and Hub installers
have valid Unity Technologies signatures. Hub's interactive installer launch was
requested. The owner then reconfirmed proceeding with Unity CLI. The signed CLI
reports 6000.6.5f1 already installed; the required 6000.4.0f1 was requested
separately through the CLI. Its registered binary matches revision 8cf496087c8f
and has a valid signature; installation completed and CLI structural verification
passed. The authored fixture ran with that exact engine revision and unchanged
package manifest/lock. Cached GUID references changed without agent edits; Unity
API migration is a plausible explanation, not independently established.
The owner approved the terms step; the interactive run then passed the fixture.
An authored-only render shows both child shapes. Independent review confirmed
that narrow visibility claim; the dark quadrilateral has low contrast and the
top-down image does not establish height (the coordinate assertions do).
The image was captured and opened locally through workbench.

A separately reviewed, reversible private lab configuration selects the exact
SHA-256-verified resource, preserves the full map loader and identity parent,
checks complete child/vertex/triangle counts, disables ped spawning and enables
the existing flight camera. The first live trial failed because upstream IMG
opening requests read/write access. A read-only open succeeded on the same
archive; a reviewed one-line lab correction changes only that access request to
read. Original permissions were preserved; writer APIs remain uninvoked.
The patched project compiled and repeated the authored fixture PASS with exit 0.
The next live trial verified the retained digest, matched all expected overlay
counts, completed map baking, spawned flight and released loading normally with
geometry loaded, no pending loads and collision ready (not a timeout).
The unchanged manifest/lock and exact engine revision were rechecked. These are
private upstream-lab changes, not merged Combine source or a supported viewer.
The direct fixture does not test the new bootstrap guards or flight lifecycle.
An unrelated Unity search-index exception was logged; no error-free claim is made.

A live viewer-window screenshot was captured and opened locally. The owner said
both map and overlay appeared viewable, provisionally. A subsequent warning was
Windows Photos asking to open the generated PNG through the WSL network-style
path, not a viewer exception. At the owner's explicit screenshot request the
warning was inspected, then its one-file Continue opening action was invoked;
no security setting changed. The owner subsequently accepted the live appearance
("It looks legit"). Independent scoped reviews found no blocking fixture/setup
defects; #40 was closed with that bounded qualification. This does not approve
draft #38 for main merge or accept gameplay. Private installers and setup records
remain local. The Unity viewer read owned files; no host-game launch occurred.

The [resource placement investigation](../research/results/2026-10-09-gtaiv-resource-placement.md)
traces the retained file back to the exact archive entry by digest, finds an IMG
directive naming that archive, and correlates candidate collision bounds with
object placements in four WPL map files. That correlation assumes world-space
WBN coordinates; it does not establish a unique street or active collision.
The owned child matrices were checked and are exactly identity, not substituted.
Private identities, map records and coordinates remain in ignored local records.
That placement investigation added no comparison tooling, supported parser
implementation, game launch or runtime trial. The location gate remains
inconclusive after the later viewer trials described above.

The [source investigation](../research/results/2026-10-09-gtaiv-composite-transforms.md)
corroborates IV composite offsets, padded matrices, child-to-parent transform
application and BVH polygon layout. The [inspector](../tools/gtaiv-collision/README.md)
now accepts one composite level containing geometry/BVH polygon meshes. It
applies explicit rigid transforms, triangulates unflagged quads and rejects
unsupported children, unknown index flags, unequal internal matrices, malformed
spans/counts and cap breaches without returning partial geometry.

The authored rotation/translation test failed before implementation and passed
afterward; the quad test likewise went red then green. Nineteen focused
command/parser tests passed. No separate Python typechecker is configured.
The repository gate passed 73 tests and link/context checks across 60 documents.
Independent Standards review found no documented violations and one duplicate-
validation suggestion, addressed with a shared helper. Spec review found no
blocking findings; both reviewed the bounded source scope rather than privately
repeating the owned-file check.

The same existing private owned WBN changed from `unsupported / unsupported-root`
to `structurally-decoded / validated-geometry`. Only the verdict was emitted.
This establishes bounded polygon decoding for that input. It does not validate
BVH search trees, child-box enclosure, margins/materials, world placement or
active physical collision. No owned data was uploaded or added to Git.

Latest runtime evidence: the earlier gameplay candidate `b403377481a33e407aeb81b78b8d38984aac4735` refused a guarded mount at `over-0.05-metres`. No game launch, staging, input or runtime test occurred for the composite decoder.

## Next step

The bounded location investigation has reached an **inconclusive stop**, recorded
in the [viewer location verdict](../research/results/2026-10-10-gtaiv-viewer-location-verdict.md).
The camera-only close/side views and exact location record are retained privately.
The resource digest still matches; no acquisition, installation or decoder work
needs repeating. Selected-resource count checks are not individual landmark
identification of every child.

Independent visual review resolves the curved elevated deck as railway, not a
road ramp. Its overlay and the neighbouring building match rendered geometry;
the exposed ground asphalt remains gray. A named junction, selected-resource
road/pavement coverage and a continuous road height change remain unestablished.
Industrial, Bohan remains a candidate, not a street-placement pass.

The earlier integration Standards/Spec review found one stale README status paragraph;
the retained implementer corrected it at `5f2d007`. Both reviewers confirmed
zero remaining actionable findings. The repository gate passed 73 tests and
63-document/context checks. #41 is resolved as an inconclusive investigation,
not a street-placement pass; #39 and draft #38 retain their source-approval gates.
The new hide/show comparison improves inspection but does not reopen the ground
measurement gate. No measurement tooling or GTA launch is authorized. The next decisive evidence
is an independently
identified named junction and proof that this exact mesh covers the intended
road, pavement and height-change checkpoints, followed by local owner street
confirmation. Do not silently replace the resource or move it into agreement.

The owner's hybrid permission covers selected viewer screenshots for AI
inspection; game files, private identities and exact coordinates remain private.
The latest side view was requested open locally through its native Windows path.
Camera readout is Unity (-GTA.x, GTA.z, -GTA.y), not a ground sample.

Review draft #38 for owner source approval; it has not been merged.
[PR #37](https://github.com/Jpatching/combine/pull/37) is merged and #34 closed;
its earlier pending-merge handoff is superseded.

Resume from the retained local location records and the resource placement report;
acquisition and decoding need not be repeated. The missing evidence is an
independently recognisable street/landmark match and qualified world placement
for this exact resource. A map-object origin inside collision bounds is only a
candidate. GTA4Unity's loader omits composite child matrices generally; do not
present it as a qualified exact-version reference without checking its limits.
Stop before measurement tooling while this relationship remains ambiguous.

After the location gate passes, choose a handful of distinctive road, pavement
and height-change checkpoints. Freeze numeric tolerance and repeatability rules
before measuring; compare GTA observations and mesh predictions at identical
coordinates and reject unavailable results. Report agreement, disagreement or
inconclusive. Agreement covers those ground checkpoints only; walls remain the
next proof. Preserve existing guards and keep placement, active collision and
Skate integration as separate evidence claims.

## Session close

Use [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Read #20's latest candidate
record before resuming. Keep resources, geometry, settings, identities and raw
logs private. Review, source merge, placement proof, gameplay and owner acceptance
are distinct evidence claims. Preserve draft [#23](https://github.com/Jpatching/combine/pull/23),
in-process/worker candidates and recovery branches; #21/#22 remain blocked.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[physical collision report](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[native query report](../research/results/gtaiv-120059-native-collision-feasibility.md).
The street experiment remains on `prototype/gtaiv-street-collision` at
`a4fec7364c957bd4bf80e3fb6eb80e04ba6eb054`; its acquisition code is not incorporated
into this source slice. The original checksum fix and research #31/#32 are merged.
