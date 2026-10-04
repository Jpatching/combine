# Handoff — requirements settled; Intervention ready, 2026-10-04

The full Synergy menu plus near-pass hit radius now has an agreed contract and
acceptance examples in [the menu guide](TRICKSHOT_MENU.md). D-013 records the
noclip/private-player scope changes; [source coverage](../research/results/2026-10-04-menu-coverage.md)
shows why Trickshot Dummy's impact-distance logic does not prove near-pass behavior.
Native compatibility, bullet/cover integration, noclip cleanup and private-session
synchronisation remain explicit implementation research. No runtime code changed.

The private [Project](https://github.com/users/Jpatching/projects/5/views/4) is the
status authority. C-017 is Done; to-spec published the C-011 contract; to-tickets
finalised C-016 as the sole Now item, ready for Phase 5 implementation. Bodies and
fields were read back; the milestone stays open. No owner input is needed until
the slice is ready for its isolated Windows trial. The card requires an exact
launch command/shortcut, binary hash and short checklist at that point.

Branch `slice/hide-hud`; HEAD/base `bfcb6073a829cb7b7f1b314a66c7006213ef0917`.
Inherited dirty work remains; no commit, source remote, PR, merge or release.
Menu/audio/Hide HUD patches are untouched. Deferred Hide HUD SHA-256 remains
`31568ed152da16aecd4a93194c602e9a8fe05af29744a52e45936e7dbf3e780a`.
`git ls-remote` refreshed runtime HEAD/v0.4.0 and Synergy HEAD/main; both still
match their unchanged pins. Source publication still requires explicit replacement
acceptance; assets, recordings, private logs and settings remain outside Git.

Board detail: 17 drafts and the extra roadmap view (View 5) were preserved. The
standard helper stopped before writes because it requires exactly three views.
A reviewed temporary `/tmp/combine-c017-update.py` used the shared helper's
snapshot/mutation functions to update only C-017, C-011 and C-016, checking private
visibility, bodies/fields and unchanged unrelated drafts/views. JSON read-backs
are `/tmp/combine-c017-{decision,spec,tickets}-readback.json`; these are temporary
reproduction artifacts, not another tracker. No roadmap dates are configured.

Verification: `python3 scripts/verify.py` passed (16 tests, two recipes, lock
structure and links in 14 documents); `git diff --check` passed. Additional
local-link checks covered all nine edited documents, including research/tracker
files outside the gate's link scan. Final board refresh confirmed 17 private
drafts, only C-011/C-016/C-017 changed, unchanged fields/four views, and field-filter
counts Now 1, Milestones 2, Needs you 4. Menu/audio/Hide HUD hashes match prior
evidence; archived backlog text is unchanged.
No native build, gameplay or new owner verdict is claimed. Inherited baseline
recovery/replay, possible freeze and audio listening evidence remain incomplete.

Next: implement the finalised Intervention contract through the existing typed
weapon path; pass its behavior/build/preview checks, then prepare a fresh trial
and supply launch instructions. Demonstrate equip/fire and input-release behavior
before asking the owner to accept it. Keep hit radius and other options outside
that first slice, and keep Hide HUD deferred.

---

# Handoff — skating audio and private highlights, 2026-10-03

October 4 follow-up: the owner supplied a local Even Flow MP3 after requesting
a funnier edit. The newest export is **`Combine highlights - Even Flow.mp4`**
in Windows Videos/Combine Clips: 26.78 seconds, 1080p/60, rewind, freeze captions,
slow-motion replay and comic effects. Even Flow replaces the earlier procedural
beat, entering at 2.30 seconds and cutting at 24.70. Full decode passed; decoded
audio matches the music stem with correlations 0.9506–0.9951 in four windows.
The video packet hash is unchanged from the visually checked comedy cut, and
the Windows copy matches SHA-256
`cebe18bd64bbde6599fc6d841eda23bec8faa45ee3b9a2f322f107465ca865ce`.
The supplied MP3 and all previous exports are preserved; nothing was published.

A ten-second chorus cue is installed as the trial's private `christ-air.wav`.
Startup log confirmed all three clips load after launch on Rust (PID 85412).
The process ended before the final process check; no panic was found, and the
exit reason was not established. Do not claim audible gameplay or a current
running process. Next: owner watches the music-backed video, then opens
**Combine Skate Audio** and checks boarding/Christ Air playback and menu silence.

The latest owner priority adds board pop/landing sounds in-game and edits the
latest OBS recording. The requested Christ Air meme song is **Even Flow by Pearl
Jam**, for both the game and clip. A 42.27-second 1080p/60 picture edit and a
42.29-second board-sound pass were exported beside the OBS recording. The latter
adds 24 editorial cues using the trial samples; listening/sync acceptance remains
pending. Both earlier files retain the original audio. The full Steam-library review is pending a complete
owned-app list; cached/installed entries were not misrepresented as ownership.

The audio source is a separate `patches/skate-audio-v0.4.0.patch`, applied after
the unchanged menu patch. Its hash is
`0f42b291c87ee2a57ee19a29603298ebd359abb9ead97743b475571101aa4456`.
It reacts to native simulation events, preloads optional local WAVs, starts a
short cue on boarding/Christ Air, prevents overlapping music, and stops on menu
capture/exit. Two real Skate collision samples are decoded privately; the exact
pop-versus-landing assignment is provisional and needs listening. No music or
game sounds are committed. See the [current result record](../research/results/2026-10-03-skate-audio-highlights.md)
for build status, private reproduction paths, evidence and acceptance checks.

Final audio executable SHA-256:
`2319178a836247efaff4b99852eebaf920e0697e1b894a7310739a0c06470807`.
Five event tests, four Windows playback tests and eighteen menu regressions pass.
The fresh trial is `%LOCALAPPDATA%\CombinePilot\v0.4.0\skate-audio-dev`, with
desktop shortcut **Combine Skate Audio**. Source assets and the earlier trials
remain unchanged. Upstream HEAD/v0.4.0 were refreshed October 4 and match the pin.
The earlier trial was launched on Rust (PID 84892, responding window observed).
That initial run had both board clips and no music; the supplied cue now loads
as recorded above. This does not establish audible gameplay. The full repository
gate passed: 16 Python tests, two recipes, lock structure and 13-document links.
The sound-pass video fully decodes, preserves the picture edit's video packet
hash, and its Windows copy matches SHA-256
`ffa72ccb9da8c8893be9b663e8e09949b234039d86731c6936697a40ddbb1e2e`.

Next concrete step: obtain an owner listening/gameplay verdict. Menu
replacement acceptance and GitHub source publication remain pending.

## Menu-only build and earlier trial

The existing practice actions now use a Synergy-derived native menu with submenus,
proportional font, cyan selection and complete hiding when closed. Physical input
is blocked through button release. The new `synergy-menu-dev` Windows trial is
prepared and launched. **Next: owner tests it and gives a replacement verdict.**
The owner reports the options are unchanged and asks about EB and a bigger game
crossover. The slice intentionally retained eight practice actions; EB is not
implemented; the owner confirmed it means explosive bullets. No acceptance was given.
The rejected text panel does not count as acceptance. Publication waits for that
verdict as required by the selected plan.

Read [player controls](../README.md), [reproduction/sense-check](TRICKSHOT_MENU.md)
and the [exact result record](../research/results/2026-10-03-synergy-menu.md).
[BACKLOG.md](../BACKLOG.md) remains the status authority.

- Branch `main`; HEAD/base `714660171c6726241075913308e3009516c3ebb6`.
  Working tree is dirty, including inherited research edits; no new commit or
  project remote. Do not discard or stage everything indiscriminately.
- Runtime pin `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; Synergy pin
  `33bcc80f5446e7543a2eb68b17c798e29d3f27c4`. Remote refs refreshed, pins unchanged.
- Reviewable source: patches/trickshot-v0.4.0.patch; SHA-256
  `44f037ae7a459209bcc081cc8ce7e26e7de886936ff414bb5ba1aa08f9e01812`.
- Earlier menu-only Windows binary SHA-256
  `298c5b4097e7fd8b18632d7dacd1b62c0c39977905eb3a9e5642c92c721dcdf0`.
  Built with Rust 1.95.0, cargo-xwin 0.23.1 and Clang/LLVM 19.1.1; exact commands
  and inherited warnings are in the result record.
- Full repository gate: `python3 scripts/verify.py` passed (16 Python tests,
  two recipes, lock structure and links in 13 documents); `git diff --check` passed.
- Windows synthetic Rust tests: 18 passed. Patch-applied pure tests: 6 + 4 passed.
  Native asset-free root/Aim/error/closed previews checked at 720p and 1080p.
  These checks do not prove controller gameplay, visual acceptance or release.
- Trial: `%LOCALAPPDATA%\CombinePilot\v0.4.0\synergy-menu-dev`, desktop shortcut
  **Combine Synergy Menu**. Existing trials preserved; copied binary hash matched
  and source runtime executable unchanged. Current trial was launched on Rust.
- `.private/trickshot/upstream` is the ignored patched build checkout; baseline
  copies and assets remain private. No game content, local settings, raw private
  logs or OBS/recordings belong in the source patch or Git.

The owner previously confirmed skating and Minecraft worked. Baseline recovery,
replay, post-session original-game comparisons and a possible freeze remain open.
No new recipe/GSC loader/network interface/game integration was introduced. The
GPL source port carries Synergy/M203/Apparition credits and the complete licence;
this does not settle game-asset rights.

After owner acceptance, review the explicit source/documentation file list, make
a real commit, establish authorized access to Jpatching/combine and publish source
and notices only. The destination's unauthenticated Git read requested credentials; connected
GitHub search and `gh repo view` also could not resolve it. Access/existence
is still unverified. No publication occurred. The separate
[stunt-launcher proposal](STUNT_LAUNCHER_PROPOSAL.md) remains inactive until this
slice is accepted.
