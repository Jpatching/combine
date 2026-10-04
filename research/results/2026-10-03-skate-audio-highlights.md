# Skate audio and recording highlights — 2026-10-03

Work began on October 3; final checks continued into October 4 (Europe/London).

The owner requests real board pop/landing sounds in the game and a short edit of
the latest OBS recording, with the skating meme music in both. The song was
identified as **Even Flow — Pearl Jam** from the [Christ Air / Steezus meme
reference](https://knowyourmeme.com/memes/jesus-skating-in-skate-3-to-pearl-jams-even-flow-steezus-christ).
The earlier Tony Hawk wording referred to music, not a new game integration.

The picture edit, board-sound pass and comedy edit exist. The owner subsequently
supplied an MP3: a new music-backed comedy export and installed ten-second game
cue now use it. Startup decoding is confirmed; listening/gameplay acceptance
remains outstanding.

## Source and behavior

Apply `patches/trickshot-v0.4.0.patch`, then
`patches/skate-audio-v0.4.0.patch` to runtime
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
Audio patch SHA-256:
`0f42b291c87ee2a57ee19a29603298ebd359abb9ead97743b475571101aa4456`.
Both patches apply cleanly in sequence; all 19 resulting files match the build
checkout. The menu patch and its attribution/licence are preserved unchanged.

```text
Completed Skate tick -> jump / airborne / landing / Christ Air signals
  -> bounded event queue -> current local skating presentation
  -> predecoded local WAV -> game audio output
Inactive, captured input, teardown -> discard cues and stop these voices
Missing or invalid WAV -> one startup warning; gameplay continues
```

The bridge collects cues at simulation-tick frequency, so rendering batches do
not lose short animation events. `physics/bridge_audio.rs` gates rising jump and
Christ Air attributes and native airborne-to-ground transitions. Drops make no
pop. Activation/teleport/biped states break the sequence. Landing volume scales
with measured fall speed. Christ Air has a ten-second cooldown.

`crates/render_anim/src/skate.rs` forwards only current-epoch, uncaptured local
cues. `crates/audio/src/skate.rs` preloads WAVs and plays them through the existing
Bevy audio output/master volume. Boarding starts the optional music cue; Christ
Air can trigger it again when no music cue is playing. Music lasts at most ten
seconds, with a short ending fade. Menu resume does not restart it. Leaving
skating, menu capture or leaving the game screen stops the voices.

This is a small native adapter, not a recreation of Skate's complete audio mix.
Surface variation, rolling loops, grinding, bails, original per-material mixing
and new keyboard skating controls are excluded.

## Local sound files

Set `IW4L_SKATE_AUDIO` to a private directory containing `pop.wav`, `land.wav`
and optionally `christ-air.wav`. Without that variable, the fallback is
`IW4L_SKATE_ASSETS/private/audio`. WAV files are limited to 16 MiB; effects to
five seconds and the music input to twenty seconds. Preloading occurs at startup;
restart the trial after supplying/changing a file.

Two genuine samples were decoded from the locally supplied
`data/audio/audiofiles.big` -> `data/audio/Skate_Collisions.bnk`:

| Trial assignment | Native stream | Duration | Status |
| --- | --- | --- | --- |
| pop.wav | 0 | 0.24025 s | Decode verified; exact event assignment needs listening |
| land.wav | 15 | 0.429645833 s | Decode verified; exact event assignment needs listening |

These are provisional selections from the collision bank, not a verified mapping
of retail pop/landing events. The local manifest records bank and sample hashes.
No audio asset is included in the source patch.

The private extraction used reviewed `BigArchive`, RefPack and XMA-wrapper source
from [SK8-Engine-sleepen](https://github.com/sleepenskates/SK8-Engine-sleepen/tree/29c9c7caf8692eaa2ce20689f9e1de535bd7145c/tools/skate3_ui_extract),
revision `29c9c7caf8692eaa2ce20689f9e1de535bd7145c`, with local FFmpeg decoding.
Extractor source and all output remain ignored/private; none is added to this
repository's deliverable. This does not resolve the existing asset-provenance or
distribution questions.

## Checks

- Five pure sound-event tests passed: held-state deduplication, drop versus jump,
  activation/teleport/biped/contact exclusions, Christ Air cooldown and invalid
  sample reset.
- Final Windows playback tests: **4 passed, 0 failed**, 0.09 s, including boarding
  music and menu-resume behavior. Together with the five event tests and eighteen
  menu tests, 27 focused Rust tests passed across Linux/Windows.
- Existing Windows menu regression suite: 18 passed, 0 failed, 0.11 s.
- Final audio runtime build passed in **1m47s** using the established toolchain.
  Executable SHA-256:
  `2319178a836247efaff4b99852eebaf920e0697e1b894a7310739a0c06470807`.
- Existing warnings remain: `render_frame` static `must_use`, and two
  `skate-host` visibility warnings. No warning was suppressed.
- Full repository gate `python3 scripts/verify.py` passed: 16 Python tests,
  two recipes, lock structure and links in 13 documents. `git diff --check` passed.

An audio-only Cargo test build rebuilt a different Bevy feature set (5m18s).
The documented combined audio/console invocation preserves the established
feature set; it also completed successfully. Cargo.lock remained unchanged at
SHA-256 `dc1689f140c5fac899126f60dfa82dee97df76d65eccd78e604952061a783a5d`.
Upstream HEAD and v0.4.0 were refreshed on October 4 and still resolve to the
selected `f608f85e407ff1b7689d54a9aafdd16e95711ac4`; no baseline was changed.

Build with Rust 1.95.0, cargo-xwin 0.23.1 and native Clang/LLVM 19.1.1 using the
same paths/cache as the [menu build record](2026-10-03-synergy-menu.md):

```sh
cargo +1.95.0 xwin test --offline --locked --profile play --target x86_64-pc-windows-msvc -p audio -p console --lib --no-run
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l
```

Run the produced audio test executable with filter `skate::tests`; run the console
test executable with filter `practice`. These tests inspect events and playback
entities, not human hearing or controller gameplay.

## Separate Windows trial

Prepared `%LOCALAPPDATA%\CombinePilot\v0.4.0\skate-audio-dev`, with the desktop
shortcut **Combine Skate Audio**. The final installed executable hash matches
the build hash above; both sample copies were checked. Earlier trials and the
original executable were preserved.

Launched on Rust on October 4: process 84892 was responding with window title
`iw4l - mp_rust`. A local inspection of the native startup log confirmed
`pop=true`, `land=true`, `Christ Air music=false`; the missing-file diagnostic
was for `christ-air.wav`. No raw log is included here. This verifies startup
decoding, not audible playback or owner acceptance.

## Highlights edit

Input: latest completed `Combine 2026-10-03 22-05-50.mp4`, 452.682 seconds,
1920x1080, approximately 60 fps. Reviewed overview and denser action frames.
Output: `Combine highlights - picture edit.mp4`, **42.271333 seconds**,
1920x1080/60, H.264 + stereo AAC, 74,578,094 bytes. Menu setup/waiting was removed;
six cuts retain flips, forest skating, a water drop and a ravine finale.

| Source interval (seconds) | Edit |
| --- | --- |
| 24.20–32.20 | First flips |
| 99.00–109.50 | Backflip line |
| 153.10–160.70 | Forest tricks |
| 182.50–187.00 | Water drop |
| 390.00–395.20 | Gap attempt |
| 405.00–411.45 | Ravine finale |

SHA-256: `a9e23b166f31f9424af65ab7aab5369e9b87f0e9378330cd01fa2af64774b261`.
Full FFmpeg decode returned 0 with no errors; output contact sheet inspected.
Copied beside the original in `%USERPROFILE%\Videos\Combine Clips`, with matching
hash. Original recording is preserved. The edit currently keeps original audio;
it contains no added music and is not evidence that the new live sounds worked.

An additional **`Combine highlights - board sounds.mp4`** is exported beside it:
42.290 seconds, 1920x1080/60, H.264 + stereo AAC, 74,747,834 bytes. It adds
24 pop/impact cues using the same provisional samples as the trial. Timings were
estimated from four-frames-per-second contact sheets; listening/sync acceptance
is still pending. These editorial cues are not game telemetry. Original audio
is retained at 80 percent; the final measured peak is -5.8 dBFS. No music is mixed.

Sound-pass SHA-256:
`ffa72ccb9da8c8893be9b663e8e09949b234039d86731c6936697a40ddbb1e2e`.
The Windows copy matches. Full FFmpeg decode passed with no errors; the video
packet hash matches the picture edit, confirming that its images were preserved.
Private `mix-board-sounds.py` and `board-sounds-edit.json` preserve the mix recipe
and event timings. The picture-only edit and original recording remain intact.

## Comedy revision — October 4

The owner requested a funnier, more heavily edited version. Exported
**`Combine highlights - overedited.mp4`** beside the earlier clips: 26.783333
seconds, 1920x1080/60, H.264 + stereo AAC, 42,152,893 bytes. It uses sixteen
segments: a ravine cold open, rewind, “Call of Duty / Pro Skater” title,
freeze-frame captions, a cropped slow-motion bail replay, faster transitions,
and the final fall as the punchline. The earlier exports remain intact.

The mix retains retimed recording/board audio and adds original procedural
drums, bass and comic effects. It **does not contain Even Flow**. The owner
reported never hearing the song, then requested a YouTube download; no track
was downloaded by the agent. This earlier export remains intact; the later
owner-supplied-file mix below completes the soundtrack preparation.

SHA-256: `47938bf2b06f0ff9e39e343586752a3f04cffb8685f311686cb9fe58b57c9269`.
The Windows copy matches. FFprobe counted 1,607 video frames; audio/video
durations agree within one millisecond. Full FFmpeg decode passed with zero
errors; measured audio peak is -3.7 dBFS. A contact sheet covering all sixteen
segments was visually inspected for caption placement and composition. This
does not constitute a listening verdict or owner acceptance of the humor.

Private reproduction: `python3 .private/video-edit/render-comedy.py`, using
FFmpeg 6.1.1, NumPy 2.4.1 and the local Impact font. The script refuses to replace
its finished export, records source/output timing in `comedy/timeline.json`,
and verifies the source clip's hash is unchanged. Renderer, stems, captions,
contact sheet and videos remain ignored/private. No runtime source changed.

## Supplied Even Flow mix — October 4

The owner supplied a local 325.51-second stereo MP3. The input is preserved.
Local speech timing placed the first chorus around 73.7 seconds; the edit uses
73.55 seconds as its start, including a short lead-in. Transcription was used
only as an approximate timing aid; no audio was uploaded. Its private transcript
and temporary ASR environment/model remain outside Git.

New export: **`Combine highlights - Even Flow.mp4`**, 26.783333 seconds,
1920x1080/60, H.264 + stereo AAC, 42,143,177 bytes. It retains the inspected
comedy video's exact encoded pictures and original/comic effects. Even Flow
replaces the procedural beat, playing from 2.30 to 24.70 seconds, ducking under
the replay/freeze joke and stopping at “Objective Failed.”

Video SHA-256: `cebe18bd64bbde6599fc6d841eda23bec8faa45ee3b9a2f322f107465ca865ce`.
The Windows copy matches. Full FFmpeg decode passed without errors; decoded
audio peak is -2.09 dBFS. Comparison of decoded video audio against the music
stem at four intervals gave correlations 0.9898, 0.9951, 0.9942 and 0.9506,
confirming that the supplied music is actually in this export. This is a signal
check, not an owner listening verdict.

Game cue: ten seconds from the same chorus, PCM16 stereo at 48 kHz, 1,920,044
bytes, with a short fade-in and 0.4-second ending fade. Installed as
`skate-audio-dev/combine-audio/christ-air.wav` after checking the trial binary.
Cue SHA-256: `6d844e7611c0bb7233dbce8551ab671ede738f8d49e0827b42fe41151b68fbd2`;
the installed file matches. The former session had closed by installation time.
A fresh Rust launch (PID 85412) confirmed `pop=true`, `land=true`,
`Christ Air music=true`, with no missing-cue diagnostic. The process had ended
by the final poll; no panic was found in inspected logs, but the reason is
unverified. Audible boarding/Christ Air behavior is still untested by the owner.

Private reproduction: `mix-even-flow.py <provided-mp3> --chorus-start 73.55`;
`even-flow-mix.json` and `even-flow-verification.json` record source hashes,
timings and checks. `install-even-flow.ps1` copies only hash-verified new files;
`start-music-trial.ps1` launches only when no `iw4l` process exists. No runtime
code or executable changed, and originals/earlier exports remain intact.

## Remaining acceptance

Watch the new music-backed comedy edit. Listen to the provisional board samples and replace their
assignment if they do not sound like a pop/landing. In the separate trial, test
three pops and landings, drop off an edge, open/close the menu and leave skating;
verify one sound per action and silence at the boundaries. Then test boarding and
Christ Air music with the installed cue. Formal menu acceptance/publication remains
pending; no GitHub publication occurred.

The separate full Steam-library review is pending a complete owned-app list.
Public game pages required sign-in. Local installed manifests, 456 cached app
records and partial per-account caches were not treated as complete ownership.
No inventory or Steam account identity is included in Git.
