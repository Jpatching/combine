# Current context

## Current task

Reviewed: 2026-10-11

Task: implement the owner-approved faster ground collection command for [#39](https://github.com/Jpatching/combine/issues/39), preserving the qualified ground work under [#52](https://github.com/Jpatching/combine/issues/52) and complete riding acceptance under [#20](https://github.com/Jpatching/combine/issues/20).

Source branch: `implement/gtaiv-ground-collector`

Source revision: `3fef129c39e61e97c278c156562e6a85719f53d7`

The ground source is published in [draft PR #57](https://github.com/Jpatching/combine/pull/57)
for [#53](https://github.com/Jpatching/combine/issues/53), stacked with explicit owner
approval on retained [PR #23](https://github.com/Jpatching/combine/pull/23).
Its fixed review base is `b27929a16e420a8cfa1d319825966a90309ca566`.
The exception permits source implementation without merging the parent
or treating authored geometry as GTA qualification.

Disposition: [draft PR #58](https://github.com/Jpatching/combine/pull/58) awaits
owner source review and the relevant live evidence. The owner-authorized focused
child starts at `4677e1616b8d41e218f08bdbf13139b73f3ab45d`; the source revision
above identifies the reviewed implementation. The issue owns the final
publication revision. See the
[collector preparation record](../research/results/2026-10-11-gtaiv-ground-collector.md).
The reviewed parent follow-up is synchronized from
`45d409a1b6e8bb72d6f5361355c44c58228892c4`; its
[native refusal proof](../research/results/2026-10-11-gtaiv-native-refusal-proof.md)
passes both standalone backends. Draft PR #57 remains awaiting owner source
review and approval. Collector CI passed at its previous published head
`1f8b1ef876394c273f7fad8883fc7902b7283dce`; that result does not cover this
synchronized candidate. Both adapters
now accept bounded triangle collision through explicit
surface preparation/mount/tick commands. Observations carry query coordinates,
layer and availability; mesh support is evaluated independently at returned poses.
The clean rebuilt Windows Session ramp and suspended-worker cancellation trials
pass. Ordinary F6 still uses the preserved
flat route: a qualified street supplier and independent loaded/layer evidence are
pending. Owner-approved temporary runtime diagnostics were restored; see the
latest runtime evidence below. The qualified triangle route remains inactive.

The test-command prerequisite is published on #23 at the fixed review base above. The
parent integration conflict is resolved at `457a7cfeedd16e016c9683323dfb807d858b5752`,
incorporating synchronized `main` at `82d35ad1e43620389abb69fa6bcb591cca1d6279`.
This branch incorporates that parent update while keeping #57 separate from #23.
Each draft owns its current CI result; earlier successful CI is not evidence for
a later revision. The
remaining approved slices are [local qualification/trial #54](https://github.com/Jpatching/combine/issues/54),
[board #55](https://github.com/Jpatching/combine/issues/55), and
[rider-interface proof #56](https://github.com/Jpatching/combine/issues/56), with
native blocking edges. #54 waits for #53 and retained qualification #39; board
waits for that ground milestone, then rider follows board.

## Evidence

The new collection command retains private observations and runs the unchanged
four-point comparator, with authored command tests passing. Windows observer
syntax and window/input interop compilation pass without input. These are source
checks only. Repository gate: 91 tests and 70 document/context checks. Final
independent Standards and Spec reviews have zero remaining actionable findings.
All 16 retained images were requested locally without AI upload;
exact surface/layer interpretation remains pending. Ordinary character support
has no validated independent loading/layer criterion. No new GTA collection,
runtime replacement, restart or speed-improvement claim is established. The
collector record and live issue separate these remaining gates from source work.

The fresh native harness now proves missing/incomplete geometry refusal without
pose exposure or partial reuse, ground disagreement above 5 cm, query-position
mismatch and stale-time refusal, alongside the existing ramp/availability/layer
proofs. All five riding faults clear poses on stop and recover through remount.
Spec review strengthened partial-consumption proof with an immediate vertex
refusal without restarting preparation; both freshly relinked backends passed
that corrected assertion. The worker passed in 49.445 s with a maximum measured
mount/poll/tick call of 1.027 ms. The optimized in-process candidate passed in
198.778 s with a maximum measured call of 19,751.443 ms; synchronous preparation
does not establish GTA thread suitability. Configuration/upload/stop are outside
these metrics. These complete existing related local test changes; no new
adapter implementation or red/green claim is made. The dated record separates
compiler preparation, source matching and standalone execution from gameplay.

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
The separate `native-surface.exe --in-process` harness now executes the public
ABI against the actual Session. An optimized default-feature library passed
authored ramp movement, unavailable/wrong-layer refusal, discarded dismounted
poses and remount recovery with a 16 MiB standalone stack. The default debug
build first overflowed a 2 MiB stack; increasing only its stack allowed mounting
but exposed a 383 ms tick and 406 ms tick-start gap, beyond the 250 ms limit
on time continuity. Optimizing the library resolved that observed riding refusal. The passing
run took 97.354 seconds; maximum measured mount/poll/tick call was 20,863.339 ms,
dominated by synchronous mounting. The same optimized library also passed with
the original 2 MiB stack in 93.294 seconds; its maximum measured call was
17,569.624 ms. Configuration, upload and stop are outside that metric. This is
standalone authored evidence, not GTA thread suitability. The builder now offers `--release`
for the in-process candidate; the tested library was built with manual Cargo
release commands, not that new CLI option. Existing upstream private-interface
warnings remain, along with module dead-code warnings in focused builds.
The new harness also passed its explicitly selected worker mode with native
exit zero in 23.448 seconds, using a source-matched retained library/worker;
maximum measured mount/poll/tick call was 1.024 ms. It verifies the same ramp,
fault-refusal and remount behaviors, without replacing the earlier worker's
cancellation/failure proofs. Neither timing metric includes configuration,
upload or stop.

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
contracts and `git diff --check` also passed. Draft #57 owns current CI status;
the issue owns source acceptance and the publication record.

Latest runtime evidence: installed runtime reference remains `b403377481a33e407aeb81b78b8d38984aac4735`.
The [automated diagnosis](../research/results/2026-10-10-gtaiv-automated-ground-diagnosis.md)
and [latest issue evidence](https://github.com/Jpatching/combine/issues/20#issuecomment-6101508989)
record a privately captured flat-guard refusal and the earlier six boolean-success
ground calls. A subsequent private plugin-owned-buffer trial paired six actual
boolean-success calls with finite changed heights and intact guards; both fixed
points had 0 mm spread across three readings. Centre character-height agreement
was 0 mm with horizontal position within 1 mm; these are rounded diagnostics,
not four-checkpoint qualification. Per-point loaded collision and intended layer
remain unverified. A memory-read/write probe
caught an exception; missing scoped permission is a likely prerequisite mismatch.
Windows denied the scoped filename rename; rollback verified. Global permissions
and ACLs stayed unchanged. The paired-height trial restored and hash-verified
the exact retained plugin, script, definitions and manifest after normal shutdown.
The subsequent offline-menu runner passed fresh foreground unmounted GTA
gameplay/control after normal restart, and a separate hash check matched all
retained runtime files. No complete riding/restart
proof, visible board or solved GTA rider acceptance exists. Preserve private recovery.

The cursor-free viewer follow-up produced all 16 fresh four-checkpoint view
images with viewer coverage/readiness/fresh-marker checks, no observed C#
compiler errors and full PNG decode at 960 × 720. Pixel interpretation and exact
anchor-base association remain pending. The capture editor was normally closed;
exact previous scripts, metadata and absences were restored, with project-version,
package-manifest, ECSMain scene and bootstrap hashes preserved. No shared pointer or keyboard
input was used. Media and preparation failures remain private; local viewer
requests do not establish owner viewing or acceptance.
A final GTA snapshot still matched all retained runtime hashes; the retained game
was responding but minimized with stale native status. Reestablish fresh
foreground readiness before any further guarded GTA trial.

A private physical-state probe is prepared but unexecuted. It reuses the reviewed
plugin-owned height buffer and existing native definitions to observe three fixed
actual-character-position queries and six before/after character-state records.
Its reviewed staging/collection source binds shutdown and collection to exact
process identities, rejects late collection and samples foreground readiness.
JavaScript and PowerShell syntax checks pass. The two-second scheduling delay
is not a handshake; interrupted staging requires manual recovery from retained
transaction/backups. No physical-contact, loaded-collision or floor/layer flag is
inferred. Do not treat this preparation as a passed runtime trial or checkpoint
association.

The existing four checkpoints and comparison command remain available. Owner
location confirmation is complete; precise surface/layer associations and paired
successful GTA readings remain incomplete under [#39](https://github.com/Jpatching/combine/issues/39).
Use three valid readings per point, maximum 2 cm spread and 5 cm mesh error without
moving geometry. A finite height alone is not success/loaded evidence.

## Next step

Present the retained labelled checkpoint pictures locally with plain explanations
before asking the owner to identify their marker bases. The R1/P1/H1/H2 labels
alone do not let the owner establish exact surface/layer associations. A private
gallery now explains and pairs all 16 retained views; its local browser opening
was requested successfully, without AI pixel upload or interpretation. Owner
viewing and identification remain unverified. Preserve
collector #58 and reuse its published command rather than rebuilding collection.
Independent per-point loading evidence still needs validation and an explicit
owning-issue decision. Never promote character flags or a successful height
query into that evidence. #54/#55/#56 remain behind their native blocking edges.

Keep collector draft #58 pending acceptance. After exact surface/layer
associations and the independent loading method are established, prepare/stage
the reviewed diagnostic through retained recovery, establish fresh foreground
readiness, and collect the frozen three readings per point. Measure this loop
against a real previous-loop baseline before calling it faster.

Keep both PRs in draft pending their required acceptance; source approval does not
establish GTA gameplay acceptance. Paired native success and height observation
now pass; independent loaded/layer evidence remains open. Reuse the private offline-menu
runner and current-run log reader. Inspect the retained fresh cursor-free view
sets for all four anchor bases locally. Resolve exact
surface/layer association, then obtain three genuine successful, loaded,
matching-layer GTA readings per fixed point. Neither a running Unity process nor
fixture output establishes this qualification. Resume the next slice from its live issue and
blocking edges after preserving this evidence; keep each agent's file ownership
explicit and use fresh independent Standards and Spec review contexts.
Preserve the versioned matching parent/worker pair: old worker frames are rejected.
A bounded writer thread keeps large geometry uploads off the cancellable supervisor.
The normal F6 script is deliberately not wired to assume a qualified supplier.
Do not enable it by turning a finite native ground height into successful availability.
The bounded native catalogue review found no already-qualified independent
arbitrary-point loading/floor oracle. Ordinary GTA physical support at each
independently associated checkpoint is the next empirical witness to investigate;
its use as the loading criterion needs an explicit owning-issue decision. Do not
silently equate success, ped waiting state or character-height agreement with
loaded matching-layer collision.

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
Git and AI uploads. Bounded GTA diagnostics and normal restarts ran with owner
approval; their temporary plugin/script/definition changes were restored. The standalone
Session passes remain distinct from GTA gameplay acceptance.
The viewer capture also restored its exact source/metadata changes and left the
isolated lab closed. Do not replace its preserved initial marker implementation
without the same source-identity and recovery checks.

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
