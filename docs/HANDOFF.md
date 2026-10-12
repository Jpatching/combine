# Current context

## Current task

Reviewed: 2026-10-12

Task: implement the owner-approved [persistent candidate and diagnostic workflow #61](https://github.com/Jpatching/combine/issues/61), local GTA IV recovery/testing and keyboard/mouse riding; diagnose the mount blocker before full ride acceptance under #20.

Source branch: `integration/gtaiv-evidence-loop`

Source revision: `f71efeafdd8c2007ba9e4a318c9538cf227e9698`

The candidate PR owns its final publication revision. The current source includes
the preserved short-footprint experiment and its revert, plus an authored
mid-ride collision replacement path. No unrelated local edits were present at
this review.

Disposition: [draft integration PR #62](https://github.com/Jpatching/combine/pull/62)
awaits gameplay qualification and owner acceptance.
Retain [riding #23](https://github.com/Jpatching/combine/pull/23),
[non-flat ground #57](https://github.com/Jpatching/combine/pull/57),
[collector #58](https://github.com/Jpatching/combine/pull/58) and
[context #60](https://github.com/Jpatching/combine/pull/60).
The collector ancestry includes the retained riding/non-flat source. It is
combined here for review, without merging main or activating triangle riding.

## Evidence

Latest runtime evidence: on 2026-10-12, the owner confirmed GTA was at the
retained street spot. A guarded F6 test of the still-loaded, backed-up 4 m
flat-grid experiment ran in windowed foreground gameplay. Fresh status never
showed a mount; the adapter reported `over-0.05-metres`. Movement input was
withheld, and fresh unmounted GTA control was verified afterward. A private
15-second clip was captured and opened locally for owner viewing. This is a
second flat-grid refusal at that spot, not a test of the new source or proof
of physical unevenness, loaded collision, a selected floor/layer or skating.

Latest runtime diagnostic: after the owner accepted an independent in-game
differential witness as an alternative to a direct engine signal, an opt-in
physical-support trace was prepared for R1 with an exact backup. Its authored
preparation/restoration checks passed within a 107-test gate run. The temporary
script was installed only in the isolated runtime after normal shutdown. An
initial relaunch refused a private manifest; a corrected inventory-only check
passed. The next windowed launch prepared a matching session, but preflight
refused `fresh-gameplay`. Local menu capture timed out or classified `unknown`.
No F7 probe input or ground reading was sent, so no physical-support, loading or
layer verdict exists. The game then closed normally and the original checkpoint
script was restored and hash verified. GTA is currently closed. The unmerged
prototype and private records remain outside Git. A separate baseline relaunch
using the restored original script also prepared a matching windowed session,
then refused `fresh-gameplay` and produced an `unknown` local menu classification.
It closed normally without test input. The same startup boundary on both
configurations does not identify the cause; stop repeating it until a changed
diagnostic variable can produce new evidence.

The owner confirmed the retained checkpoint pictures show the intended surfaces:
[confirmation on #39](https://github.com/Jpatching/combine/issues/39#issuecomment-6112509746).
Reuse this decision. Independent collision loading/layer evidence and qualified
checkpoint readings remain unresolved. Full riding acceptance stays under #20.
The merged PR #59 is historical; its former awaiting-approval status is superseded.

Source integration preserves the authored triangle implementation and collector.
The new Rust replacement path updates Session collision without remounting on
both native backends. The exact-source Windows release builds, plugin links and
changed-slope Session harness passed for in-process and worker variants; the
worker parent measured under 1 ms per public call in that harness. Pinned
definition contracts, focused adapter checks and the 105-test repository gate
passed. These authored tests establish replacement behavior, not GTA floor
qualification or gameplay acceptance. Private clips, logs, configurations,
identities and coordinates stay outside Git and AI uploads.

## Next step

Pursue the owner's broader geometry-backed goal under #52/#39/#54. The owner
explicitly set completion acceptance to mounting and continued riding on suitable
GTA floors at different heights, including stacked levels, with collision
coverage updated as the player moves and normal GTA control restored on dismount
or query failure. One qualified street block is only a proof step. The existing
triangle path passes authored tests but normal F6 still invokes the flat-grid
fallback. The authored replacement command is not yet called from live GTA.
First diagnose why the reviewed launch reaches neither a classifiable offline
menu nor fresh windowed foreground gameplay; change one startup variable before
another run and do not guess at menu input. Then run a bounded physical-support
probe with a wrong-floor control and an unchanged checkpoint. Accept it only if
the observed motion distinguishes the intended floor. Establish independent evidence that the
intended GTA floor is loaded at each fixed checkpoint, then collect three valid
host readings per point under the existing 2 cm repeatability and 5 cm
mesh-agreement gates. Select and activate the triangle path only after
those prerequisites. An exact-version collision query is under local analysis;
do not infer a positive witness from standing or a finite height alone.

Read-only exact-build analysis found the `FindGroundZFor3DCoord` diagnostic
string, but no code references or usable collision-query ABI. No loaded-layer
signal or runtime probe has been established. The private Ghidra project is
retained for tracing the native dispatch or physics call path.
Keep the game windowed and preserve input-ownership and restoration checks.
The source candidate remains in draft PR #62; private diagnostic records remain
local. Do not mark it ready or merge until review, gameplay checks and owner
approval pass.

## Session close

Follow [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Keep GTA windowed during all
runtime checks. Source preparation, runtime observation, owner viewing, gameplay
acceptance and merge are separate claims. Report actual checks and recovery;
never turn unknown loading/layer evidence into a pass. Retain private recovery
transactions and all prior branches.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md),
[ground qualification #39](https://github.com/Jpatching/combine/issues/39),
[live riding #54](https://github.com/Jpatching/combine/issues/54),
[complete riding #20](https://github.com/Jpatching/combine/issues/20),
[native authored proof](../research/results/2026-10-11-gtaiv-native-refusal-proof.md).
Historical methods do not authorize new work.
