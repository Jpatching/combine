# Current context

## Current task

Reviewed: 2026-10-13

Task: finish the working ride and reporting under [workflow #61](https://github.com/Jpatching/combine/issues/61), and organize the owner's [automatic-floor, board, GTA animation and tricks specification #64](https://github.com/Jpatching/combine/issues/64).

Source branch: `integration/gtaiv-evidence-loop`

Source revision: `50bdc0207a3c35ea931c5d1e061e741dff9398f9`

The candidate PR owns its final publication revision. Preparation timeout and
diagnostic/recovery reporting fixes are under review against this source baseline.
The pre-existing uncommitted evidence measurement display is preserved separately.

Disposition: [draft integration PR #62](https://github.com/Jpatching/combine/pull/62)
awaits gameplay qualification and owner acceptance.
Retain [riding #23](https://github.com/Jpatching/combine/pull/23),
[non-flat ground #57](https://github.com/Jpatching/combine/pull/57),
[collector #58](https://github.com/Jpatching/combine/pull/58) and
[context #60](https://github.com/Jpatching/combine/pull/60).
The collector ancestry includes the retained riding/non-flat source. It is
combined here for review, without merging main or activating triangle riding.

## Evidence

Latest runtime evidence: the owner reports mounting works at the teleport spot,
but stops again elsewhere. Retained local log classification also contains mounted
notifications. The configured installed candidate names the source baseline above;
its two prepared surfaces each have a 3 m radius. This establishes neither a
measured complete ride nor automatic floor coverage.

The earlier H2 witness distinguished stacked supporting floors and passed three
queries per floor through the existing 2 cm spread and 5 cm mesh-agreement gates.
Those observations remain local evidence for the bounded area, not whole-map proof.

The latest automated mount record remains unavailable with recovery unverified.
A read-only check found one responding windowed GTA process, but foreground and
fresh adapter readiness were unverified. No new gameplay input or runtime staging
was performed during this reporting/specification work. Reconcile the retained
recovery transaction before reusing its queue. Private records remain outside Git.

## Next step

Finish one push, both steering directions and dismount trial after fresh windowed
foreground readiness and recovery verification. Reuse the bounded floor evidence;
do not repeat four-checkpoint qualification as a prerequisite to this local ride.
The reporting fix needs matching installed-source verification before its runtime
behavior is claimed. The wider #20 goal and PR #62 remain unaccepted and unmerged.

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
