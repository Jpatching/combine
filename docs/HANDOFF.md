# Current context

## Current task

Reviewed: 2026-10-09

Task: establish bounded composite collision decoding for [#20](https://github.com/Jpatching/combine/issues/20), then independently verify street placement before Skate integration.

Source branch: `implement/gtaiv-composite-collision`

Source revision: `911925c81d8997dff08f7768d348b65020509049`

This is the merged inspector baseline from PR #37. The live issue owns the new
candidate's publication revision and review evidence.

Disposition: composite decoder source candidate prepared; the existing owned file decodes, but independent street placement remains blocked. No PR exists for this new slice yet.

The owner authorized the bounded investigation and focused implementation with
TDD, using subagents where efficient. The broader target remains one real GTA IV
street with visible board/animation, curb/wall contact, dismount and ordinary GTA
driving. Traffic/pedestrians stay active; riding contact with moving objects is
deferred. Source integration and gameplay acceptance remain separate.

## Evidence

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
Independent final review is pending at preparation.

The same existing private owned WBN changed from `unsupported / unsupported-root`
to `structurally-decoded / validated-geometry`. Only the verdict was emitted.
This establishes bounded polygon decoding for that input. It does not validate
BVH search trees, child-box enclosure, margins/materials, world placement or
active physical collision. No owned data was uploaded or added to Git.

Latest runtime evidence: the earlier gameplay candidate `b403377481a33e407aeb81b78b8d38984aac4735` refused a guarded mount at `over-0.05-metres`. No game launch, staging, input or runtime test occurred for the composite decoder.

## Next step

Complete source review and publish the focused draft candidate for owner approval.
[PR #37](https://github.com/Jpatching/combine/pull/37) is merged and #34 closed;
its earlier pending-merge handoff is superseded.

Before feeding triangles to Skate, qualify an independent local reference and
establish that this resource supplies the selected street's active collision.
The preserved experiment contains no physical checkpoints. Compare scale,
orientation, floor/curb/wall contact and a clear-space control, with measurements
and tolerances fixed before a runtime trial. An exporter comparison alone cannot
prove active host collision. Do not substitute identity transforms, synthetic
floors or relaxed guards for missing evidence. No runtime launch or integration
was performed by this source slice.

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
