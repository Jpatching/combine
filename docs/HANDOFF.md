# Current context

## Current task

Reviewed: 2026-10-09

Task: trace the decoded collision resource to an independently identifiable GTA IV street for [#20](https://github.com/Jpatching/combine/issues/20), before measurement tooling or Skate integration.

Source branch: `implement/gtaiv-composite-collision`

Source revision: `47e8a2c0d46981ffb3b9cfeec5afd98eb91bffbb`

This is the unchanged decoder revision used for the location investigation.
The issue and PR own the publication revision of the subsequent evidence update.

Disposition: draft [#38](https://github.com/Jpatching/combine/pull/38) awaits owner source approval. The existing owned file decodes; provenance and a candidate map area are traced, but independent street placement remains blocked.

The owner authorized the bounded investigation and focused implementation with
TDD, using subagents where efficient. The broader target remains one real GTA IV
street with visible board/animation, curb/wall contact, dismount and ordinary GTA
driving. Traffic/pedestrians stay active; riding contact with moving objects is
deferred. Source integration and gameplay acceptance remain separate.

## Evidence

The [resource placement investigation](../research/results/2026-10-09-gtaiv-resource-placement.md)
traces the retained file back to the exact archive entry by digest, finds an IMG
directive naming that archive, and correlates candidate collision bounds with
object placements in four WPL map files. That correlation assumes world-space
WBN coordinates; it does not establish a unique street or active collision.
The owned child matrices were checked and are exactly identity, not substituted.
Private identities, map records and coordinates remain in ignored local records.
No comparison tooling, supported parser implementation, game launch or runtime
trial was added. The location gate remains inconclusive.

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
