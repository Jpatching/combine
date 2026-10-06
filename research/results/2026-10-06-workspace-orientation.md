# Workspace orientation and bounded Skate asset check — 2026-10-06

This slice makes Combine understandable on return and checks one prerequisite
on the Fortnite route. It changes explanations, not runtime behavior. The
existing board, roadmap and Fortnite wayfinder map remain the authorities;
no dashboard, launcher, wrapper or new decision ticket was added.

## What works, what is blocked, who acts

| Outcome | Phase and current evidence | Exit evidence / blocker / next actor |
| --- | --- | --- |
| Full Fortnite island + Skate only | C-024: Phase 1, input qualification. Spec/tickets exist; C-023 native world validation is implemented | Need mountable identified island, dependency census, export/collision witness. Recorded parser attempts mount 0/10 containers. Codex qualifies compatibility; no bypass. Replacement permitted, none selected |
| Standalone skating, fallback while input is blocked | C-025: Phase 4 contract ready; asset presence checked today, rendering not implemented | Need successful pinned host load, render/input/camera/lifecycle checks. Broader host tests have missing upstream test source. Codex checks initialization before implementing |
| Actual Synergy + hit radius, separate experience | C-016: Phase 6 physical input trial pending; automated Intervention/input evidence exists | Owner tests exact c591086 folder. Full option effects and hit radius unfinished; menu guide retains requirements. Trial acceptance is separate from menu implementation |
| Existing MW2/Skate/Minecraft baseline | Owner-reported skating/Minecraft play | Recovery/replay/freeze and original-file comparison incomplete; owner follows Windows baseline runbook |
| GitHub catalogue/community evidence | C-021 format decision complete, C-022 threshold deferred | Existing roadmap/map retained. Additional games wait for Fortnite first playable milestone; owner threshold decision is deferred |

```text
Chat + handoff -> live board + Git -> one missing check
  Fortnite input -> mount/export/collision witness -> adapter work
       | externally blocked
       v
  prepared Skate assets -> host load -> standalone render/input -> owner trial
  separate Synergy exact build -------------------------------> owner verdict
```

The fallback removes a prerequisite on the same Fortnite destination; it does
not turn synthetic skating into Fortnite play or replace the Synergy trial.

## Short tour: what you actually use

Start by saying **Continue Combine**, with docs/HANDOFF.md available. The owner
uses the prepared trial shortcuts and checklist for a requested physical test.
The developer commands below are for Codex; no script names need memorising.
README/ROADMAP explain the destinations; the private board supplies current phase,
blocker and actor. docs/REPRODUCING.md and patches/README.md supply source steps.

Our runtime changes are source patches in `patches/`, applied to the pinned
upstream Rust runtime. Upstream owns the engine, rendering, input and Skate
systems; Combine changes selected behavior. The Synergy chain applies menu,
audio, Intervention, actual GSC and input patches in documented order. Earlier
native presentation is historical but remains a patch prerequisite, so it cannot
simply be deleted. The standalone Skate patch applies independently to a clean
pin; it validates native world geometry, not Fortnite files or gameplay.

Private Windows trials contain separately prepared local assets/settings and an
exact executable; they are distinct from source patches and build directories.
A file tree means prepared input, a running process means launched, and physical
results mean gameplay evidence. None alone means owner acceptance.

## Script review (source-inspected; not all rerun)

References checked across README, docs, research/results and tests. No script
consolidation is justified by this orientation; useful shared launch/review behavior
already lives in the global workflow module. No codebase-design change is needed.

