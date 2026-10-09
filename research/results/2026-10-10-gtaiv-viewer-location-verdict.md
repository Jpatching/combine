# Retained collision resource: viewer location verdict

Question: can the exact retained collision resource be tied to an identifiable
street at unchanged placement, before building ground-comparison tooling?

Verdict: **inconclusive**. The qualified viewer narrows the candidate area and
shows useful building/railway correspondence. It does not yet establish a named
junction or selected-resource coverage of the required ground checkpoints.

Scope: approved [spec #39](https://github.com/Jpatching/combine/issues/39), completed
[viewer qualification #40](https://github.com/Jpatching/combine/issues/40), and
[location investigation #41](https://github.com/Jpatching/combine/issues/41).
Source preparation is integrated at `b75eb037`; decoder source remains unchanged
from `47e8a2c`. Draft [#38](https://github.com/Jpatching/combine/pull/38) remains
subject to owner source approval. This report does not accept gameplay or merge.

## Established evidence

- Earlier exact-version Unity runs passed the authored resource-to-scene fixture,
  including literal asymmetric positions, scale, orientation, height and topology.
  This qualified existing renderer behavior; no behavioral TDD cycle is claimed
  for that baseline. Independent review confirmed both rendered authored shapes.
- The selected private resource was identified by digest, with complete expected
  child/vertex/triangle counts checked in the live viewer. Explicit child matrices
  are identity. The original retained file's digest was rechecked on 2026-10-10
  and still matches. Count checks do not mean every child was individually matched
  to a named landmark.
- The live map and selected overlay remained available. Close and side views were
  captured after moving only the flight camera; collision/map placement was not
  adjusted. Private evidence and its location record remain outside Git/issues.
- Independent visual review corroborated overlay correspondence on a brick
  building, its rooftop water tanks, and a curved elevated railway. Tracks,
  sleepers and railings distinguish that railway from a road ramp. The visible
  ground street below the railway remains gray in these views; adjacency does not
  prove that the selected resource supplies its collision surface.
- Road markings, pavement margins and different vertical levels are visible.
  No uniquely named junction or continuous road-ramp gradient was established.

The owner accepted the earlier viewer appearance and selected a hybrid approach:
AI inspection of selected screenshots to narrow candidates, followed by local
owner confirmation. That appearance acceptance is distinct from street identity.
The latest side view was requested open locally using its native Windows path,
avoiding the WSL-path Photos prompt. Owner street confirmation remains absent.

## Candidate and independent reference

Industrial, Bohan remains a plausible candidate area. Two firsthand guides place
the unfinished Northern Expressway approach at Leavenworth Avenue and describe
the separated bridge sections: [Ratchet12345's guide](https://gamefaqs.gamespot.com/ps3/933036-grand-theft-auto-iv/faqs/54410)
and [YuGiOhFm2002's guide](https://gamefaqs.gamespot.com/ps3/933036-grand-theft-auto-iv/faqs/52838).
Those descriptions support a candidate; they do not uniquely identify the ground
junction in the new views. The curved railway seen beside the building must not
be substituted for the guides' unfinished road approach.

## Stop condition and next decisive evidence

Street placement has not passed. No GTA launch, ground-comparison tooling,
checkpoint measurements, comparison tolerance or wall proof was produced.
This is an inconclusive result rather than disagreement: no paired GTA/mesh
measurements exist.

To reopen the gate, independently identify a named junction connecting the
observed landmark group, obtain the owner's local location confirmation, and
establish that the exact selected mesh covers suitable road, pavement and height-
change surfaces at its retained coordinates. A nearby street, camera position or
railway level alone is insufficient. If those surfaces are outside this resource,
do not silently substitute another resource or move this one into agreement.

Only after that gate passes should the ground experiment freeze tolerances and
repeatability rules, then compare observations and predictions at identical
coordinates. Ground agreement would cover those checkpoints only; walls and
active GTA collision remain separate proofs.
