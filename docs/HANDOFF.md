# Current context

## Current task

Reviewed: 2026-10-09

Task: finish publication of research [#31](https://github.com/Jpatching/combine/issues/31)
and [#32](https://github.com/Jpatching/combine/issues/32), then implement
[#34](https://github.com/Jpatching/combine/issues/34) in a fresh session.

Source branch: `research/gtaiv-physical-collision`

Source revision: `c0ba526b531b5bd272abd41978c2f9efb516c414`

This is the accepted
Sandcastle report before host provenance correction and this handoff. Fetch #32
for the final publication revision and PR link.

Disposition: research publication awaiting owner approval. No PR exists for #34. #31/#32 each have a
separate report branch; their issues own the draft PR links. No implementation
of #34 has started. The previously approved runner PR #33 merged as
`1db98bdf0cd567548da3394d058c779c8be10dcc`; #30 is closed.

## Evidence

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

Review and approve the two research PRs, squash merge them and synchronize main.
Close #31/#32 only with their final merged revisions recorded. Then start a fresh
session against the self-contained #34, from synchronized main on a new focused
branch. Its first experiment inspects one owned collision resource with bounded
structural validation. The concrete public reader makes this a smaller initial
unknown than qualifying an undocumented native interface. Unsupported layouts
must refuse explicitly. A structural pass does not establish world placement,
active host collision, Skate contact or gameplay.

Keep the native-query route as a comparison and possible future physical oracle.
Do not start a city extractor or broaden #34 into the full integration. Preserve
`integration/gtaiv-skate-loop`, draft PR #23, the separate worker candidate and
recovery branches. #21/#22 remain blocked. PR #29 contains earlier approach research
and remains unmerged. Do not resume retired Fortnite work or relax flatness guards.

## Session close

Use [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Fetch #34 and its blockers in the
fresh session rather than carrying the full research transcript. Keep assets,
geometry, settings, authentication and raw logs outside Git and AI uploads.
Draft publication is not merge approval, runtime acceptance or release authority.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md),
[workbench guide](WORKBENCH.md), [Sandcastle guide](../tools/sandcastle/README.md)
and [glossary](../GLOSSARY.md) retain supporting facts and boundaries.
