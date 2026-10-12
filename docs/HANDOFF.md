# Current context

## Current task

Reviewed: 2026-10-12

Task: implement the owner-approved [persistent candidate and diagnostic workflow #61](https://github.com/Jpatching/combine/issues/61), local GTA IV recovery/testing and keyboard/mouse riding; diagnose the mount blocker before full ride acceptance under #20.

Source branch: `integration/gtaiv-evidence-loop`

Source revision: `a7449a90576fe889f76d4e07ea2576cb2a455233`

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

Latest runtime diagnostic: the launcher now retries foreground focus after the
window responds. A monitored windowed launch reached verified foreground, and
guarded offline menu input reached fresh gameplay. The baseline preflight and
retained checkpoint check passed. Temporary physical-support probes then ran at
R1, P1 and H1. Their traces show settling near a support surface, but do not
identify which floor GTA selected or reject a wrong floor. No loaded-floor or
layer criterion passed. The owner stopped the next probe before input; GTA
closed normally. The original checkpoint script was restored with its exact
backup hash, and the private inventory-only check passed. GTA is currently
closed. Probe scripts, traces and recovery records remain private and outside Git.

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
The startup foreground failure is resolved. Narrow the next decision to one
bounded witness that names the intended loaded floor at each checkpoint and
fails when the wrong floor is selected. The owner accepts either a direct signal
or an independent differential observation with that property. Do not repeat
the physical-support trace alone or resume an open-ended native ABI search as
the active plan. Keep those attempts as historical diagnostics. Once the witness
passes, collect three valid host readings per point under the existing 2 cm
repeatability and 5 cm mesh-agreement gates, then select and activate the
triangle path and test stacked-floor riding. No Rust candidate has been staged
in GTA, and gameplay acceptance remains open.
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