| Script | Classification | Input -> processing -> output; failure / intended user |
| --- | --- | --- |
| `scripts/verify.py` | Active | Pins, two recipes, links and tests -> offline validation -> pass/fail exit. Invalid metadata/links/tests fail. Codex's full gate; no gameplay |
| `scripts/check_recipe.py` | Active research check | Recipe JSON + lock -> strict validation -> pass/fail. Reject unsupported/executable input; never installs/launches. Codex |
| `scripts/prepare-trickshot-trial.ps1` | Active, separate Synergy route | Prepared runtime + exact binary/hash/evidence/checklist -> isolated copy and shared review bundle -> prepared/unaccepted trial. Existing destination, missing inputs/hash mismatch/copy failure stop; partial copy retained. Codex; `-Launch` is live execution and was not used |
| `scripts/launch-synergy-trial.ps1` | Active bundle adapter | Bundled verified launcher -> actual GSC with diagnostic inputs disabled -> verify-only or owner launch. Requires sibling `verified-launch.ps1` generated by preparation; not a standalone repo launch command |
| `scripts/run-synergy-diagnostic.ps1` | Active developer diagnostic | Runtime/binary/report options -> isolated bounded automated run -> private report. Refuses existing report/game process; may stop its diagnostic process on timeout. Not an owner trial; not run today |
| `scripts/synergy-diagnostic-log.ps1` | Active internal module | Diagnostic lines -> redacted ordered observations -> checker data. Called by diagnostic script/tests; owner need not invoke it |
| `scripts/check-synergy-diagnostic.py` | Active evidence checker | Redacted enabled report + same-build disabled baseline -> provenance/order/fault checks -> pass/fail. Synthetic fixtures do not prove play |
| `scripts/prepare_experience.py` | Unfinished product scaffolding | Named experience + private root -> empty workspace/manifest -> scaffolded/unaccepted. Rejects existing/unsafe destination; retains partial failure. Does not copy assets/build/launch; unnecessary for owner play |
| `tools/fortnite-export/` | Unfinished inherited, untracked | Exporter/check-runner source and dependency lock; compatibility/export incomplete. Preserved byte-for-byte and not executed or staged; requires review before execution |
| Global `projects.py summary` | Active read-only orientation | Project number + repo -> board/Git/PR observations -> timestamped Now/Next/Needs you. Missing reads explicit; no fetch/write/launch. Two owner return verdicts still pending |

## Folder review

| Area | Classification and reason |
| --- | --- |
| `docs/`, `research/upstream.lock.json`, `recipes/`, `licenses/`, `templates/`, `tests/` | Active requirements, pinned metadata, research checks, attribution and evidence fixtures. Baseline/intervention templates also retain older pending trials; not generic playable recipes |
| `research/results/` and `BACKLOG.md` | Historical evidence retained; latest linked reports remain active evidence. BACKLOG is a frozen board pointer, not today's task list |
| `patches/` | Active source authority plus historical prerequisites; standalone patch independent, Synergy chain still required |
| `.private/fortnite-runtime`, `fortnite-replay`, `fortnite-qualification` | Active private source/replay/parser workspaces; caches/outputs generated. Source revisions belong in tracked patches/evidence, not private copies |
| `.private/fortnite-input`, `fortnite-build`, `export-build`, `dotnet-10.0.401` | Private input and generated build/tool caches. Not source deliverables; input evidence is blocked, not playable progress |
| `.private/trickshot`, `synergy`, `intervention`, `skate-audio` | Preserved source copies/tools, generated previews and separate private trials. Some native previews are historical; actual Synergy and audio verdicts remain incomplete |
| `.private/c003a`, `c003b` | Preserved baseline preparation/input evidence, extracted game data and converter tooling. Original installs/trials stay intact |
| `.private/hide-hud`, `workflow-guide`, `workflow-routing` | Historical/deferred work and a separate registered Git worktree. No active HUD dependency; never remove a worktree as an ordinary folder |
| `.private/steam-review`, `obs`, `video-edit` | Earlier private inventories/recording/export work, generated media and tooling; ownership/listening/verdict gaps retained |
| `.private/separate-mashups`, `scripts/__pycache__`, `tests/__pycache__` | Private local preparation state and generated Python caches; neither proves a build |
| `.agents/`, `.aws/`, `.codex/`, `.git/` | Local configuration/credentials or Git metadata; excluded from source cleanup and publication |

**Proposed removals: none. Proposed relocations: none.** References and unresolved
trial requirements justify preservation. No blanket cleanup occurred.

## Git/worktree review and merge boundaries

Observed October 6, approximately 09:10–09:20 UTC. Refreshed origin; main is
`a5593d671142f31653d45caeaad7b926d40ff855`. Local main `bfcb607` is zero ahead,
nine behind. Initial branch `chore/resume-summary` at
`ad8b793adb4b3095884ccec1c694d10216313c5c` was clean except untracked `tools/`.
Registered other worktrees: `.private/workflow-routing/repo` at b52c28f,
and `/tmp/combine-workflow-docs` at b52c28f (Git reports prunable; preserved).

