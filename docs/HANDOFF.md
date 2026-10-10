# Current context

## Current task

Reviewed: 2026-10-10

Task: qualify four retained street checkpoints and then prove one repeatable GTA/Skate mount/move/dismount loop under [#20](https://github.com/Jpatching/combine/issues/20), continuing the bounded placement work of [#39](https://github.com/Jpatching/combine/issues/39).

Source branch: `implement/gtaiv-ground-checkpoints`

Source revision: `dca76b746bc021e846a44570790adcfd089836ee`

This is the fixed parent/starting revision. The issue records the final child
publication revision; this snapshot travels with that commit.

Disposition: focused checkpoint tooling is on the owner-authorized stacked branch above draft [#38](https://github.com/Jpatching/combine/pull/38); [#20](https://github.com/Jpatching/combine/issues/20) owns its child draft-PR link and final publication revision. Both source approval and physical qualification remain pending. The owner confirmed the intended Burger Shot / Drill Street / Lompoc Avenue area; exact checkpoint surface/layer qualification is incomplete. Ground verdict: inconclusive.

The owner authorized unchanged-resource qualification, paired GTA readings only
after that gate, and a preserved-candidate uncut gameplay trial with restart
repeat after collision qualification. Shared mouse automation is stopped. Preserve
all branches, candidates and private failed/partial evidence. The wider target is
actual Skate mechanics and visible board presentation in GTA IV, with dismount
returning ordinary GTA movement, camera and vehicle use. This source slice changes
inspection tooling, not the Skate runtime or mounting guard.

## Evidence

The [checkpoint tooling record](../research/results/2026-10-10-gtaiv-checkpoint-tooling.md)
contains the current implementation, actual failures/passes and limitations.
The authored marker command failed before implementation and passed afterward;
transient cleanup separately failed and then passed after correction. Final pinned
Unity 6000.4.0f1 fixture emitted PASS, no C# compiler errors and wrapper exit 0.
Six authored comparison-command test groups pass. The pre-documentation repository
gate passed 79 tests and 65-document/context checks; the issue owns publication
checks and final independent reviews.

The retained resource identity and aggregate counts remain unchanged. Normal live
viewer loading and actual Hide/Show markers accompany the latest reliable
same-camera pair, opened locally. R1/P1/H2 labels are visible; H1 is outside the
frame. Independent image review supports general association but cannot identify
all exact anchor bases and height layers. That live trial used the first marker
implementation; the final cleanup fix was verified only in the authored fixture.
Partial captures and a foreground-refused attempt remain private. Stale duplicate
frames are excluded as fresh evidence. No real GTA readings or gameplay clip were
produced. PC evidence viewing exists; phone playback is not configured.

Earlier [checkpoint preparation](../research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md)
retains four exact mesh-centroid candidates and frozen rules. Owner location
confirmation, previously pending in that dated record, is now complete. The
[street-reference follow-up](../research/results/2026-10-10-gtaiv-street-reference.md)
and [location verdict](../research/results/2026-10-10-gtaiv-viewer-location-verdict.md)
support the named local connection around Industrial, Bohan and the unfinished
Northern Expressway approach. That bounded connection does not qualify active
GTA collision. [#40](https://github.com/Jpatching/combine/issues/40) is closed with
viewer qualification; [#41](https://github.com/Jpatching/combine/issues/41)'s initial
inconclusive investigation is historical, not a passed complete ground gate.

Decoder source remains `47e8a2c0d46981ffb3b9cfeec5afd98eb91bffbb`.
The [composite investigation](../research/results/2026-10-09-gtaiv-composite-transforms.md)
and [placement investigation](../research/results/2026-10-09-gtaiv-resource-placement.md)
record its bounded geometry/transform support and remaining limits. Private
bootstrap/read-access setup stays outside tracked source; resource placement and
pins were preserved. Selected Game-only viewer screenshots are authorized for
AI inspection; game files, private identities and exact coordinates stay private.

Latest runtime evidence: preserved GTA/Skate candidate `b403377481a33e407aeb81b78b8d38984aac4735` previously refused a guarded mount at `over-0.05-metres`, with fresh GTA control retained. Earlier separate native trials established mounted dismount control restoration and camera destruction after a definition fix. A complete push/steer/recovery loop and visible board presentation remain unaccepted. No GTA launch or runtime change occurred in the checkpoint tooling slice.

## Next step

Finish intended surface/layer proof at unchanged R1/P1/H1/H2 coordinates using
clear anchor-base views, including H1, through commands executed inside the
Editor without shared-pointer automation. Reuse the existing viewer, retained
resource, named connection and private evidence; avoid repeating acquisition or
installation. Centroid membership and labels alone are insufficient.

Once qualified, freeze the full point set and collect three explicitly successful,
loaded, intended-surface GTA ground readings at each identical horizontal point.
Maximum repeat spread is 0.02 m; every reading must be within 0.05 m absolute
vertical error of the mesh prediction. Both limits are inclusive. Failed,
unloaded, non-finite, shifted, unstable or wrong-layer results are unavailable.
The [comparison command](../tools/gtaiv-collision/README.md#compare-qualified-ground-readings)
implements those rules but supplies no native collector. A finite returned height
alone does not establish native success. Any stable valid error above 0.05 m gives disagreement;
only all four complete passes give agreement; otherwise inconclusive. Preserve
points and placement; do not fit offsets or average away a failure.

After collision qualification, reuse the preserved candidate for a 20–40 second
uncut mount, push, steer, dismount and ordinary GTA recovery trial, then repeat
after normal restart. Keep failed/refused trials visible with concise private
SSH-readable behavior/result/clip/blocker records. Source integration is not
runtime acceptance. Ground agreement covers these points only; curb/wall contact,
visible board/animation and fuller street riding remain separate requirements.

## Session close

Follow [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). The owner authorized a focused
stacked PR based on #38 rather than expanding its cumulative diff. Preserve
published history; the child waits for parent integration and explicit source
acceptance before merge. The issue records the final revision, checks and PR.
Start a fresh independent implementation ticket only from durable current status;
compact when relevant context must survive. Clearing this chat does not clean Git.

Preserve draft [#23](https://github.com/Jpatching/combine/pull/23), in-process/worker
candidates, recovery branches and private setup/media. #21/#22 remain blocked.
Keep game assets, exact coordinates, settings, identities and raw logs outside
Git and uploads. Source review, owner source approval, measurements, gameplay,
owner gameplay acceptance and release are distinct claims.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[physical collision report](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[native query report](../research/results/gtaiv-120059-native-collision-feasibility.md).
The separate street experiment is preserved at
`a4fec7364c957bd4bf80e3fb6eb80e04ba6eb054` on
`prototype/gtaiv-street-collision`; its acquisition code is not incorporated here.
PR #37 is merged; the earlier #34 pending-merge handoff is superseded.
