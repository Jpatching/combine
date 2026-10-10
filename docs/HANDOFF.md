# Current context

## Current task

Reviewed: 2026-10-10

Task: implement the owner-approved faster test loop and qualified ground route under [#52](https://github.com/Jpatching/combine/issues/52), retaining [#20](https://github.com/Jpatching/combine/issues/20) for complete GTA riding acceptance.

Source branch: `implement/gtaiv-qualified-ground`

Source revision: `b27929a16e420a8cfa1d319825966a90309ca566`

This is the fixed review base for [ground source #53](https://github.com/Jpatching/combine/issues/53),
stacked with explicit owner approval on retained [PR #23](https://github.com/Jpatching/combine/pull/23).
No PR exists for the ground slice yet; its publication record will own the final
revision. The exception permits source implementation without merging the parent
or treating authored geometry as GTA qualification.

Disposition: both adapters now accept bounded triangle collision through explicit
surface preparation/mount/tick commands. Observations carry query coordinates,
layer and availability; mesh support is evaluated independently at returned poses.
The clean rebuilt Windows Session ramp and suspended-worker cancellation trials
pass. Ordinary F6 still uses the preserved
flat route: a qualified street supplier and native success/loaded evidence are
pending. No installed game files or runtime candidates changed.

The test-command prerequisite is published on #23 at the revision above. The
parent PR currently reports merge conflicts against `main` and no checks for its
latest revision; earlier successful CI is not evidence for this revision.
Resolve that integration separately before merging the stack. The
remaining approved slices are [local qualification/trial #54](https://github.com/Jpatching/combine/issues/54),
[board #55](https://github.com/Jpatching/combine/issues/55), and
[rider-interface proof #56](https://github.com/Jpatching/combine/issues/56), with
native blocking edges. #54 waits for #53 and retained qualification #39; board
waits for that ground milestone, then rider follows board.

## Evidence

`python3 tools/gtaiv-skate/check.py` passes all seven authored suites, including
six connection, four wire and two freshness tests (approximately 1–3 seconds).
The unchanged flat API rejects an authored slope; the triangle route accepts it.
Initial new-interface tests failed compilation before implementation; an executed
wire test then failed because invalid geometry observations were accepted, and
passes after decoder validation. These are precise source red/green claims, not
a freshly reproduced GTA failure.

The pinned x86 Windows worker/library and C++ harness compile and link. The first
target build caught an ambiguous integer type missed by portable tests; explicit
u64 sequence typing fixed it. The real standalone `native-ground-clean.exe --surface-only`
trial passed mounting on an authored ramp, 90 pushed ticks across changing heights,
height following, unavailable/wrong-layer refusal and remount recovery. The final
clean rebuilt trial also passed cancellation of maximum-sized preparation against
a suspended owned child, child exit within two seconds and fresh Session recovery;
maximum observed parent call was 1.664 ms. The focused `--surface-cancel-only`
trial passed twice. It does not directly instrument the writer's blocked state.
The same clean executable's default flat-worker trial passed push/steer, warm
remount, collision revision, stale-pose discard, suspended-child refusal and
terminated-child recovery; maximum parent call was 1.462 ms. A final text-only
success-message correction was relinked as `native-ground-final.exe`.
The in-process Rust library also builds; native execution of that backend remains
unverified. Existing upstream private-interface
warnings remain, along with module dead-code warnings in focused builds.

The cancellation regression first failed against an old executable. Symbol and
disassembly inspection showed its pipe write still ran on the supervisor; the
relinked executable contains the dedicated writer thread. Comparing exported
source alone had missed the stale executable. Clean uninstrumented rebuilds
establish the reported passes; keep the focused regression and relink after builds.

Independent Standards review found no blocking violation and one optional named
observation-type suggestion; Spec review found zero blocking findings. Both reviewed
the final cancellation harness; wording suggestions were applied. Source
review does not establish loaded GTA contact or visible rendering. The repository
gate passed 79 tests/68 document checks for the candidate. Pinned native definition
contracts and `git diff --check` also passed. Final publication is still required.

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

Finish candidate validation, review follow-ups and the focused stacked draft PR.
Preserve the versioned matching parent/worker pair: old worker frames are rejected.
A bounded writer thread keeps large geometry uploads off the cancellable supervisor.
The normal F6 script is deliberately not wired to assume a qualified supplier.
Do not enable it by turning a finite native ground height into successful availability.

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
Git and AI uploads. Only the isolated standalone Session worker ran; no GTA staging or launch occurred.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[visible ride record](../research/results/2026-10-10-gtaiv-visible-ride.md),
[checkpoint preparation](../research/results/2026-10-10-gtaiv-ground-checkpoint-preparation.md),
[checkpoint tooling](../research/results/2026-10-10-gtaiv-checkpoint-tooling.md).
Earlier branch snapshots remain in Git history; their retired next steps do not
select current work. Full upstream host tests remain unverified because the pinned
source references missing `src/tests/map_startup.rs`.
