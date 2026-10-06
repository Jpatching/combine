# Handoff — interactive Fortnite + Skate qualification blocked on launch/client seams

The current goal retains Fortnite building/editing/destruction with Skate's
movement, tricks and grinds, across the complete selected island. Static exports
cannot satisfy it. Combine, Blender and a particular version are optional.
D-026 and the [current specification/evidence](../research/results/2026-10-06-fortnite-adapter-qualification.md)
supersede conflicting static assumptions; separate Synergy remains preserved.

**Phase 1 bounded outcome:** pinned Reboot source has server building/edit hooks;
its original damage path is retained (destruction behavior inferred, not tested).
The inspected launcher starts/suspends an EasyAntiCheat process, so its normal
route fails the no-protection-bypass boundary. No permitted launch route or live client collision/movement/render bridge is
qualified. A local client input has now been verified as described below.
No new game assets acquired or binaries built. Reviewed private preparation and
stock-launcher trial executed; Fortnite itself and physical gameplay not reached. No owner acceptance, publication, merge or release.

```text
Compatible accessible Fortnite client + permitted launch + client seams
  -> on-foot build/edit -> Skate controls/tick/pose + current collision
  -> ride/jump/grind -> edit/destroy collision -> recover/exit/relaunch
Current prerequisite failure -> precise blocker; no static substitute
```

**Client found:** choose existing Fortnite 3.1 / CL-3917250 as first compatibility-
test input. Private archive is 9,902,525,829 bytes, includes one 83,333,008-byte
Windows shipping client. Fresh SHA-1 matches the recorded reference
`b017f433b1238c0eed9f43fdb80df3ea1d90361e`. No new download needed. Archive has
3,403 entries, including 68 PAKs and five EXEs. All 3,323 files extracted with
ZIP CRC checks, copied into a fresh native Windows trial and shipping hash
rechecked. Provenance remains inherited. Original Epic executable signatures Valid. Catalogues can call
this build 3.1.1; use exact CL rather than filenames. Reboot source documentation
covers S3–15; launcher claims S0–14. Neither proves this patch's gameplay.

**Startup tested:** on Windows 11 Pro 10.0.26200 / RTX 5060 Ti, original signed
BattlEye launcher opened but remained at `Installing BattlEye Service`; no game
process observed. Closed cleanly after 105 seconds; no trial processes remained.
Service Stopped; Windows consent process present, attribution unverified. Owner
confirmed headless access. Windows token is non-admin; UAC secure-desktop approval
is enabled. Linux sudo cannot elevate it. No consent auto-clicked,
no bypass/injection. At 20 seconds, zero original config changes/new config files.
Private scripts/results in `.private/fortnite-client-test`; native-root.txt locates
trial. Do not repeat extraction over existing destinations.

**Direct test:** unmodified signed shipping EXE also tested with no protection
overrides. It exited before 20 seconds; no trial process remained, exit code
not captured, cause unknown. No configuration changes reported. This does not
prove BattlEye mandatory. Archived/offline route remains the candidate; Instigator
source at c033c1c2693194a5948a760cc365d6821c5caae5 also starts/suspends EAC
threads; its normal route fails the same boundary. README tested versions exclude
3.1. No loader/dependency installed.

Owner asks to reproduce the existing repo/mashup method and find a test client.
The existing runtime loader handles IW4/T5/IW5 and launches IW4L; no Fortnite
client bridge was found in those paths. Source searches and University map/video
listing have not identified the exact live Skate+Fortnite demo the owner recalls.
The selected client is our test input, not a version attributed to that demo.

**Source:** branch `slice/fortnite-interactive-qualification`; base/inherited
checkpoint `70f35198619b514bb28b34b0b6518255aac7e168` preserves four incoming docs.
This slice changes requirements/evidence/source pins only; runtime/exporter
code remains unchanged. Resolve Git HEAD for final local revision. Origin
refreshed: `origin/main` remains `a5593d671142f31653d45caeaad7b926d40ff855`.
Stacked history still needs review before any publication/merge. This plan
excludes publication. Public Reboot master read-back differs from inspected pin;
pin not moved. See upstream.lock.json for exact inspection revisions.

