# Historical backlog and current board

Active status moved on October 4, 2026 to the private
[Combine phase board](https://github.com/users/Jpatching/projects/5/views/4).
Use **Now** for the current phase/skill/next action, **Milestones** for outcomes,
and **Needs you** for decisions and trials. Git remains the source authority.
This file is a frozen historical record, not a second active task list.

The destination is the proper Synergy menu plus trickshot hit radius, without
Combine-specific practice additions. Hide HUD work is preserved and deferred;
it is not a prerequisite. Source coverage, agreed requirements and the first slice
contract are in [the menu guide](docs/TRICKSHOT_MENU.md). The board owns their
current phase and next action; the archived snapshot below is not a resume plan.

Migration checked 17 private drafts, their values and dependency links, board
privacy and actual results of all three view filters. Requirements, decisions
and technical evidence remain in existing local files. If GitHub is unavailable,
record intended changes as sync pending in the handoff; do not revive this list.
See [tracker operations](docs/agents/issue-tracker.md).

---

## Archived snapshot — superseded October 4, 2026

Everything below records earlier status and scope. Its old authority claims,
HUD-first ordering and Combine-additions destination are superseded by the
board and D-012. Completed historical deliverables retain their original evidence.

# Local issue tracker

This file is the status authority. `done` means the stated deliverable exists and
was checked, not owner acceptance or release. There is no remote issue tracker.

## Where we are — Now / Next / Later

**Goal: the full Synergy-derived trickshot menu plus Combine's practice controls,
so players can repeat skating trickshot attempts.** Hide HUD alone does not satisfy
this goal; the menu guide's full feature inventory defines the milestone.
Issue numbers are reference labels, not steps you
must memorise. **C-003 means “test the existing mashup on Windows”**; its letters
identify parts of that larger test. “Baseline” means our first recorded test.

| Player outcome | Current evidence | What remains |
| --- | --- | --- |
| Open the mashup | Verified v0.4.0 archive, separate Windows folder, process started | A launched process alone does not prove play |
| Play Minecraft | Owner reports it worked; 26.3 completion marker and metadata/client/index hashes checked | Possible freeze, individual extracted assets and replay unverified |
| Skate in the mashup | Owner confirms skating works; preparation and DualSense detection recorded | Detailed trick/collision, recovery and replay checks |
| Play and return reliably | Original MW2 matched its before-first-launch hashes; Skate inputs unchanged by conversion | Skating session, replay and post-session MW2 comparison |

- **Now — Build a local trickshot practice menu (C-011):** owner authorized save/return,
  stationary targets, freezing/placing bots and optional aim lock against bots. The
  rejected text panel is replaced by a source-derived Synergy menu; replacement
  acceptance is pending.
- **Next:** owner tries the replacement in the fresh `synergy-menu-dev` trial.
  Publish reviewed source to Jpatching/combine only after replacement acceptance.
  Keep recovery/relaunch and post-session original-file checks outstanding.
- **Later:** Witcher 3 feasibility, then a growing list of tested combinations. Portal
  and Katamari are excluded by owner preference. No additional integration active.

Evidence: [first Windows attempt](research/results/2026-10-03-first-launch.md) and
[free-content research](docs/RESEARCH.md#free-content-search-and-readiness-follow-up--2026-10-03).
Current evidence: [skating preparation and launch](research/results/2026-10-03-skating-preparation.md).
Supplied local Xbox data passed conversion; its distribution provenance is unresolved.

| ID | Status | Owner | Work and completion evidence |
| --- | --- | --- | --- |
| C-001 | done | lead | Initialize Git; add project instructions, evidence records and local verification. See docs/HANDOFF.md. |
| C-002 | done | research | Pin v0.4.0 source and release metadata; inspect integration/setup and record contradictions. See research/upstream.lock.json and docs/RESEARCH.md. |
| C-003 | partial, owner-reported play | owner + runtime | **Test the existing mashup on Windows.** Archive verified and Windows process launched; owner reports Minecraft worked and a possible freeze. Full gameplay acceptance remains incomplete. |
| C-003a | deferred by owner | owner + runtime | **Play MW2 on-foot and return.** Setup completed and process launched; ten-minute Rust play/relaunch not observed. Owner prioritised skating before this acceptance run. |
| C-003b | owner-reported skating; replay pending | owner + runtime | **Skate in the mashup.** Xbox input checks and conversion passed; isolated trial launched; DualSense detected. Owner confirms skating worked; detailed recovery/replay checks remain. |
| C-003c | partial report; further checks pending | owner + runtime | **Play Minecraft, then skate there.** First-play success is owner-reported; next confirm replay. Separately test skating on changed terrain after C-003b. Do not mark the skating recipe passed. |
| C-004 | done | lead | Define recipe v1 and two candidate examples; offline checks reject unsupported/executable input. Does not prove runtime support. |
| C-005 | friction recorded; proposal pending | product | **Make setup understandable.** Owner could not interpret C-003, which modes were enabled, current readiness or the next step. Plain-language status added; a product setup screen still needs a separately accepted slice. |
| C-006 | unresolved | owner + reviewer | Resolve code/converter provenance, asset access and proposed distribution/monetisation rights. Evidence checklist in docs/RESEARCH.md. Blocks public redistribution. |
| C-007 | ready to recruit | owner | Research protocol and recording sheet prepared in docs/VALIDATION.md. Recruit ten players and three creators; no outreach has occurred. |
| C-008 | pending C-003/C-005/C-006 | lead | Specify and implement only the smallest demonstrated usability improvement. Before code, record trigger, interfaces, measurable outcome and acceptance checks. |
| C-010 | needs reproduction | owner + runtime | **Investigate possible freeze.** Owner reports Minecraft worked but believes startup/gameplay froze. Exact stage, duration, recovery and repeatability unknown. Record those before changing versions or settings. |
| C-009 | pending study | owner + lead | Complete continue/change/stop decision in docs/DECISIONS.md using real results; do not fabricate missing measurements. |
| C-015 | setup verified; experience review pending | lead | **Use a repeatable workflow across projects.** Nine pinned Matt Pocock skills plus a Codex router installed globally; custom grill-me preserved. Installed-file validation, manual routing checks and the repository gate passed (16 tests, two recipes, 14-document links). Combine retains its tracker, requirements and release rules. See [workflow guidance](docs/WORKFLOW.md) and [validation](research/results/2026-10-04-matt-workflow.md). Owner asked to leave Hide HUD alone; its proposed workflow pilot is excluded. Two-slice experience review remains future work. |

## Baseline follow-up — Skate in the mashup (C-003b)

**Outcome:** enter Rust, switch onto a board, move and attempt a trick, then return
successfully to the same setup. First skating is owner-reported. These are remaining baseline checkpoints
within it, not independent projects:

| Checkpoint | Completion evidence | State |
| --- | --- | --- |
| Check supplied files and controller | Xbox `default.xex` and required data confirmed; DS5 identified | Technical input checks passed; source provenance unresolved |
| Prepare skating | Fresh `mw2-skate` trial; bundled converter output checks; isolated settings | Passed via agent-assisted CLI; converter 41.53 seconds |
| First skating | Owner explicitly reports skating worked | Owner-reported; individual tricks/collision not separately recorded |
| Recover and return | Ten on/off transitions, fall/recovery, exit/relaunch; record failures; compare original file hashes | Not tested |

- **Exclusions:** public multiplayer, updates, IW4x, a new engine/UI, Minecraft
  skating acceptance, purchases and redistribution. Reuse the bundled converter.
- **Evidence:** use templates/baseline-result.md and the Windows runbook; raw paths,
  manifests and logs stay private. Record pass/fail/blocked/not tested per checkpoint.
- **Failure behavior:** stop on checksum mismatch, absent assets, security warning
  or original-file changes. Record conversion/game errors; preserve the trial.
- **Next decision:** confirm skating behavior on Rust, then choose Minecraft skating
  or freeze reproduction from observed results. No purchase is needed for the current test.

## Active implementation — Local trickshot practice menu (C-011)

- **Outcome:** use the DualSense to save a spot, place a stationary bot, attempt a
  shot and return; optional bot-only aim lock while aiming, disabled by default.
- **Where/why:** small patch against pinned upstream v0.4.0, reusing its movement,
  bot and input systems; separate development runtime preserves the working trial.
- **Exclusions:** noclip, firing while skating, auto-fire, public-match assistance,
  new game integrations, purchases and redistributing game data. Source publication
  to Jpatching/combine is conditionally authorized after replacement acceptance.
- **Acceptance:** Windows build; menu does not leak input; saved spot invalidates
  on map change; no-target/no-save errors are clear; return exits skating first;
  aim lock ignores humans, teammates and occluded/dead bots and stops on release.
- **Evidence:** patch, exact build tools/commands, focused policy/math tests, full
  repository gate, separate launched/gameplay-tested results. Human play still needed.
- **Implementation:** Synergy-native menu implemented and Windows build verified;
  18 synthetic Rust integration/navigation/policy tests pass. Native asset-free
  previews checked at 720p/1080p; gameplay and replacement acceptance remain pending.
- **Evidence:** [replacement report](research/results/2026-10-03-synergy-menu.md),
  [build/trial guide](docs/TRICKSHOT_MENU.md), and [source patch](patches/trickshot-v0.4.0.patch).
- **Next decision:** owner tries the replacement and gives an explicit verdict.
  Previous text-panel rejection does not count as acceptance. Owner follow-up:
  options unchanged; asks about EB and a bigger crossover. Owner confirms EB means
  explosive bullets, then requests review of the entire Steam library. Full
  ownership inventory is pending. C-013 audio follow-up is now authorized; no new
  game integration has started.

## Proposed follow-on — Stunt launcher (C-012)

Recorded only; starts after the replacement menu works and is accepted.
[Proposal](docs/STUNT_LAUNCHER_PROPOSAL.md): save launch point → set target → fixed
on-foot launch → shot attempt → reset on Rust. Acceptance is three repeatable
controller attempts without console commands. No firing while skating, map
editing or new integration. No launcher implementation is active.

## Active follow-up — Skate sounds and highlights (C-013)

Owner requests the latest OBS recording cut to its interesting moments, actual
Skate board pop/landing sounds in-game, and the Christ Air meme music in both
game and clip. The identified song is Pearl Jam's **Even Flow**; the owner has now
supplied an MP3, used for the video and installed game cue. Earlier “Tony Hawk” wording referred to the music,
not a new game integration.

- Outcome: actual jump/landing events play local board samples once; boarding or
  Christ Air starts an optional local music cue. Trim the recording into a separate video.
- Implementation boundary: source patch and tests only in Git; recordings,
  extracted game sounds, soundtrack, inventories and local settings stay private.
- Checks: no repeated sound on held states, no pop when merely falling, no false
  landing on activation/teleport, clear missing-file behavior, stop on leaving
  skating/map change/menu capture. Build and test before a separate trial.
- Evidence needed: decoded local samples, synthetic event/playback tests, Windows
  build and owner listening/playback verdict. No new integration or publication.
- Full Steam library review remains requested, awaiting a complete owned-app
  list; installed manifests and local caches are not accepted as full ownership.
- Picture edit exported: 42.27 seconds, 1080p/60, original recording audio only.
  A separate 42.29-second sound pass adds 24 editorial pop/impact cues. Both
  decode successfully; originals are preserved. These earlier files retain their
  original mixes; the music-backed comedy export is separate.
- Board-event code built, deployed and launched in `skate-audio-dev` on Rust;
  startup decoding confirms both samples loaded. All 27 focused Rust tests and
  the repository gate pass. Sample choice, sync and listening/gameplay acceptance
  remain pending; no source publication has occurred.
- October 4 comedy revision exported separately: 26.78 seconds, 1080p/60,
  rewind, freeze captions, slow-motion replay, original beat and comic effects.
  Full decode and Windows copy hash passed; sixteen segment previews checked.
  Owner humor/listening verdict pending. This earlier version has a procedural
  beat; the new `Combine highlights - Even Flow.mp4` replaces it with the supplied
  song, audible from 2.30 to 24.70 seconds with deliberate ducks. Decoded-audio
  comparison confirms the track is present; file decode and copy hashes pass.
- A ten-second chorus WAV is installed in the audio trial. A fresh launch
  confirmed pop, landing and music all decode. The process had ended by the final
  check, with no panic in inspected logs; reason unverified. Actual boarding/
  Christ Air playback still needs an owner check. No runtime source changed.

## Proposed setup improvement — recorded, not implemented

A future local companion should show the chosen outcome (for example “Skate on
Rust”), detected MW2 files, Minecraft preparation status, missing Skate files,
controller status, and one next action. Use states such as “missing”, “preparing”,
“ready to try” and “play confirmed”; a file check must not claim play was tested.
Explain optional Minecraft downloads and keep errors next to the affected step.
Show friendly trial names such as “Minecraft/on-foot trial — skating off” rather
than treating an internal folder name as the enabled feature list.

First product acceptance check: the owner can identify what is ready, what is
missing and the next action without decoding an issue number. No launcher/UI is
being implemented before the manual baseline justifies its scope.

## Effort allocation (budget, not delivery promise)

- Days 1–2: foundation, source inspection, release pin and provenance questions.
- Days 3–4: Windows reproduction and failure matrix; stop early if prerequisites fail.
- Days 5–6: setup observation, recipe-sharing task and smallest guided-flow proposal.
- Days 7–8: owner-run interviews and observed player sessions when prerequisites allow.
- Days 9–10: synthesise evidence and decide; seven-day return observations may finish later.

Do not claim these days were worked merely because materials exist. If a dependency
is unavailable, record the gap and use remaining effort on independent research.
Do not expand scope to make an unsuccessful experiment look successful.

## Delivery after baseline: vertical slices

These are the proposed increments for C-008 if observed friction justifies a companion.
Each crosses only the layers needed for one player outcome; do not build whole UI,
backend or catalogue layers ahead of usable behaviour.

1. **Play one combination:** choose one supported recipe → validate local prerequisites
   → prepare an isolated profile → launch → see a useful error/retry if it fails.
   Done when an eligible novice succeeds unaided and originals remain unchanged.
2. **Return to it:** save the configuration → exit → reopen that same pinned profile.
   Done when settings persist and failed preparation preserves the last good profile.
3. **Share it:** export recipe → another eligible Windows PC checks/imports it → plays
   the same world/modes. Done with no shared game assets, secrets or private paths.

Only then add another configuration or a discovery website. Reassess whether a
companion is needed after the manual baseline; metadata validation does not complete
these player-facing slices. Use the owner checkpoints in docs/AGENT_ROLES.md.
