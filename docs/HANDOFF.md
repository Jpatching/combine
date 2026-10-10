# Current context

## Current task

Reviewed: 2026-10-10

Task: implement the owner-approved faster test loop and qualified ground route under [#52](https://github.com/Jpatching/combine/issues/52), retaining [#20](https://github.com/Jpatching/combine/issues/20) for complete GTA riding acceptance.

Source branch: `integration/gtaiv-skate-loop`

Source revision: `b27929a16e420a8cfa1d319825966a90309ca566`

This is the retained source tip before integrating synchronized `main`
(`82d35ad1e43620389abb69fa6bcb591cca1d6279`). The handoff conflict resolution
passed independent Standards and Spec review. Existing draft
[PR #23](https://github.com/Jpatching/combine/pull/23) owns the final published
revision and current CI status. No gameplay acceptance or merge to `main` is claimed.

Disposition: one portable authored adapter check command now runs the existing
JavaScript, Rust and C++ checks. CI uses the same command and gains the previously
omitted connection tests. Existing CI already covered the other adapter checks;
this is consolidation and added coverage, not a claim that none ran before.

The owner approved a focused stacked `implement/gtaiv-qualified-ground` branch
from this retained source for [the ground source slice](https://github.com/Jpatching/combine/issues/53).
The ground source is now published separately in
[draft PR #57](https://github.com/Jpatching/combine/pull/57) at
`bfc8eba32dcfd4c26f4af055f9e9ecd0ee303f1c`, awaiting owner source acceptance.
Its authored ramp and standalone Windows Session evidence belong to that PR;
none of its source is incorporated here. This exception does not authorize an
automatic merge or real-street activation before qualification. New ground,
board and rider changes stay off this broad PR.

## Evidence

`python3 tools/gtaiv-skate/check.py` passed all seven existing authored suites
in approximately 1.1 seconds, including execution from another working directory.
Missing-tool and deliberately failing temporary compiler checks returned nonzero
with named failures. Temporary executables are isolated and removed. Six existing
Rust dead-code warnings remain. `python3 scripts/verify.py` passed 79 tests and
68 document/context checks before this handoff update. Independent Standards and
Spec review of the focused runner/CI/README diff each reported zero findings.
The integration merge candidate also passed the repository gate (79 tests and
68 document/context checks), all seven portable adapter suites in 1.29 seconds,
and staged whitespace checks. Independent Standards and Spec reviews of that
candidate each reported zero findings. These are source checks; the Windows
Session harness and GTA were not run for this integration update.

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

Keep #23 and #57 in draft pending their required acceptance; inspect each PR for
its current revision and checks. Keep #57 separate and follow its source acceptance
before integrating it. For #39, establish the exact private surface/layer anchors
and collect three successful, loaded, matching-layer readings per checkpoint
within the stated spread and mesh tolerances. The remaining approved task graph
is [qualification/trial #54](https://github.com/Jpatching/combine/issues/54),
[board #55](https://github.com/Jpatching/combine/issues/55), then
[rider-interface proof #56](https://github.com/Jpatching/combine/issues/56).
#54 waits for #53 and retained qualification #39. Ordinary F6 still uses the
preserved flat route; no qualified street supplier has been activated. Preserve
the mounting guard and all retained candidates.

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
[checkpoint tooling](../research/results/2026-10-10-gtaiv-checkpoint-tooling.md),
[physical collision report](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md).
Earlier branch snapshots remain in Git history; their retired next steps do not
select current work. Full upstream host tests remain unverified because the pinned
source references missing `src/tests/map_startup.rs`.
