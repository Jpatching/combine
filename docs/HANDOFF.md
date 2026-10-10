# Current context

## Current task

Reviewed: 2026-10-10

Task: prioritize a visible guarded flat-patch GTA/Skate mount/move/dismount trial under [#20](https://github.com/Jpatching/combine/issues/20), continuing the bounded placement work of [#39](https://github.com/Jpatching/combine/issues/39).

Source branch: `integration/gtaiv-skate-loop`

Source revision: `849c631a2ec456ea1491f59f1e0bdfa540d867b6`

This is the capture-support integration checkpoint. The issue records later
publication revisions; the installed adapter remains the separate runtime identity below.

Disposition: the owner selected visible ride proof before completing street
qualification. Reuse the preserved candidate on a surface accepted by its unchanged
flat-patch guard. Street qualification remains unresolved; this diagnostic does not
prove decoded mesh contact. Draft [#23](https://github.com/Jpatching/combine/pull/23)
is the existing integration PR. Draft [#42](https://github.com/Jpatching/combine/pull/42)
and parent [#38](https://github.com/Jpatching/combine/pull/38) remain preserved and
unmerged. No source or gameplay acceptance is implied.

The target trial is 20–40 seconds uncut: mount, push, both steering directions,
dismount and ordinary GTA recovery, then repeat after normal restart. Preserve
failed/refused takes. Shared mouse automation is stopped; private keyboard helpers
must refuse unless GTA is already focused. Keep branches, candidates and evidence.
The wider target still includes visible board presentation, actual street contact
and normal GTA vehicle use.

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
frames are excluded as fresh evidence. No paired GTA readings have passed. The [visible ride record](../research/results/2026-10-10-gtaiv-visible-ride.md)
records an actual brief mount and native control/camera recovery, an incomplete
32-second clip opened locally, and a second attempt refused before input because
status became stale. PC evidence viewing works; phone playback is not configured.

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

Latest runtime evidence: preserved candidate `b403377481a33e407aeb81b78b8d38984aac4735`
loaded from the staged runtime and mounted briefly. No fresh push/steer verdict
arrived; `surface/input/time unavailable` ended the ride, followed by verified
native player control and owned-camera destruction. The owner saw entry into Skate
without board/animation. A second take refused before input; GTA remained running
but status was stale. A subsequent health check found GTA responsive but
minimized/not focused; the owner was asked to restore it manually. A complete
loop and restart repeat remain unproved. Runtime
files and guard are unchanged. Earlier refusal and camera-fix trials are retained.

## Next step

Restore the minimized GTA window manually, then re-establish fresh on-foot
gameplay in the preserved runtime with a connected
neutral controller and GTA focused. Start private recording before the mount,
run the existing guarded push/steer playback, dismount and observe walking
recovery. Open the actual clip locally. Retain refusal and incomplete evidence;
repeat after normal restart only when prerequisites are established. The existing
short recorder has a private 32-second copy; Linux encoding avoids installing a
new Windows capture dependency. Preserve the first incomplete take and the
second pre-input refusal. Universal Modder recording CLI help passed, but
Windows FFmpeg was unavailable in the bounded lookup; no UM recording is claimed.

Capture-support source now generates per-point oblique/overhead Hide/Show pairs
inside Unity without desktop input. An isolated authored fixture executed missing
menu failure, then passed eight meaningful images and scene restoration; existing
output refusal also passed. This is inspection tooling only and has not qualified
any live checkpoint. Preserve it for the subsequent street step. Final shared-centroid validation
fix also passed the authored fixture; both independent review axes have no
remaining actionable finding.

After the visible diagnostic, finish intended surface/layer proof at unchanged R1/P1/H1/H2 coordinates using
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

Keep all trial attempts visible with concise private SSH-readable
behavior/result/clip/blocker records. Source integration is not
runtime acceptance. Ground agreement covers these points only; curb/wall contact,
visible board/animation and fuller street riding remain separate requirements.

The [presentation comparison](../research/results/2026-10-10-gtaiv-visible-ride.md#why-presentation-is-missing)
shows that Session already evaluates animation, but the GTA wire carries only
position/heading. Next visible presentation slice: prove an exact-version drawing
interface, then a board driven by the accepted pose with dismount/failure cleanup,
followed by rider pose mapping. Asset import alone does not supply that interface.

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
