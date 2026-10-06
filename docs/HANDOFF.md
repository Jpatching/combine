# Handoff — Core source qualification; existing mashup backup

**Objective/result:** establish whether Core can connect the existing Fortnite
CL-3917250 client to genuine Skate simulation. The [pinned Core report](../research/results/2026-10-06-core-cl3917250-qualification.md)
ends with a precise blocker. Core client initialization does not start gameplay;
listen mode waits for an already authoritative world. No permitted startup/DLL
loading route is established. Core server session/challenge validation changes
are a separate concern from OS anti-cheat; no OS bypass is inferred. Current
collision export/lifecycle, C++/Rust callable boundary and skater rendering
remain unimplemented. Exact-CL compatibility is unverified; no 7.40 download.

**Source:** `slice/core-client-qualification`, clean starting/base revision
`064f65f1bf609c45bc0b1ced9a787d7494f7b4e4`; final revision is Git HEAD.
Core pin `6dc0e9a0ff91d619b49b0d3772308ff41cb51cd0`; limited Lawin backend
inspection `7f0f26d7a772c6122c42b1783fd75f497e86d3a9`. Existing Rust pin and refreshed remote HEAD remain
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Public source only was fetched;
no dependency installation, compilation, game launch or private asset upload.
Prior client identity/startup results are inherited, not retested.

**Owner follow-up:** package the existing mashup as a private Downloads folder
and ZIP; owner selected latest prepared Synergy c591086. Completed folder and
ZIP are named **Combine MW2 Skate Minecraft - c591086 - 2026-10-06** in Windows
Downloads. Root shortcuts: **Play MW2 and Skate.cmd** and **Play Minecraft and
Skate.cmd**. Both resolve sibling copied data; original path-specific settings
are excluded. Read the packaged README before launching. Originals and the
already running, different trial were preserved; no game was launched here.

Backup verification: 28,701 copied files plus four generated helpers; input
12,620,655,566 bytes; ZIP 12,327,689,936 bytes. All copied-file and ZIP-member
SHA256 checks passed, including source-change checks during copying. Portable
launcher settings and required data paths passed static checks. Original
executable retains expected `e06c7f1fc217523485363fe156fe448ea94b2cba8b14c52cb66a3d4fff5e9268`.
ZIP SHA256: `cfb28e2aaddc8ae426a065a634a3d76044a87206490f6000d607887ee9430e4d`;
a `.zip.sha256` sidecar is alongside it. Elapsed 805.2 seconds. Reproduction
uses the ignored `.private/package-c591086/package.py` with native Windows
Python: inventory by default, `--execute` creates new destinations and
fails on existing output or mismatch. Local paths and detailed file manifest
remain private. Logs, recordings and generated render cache are excluded.
This backup includes game data; it is not authorized for public distribution.
Prepared/verified does not establish fresh play, acceptance or release.

**Verification:** lead source review checked client/listen control flow and
all five recorded source hashes; final report references/local links and
`git diff --check` passed. This is lead self-review, not independent review.
Packaging checks above passed. C-019/C-020/C-024 comparison updates were read
back successfully, preserving unrelated items, fields and views. Repository
gate `python3 scripts/verify.py` PASS: 34 tests, two recipes, links in 17
documents. Final source revision/publication is recorded on the live cards
after commit and remote-SHA verification; resolve this slice with Git HEAD.
Inherited native broad-suite missing-test and exporter rebuild/analyzer debts
remain; no new runtime work waives them.

**Owner correction/next:** four combinations compared in the report: Core
with existing CL-3917250, Core with conditional 7.40, FortExternalServer 3.6,
and official current Fortnite/UEFN. None qualifies yet; FortExternalServer
implementation retrieval was incomplete and its row is documented-only.
The recommendation to diagnose the existing client first is superseded. Existing CL-3917250 remains a candidate, not a commitment. Obtain
build-specific evidence of permitted startup/loading and local world creation
for the strongest route. Then use a bounded prototype to advance genuine Session ticks,
apply pose and replace current collision; coordinate-only logs are insufficient.
Existing build/skate/jump/grind/edit/destroy/recover/relaunch acceptance remains.
No merge, release or owner gameplay acceptance is claimed.

---

## Previous connection assessment (historical status)

# Handoff — assess actual Skate connection before a Fortnite diagnostic

