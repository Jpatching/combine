# Retained street resource: ground checkpoint preparation

Observed: 2026-10-10, following the owner's instruction to proceed from the
[named local connection](2026-10-10-gtaiv-street-reference.md). Existing branch
`implement/gtaiv-composite-collision`, starting at
`913370c7c400a68dc797919c7c83aadd8e141cfa`. The source implementation remains
`2f228b4ae128090d59dde36ffe67cdd916ed5ec6`; no supported tooling or game runtime
was changed for this preparation.

## Current result

**Four mesh-coordinate candidates retained; checkpoint qualification incomplete.**
The named area remains Industrial, Bohan, around Burger Shot at Drill Street /
Lompoc Avenue and the unfinished Northern Expressway approach. A new, closer
same-camera map-only/restored pair was captured and automatically opened locally.
Only the inspection camera moved; resource and map placement stayed fixed.

After correcting the pedestrian strip and upper endpoint, independent review
supports all four intended surfaces as image candidates. Their exact coordinate
and surface/layer association still need qualification. No paired GTA/mesh measurement exists;
ground agreement remains **inconclusive**. Walls remain a later proof.

| Point | Intended surface | Preparation status |
| --- | --- | --- |
| R1 | Ordinary shoreline road beside Burger Shot | Image candidate independently supported; retained mesh centroid |
| P1 | Pale curb/paved margin beside the shoreline road, west of the parked trailer | Corrected image candidate independently supported; retained mesh centroid; precise surface association pending |
| H1 | Lower portion of the unfinished road approach | Image candidate independently supported; retained mesh centroid |
| H2 | Upper portion of that same road carriageway | Corrected image candidate independently supported, away from divider; retained mesh centroid |

The selected endpoint centroids have different decoded heights. That is evidence
of non-flat candidate geometry, not measured GTA contact or a verified continuous
longitudinal slope. The neighbouring elevated railway is excluded.

## What was checked and rejected

The existing bounded decoder read the same digest-verified retained resource and
matched retained aggregate vertex/triangle counts. Face centroids provide fixed
mesh-coordinate candidates without moving geometry, creating a new ground-query
implementation or querying GTA. An ignored local analysis associated those
centroids with the existing viewer using its camera Inspector readings and
pinned perspective settings, corroborated by the live Inspector. Camera readings have display precision; this
association is provisional and is not a ground sample or exact pixel proof.
Private geometry, identities, coordinates, screenshots and records remain local.

Independent visual review rejected the initial apparent pavement points because
they overlap a parked trailer/box vehicle. It suggested the nearby pale pedestrian
strip instead. Follow-up review rejected two replacement centroids on the brown
grass/dirt verge and supported the alternative on the pale curb/paved margin.
The western underpass target lacked a reliable centroid association
and was excluded. An optional middle approach point was also excluded because
nearby centroids can belong to a lower layer. Failure to associate a centroid does
not prove the mesh has a hole or that GTA collision is absent.

The upper approach target was moved inside the lower point's carriageway;
the initial upper target was too close to the divider and opposite lane.
These are checkpoint-selection corrections, not adjustments to resource placement
or numerical fitting to host measurements.

Unity's clipboard coordinate-reading helper stalled and was stopped by its exact
task identity. The isolated viewer was preserved. A subsequent read-only local
Inspector/OCR capture succeeded; no clipboard-derived coordinate result is used.
The actual Hide/Show pair, including the closer map context, was opened through
`scripts/workbench.py evidence` with exit 0. Local opening is not owner acceptance.

## Comparison rules fixed before measurement

These numeric rules are frozen for this candidate experiment before observing
any paired GTA measurements. They do not authorize tooling, game launch or
waive the remaining checkpoint gate.

- Use the retained fixed GTA horizontal coordinates for each qualified point;
  compare GTA ground height with the mesh height at those identical coordinates.
  Do not fit a translation, rotate geometry or substitute a nearby sample.
- Require **three valid readings per point** after the relevant ground is loaded.
  The maximum minus minimum height must be **at most 0.02 m**. Otherwise the
  point is unavailable because the readings are unstable.
- Require explicit query success, finite values and an independently identified
  intended surface/layer. Failed, unloaded, unstable or wrong-layer results are
  unavailable. Do not replace unavailable results with zero or a fallback point.
- Compare each valid reading to the fixed mesh prediction. The absolute vertical
  error must be **at most 0.05 m**, including the boundary. All three readings
  must pass; averaging must not conceal a failing reading.
- Report **disagreement** if any stable, valid point exceeds tolerance. Report
  **agreement** only if every retained qualified point has three stable, valid
  readings and all pass. Otherwise report **inconclusive** and identify the
  unavailable points. Do not drop a point after seeing its GTA result to obtain
  agreement.

The limits are experiment choices, not measured engine accuracy or changes to
existing runtime guards. Any necessary protocol revision must be explicit,
recorded before new observations, and treated as a separate experiment.
Agreement covers these ground points only, not walls, the whole resource,
active collision everywhere or Skate integration.

## Remaining work

Confirm the replacement pavement centroid is on the intended pedestrian strip
and the upper centroid is inside the same road carriageway. Resolve foreground
surface/lower-layer ambiguity at unchanged coordinates; add a confirming view or
local scene inspection where needed. Complete local owner location confirmation.
Then retain the qualified point set before implementing any paired measurement
slice at an agreed public test boundary. Missing qualification remains an
inconclusive stop under [spec #39](https://github.com/Jpatching/combine/issues/39).
