# Current context

## Current task

Reviewed: 2026-10-10

Task: prepare distinctive ground checkpoints on the retained resource after establishing its named local connection under [spec #39](https://github.com/Jpatching/combine/issues/39) for [#20](https://github.com/Jpatching/combine/issues/20). [Viewer ticket #40](https://github.com/Jpatching/combine/issues/40) is closed with bounded qualification; [street ticket #41](https://github.com/Jpatching/combine/issues/41) recorded an initial inconclusive investigation, now followed by a supported named local connection.

Source branch: `implement/gtaiv-composite-collision`

Source revision: `2f228b4ae128090d59dde36ffe67cdd916ed5ec6`

This is the reviewed focused visibility implementation, compared with `51e258a`.
The integrated baseline viewer fixture/procedure is `b75eb037`. Decoder source
remains unchanged from `47e8a2c`. The issue owns later publication revisions.

Disposition: draft [#38](https://github.com/Jpatching/combine/pull/38) awaits owner source approval. The exact retained resource is linked to Industrial, Bohan, around Drill Street / Lompoc Avenue and the unfinished Northern Expressway approach. Four mesh-coordinate checkpoint candidates are retained privately and comparison rules are frozen; precise surface qualification and owner location confirmation remain pending. No GTA/mesh agreement is established.

The owner authorized the bounded investigation and focused implementation with
TDD, using subagents where efficient. The broader target remains one real GTA IV
street with visible board/animation, curb/wall contact, dismount and ordinary GTA
driving. Traffic/pedestrians stay active; riding contact with moving objects is
deferred. Source integration and gameplay acceptance remain separate.

## Evidence

The owner then requested checkpoint preparation. A closer camera-only Hide/Show
pair was captured and opened locally. Read-only analysis through the existing
decoder matched the retained digest and counts and retained four exact face-
centroid candidates: road, replacement pavement, lower and upper road approach.
Independent image review supports the road/approach candidates, rejects apparent
pavement on a parked trailer and moves the upper target away from the divider.
Camera display readings support provisional image association only. A stalled
clipboard helper was stopped by exact task identity; no result from it is used.
An underpass association and an ambiguous intermediate/lower-layer candidate
were excluded. No ground-query implementation or GTA measurements were added.
The [checkpoint preparation record](../research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md)
fixes comparison rules before host measurements: three valid readings, maximum
0.02 m spread and maximum 0.05 m absolute vertical error for every reading.
The point set still needs precise surface qualification and owner confirmation.

The latest camera-only follow-up connects Burger Shot, Menala Metal's tank-roof
building, adjoining streets, railway and separated unfinished bridge spans in
one scene. A same-camera map-only/restored pair was captured through actual
Hide/Show commands and automatically opened locally. The retained digest was
rechecked unchanged; live complete-count and normal-loading markers remain
available with both visibility markers and zero C# error entries. An independent
visual reviewer supports the named nearby junction using the original base-game
landmark guide and gameplay/map references. This resolves the general street-name
search, not exact checkpoint coverage or active GTA collision. See the
[street-reference follow-up](../research/results/2026-10-10-gtaiv-street-reference.md)
and updated [location verdict](../research/results/2026-10-10-gtaiv-viewer-location-verdict.md).
No source implementation, mesh placement, measurement tooling or host-game
launch changed during this follow-up. Private evidence remains local.

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
remain uncovered. That earlier pair established visual correspondence, not named
street identity or qualified coordinate checkpoints. Its initially inconclusive
location finding is superseded by the bounded named connection above.
Independent Standards and Spec reviews found no actionable
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
implementation, game launch or runtime trial. Later viewer trials support the
named local connection; precise ground checkpoints remain unqualified.

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

The general street-name search is resolved: Industrial, Bohan, around Drill
Street / Lompoc Avenue, near Jackhammer Street and the unfinished Northern
Expressway approach. Reuse the retained private named-connection record and
opened connected screenshot pair. Do not repeat acquisition, installation,
decoding or general skyline searches.

Continue from the four retained coordinate candidates in the
[checkpoint preparation record](../research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md).
Confirm the replacement pedestrian-strip centroid and upper same-carriageway
centroid, resolving any lower-layer ambiguity before finalising the point set.
Patchy overlay rendering establishes neither complete coverage nor gaps.
A railway level is not a road height change. Complete local owner location
confirmation separately. Count checks do not individually identify every child
or qualify the chosen ground points.

The earlier integration Standards/Spec reviews found no remaining actionable
findings after a README correction at `5f2d007`; the focused visibility source
also passed independent review and the repository gate (73 tests and 63-document
checks). #41's earlier inconclusive disposition is historical. The complete
ground-preparation gate remains incomplete, and #39 and draft #38 retain their
approval boundaries. Measurement tooling and GTA launch remain outside this
spec. Do not substitute another resource or move this one into agreement.

The owner's hybrid permission covers selected viewer screenshots for AI
inspection; game files, private identities and exact coordinates remain private.
The latest connected pair was opened locally through its native Windows paths.
Camera readout is Unity (-GTA.x, GTA.z, -GTA.y), not a ground sample.

Review draft #38 for owner source approval; it has not been merged.
[PR #37](https://github.com/Jpatching/combine/pull/37) is merged and #34 closed;
its earlier pending-merge handoff is superseded.

The independently recognisable street/landmark connection is supported. Qualified
ground points are the remaining placement evidence. A map-object origin inside
collision bounds is only a candidate. GTA4Unity's loader omits composite child
matrices generally; this retained resource's matrices are explicitly identity.
Do not extend that bounded qualification to other resources.

After the complete gate passes, finalise the qualified checkpoint set and use the
already frozen comparison rules: three stable valid readings, at most 0.02 m
repeat spread and at most 0.05 m absolute vertical error at identical coordinates.
Reject unavailable results; do not fit placement or average away failures.
Report agreement, disagreement or inconclusive. Agreement covers those ground
checkpoints only; walls remain the next proof. Preserve existing guards and keep
placement, active collision and Skate integration as separate evidence claims.

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
