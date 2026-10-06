# Handoff — check Fortnite input, then render standalone skating

**Now:** Check Fortnite island input — C-024. Full-island specification and ticket slicing
are complete; eight dependent implementation tickets remain tracked. Integration is incomplete. C-023 preparation
and C-021 GitHub hub-format decision stay Done. **Next:** Render standalone skating
— C-025, after the local Skate asset prerequisite check. **Needs you:** the exact-build
Synergy physical trial remains pending; C-022 pilot threshold is a deferred decision.
No replacement Fortnite version decision is required: the owner permits a suitable
accessible alternative, but the actual choice must be recorded before substitution.

Read the live board and Git together with this read-only terminal command:

```sh
python3 ~/.codex/workflows/solo-development/projects.py summary 5 /path/to/combine
```

It observes current state, prints a UTC observation time, and reports missing remote
branches, unavailable reads and contradictory current pointers. It does not fetch,
write Git/board state, launch games or print raw diagnostics/private asset paths.
At the next two returns, time whether Now, Next and Needs you are clear within one
minute; record the verdict in the existing board. Retire the helper if it adds friction.
Those two owner experience checks have not happened.

Remote observation on 2026-10-06: `main` is
`a5593d671142f31653d45caeaad7b926d40ff855`; published qualification branch is
`b399c55b3abff6fc864fd3158f7df36b17906eac`. [PR #1](https://github.com/Jpatching/combine/pull/1)
is OPEN, with recorded local checks and zero attached automated checks. Review its
entire diff against remote main before proposing merge. Local `main` remains
`bfcb607`, nine commits behind remote main and zero ahead. Reconciliation branch:
`chore/resume-summary`, base `b399c55`; resolve current HEAD with the summary command.
This reconciliation remains local; no merge, CI, branch protection or deployment.
Untracked `tools/fortnite-export/` is preserved and excluded from this slice.

C-024 resumed through a [bounded metadata check](../research/results/2026-10-06-resume-reconciliation.md): local identity records
`++Fortnite+Release-3.1-CL-3917250-Windows`, 3,323 reference/archive files with no
missing/extra files, and matching shipping executable hashes. This is recorded
identity evidence, not a new complete file rehash or rights clearance. Recorded
parser attempts mount 0 of 10 containers, report incomplete inventory and find
zero worlds; one inventory declares all ten encrypted/unmounted. No export,
collision witness or gameplay is verified. No replacement version selected, no
bypass attempted, no game assets/logs uploaded, and the untracked exporter was not run.
C-025 prerequisite discovery found the earlier extracted Xbox data, but no expected
runtime `private/stock` asset directory in the bounded project search; original
Windows trial assets may exist outside this search. Confirm the prepared Skate
asset root and its stock input/config/graphs before starting standalone rendering.

Inherited verification debt: upstream `physics.rs` references absent
`src/tests/map_startup.rs`, so the broader Skate-host all-target test build fails
before tests execute. Next required check before claiming broader runtime
verification: inspect a reviewed upstream correction or restore the intended test
source, then rerun the full host suite; do not delete the reference to hide debt.
The recorded 13 focused Rust tests establish synthetic world validation and host
boundary error behavior. The repository gate checks Python research/scaffolding,
recipes and document links. Neither establishes Windows rendering, controller
behavior, collision in real island data, recovery, performance or physical gameplay.
Those require exact-build trials and explicit owner acceptance separately.

Reconciliation verification: repository gate PASS (27 tests, 2 recipes, links in
17 documents); global workflow tests PASS (15), summary tests PASS (7), diff
whitespace check PASS. Independent Standards/Spec findings corrected with focused
regressions. Installed global helper/test hashes and exact reproduction are in the
linked evidence. Runtime tests were not rerun for this documentation/helper slice.
Upstream HEAD/v0.4.0 still match the pin. Board fields/titles/views read-back PASS;
final evidence update is recorded on the live C-020/C-024/C-025 cards.

Phase 5 reconciliation verified | chore/resume-summary, base b399c55 (resolve HEAD
with summary) | local/unpushed | gate 27, global 15+7 PASS | board read-back checked |
next Codex: locate and validate the prepared Skate asset root for C-025.

Next actor: Codex. Record the C-024 container/parser blocker; check C-025's prepared
Skate assets, then implement the standalone renderer while preserving the full-island
destination. Release and Synergy acceptance remain separate.

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
