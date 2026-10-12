# Current context

## Current task

Reviewed: 2026-10-12

Task: implement the owner-approved [persistent candidate and diagnostic workflow #61](https://github.com/Jpatching/combine/issues/61), local GTA IV recovery/testing and keyboard/mouse riding; diagnose the mount blocker before full ride acceptance under #20.

Source branch: `integration/gtaiv-evidence-loop`

Source revision: `0fa71777187f59d88be42eb4a4ec213eff030fdb`

The candidate PR owns its final publication revision. The current source includes
a preserved short-footprint experiment and its revert; the checkout is clean.

Disposition: integrated candidate in preparation; No PR exists for this candidate yet.
Retain [riding #23](https://github.com/Jpatching/combine/pull/23),
[non-flat ground #57](https://github.com/Jpatching/combine/pull/57),
[collector #58](https://github.com/Jpatching/combine/pull/58) and
[context #60](https://github.com/Jpatching/combine/pull/60).
The collector ancestry includes the retained riding/non-flat source. It is
combined here for review, without merging main or activating triangle riding.

## Evidence

Latest runtime evidence: a backed-up isolated worker bundle was staged after
normal GTA shutdown. The owner advanced the offline menu. Preflight and the
retained checkpoint passed in windowed, foreground gameplay. One mount trial of
the short 4 m flat-grid experiment refused `over-0.05-metres`; input cleanup and
fresh unmounted GTA control were verified. The owner confirmed the player was
standing in the middle of the road. This does not establish physical unevenness,
loaded collision, a selected floor/layer, or successful skating.

The live GTA process still has the experimental 4 m bundle loaded, while the
source checkout reverted that experiment to the original 8 m flat fallback.
Reconcile source, staged artifacts and session before another guarded test.
Private runtime backups and evidence are retained. The pre-revert experiment
passed seven focused adapter suites and the 105-test repository gate; those
checks did not prove a mount fix. No post-revert gate has been claimed.

The owner confirmed the retained checkpoint pictures show the intended surfaces:
[confirmation on #39](https://github.com/Jpatching/combine/issues/39#issuecomment-6112509746).
Reuse this decision. Independent collision loading/layer evidence and qualified
checkpoint readings remain unresolved. Full riding acceptance stays under #20.
The merged PR #59 is historical; its former awaiting-approval status is superseded.

Source integration preserves the reviewed authored triangle implementation and
collector. Existing native refusal proof qualifies authored behavior, not street
collision. The new evidence hub records source checks, named runtime diagnostics
and pending owner acceptance separately. Private clips, logs, configurations,
identities and coordinates stay outside Git and AI uploads.

## Next step

Pursue the owner's broader geometry-backed goal under #52/#39/#54. The owner
explicitly set completion acceptance to mounting and continued riding on suitable
GTA floors at different heights, including stacked levels, with collision
coverage updated as the player moves and normal GTA control restored on dismount
or query failure. One qualified street block is only a proof step. The existing
triangle path passes authored tests but normal F6 still invokes the flat-grid
fallback and its collision geometry is fixed for one ride. Establish independent
evidence that the intended GTA floor is loaded at each fixed checkpoint, then
collect three valid host readings per point under the existing 2 cm repeatability
and 5 cm mesh-agreement gates. Select and activate the triangle path only after
those prerequisites. An exact-version collision query is under local analysis;
do not infer a positive witness from standing or a finite height alone.

REA CLI has a privately installed, checksum-verified Ghidra provider. Its first
read-only pass over the owned executable hit the default startup timeout; a
longer pass completed an x86 PE overview. REA CLI reimports the target for each
query, so a persistent, private Ghidra project was created under `/tmp` for
fast local follow-up. A broad `CWorld` text search found only an unrelated type.
The exact build's `FindGroundZFor3DCoord` diagnostic string was located, but
neither analyzed code references nor bounded raw pointer references were found
for that seed. No collision-query ABI, loaded-layer signal or runtime probe has
been established. Next trace the native dispatch or physics call path using
the retained index; stop if call arguments or output bounds remain ambiguous.
The private project was archived and its archive integrity checked so a fresh
context can restore it without repeating the ten-minute import.
Reconcile the live experimental runtime with source before more guarded input.
Keep the game windowed and preserve input-ownership and restoration checks.
Present one candidate revision/evidence bundle for explicit approval. Do not
merge until review, checks and owner approval pass.

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
