# Current context

## Current task

Reviewed: 2026-10-12

Task: implement the owner-approved [persistent candidate and diagnostic workflow #61](https://github.com/Jpatching/combine/issues/61), local GTA IV recovery/testing and keyboard/mouse riding; diagnose the mount blocker before full ride acceptance under #20.

Source branch: `integration/gtaiv-evidence-loop`

Source revision: `844fcdad69be245c4a8df9c36a6c1f1019599d5f`

This is the synchronized-main starting point. The candidate PR owns its final
publication revision.

Disposition: integrated candidate in preparation; No PR exists for this candidate yet.
Retain [riding #23](https://github.com/Jpatching/combine/pull/23),
[non-flat ground #57](https://github.com/Jpatching/combine/pull/57),
[collector #58](https://github.com/Jpatching/combine/pull/58) and
[context #60](https://github.com/Jpatching/combine/pull/60).
The collector ancestry includes the retained riding/non-flat source. It is
combined here for review, without merging main or activating triangle riding.

## Evidence

Latest runtime evidence: on 2026-10-12 read-only checks found one windowed but
unresponsive GTA IV process with unknown native gameplay state. Authorized normal
recovery returned `normal-close-refused`; foreground-first opening still timed out.
The owner subsequently approved one exact-process hung termination: its exit was
verified and the replacement GTA process is responding, windowed and foreground.
The signed executable's launcher handoff initially returned `process-changed`;
the local opener subsequently verified the replacement window without another
termination. Private selected-window observation was unavailable before recovery;
no diagnostic key was sent.
Corrected session preparation identifies `inventory-mismatch-definitions` against
each of three retained manifests. The new controls are source-tested and freshly
built in an isolated worker bundle, not installed
or accepted in gameplay. The retained windowed-game trials reported the default
flat-route refusal `over-0.05-metres`; subsequent session records describe a
non-finite ground query after offline menu recovery. These observations do not
establish that the real ground is uneven or that querying is qualified.
Current runtime state must be checked independently before new input.

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

Complete and verify the guarded runner and private evidence hub under #61.
Use [the evidence hub guide](EVIDENCE_HUB.md) for its commands and private setup.
Resolve the unresponsive process within the owner's recovery authority and stage
one reviewed, backed-up runtime bundle with exact source/build provenance. Do not
regenerate a matching manifest from unverified installed bytes. Normal recovery
remains the default; any hung termination requires explicit owner approval.
Present one candidate revision/evidence bundle for explicit approval. Do not merge
until review, checks and owner approval pass.

Diagnose native query availability at one checkpoint before all-four-point
collection or triangle activation. Preserve three valid readings per point,
2 cm maximum spread and 5 cm mesh error, independent loading/layer evidence,
fixed geometry, the flat-route guard and lost-focus/input-ownership safeguards.
Ten diagnostic attempts are a maximum; unchanged failures stop a scenario and
require a new experimental variable. Restart/controller acceptance remains separate.

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