**Checks:** repository gate passed (34 tests, two recipes, links in 17 documents).
Independent Standards/Spec review found two evidence-description gaps; corrected
with fetch commands/hashes and resolved-versus-fixed pin wording. Latest local
client evidence includes isolated preparation and a stock-launcher startup test;
Standards/Spec review completed; stale execution summaries corrected. Inherited debts remain: fresh exporter rebuild/NuGet analyzer cache;
broad native suite missing `src/tests/map_startup.rs`; PR #1 rail regression
unfixed before merge; Windows/full-island performance and physical trials absent.
No native rebuild needed for the documentation-only change.

**Tracker:** nine existing records C-019/C-020/C-024/C-025–C-030 updated and
read back, with views/fields/unrelated items preserved. Current interactive
requirements replace static assumptions; historical contracts and named edges
remain visible. `ready-for-agent` marks only C-024 bounded qualification.
Latest test evidence synchronized to C-019/C-020/C-024 and read back; final
adapter-method/Instigator findings synchronization recorded at handoff.
C-024 route stays open despite a valid bounded blocker outcome. Other route-
dependent implementation is conditional; rail repair remains separate debt.

**Method:** host adapter + existing Skate Session + thin bridge. First read one
host value; then controls/camera and collision/lifecycle. No IPC/public protocol
is selected; raycasts alone are not proven sufficient for Skate geometry/rails.

**Next:** qualify an actual Fortnite client extension route for live collision,
structure lifecycle, movement and rendering against the existing Skate Session.
The owner asks for the existing MW2/Skate/Minecraft method; BattlEye is not that
integration method. Normal Windows elevation is needed only if we repeat the
stock-startup diagnostic; that repeat is not the next mashup milestone. Existing
IW4L cannot consume a Fortnite client directly. No more static adapter work
resumes. Owner acceptance remains separate.

---

## Preserved historical static-route handoffs (superseded by D-026)

# Handoff — public island leads found; asset access and real-data qualification open

