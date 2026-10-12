# Retained checkpoint tooling and incomplete street qualification

Reviewed: 2026-10-10

The owner authorized continuing [#20](https://github.com/Jpatching/combine/issues/20)
from the retained four-point preparation, confirmed the intended Burger Shot /
Drill Street / Lompoc Avenue area, and confirmed two TDD boundaries: authored
resource to observable viewer scene, and authored readings to a public comparison
command. The owner subsequently selected a focused stacked PR after raising
concerns about the growing parent branch and shared mouse interference.

## Source slice

Branch `implement/gtaiv-ground-checkpoints` starts at
`dca76b746bc021e846a44570790adcfd089836ee`, the retained head of draft
[#38](https://github.com/Jpatching/combine/pull/38). The owner authorized this
stacking exception to the normal new-slice-from-main convention. Parent source,
decoder, resource placement, gameplay candidate and mounting guard are preserved.
The issue owns the final publication revision and child PR link.

The [Editor marker command](../../tools/gtaiv-viewer/README.md) validates supplied
centroids against the selected collision-only scene root, displays temporary
anchors without colliders, preserves previous markers on invalid input and clears
its transient roots/materials. Scene membership is not intended-surface or active
GTA collision qualification. The [comparison command](../../tools/gtaiv-collision/README.md#compare-qualified-ground-readings)
implements the frozen three-reading, 0.02 m spread and 0.05 m per-reading error
rules with complete-set agreement and stable-failure precedence. It queries no
natives and trusts separately established qualification/observation flags.

## Actual checks

- The authored resource-to-scene marker check compiled but failed with the public
  command missing, wrapper exit 6. After implementation it passed, exit 0.
- A subsequent public Clear check failed because ordinary Unity object search
  excludes unsaved `DontSave` roots. Including the tagged transient scene roots
  fixed it. Final execution in pinned Unity Editor 6000.4.0f1 emitted fixture PASS,
  no C# compiler errors and wrapper exit 0. Literal anchors, unchanged meshes,
  unrelated visibility, no colliders, invalid-input preservation and cleanup
  were checked. Private setup/logs remain local.
- `python3 tests/test_gtaiv_ground_comparison.py -v` passed six authored command
  test groups, including inclusive boundaries, unstable/unavailable data,
  unchanged coordinates, missing points, invalid identities, stable disagreement
  precedence and duplicate JSON-key rejection.
- `python3 scripts/verify.py` passed 79 tests and 66-document/context checks for
  the source and documentation follow-up. Publication validation is recorded on
  the issue.
- Independent Standards and Spec reviews found no actionable code defects.
  Final documentation review caught an imprecise threshold sentence; it was
  corrected to require an error above 0.05 m for disagreement.
  The reviewers did not reproduce owned-file or native gameplay observations.

## Live evidence and failures

The retained private resource identity/counts were rechecked unchanged. The
existing viewer loaded normally, without a timeout, and accepted all four
retained centroid markers. Actual Hide/Show logs accompany the final reliable
same-camera map-only/restored pair; private images were opened locally.

R1, P1 and H2 labels are visible; H1 is below the viewport. Independent visual
review supports general road and paved-margin association, but the anchor bases
are insufficiently distinct for exact pavement/verge and upper/lower road-layer
proof. Labels above the ground do not resolve those questions. The live lab used
the initial marker implementation; the later transient cleanup fix was verified
in the authored fixture, not restaged into that live trial.

Earlier partial captures and a foreground-refused capture are retained. The
refused attempt produced no fresh pair; stale copied frames are explicitly
excluded as new evidence. Shared cursor helpers were stopped after owner feedback.
Future inspection should execute commands inside the Editor and capture clear
anchor bases without shared-pointer input.

Each attempted trial has a concise private SSH-readable behavior/result/media/
blocker record. No gameplay clip exists for this slice; the checkpoint gate did
not pass. PC evidence playback is available; phone playback is not configured.
No GTA launch, paired ground readings, riding, restart repeat, curb/wall contact
or owner gameplay acceptance occurred. Current physical verdict is inconclusive.

## Next objective

Finish exact surface/layer qualification of R1/P1/H1/H2, including a clear H1
view. Keep the existing resource and coordinates. Then collect three explicitly
successful, loaded, intended-layer GTA readings at each fixed horizontal point,
compare them with unchanged mesh predictions and report agreement, disagreement
or inconclusive. The native collector must establish success separately from a
finite height. Ground agreement is limited to these points.

After collision qualification, reuse the preserved GTA/Skate candidate for a
20–40 second uncut mount → push → steer → dismount → ordinary GTA recovery trial,
then repeat after normal restart. Retain refused/failed trials too. Visible board
presentation and curb/wall contact remain fuller street-demo requirements.
The source slice is inspection tooling, not a new Skate integration or an
accepted ride. Parent/child source merge and gameplay acceptance stay separate.

## Session lessons

Use a focused branch before adding a new independently testable source behavior;
review the child against its pinned parent rather than expanding an old PR.
Prefer direct Editor operations for repeatable inspection; shared-pointer input
made framing fragile and interfered with the owner's PC use. Existing CI already
runs the repository gate. No new global steering rule or speculative framework
was added. Preserve this result and the live issue before changing context.