PR #1 is OPEN: qualification b399c55 -> main, zero attached automated checks.
Its complete file inventory and commit outcomes were inspected; the full runtime
diff was retained for merge review. This is
an orientation/merge-boundary review, not a fresh correctness approval of 3,833
lines of runtime patch. The earlier full source review/checks are linked from the
standalone evidence. A new complete Standards/Spec review is required before
proposing merge; no merge is proposed here.

Identifiable outcomes above main: b5a2d7a unfinished workspace scaffold;
82ea441 specification/docs; adf769c native world validation; b399c55 verification
handoff; ad8b793 resume summary (global helper itself lives outside Combine Git).
Do not merge these ancestors merely to clean the workspace. Scaffold, runtime
and documentation outcomes need explicit boundaries/prerequisites in a merge review.

New `docs/project-orientation` was created from refreshed origin/main, then
fast-forwarded to the existing `chore/resume-summary` prerequisite. No main or
ancestor was rewritten. Its focused review diff starts at ad8b793; its complete
main-relative diff still contains those unmerged ancestors. New source branch
publication, merge and release were not performed.

## Bounded Fortnite-route check: prepared Skate asset presence

Inputs: recorded baseline trial location, its asset setting, and pinned host
source (`skate-data/src/manifest.rs`, `input_config.rs`, `animation_banks.rs`,
`skate-host/src/graph_runtime.rs`). Processing: read-only existence/path checks;
print only booleans/version, never setting values, asset bytes or private logs.
Output: one recorded trial root and its `skate-data/assets` directory found.
One unrelated Windows profile was inaccessible; skipped, not evidence of absence.

The earlier search for a stock root missed `skate-data/assets/private/stock`.
Verified: configured asset root resolves to this tree; game manifest version 1;
character_scene/action_graph/motion_graph use safe relative paths and exist;
private/skater.glb, stock input.cfg, physics-skeletons.json,
skater-collections.json, OnBoard.abin and OffBoard.abin exist.
An exploratory check for guessed Andale/ped filenames returned absent; the source
requires OnBoard/OffBoard, so those guesses do not establish missing prerequisites.

Reproduce locally: in the preserved baseline runtime, resolve IW4L_SKATE_ASSETS
without printing it; check the relative files above and the three manifest
references with is_file, after rejecting absolute/traversal/colon/backslash paths.
Do not run the converter or change settings for this check. Missing/unsafe paths
must block initialization. Asset contents, compatibility, hashes and host loading
were not validated. Next Codex check is isolated pinned host initialization;
only then implement standalone rendering. The parser's reported encryption is
still a report, not a proven diagnosis; input compatibility remains C-024 Now.

## Verification and handoff

Required gate: `python3 scripts/verify.py`; whitespace: `git diff --check`.
Results recorded below. No runtime changes mean
no new runtime build/test or physical-play claim. Inherited full host test debt:
missing `src/tests/map_startup.rs`; restore/review intended source before rerun.
No game assets/private logs uploaded, exporter run, install modified or game launched.

Orientation acceptance remains the owner's next-return sense-check: with the
reminder, identify usable today, current task, blocker/next actor and next instruction.
If unclear, simplify existing text before adding tools. No owner verdict inferred.

Final evidence: repository gate PASS, 27 tests, two recipes and links in 17
documents; whitespace PASS. Self-review of the orientation diff completed;
no independent runtime review claimed. Upstream HEAD/tag still match runtime
f608f85e407ff1b7689d54a9aafdd16e95711ac4; Synergy HEAD/main still match
33bcc80f5446e7543a2eb68b17c798e29d3f27c4. Pins unchanged.
C-020/C-024/C-025 evidence/fields read-back PASS; unrelated items, fields and
views preservation PASS. The global helper's field-write/read-back primitives
were used with explicit preservation checks; no view-template reset performed.

Phase 5 orientation checked | docs/project-orientation, prerequisite ad8b793
(resolve final HEAD with Git) | local/unpushed | gate 27 PASS |
board evidence read-back PASS | Codex next: isolated pinned Skate host load;
Fortnite input compatibility remains Now. Owner next-return usability verdict
and exact Synergy physical trial remain pending independently.