**Objective:** full Fortnite island with the pinned Skate runtime, solid ground,
walls/stairs, grinds and recovery/exit/relaunch. Phase 1 qualification continues
on the existing map and export decision. No new map, runtime or schema selected.
[Exact pins, source traces, input leads and blocked experiments](../research/results/2026-10-06-fortnite-adapter-qualification.md#paired-route-follow-up--2026-10-06).

**New evidence:** pinned SK8 addon 1.15.0 requires Blender 5.0+. Its v15 binary
layout matches the pinned reader at source level, but Combine rejects BGRP break
groups, hinged doors and nonstatic MOBJ physics. Exporter coordinate conversion
has no unit multiplier. CUE4Parse USD declares centimetres/Z-up; actual Blender
import dimensions remain to measure. World export paths can omit missing
actors/levels; source collision preservation remains unverified.

Owner confirms no alternative local input; requests online input. Public Chapter
1 island, Tilted Towers and Chapter 6 listings have readable metadata and are
marked downloadable. All three anonymous official download endpoints returned
401; no model was acquired or inspected. Coverage/scale/materials/collision are
unknown. Existing 3.1 diagnosis remains inherited: 0/10 containers mounted, zero
worlds. No new game-data execution is claimed. Linux PATH has no Blender;
Windows tool readiness unknown. No private assets/logs sent to AI services.

**Clarification (D-025):** no particular Fortnite build or Blender is required
for the gameplay goal. The same source build is needed only to compare the two
exporters fairly. An existing world model could advance downstream loading even
without original build identity, after measured content/collision checks. Blender
is the current candidate conversion step. No replacement or route accepted.

```text
Accessible raw world -> two exporters on same sample -> compare results
Accessible existing mesh -> inspect content/scale/collision -> compatible map
  | access/content missing: retain explicit blocker
  v
Pinned reader/host + standalone rendering -> real skating trial -> full island
```

**Source:** current branch `slice/fortnite-reuse-qualification`; this follow-up
base `f830595d3e70de2ae273b74b4bf815018ea94afb`; final local checkpoint is Git HEAD.
Origin refreshed; `origin/main` remains `a5593d671142f31653d45caeaad7b926d40ff855`.
Inherited source checkpoints `86a2c6e`, `7b43d11`, `62cff9a` preserved. Stacked
ancestry still requires review before publication/merge. No push/merge/release.
Only qualification/decision/handoff docs changed; no runtime or exporter code.

**Checks:** `python3 scripts/verify.py` PASS: 34 tests, two recipes, links in
17 documents. `git diff --check` PASS. Independent Standards and Spec review
of the export follow-up: no actionable findings; final host-discussion addition
review pending. Source hashes verified; no real map compatibility/play evidence.
Inherited debts unchanged: missing fresh exporter rebuild/NuGet analyzer cache;
native broad suite lacks `src/tests/map_startup.rs`; reproduced PR #1 rail
regression still blocks merge. Prior native tests do not waive these failures.
No Windows build, launch, gameplay, owner acceptance or full-island measurement.

**Tracker:** intended update is this source research plus separate evidence gates
and anonymous-download blocker on existing export decision/map; export acceptance
remains unchecked and parked implementation/dependencies remain preserved.
Read-back pending until final synchronization below.

**Latest owner steering:** questions whether Combine should be the host and
whether existing export/custom-map methods are being overcomplicated. Upstream
SK8 documents an existing complete custom-map session; recommend assessing it
before building a Combine standalone bridge. This is documented/inferred, not
locally reproduced. No host switch selected. Exact preview.18 ref/dependencies,
its separate Skate input and current updater/security behavior need qualification
if chosen. Existing exporter source pin remains preview.15.

**Next concrete step:** Codex compares the existing standalone Rust Engine and
SK8 Custom Engine Layer for the Fortnite + Skate-only trial before committing
to new Combine session work. The owner asks for experience-specific runtime
research; explicit final host choice remains open. ReSkate's author-documented
GTA III port is a concrete existing cross-game example, not our tested route.
Qualify normal asset-download access and inspect a real terrain/building scene
before conversion/gameplay.
No particular Fortnite build is required for that mesh inspection. Paired
exporters need the same raw input only if that comparison is pursued. Preserve
earlier trials/installations and separate Synergy/hit-radius work.

# Preserved runtime handoff — Fortnite input diagnosed; export route blocked

**Outcome:** reproduced 3.1 mount failure twice: 0/10 containers, zero worlds.
Fresh container hashes match recorded references. Independent v4 footer checks
confirm ten encrypted-index flags and valid ranges; pinned parser skips mounting
these before decoding. No supported compatibility correction or qualified
replacement was established. Payload encryption itself remains untested.
[Diagnosis and reproduction](../research/results/2026-10-06-fortnite-input-diagnosis.md).

**Next actor/action: Codex**, initialize the pinned Skate host against the existing
prepared private assets in isolation (C-025); require a loaded/rejected result
before renderer work. The prior presence check located `skate-data/assets`, manifest
version 1, safe scene/action/motion references, stock input, skeletons, collections
and OnBoard/OffBoard banks. Presence is not host-loading proof. C-024 remains
blocked/open: replacement must be identified and yield a real island/export/collision
witness before substitution. Full island + Skate-only destination remains.

**Source:** local branch `slice/fortnite-input-diagnosis`, base
`397f535a952014b3b706fb4b1d52450331298da2`; resolve final checkpoint with Git.
Only new read-only header diagnostic/tests and this evidence/handoff are included.
Inherited exporter source/lock remain untracked, unchanged and preserved.
No Git integration review, push, merge or release. Original installations,
archive, private reports and earlier trials remain; no game bytes/keys/raw logs
uploaded and no protection bypass attempted.

**Checks:** seven focused header tests and ten inherited runner CLI checks pass.
Full repository gate PASS: 34 tests, two recipes, local links in 17 documents.
Fresh exporter compilation is blocked
by missing inherited NuGet cache/analyzer files after correcting the read-only
.NET first-use cache; reproduction uses the recorded inherited DLL, not a newly
built runner. No world export, runtime build, game launch or gameplay acceptance.
Inherited broad Skate host suite still lacks `src/tests/map_startup.rs`.
Upstream remote reads confirm parser master remains e4ea4ba and runtime HEAD/tag
v0.4.0 remain f608f85; pins unchanged.

**Board:** C-024 body/fields updated and read back; Phase 1 stays blocked/open.
Reproduced skip policy, fresh hashes, independent headers, missing rebuild cache
and no replacement recorded; next action is isolated C-025 host loading. Shared
helper initially rejected owner-visible columns before writes; retry validated
the existing live layout and preserved all views/unrelated items. No new tracker. [Live input task](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192669).

**Usable today:** existing Windows mashup has owner-reported skating/Minecraft;
recovery/replay remain unverified. Actual Synergy exact c591086 trial is prepared
and unaccepted. Hit radius/menu coverage remain unfinished. No playable Fortnite
adapter exists. Those separate trials and requirements are preserved.

---

## Preserved preparation handoff (historical state; current summary above supersedes it)

# Handoff — full-island spec published; first Rust preparation slice implemented

The full selected Fortnite island + Skate-only specification and eight dependent
tickets are published on the private board. A new source patch validates native
world geometry and prepares the existing Skate host without MW match startup.
No Fortnite decoder, rendered standalone session, real-data preparation or play
is claimed. Actual Synergy trial and hit radius remain separate and unchanged.

[Specification](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=262165772) ·
[Preparation slice](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192627) ·
[Source qualification](../research/results/2026-10-06-fortnite-adapter-qualification.md) ·
[Implementation/reproduction](../research/results/2026-10-06-standalone-world.md).

```text
Validated native world -> existing Skate host preparation (source slice)
  -> standalone render/input/lifecycle -> real export adapter -> full-island travel
Authentic selected-build input -> exporter witness/census --^
Invalid geometry -> explicit error before assets/physics
```

## Current evidence and Git boundary

Branch `slice/separate-mashup-qualification`, starting/base commit
`a5593d671142f31653d45caeaad7b926d40ff855`. Local checkpoints: `b5a2d7a` preserves inherited scaffolding; `82ea441` records
the specification/docs; `adf769c33756380456a2a7267798f5f16908a3d5` records the
verified runtime source. Final handoff/patch-context correction is a separate
documentation checkpoint; resolve branch HEAD for its exact revision.
No push, merge or release.
Owner explicitly invoked implement after requesting clearer branch-to-main
handling; local reviewable commits resume. Inherited scaffolding was checkpointed separately as unfinished directory
preparation; its original two file hashes are unchanged.

Remote refreshed October 6: only chore/workflow-routing and
slice/synergy-input-isolation exist. No remote main; local main is nine historical
commits behind the starting revision. Review the complete baseline before
publishing a main target/PR; do not silently merge stacked unrelated work.

Runtime pin unchanged: `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; remote HEAD/tag
still match. New source-only patch `patches/skate-standalone-v0.4.0.patch` applies
directly to a clean pin, independently of the Synergy patch chain. Its SHA-256 is
`0c9ee1c9d295c3508d95fe067ceb4b6bae13fba2ebeb208372d507e36df11c3c`.
Original dirty runtime and existing trials remain untouched. Public CUE4Parse
source downloaded/inspected at `e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc`, not run.
No verified local Fortnite build or export; no game archive downloaded.

## Checks

- Native Linux Rust 1.95.0 public host-boundary tests: 13 passed, 0 failed.
- Standalone example validates synthetic world without loading assets or starting
  host/gameplay; missing assets and invalid CLI arguments exit 1.
- Patch replay: all 5 files byte-identical in a clean pinned checkout. The
  packaging diff uses one context line to avoid a whitespace diagnostic on a
  blank context line inside the patch; runtime source bytes are unchanged.
- Broader Skate-host `--all-targets` test build FAILED on upstream missing
  `src/tests/map_startup.rs`; full host suite remains unverified. Three inherited
  compiler warnings preserved. No Windows build or physical gameplay this slice.
- Repository gate: PASS, 27 tests (including 4 inherited scaffolding tests),
  2 recipes and links in 17 documents. `git diff --check`: PASS.
- Independent Standards and Spec review: both arithmetic findings fixed and
  re-reviewed; no remaining actionable findings in this source slice.

## Board and next actor

C-019 specification and C-023 through C-030 tickets read back successfully;
duplicate historical paragraphs consolidated earlier, full-island destination
corrected, fields/views/unrelated drafts preserved. Readiness and named blockers
are body text because private drafts lack labels/native dependency links.
Final read-back PASS: C-023 Done for its bounded source contract; C-025 Todo/Now
as the next implementation; C-019 remains In Progress for the full integration.
All views/fields preserved. Phase 5 source slice complete | current slice branch
with local checkpoints above | unpushed | focused/gate pass, inherited host-suite
failure | board synced | Codex next: C-025 asset check and standalone rendering.

Next Codex: [render/control an isolated Skate session (C-025)](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263192734),
after confirming the local Skate asset setup. It must use standalone input/pose/
camera ownership and exclude MW startup/UI/combat; test failure/exit without
claiming Fortnite play. C-024 independently requires legitimate selected-build
input and an inspected export before freezing serialization. Full-island
residency/streaming stays undecided until census and performance measurements.

---

## Preserved earlier handoff history (superseded current status/order)

 Handoff — reconciled guidance; Fortnite + Skate-only wayfinding started

The owner first selected hit radius before other menu batches (D-019), then
requested Fortnite + Skate-only qualification and a substantial open-source
roadmap/player hub (D-020). Fortnite has no MW2 combat or Synergy. Actual pinned
Synergy remains a separate experience; hit radius is still first within its menu
implementation work. The exact Synergy physical trial stays prepared/unaccepted.
No gameplay code, adapter, game assets, commits, pushes, promotion or release were
produced in this session.

```text
Live board + requirements + latest correction + evidence -> one missing check
  | Fortnite + Skate-only -> access/export + Rust importer qualification
  | separate actual Synergy -> hit-radius integration; owner input trial pending
  v
Source checks -> exact build ready to try -> physical test -> explicit acceptance
```

## Source and preserved work

Branch `slice/separate-mashup-qualification`; HEAD/base
`a5593d671142f31653d45caeaad7b926d40ff855`.
Correction remains uncommitted/unpushed. Tracked changes: README, AGENTS, workflow,
menu guide, helper/tracker guidance, decisions, source metadata and this handoff.
New docs: ROADMAP, REPRODUCING, GROWTH; new redacted evidence: hit-radius source
trace and Fortnite wayfinding. Exact final dirty state is available via
`git status --short`; no remote-publication result is claimed.

Inherited untracked `scripts/prepare_experience.py` and `tests/test_experiences.py`
are preserved, excluded from the correction and not playable progress. SHA-256:
script `b0ae2b3c2a43e0c8be720846dc44ee4a22e7976e56d800ecb95d1d673e32dbda`;
test `cf50480ac0749048f66b91d132d5552dffca837d55fd33abaa7bdaee76d4bcd5`.
Full gate discovers inherited tests; report their coverage separately.

## Changed guidance and checks

README describes separate experiences and actual Synergy controls; native-menu
procedures remain explicitly historical in the menu guide. Source metadata keeps
historical menu_port unchanged and separately records actual menu_execution.
D-019/D-020 preserve previous decisions and explain superseding order/composition.
Roadmap describes destinations; board owns detailed status. Reproduction guide
separates public checks, pinned Rust build and private-data trial prerequisites.
Growth recommendations cite GitHub guidance; no keywords/settings were applied
remotely. Rust owns runtime gameplay; GSC owns Synergy menu; Python/PowerShell
validate data and prepare trials. Existing adapted engineering setup verified:
AGENTS tracker/domain pointers exist; triage is absent, so no label setup needed.

Approved global edits changed only existing ROUTING.md and matt-workflow/SKILL.md.
Shared `python3 -B ~/.codex/workflows/solo-development/test_workflow.py`: 15 pass.
Skill validator: valid. Reminder hook/config hashes unchanged:
`5ef1f4c0069771ef7346d76529511dc4c066b48fe15f2730fb57c4db3219ffc8` /
`3e154e61c17258b933abeb8a43bb4cf2f8c4967b7372b3fd3a844b51defe738c`.
No new hook/dashboard/automatic pickup/skill upgrade. Static reminder does not
synchronize status or check documentation.

Upstream `git ls-remote` refreshed October 5: runtime HEAD/v0.4.0 match
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`; Synergy HEAD/main match
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`. Pins unchanged.
Repository gate `python3 scripts/verify.py`: PASS, 27 tests (23 existing + 4
inherited scaffolding tests), 2 recipes, links in 17 documents. No inherited
failures; historical runtime/statistics and physical-play gaps remain unchanged.
`git diff --check`: PASS. Owner answer round resolved: first hub is a GitHub catalogue; community-tested
means exact build plus participant results (minimum count undecided); additional
game candidates wait until Fortnite + Skate first playable milestone. C-021 is
resolved and read back; C-022 pilot threshold remains open.

Cold document/board resume check by a read-only helper passed the required
distinctions: actual GSC, hit-radius-first within menu work, pending c591086
physical verdict, preserved unfinished scaffolding, Fortnite + Skate-only
Phase 1 and compatibility prerequisites. It found an old menu-then-Fortnite
phrase in AGENTS; corrected to a pointer to current board/latest decisions.
Historical ordering is explicitly labelled in the preserved appendix/card.
This checks a fresh helper read, not a new Codex client or hook operation. No Rust rebuild or gameplay required/claimed for documentation changes.

## Board and next step

Reconciliation of existing menu milestone/input trial and static overview read
back successfully; unrelated drafts, fields and all views preserved. Helper
initially rejected existing live columns/filter before writes; temporary update
validation retained the live layout rather than resetting it.
Wayfinding chart read-back PASS: existing Fortnite qualification is reused,
new map and two decisions created; unrelated drafts, fields and all views preserved.
[Map](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263154297),
[Fortnite qualification](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=262165772),
[hub readiness](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263160968),
[traction pilot](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=263161021).
The map and qualification are Phase 1/Now; separate menu milestone is Next;
C-016 remains Phase 6/Now with owner Trial input. API parsing errors during charting
left a partial map draft; it was repaired in place without duplicate maps.
Final C-019/C-020 evidence/blocker/next-check update read-back PASS; all unrelated
state preserved. Pending source/access evidence remains a blocker, not a playable claim.

The pinned runtime gives concrete adapter precedent: its Minecraft loader/render
loop streams custom collision into sim::voxel while the Skate and Minecraft
systems coexist. See the updated [Fortnite qualification evidence](../research/results/2026-10-05-fortnite-wayfinding.md). It demonstrates an extension pattern, not Fortnite format compatibility.
Skate consumes `ClipCollision`, extracts solid triangles from meshes/brushes/static models and detects rails from walkable edges; Minecraft has a separate voxel-face bridge. Fortnite should qualify a static `ClipCollision` path first. Critical unknown: standard proxy-map session setup may retain MW2 weapons/combat/Synergy. Next compatibility check must find an explicit no-MW2 match configuration before implementation. Source-only tracing can proceed while access/export is unresolved. A lawful,
identified selected-build export witness is required before genuine conversion
or gameplay. See [Fortnite evidence](../research/results/2026-10-05-fortnite-wayfinding.md).
For the separate menu slice, next qualification is forward penetration intervals,
body pose producers and target-side cover witness, per the
[hit-radius source trace](../research/results/2026-10-05-hit-radius-qualification.md).

## Preserved exact Synergy trial evidence

The following earlier handoff retains its build/evidence and historical next-action
ordering. Its basic-loadout-first instructions are superseded by D-019/D-020 and
the live board. Never infer a new physical verdict or rebuild from this history.

# Handoff — actual Synergy trial ready for owner test

The actual pinned Synergy GSC menu runs with its own presentation/options.
Intervention equip and input isolation passed bounded runtime and synthetic
checks. A versioned local trial is prepared; owner gameplay testing and exact-build
acceptance remain separate. Other option effects and trickshot hit radius are
unverified. The owner reports Intervention worked in the preceding most recent
trial, with other options missing; its exact build was not identified.

Phase 6 owner trial for the input checkpoint; one coverage batch follows, basic
loadout controls. The supplied six-batch order and release definitions are in
[WORKFLOW.md](WORKFLOW.md), D-018 and the live private board. Hide HUD stays deferred.
Fortnite qualification remains after the menu dependencies.

```text
Physical input -> actual Synergy GSC -> original menu action
       | captured / closing / held controls -> block gameplay
       | neutral release -> fresh input -> ordinary gameplay
       v
Exact trial -> owner test/report -> further option batches -> explicit acceptance
```

## Exact trial and source

Desktop folder: **Combine Synergy - 2026-10-05 - c591086**. Shortcuts:
**Test Synergy**, **Open trial files**, **Read checklist**. Source checkpoint
`c5910860c57b69c7e7c8dc2edae88f3cf99a31f7`, branch
`slice/synergy-input-isolation`, base
`b52c28f6fe1a21c81f610a7d96a7e48d7f953650`.
The subsequent documentation commit records delivery without changing build source.
Resolve branch HEAD with Git; never infer a merge or release.

Executable SHA-256:
`e06c7f1fc217523485363fe156fe448ea94b2cba8b14c52cb66a3d4fff5e9268`.
Review manifest read-back matches source checkpoint, executable, prepared/unaccepted
state and three shortcuts. `launch.ps1 -VerifyOnly` passes without launching.
Source runtime executable and settings are preserved; older trials remain.
The manifest includes all five patch hashes and unchanged runtime/menu pins.
Input delta is committed as `patches/synergy-input-v0.4.0.patch`; the ignored runtime
checkout is still intentionally dirty. Private logs/assets/settings remain excluded.

## Checks and limits

[October 5 evidence](../research/results/2026-10-05-synergy-input.md) records commands,
failed runs and inherited debt. Current successful checks:

- Windows build: pinned Rust 1.95.0 / cargo-xwin / play profile, launcher `iw4l`;
  hash unchanged after rebuild. Existing compiler attribute/private-interface
  warnings remain, no new warning repair included.
- Windows sim `synergy`: 4 passed; console `practice`: 20 passed.
- Repository gate `python3 scripts/verify.py`: 23 tests, 2 recipes, links in 14 docs.
- PowerShell log redaction/order fixtures and Synergy review adapter fixtures pass;
  shared review bundle suite: 14 checks pass.
- Input patch replays byte-for-byte across 16 runtime files.
- Corrected diagnostic 13 versus same-build disabled diagnostic 12 passes the
  strict checker: actual hierarchy/Intervention held/close/fresh shot, no observed
  open-menu shot, normal exit 0. Statistics/schema fault reproduced disabled.
- Corrected four PNGs are 1920x1080; preserved 720 captures are 1280x720.
  Root/Intervention visual inspection finds the original readable Synergy menu.

The 1080 PNG named closed still shows the menu; it does not prove closed
presentation. The stream records extra reopen/close transitions after the successful
close/fresh shot. Physical reliable close/reopen is an explicit owner checklist
item. Automated timed inputs and synthetic focus/reconnect checks do not establish
physical gameplay. Diagnostics 10 and 11 failed and are preserved privately;
old report 09 no longer passes the stricter provenance contract.

Independent bounded Standards/Spec review identified four diagnostic-evidence
issues; all corrected and re-reviewed without remaining actionable source findings.
Diagnostic faults from imported modules are retained with private arguments removed;
statistics exemption requires successful disabled same-build provenance.

Source publication read-back verified delivery revision
`c538565f49fe06b159a946888c74d560cb6256d7`; the existing card was moved to
Phase 6 and read back, preserving live views and unrelated items. Subsequent
handoff-only commits do not change trial source or executable; resolve current
branch HEAD and remote before continuing. No owner acceptance, local release, merge or public release.
Baseline recovery/freeze, audio listening and original-file comparisons remain
inherited gaps; no Fortnite adapter/assets are added.

## Next actor and check

Owner can test the game using Test Synergy: open with Aim+Melee, equip Intervention,
check keyboard/controller capture, close while holding Fire, release then fire,
focus/reconnect and quit/relaunch. Report this exact folder/build, any failing
control and which option effects worked. Other sections are available for inspection
but not verified as working. Codex then continues the basic loadout batch, checking
effects/reversal/failure/interaction, retaining unsupported entries as requirements.
