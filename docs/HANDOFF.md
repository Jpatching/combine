# Current context

## Current task

Reviewed: 2026-10-10

Task: implement the owner-approved faster test loop and qualified ground route under [#52](https://github.com/Jpatching/combine/issues/52), retaining [#20](https://github.com/Jpatching/combine/issues/20) for complete GTA riding acceptance.

Source branch: `integration/gtaiv-skate-loop`

Source revision: `fd9f8c4933d3aed193273a2ce5d78fb076886972`

This is the fixed review base for the test-command prerequisite; the issue and
existing draft [PR #23](https://github.com/Jpatching/combine/pull/23) own final
publication revisions. No gameplay acceptance or merge is claimed.

Disposition: one portable authored adapter check command now runs the existing
JavaScript, Rust and C++ checks. CI uses the same command and gains the previously
omitted connection tests. Existing CI already covered the other adapter checks;
this is consolidation and added coverage, not a claim that none ran before.

The owner approved a focused stacked `implement/gtaiv-qualified-ground` branch
from this retained source for [the ground source slice](https://github.com/Jpatching/combine/issues/53).
This explicit exception avoids waiting for #23 gameplay acceptance before building
its ground fix. It does not authorize an automatic merge or real-street activation
before qualification. New ground, board and rider changes stay off this broad PR.

## Evidence

`python3 tools/gtaiv-skate/check.py` passed all seven existing authored suites
in approximately 1.1 seconds, including execution from another working directory.
Missing-tool and deliberately failing temporary compiler checks returned nonzero
with named failures. Temporary executables are isolated and removed. Six existing
Rust dead-code warnings remain. `python3 scripts/verify.py` passed 79 tests and
68 document/context checks before this handoff update. Independent Standards and
Spec review of the focused runner/CI/README diff each reported zero findings.
These are source checks; the Windows Session harness and GTA were not run.

Latest runtime evidence: installed runtime reference remains `b403377481a33e407aeb81b78b8d38984aac4735`.
The [latest diagnostic](https://github.com/Jpatching/combine/issues/20#issuecomment-6099798185)
records flat-guard refusals with GTA control retained and a temporary relative-sample
diagnostic installed after isolated backup/restart. Changing observations while the
owner moved are not a stationary ground survey. No complete riding/restart proof,
visible board or solved GTA rider acceptance exists. Preserve its private rollback.

The existing four checkpoints and comparison command remain available. Owner
location confirmation is complete; precise surface/layer associations and paired
successful GTA readings remain incomplete under [#39](https://github.com/Jpatching/combine/issues/39).
Use three valid readings per point, maximum 2 cm spread and 5 cm mesh error without
moving geometry. A finite height alone is not success/loaded evidence.

## Next step

Finish the focused source-check publication on #23, then switch the attached clean
checkout to the approved stacked ground branch for #53. Establish the failing
non-flat reproduction before implementing the triangle route. Change mounting,
collision and containment together; pair each observation with its query position.
Preserve the flat fallback guard and all retained candidates.

Use the existing real-Session Windows harness for native proofs and bounded live
observer for GTA. The owner launches/focuses GTA; the runner must refuse lost focus,
never steal it, and release only its own inputs. Playback does not prove physical
controller delivery; retain a short manual controller pass. Real-street activation
waits for qualification, and full acceptance requires the uncut 20–40 second ride,
recovery and restart repeat opened locally for the owner.

Board follows ground, then a bounded exact-version rider-pose interface proof.
Reuse research #45/#46/#47 and PRs #49/#50/#51 rather than repeating research.
Sandcastle can run eligible source-only slices after reviewed profiles and main
prerequisites; its existing image has no Rust/MinGW and cannot prove GTA rendering.

## Session close

Follow [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Preserve draft #23, #38 and #42,
private resources/placement, source branches and runtime recovery. Do not close
#20 or #52 on authored test evidence. Owner acceptance and merge remain pending.
Keep assets, identities, exact coordinates, settings, recordings and logs outside
Git and AI uploads. No runtime staging or launch occurred for this prerequisite.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[visible ride record](../research/results/2026-10-10-gtaiv-visible-ride.md),
[checkpoint preparation](../research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md),
[checkpoint tooling](../research/results/2026-10-10-gtaiv-checkpoint-tooling.md).
Earlier branch snapshots remain in Git history; their retired next steps do not
select current work. Full upstream host tests remain unverified because the pinned
source references missing `src/tests/map_startup.rs`.
