# Retained collision resource: viewer location verdict

Question: can the exact retained collision resource be tied to an identifiable
street at unchanged placement, before building ground-comparison tooling?

Verdict: **named local connection supported; ground-preparation gate incomplete**.
The retained overlay is linked to Industrial, Bohan, around Drill Street / Lompoc
Avenue and the unfinished Northern Expressway approach. Exact selected-resource
coverage of road, pavement and height-change checkpoints and owner location
confirmation remain pending. Ground agreement is inconclusive: no paired
GTA/mesh measurements exist.

Scope: approved [spec #39](https://github.com/Jpatching/combine/issues/39), completed
[viewer qualification #40](https://github.com/Jpatching/combine/issues/40), and
[location investigation #41](https://github.com/Jpatching/combine/issues/41).
Source preparation is integrated at `b75eb037`; decoder source remains unchanged
from `47e8a2c`. Draft [#38](https://github.com/Jpatching/combine/pull/38) remains
subject to owner source approval. This report does not accept gameplay or merge.

## Earlier evidence before named identification

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
The earlier side view was requested open locally using its native Windows path,
avoiding the WSL-path Photos prompt. Owner street confirmation remains absent.

## Focused visibility implementation

Following the owner's `implement` request, selected-overlay Hide/Show commands
were added at the existing authored resource-to-scene boundary. The fixture
failed on the missing Hide command before implementation and passed afterward;
both behavioral runs compiled without C# errors. The failing CLI wrapper returned
6; the passing wrapper returned 0. Literal world positions and face topology
remain checked after restoration, and an unrelated renderer remains enabled.
Mixed and absent selections are refused. Those guard checks are qualification,
not a separately observed red/green cycle. Earlier package GUID errors prevented
execution and do not count as behavioral failures.

A reviewed private bootstrap change adds a dedicated identity parent for the
exact resource's mesh children. Live digest/count checks still passed and loading
released normally. A same-camera game-view pair was captured after actual HIDDEN
and SHOWN markers and automatically opened locally. Independent visual review
confirmed disappearance/restoration of green surfaces with the crane, industrial
building, truss crossing and skyline retaining their positions. Green geometry
broadly follows the foreground bridge approach, parts of the yard, a small
building and roadside/verge surfaces. Farther disconnected bridge spans remain
uncovered. The arrow-like patterns on the foreground deck appear only with the
overlay, so they are not independent rendered-map road markings.

This establishes a usable inspection control and broad visual correspondence.
That pair alone did not establish a named junction, exact coordinate agreement,
coverage of the required ground checkpoints, or active GTA collision. Its verdict
was **inconclusive**. No game files or private coordinates were added to source or tracker evidence.

The focused source revision is `2f228b4ae128090d59dde36ffe67cdd916ed5ec6`, reviewed
against `51e258a`. Independent Standards and Spec reviews found no actionable
findings. `python3 scripts/verify.py` passed 73 tests and 63-document/context
checks. Unity compilation and live pixel evidence are separate from that gate.
The final authored rerun after sharing unchanged literal expectations emitted
PASS with no C# errors and CLI exit 0; exact staged source and pins were rechecked.

## Earlier candidate and independent reference

Industrial, Bohan was initially a plausible candidate area. Two firsthand guides
place the unfinished Northern Expressway approach at Leavenworth Avenue and describe
the separated bridge sections: [Ratchet12345's guide](https://gamefaqs.gamespot.com/ps3/933036-grand-theft-auto-iv/faqs/54410)
and [YuGiOhFm2002's guide](https://gamefaqs.gamespot.com/ps3/933036-grand-theft-auto-iv/faqs/52838).
Those descriptions support a candidate; they do not uniquely identify the ground
junction in those earlier views. The curved railway seen beside the building must not
be substituted for the guides' unfinished road approach.

## Named connection: later same-day follow-up

New camera-only views connect Burger Shot, the adjoining streets, Menala Metal's
tank-roof building, the railway and the unfinished waterfront deck in one scene.
The latest same-camera map-only/restored pair was automatically opened locally.
The retained file's digest still matches and live digest/count/normal-loading
markers remain available, including actual HIDDEN/SHOWN markers and zero C# error
entries. Neither selected resource nor map placement was adjusted.

[Rusk's original base GTA IV guide](https://gamefaqs.gamespot.com/xbox360/933037-grand-theft-auto-iv/faqs/53734)
places Industrial Burger Shot at Drill Street / Lompoc Avenue, Menala Metal near
Jackhammer Street / Lompoc Avenue, and the separated unfinished bridge approach
at Northern Expressway / Leavenworth Avenue. The primary investigator inspected Psy's original
gameplay images/map to distinguish that waterfront route from the alternative
South Bohan construction approach. See the cited [street-reference follow-up](2026-10-10-gtaiv-street-reference.md).

Independent visual review supports the resource's connection to this named local
street area. Ground roadway/frontage and elevated geometry are visible checkpoint
candidates. Patchy overlay appearance proves neither complete coverage nor gaps;
depth interference is possible. This resolves the general street-name search,
not precise checkpoint geometry or active GTA ground collision. The previous
inconclusive investigation remains historical; this is new, bounded evidence.

## Remaining gate and next decisive evidence

The later [checkpoint preparation](2026-10-10-gtaiv-ground-checkpoint-preparation.md)
retains four mesh-centroid candidates and fixes numeric comparison/repetition
rules before host measurements. Surface association remains provisional; the
complete ground-preparation gate has not passed. No GTA launch, ground-query or
comparison implementation, paired checkpoint measurements or wall proof exists.
This is an inconclusive result rather than disagreement: no paired GTA/mesh
measurements exist.

The named local connection is now supported. Obtain the owner's local location
confirmation and establish that the exact selected mesh covers suitable road,
pavement and height-change surfaces at its retained coordinates. A nearby street, camera position or
railway level alone is insufficient. If those surfaces are outside this resource,
do not silently substitute another resource or move this one into agreement.

Only after that gate passes should the ground experiment compare observations
and predictions at identical coordinates under the already fixed rules.
Ground agreement would cover those checkpoints only; walls and
active GTA collision remain separate proofs.
