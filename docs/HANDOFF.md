# Current context

## Current task

Reviewed: 2026-10-13

Task: implement the owner's [automatic-floor, board, GTA animation and tricks specification #64](https://github.com/Jpatching/combine/issues/64), starting with the usable ride prerequisite [#20](https://github.com/Jpatching/combine/issues/20) under [workflow #61](https://github.com/Jpatching/combine/issues/61).

Source branch: `integration/gtaiv-skate-spec64`

Source revision: `093497607ee891ee286a55e7e5bf762173786bb8`

The candidate PR owns its final publication revision. Reviewed source adds a
bounded mount, push, both steering directions and dismount proof, plus read-only
recovery reconciliation. Full riding acceptance remains open. The pre-existing
uncommitted evidence measurement display is preserved separately.

Disposition: [draft integration PR #69](https://github.com/Jpatching/combine/pull/69)
awaits gameplay qualification and owner acceptance.
Retained [draft PR #62](https://github.com/Jpatching/combine/pull/62) is unchanged
and awaits gameplay qualification and owner acceptance.
Retain [riding #23](https://github.com/Jpatching/combine/pull/23),
[non-flat ground #57](https://github.com/Jpatching/combine/pull/57),
[collector #58](https://github.com/Jpatching/combine/pull/58) and
[context #60](https://github.com/Jpatching/combine/pull/60).
The collector ancestry includes the retained riding/non-flat source. It is
combined here for review, without merging main or activating triangle riding.

## Evidence

Latest runtime evidence: the owner reports mounting works at the teleport spot,
but stops again elsewhere. Retained local log classification also contains mounted
notifications. The retained prepared setup has two surfaces, each with a 3 m
radius. The same qualified surfaces are retained in the staged candidate; they
establish neither a measured complete ride nor automatic floor coverage.

The earlier H2 witness distinguished stacked supporting floors and passed three
queries per floor through the existing 2 cm spread and 5 cm mesh-agreement gates.
Those observations remain local evidence for the bounded area, not whole-map proof.

The original failed mount record is retained. Its specific recovery batch was
reconciled by observing that the original session exited, without gameplay input.
The old responsive process was closed normally without gameplay keys. Official
staging verified all eight artifact roles against reviewed source: the independently
changed script is backed up, and the reused native plugin and worker were proven
identical across their recorded source revisions, preserving binary provenance.
Startup returned `process-changed`. Read-only inspection then found exactly one
stable responding windowed process with the expected executable identity and
matching staged hashes; staged files predate its start. No fresh session or runtime
configuration pointer was created, and no focus change or gameplay input occurred.

Automatic approval review twice rejected attaching to, focusing and rebinding this
replacement window because it differs from the saved session and lacks foreground
ownership. Explicit owner permission for that window is pending. Private records
remain outside Git.

Docker daemon, pinned image and Sandcastle doctor checks passed. The subscription
marker matches the model and image; the separate research qualification
fingerprint is stale.
Automatic nearby floors [#65](https://github.com/Jpatching/combine/issues/65) and
continuous coverage [#66](https://github.com/Jpatching/combine/issues/66) still have
open blockers and lack reviewed task profiles; neither was dispatched.

## Next step

The old recovery transaction is reconciled and reviewed source is staged. Obtain
explicit permission to attach to the current replacement window, then establish a
fresh session and verify windowed foreground readiness before one bounded ride
proof. Reuse established floor evidence; report movement and control restoration
separately from acceptance. The wider #20 goal and PR #62 remain unaccepted and
unmerged.

Use #64 and its approved slices for automatic nearby floor selection and moving
coverage without a spot whitelist or arbitrary world-height ceiling, solved board,
GTA-model animation and Skate tricks. Board/presentation need not wait for city-wide
coverage. Exact-version collision supply and bone updates remain explicit gaps.

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
[Coverage and presentation source research](../research/results/2026-10-13-gtaiv-coverage-and-presentation.md).
Historical methods do not authorize new work.