**Owner decision/phase:** option A, recorded in D-029. Phase 1 source research:
qualify a connection to the existing Skate simulation before building a
movement-only diagnostic. Actual Skate physics, interactive island behavior and
same-process preference remain fixed.

**Result:** [connection assessment](../research/results/2026-10-06-fortnite-guidance-qualification.md#actual-skate-connection-assessment--owner-choice-a-2026-10-06)
finds useful official observation, collision-query and animation APIs, but no
established creator-native call path to Rust Session. Verse WebAPI does not
establish local simulation access; MCP runs in the editor. Input, current
triangle/rail collision and live bone/pose rendering gaps remain explicit.
Universal Modder's checked examples contain no Fortnite-specific demonstration;
its PR search was incomplete. Prior community launch blockers remain unchanged.
No diagnostic, adapter, replacement physics or runtime execution was performed.

**Source:** branch `slice/fortnite-skate-connection`, clean starting revision
`3482d4d9f3f00aca493938c535f494adde35c977`; final revision is Git HEAD.
Only the qualification reports, decisions and handoff change. Runtime
remote HEAD remains `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; pin unchanged.

**Checks:** independent Standards review found stale diagnostic-first wording;
corrected by a prominent D-029 notice and explicit historical labels. Spec review
found no actionable issue. Added the documented experimental/publication limit
for Scene Graph skeletal animation. Reviewer confirmed both corrections: no
remaining Standards or Spec findings. Repository gate PASS: 34 tests, two recipes,
links in 17 documents; report local links and `git diff --check` PASS.
C-019/C-020/C-024 updates read back successfully; unrelated cards, fields and
views preserved. They retain phase 1 and record D-029 and the runtime-seam blocker.
Assessment commit `fdf5171f90bb8e6c4530e99bc797734717d49599` was pushed on
`slice/fortnite-skate-connection`; remote SHA matched local HEAD. This handoff
checkpoint records that result. Final checkpoint is Git HEAD and its verified
revision is attached to the board. No PR merge/release or gameplay claimed.

**Compact state:** phase 1 connection blocked | `slice/fortnite-skate-connection`
| assessment `fdf5171` pushed/remote verified | 34 tests + recipes/links PASS |
board read-back verified | next: permitted native/local simulation seam.
Existing native broad-suite missing-test and exporter rebuild/analyzer debts
remain inherited; no new runtime checks waive them.

**Next:** require a build-specific, primary-source example of a permitted native
extension or supported transport to the existing local simulation. Then qualify
input, changing collision and pose/render ownership before adapting Session.
Do not count a camera log or editor connection as the missing bridge. Later
build/skate/jump/grind/edit/destroy/recover/relaunch acceptance remains required.
No owner gameplay acceptance, merge or release is claimed.

---

## Previous qualification handoff (historical status)

# Handoff — Fortnite route qualification remains blocked by host access

**Objective/phase:** interactive Fortnite world with existing Skate simulation;
phase 1 research. The [new qualification report](../research/results/2026-10-06-fortnite-guidance-qualification.md)
contains pinned Universal Modder guidance, Reboot-first source checks, bounded
Rift/Era comparison, Session interface gaps, reproducible hashes and the first
live-value experiment. D-028 records the tooling role. Same-process remains
preferred; no measured reason for IPC and no runtime API added.

**Result:** no inspected launch/extension route qualifies. Reboot suspends EAC;
Era requests protection-disabling options and an unreviewed DLL; Rift's package
catalogue does not establish a native extension or supported client launch.
Universal Modder's Unreal guide explicitly excludes Fortnite's protected route.
No tools installed, game data uploaded, game launched or gameplay accepted here.
Existing 3.1 stock/direct startup failures are inherited, not newly reproduced.

**Source:** `slice/fortnite-guidance-qualification`, starting/base revision
`02d3b8a9c11dc8b67c07720d31cf16f104ccf37c`; this slice's final
revision is Git HEAD. The starting tree was clean. Its inherited rail correction
`b45d878` and merge `02d3b8a` are preserved; the prior handoff's next-step rail-fix
instruction is stale. [Rail evidence](../research/results/2026-10-06-rail-validation-fix.md)
records the prior focused regression checks. No merge performed by this slice.

**Verification:** independent Standards and Spec review found no actionable
issues; all eight report hashes matched inspected source copies.
`python3 scripts/verify.py` PASS: 34 tests, two recipes, local links in 17
documents. `git diff --check` PASS. No runtime changes in this slice.
Runtime remote HEAD refreshed at unchanged
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Inherited broader native missing-test
and exporter rebuild/NuGet analyzer debt remain; documentation checks cannot
waive them or prove Fortnite play.

**Tracker:** C-019/C-020/C-024 updated and read back successfully; live views,
fields and unrelated cards preserved. Shared helper initially refused the custom
Now columns before mutation; direct validated field/body updates preserved that
configuration. Cards record source research complete with precise host-access
blocker, live experiment defined/not run, and existing acceptance sequence.
Qualification report revision `66f850634819cd69d5b6f054abe2d68c4c4d043d`
was pushed; `git ls-remote origin refs/heads/slice/fortnite-guidance-qualification`
matched local HEAD exactly. This subsequent handoff update records that verified
publication. Final handoff revision is Git HEAD; the board carries the final
remote-verified SHA. No PR merge or release performed.

**Compact state:** phase 1 blocked qualification | `slice/fortnite-guidance-qualification`
| report `66f8506` pushed/remote verified | 34 tests + recipes/links PASS |
board read-back verified | Codex: permitted host route before live-value experiment.

**Next:** Codex resumes only when a reviewable permitted client launch/extension
route is identified; first demonstrate a host player/camera value changing with
movement. Process startup or synthetic samples do not pass. Later acceptance
still requires build → skate/jump/grind → edit/collision → destroy/removal →
recover/relaunch. Owner gameplay acceptance, merge and release remain separate.

---

## Previous same-process source handoff (superseded status, retained evidence)

# Handoff — same-process Fortnite adapter selected; source publication and rail fix

The owner selects same-process Skate reuse unless an observed host constraint
requires IPC. The [current specification](../research/results/2026-10-06-fortnite-adapter-qualification.md)
and [pinned process-model evidence](../research/results/2026-10-06-adapter-process-model.md)
record D-027. Existing IW4L embeds MW2, Skate and Minecraft in one process;
Skate uses worker-thread channels. The public Minecraft crossover is a separate
two-process shared-memory design, not an existing Fortnite adapter.

**Fortnite:** existing 3.1 CL3917250 client extracted/copied/verified; stock BE
launcher stalled at installation and was closed; direct unmodified shipping EXE
exited by 20 seconds for unknown reason. No game or bridge verified. Reboot and
Instigator inspected normal launch paths manipulate EAC and remain unqualified.
Next Fortnite experiment: establish a permitted client extension and read one
live player/camera value, then qualify same-process Skate Session integration.
Original installations/private assets and separate Synergy requirements remain.

**Git:** focused branch `slice/fortnite-same-process`, publication-copy base
`76a03831e562ddc7e31304c5d8018b456ddab8c0`; final revision is Git HEAD. Nine
source/evidence commits retained; two obsolete interview-only commits omitted.
Machine-specific documentation paths redacted throughout unpublished history.
Original `slice/fortnite-interactive-qualification` at `be8d3b8` remains a local
recovery copy. No published history rewritten. Local main is synchronized to
`a5593d671142f31653d45caeaad7b926d40ff855`. Push only the reviewed topic branch;
remote-SHA verification and board read-back finish this handoff.

**Checks/debt:** repository gate passed (34 tests, 2 recipes, links in 17
documents); source/spec review completed with publication wording corrected.
No runtime code changed in this specification slice. Existing exporter rebuild/
NuGet analyzer and broader native missing-test debt remain. PR #1's reproduced
rail validation bug is separate: owner now requests its narrow arithmetic fix,
regression check and normal-rail verification before reconsidering merge. No
Fortnite gameplay, owner acceptance, merge or release is claimed.

**Workflow:** global Codex instructions saved the owner's lightweight routing and
review/check/commit/push/remote-verify defaults. Pending gameplay acceptance does
not hold authorized experimental source locally. Codex prepares a concrete merge
recommendation; physical gameplay acceptance and release remain separate.

**Next:** finish this source handoff, then fix/test the isolated PR #1 rail
validation defect. Fortnite host access remains the active integration question;
no additional workflow project or generic IPC framework is authorized.

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
