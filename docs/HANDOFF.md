# Current context

## Current task

Reviewed: 2026-10-09

Task: implement [#34](https://github.com/Jpatching/combine/issues/34), a bounded
read-only inspector for one owned GTA IV collision resource.

Source branch: `implement/gtaiv-collision-inspector`

Source revision: `ba7fb89074860723fd592804de3b06ce2e49da47`

This is the inspector implementation revision before this handoff update; #34
owns the final publication revision and review evidence.

Disposition: source implementation complete, pending independent review and draft
publication. No PR exists for #34 yet. Owned-resource verification is blocked. Owner-approved
research PR [#35](https://github.com/Jpatching/combine/pull/35) merged as
`9cecd6448c35ff8455376be0a96d5c60d5853970`; PR
[#36](https://github.com/Jpatching/combine/pull/36) merged as
`00fd570d98b86c3479c9607b75eb299172095221`. #31/#32 are closed, with merged revisions recorded on each issue.

## Evidence

The [standalone inspector](../tools/gtaiv-collision/README.md) validates one
bounded geometry root and emits only a verdict/reason pair. GPLv3 terms,
attribution and pinned format sources are recorded with the tool. Seven focused
command/parser tests passed using authored synthetic data; the worker repository
gate passed all 61 tests. These checks do not establish owned-file compatibility.

Both Sandcastle jobs returned `requires-local-proof`, passed report checks and
independent Standards/Spec reviews with zero findings. Host publication review
also passed both axes after an editorial correction. The apparent guidance-hash
discrepancy was resolved: the runner hashes trimmed text, not raw blob bytes.
All four supplied hashes were reproduced; source pins did not change.

The [physical report](../research/results/gtaiv-120059-physical-collision-feasibility.md)
identifies a concrete public `.wbn` reader, but incomplete shape/transform coverage
and unverified exact-version compatibility. The native report on
`research/gtaiv-native-collision` finds no qualified GTA IV 1.2.0.59 segment/hit/normal
interface. See #31 for its report and publication revision. Neither research job
ran the game, decoded owned assets or proved collision fidelity.

Latest runtime evidence: the retained staged gameplay candidate
`b403377481a33e407aeb81b78b8d38984aac4735` refused a guarded mount at
`over-0.05-metres` before playback, with fresh GTA control retained. Restoring the
minimized window recovered status; a later window change was verified at 1280x720.
No accepted ride or world-collision capability was proved. This is earlier evidence,
not a runtime test of the research reports.

## Next step

Complete independent Standards/Spec review and publish #34's draft PR for owner
approval. The source implementation and synthetic checks are complete.
The owner-authorized read-only search of the discovered GTA IV installation found
no loose `.wbn` or `.wbd` resources; game archives were present. No archive contents
were inspected, no game data was extracted, and no owned resource was decoded.
An already-extracted resource from reviewed tooling is the remaining local-input
requirement. Do not expand this ticket into an archive extractor.

A structural pass does not establish world placement, active host collision,
Skate contact or gameplay. Unsupported layouts must refuse explicitly.

Keep the native-query route as a comparison and possible future physical oracle.
Do not start a city extractor or broaden #34 into the full integration. Preserve
`integration/gtaiv-skate-loop`, draft PR #23, the separate worker candidate and
recovery branches. #21/#22 remain blocked. PR #29 contains earlier approach research
and remains unmerged. Do not resume retired Fortnite work or relax flatness guards.

## Session close

Use [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Fetch #34 and its latest evidence before resuming implementation or local proof. Keep assets,
geometry, settings, authentication and raw logs outside Git and AI uploads.
Draft publication is not merge approval, runtime acceptance or release authority.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md),
[workbench guide](WORKBENCH.md), [Sandcastle guide](../tools/sandcastle/README.md)
and [glossary](../GLOSSARY.md) retain supporting facts and boundaries.
