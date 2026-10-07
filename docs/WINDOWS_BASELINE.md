# Windows baseline — C-003

This procedure tests the upstream runtime on the owner's Windows PC. “C-003” is
just the backlog reference for that test, not a player-facing product name.
Windows PowerShell is accessible through WSL with sandbox approval. Human observation
is needed for gameplay; successful commands do not establish playable behaviour.

**Current priority: skating on Rust.** MW2 Multiplayer is installed, the v0.4.0
archive was verified and a separate trial launched. The owner reports Minecraft
worked and a possible freeze. See [the result](../research/results/2026-10-03-first-launch.md)
and [retained evidence](HANDOFF.md) before repeating any preparation.

**IW4x is not required.** The pinned release includes the skating integration and
converter. It still needs the player's Skate 3 Xbox 360 `default.xex` and accompanying
`data` folder, plus a controller. A standalone engine or store DLC is not that data.

## Resume the prepared skating trial

Preparation is complete in `%LOCALAPPDATA%\CombinePilot\v0.4.0\mw2-skate`,
inside `2010-Rust-Rewrite-Mashup`. The converter passed and its process was launched;
DualSense is detected over Bluetooth. See the
[preparation evidence](../research/results/2026-10-03-skating-preparation.md).
Game-data distribution provenance remains unresolved.

1. In the launched trial, choose Create Game → Rust, then press **J**.
2. Use the DualSense to move/turn and attempt a trick. Record board visibility,
   collision, controller response and any freeze/error.
3. Test ten on/off transitions, recovery and ten minutes of play; exit and relaunch.
4. Compare original MW2 files after exit. Then decide whether to test Minecraft
   skating or investigate a reproducible failure. Do not repeat extraction first.

## Runtime preparation and evidence

These are upstream functions at the selected revision, not code we implemented.
Our ignored `.private/c003b/prepare-skating.ps1` only orchestrates local preparation.

| Step | Reference | Evidence |
| --- | --- | --- |
| Convert extracted Xbox inputs into runtime assets | [Converter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/converter/iw4l_skate_convert.py), `convert()` | Adapts original data to the mashup; exit code 0 and four required outputs verified |
| Read configured paths and prepare board assets | [First run](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/launcher/src/first_run.rs), `prepare()` | Connects converted assets to startup; board.json and rig.json found after launch |
| Translate controller input and update skating | [Skating adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs), `pad_frame()`, `update()`, `preload_map()` | Connects controller, simulation and world; source inspected, human movement/collision checks still pending |

```text
Xbox files -> converter -> runtime assets -> launcher -> controller + world -> skating
 missing      fails          missing         fails       no response        observe
    +------------+--------------+--------------+--------------+-> record exact stage
```

Each stage has a different check. A successful converter proves preparation, while
moving and colliding correctly in Rust supplies gameplay evidence. Trace one stage
at a time when learning or diagnosing a failure.

The prior MW2-only on-foot ten-minute test is deferred at the owner's request.
Minecraft first-play success is owner-reported; replay, session duration and the
possible freeze still need a recorded test. Keep those observations separate from
skating acceptance. Do not mark either skating recipe complete yet.

## Prerequisites and boundaries

- A legitimate local MW2 (2009) Steam installation including Multiplayer files.
- For both skating recipes, extracted Skate 3 Xbox 360 content: `default.xex` and
  its accompanying `data` folder. An ISO alone is not the mashup's documented input.
- A controller; the current trial uses a detected DualSense. Record actual input results.
- Internet for upstream first-run content downloads. Read C-006 in the research
  record before deciding whether to run the content downloader. This runbook is not
  permission to acquire files or bypass protection.
- A dedicated writable folder outside either game's installation. Leave ordinary
  saves and installs untouched. Do not connect to public multiplayer servers.
- Read the [release notes](https://github.com/chasmlol/2010-rust-rewrite-mashup/releases/tag/v0.4.0).
  Record Windows version, GPU/driver, CPU, RAM, controller, game editions and date.

Stop and record `blocked` if prerequisites are missing. Do not buy games, obtain
third-party game archives or make up results to finish the checklist.

## 1. Verify the exact archive

Download **2010-Rust-Rewrite-Mashup-windows-x64.zip** from the explicit v0.4.0 release
page above. Do not use `/latest` or a rehost. From PowerShell at this repo's root:

```powershell
$baseline = Get-Content -Raw 'research/upstream.lock.json' | ConvertFrom-Json
$archivePath = Join-Path $env:USERPROFILE ('Downloads\' + $baseline.runtime.asset.name)
$actualHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actualHash -ne $baseline.runtime.asset.sha256) { throw 'Archive checksum mismatch; stop.' }
if ((Get-Item -LiteralPath $archivePath).Length -ne $baseline.runtime.asset.size_bytes) { throw 'Archive size mismatch; stop.' }
$actualHash
```

If saved elsewhere, change only `$archivePath`. Record the resulting hash in the
baseline report. A matching publisher hash establishes archive identity, not safety,
rights clearance, or reproducibility of its build from source. Do not disable security
software if it blocks execution; record the exact warning and stop for investigation.

## 2. Prepare the current trial in a separate folder

```powershell
$pilotRoot = Join-Path $env:LOCALAPPDATA 'CombinePilot\v0.4.0'
# Prepare only the current trial; use 'minecraft-skate' for the later test.
foreach ($trialName in @('mw2-skate')) {
    $trialDir = Join-Path $pilotRoot $trialName
    if (Test-Path -LiteralPath $trialDir) { throw 'Trial folder already exists; use a fresh named trial.' }
    Expand-Archive -LiteralPath $archivePath -DestinationPath $trialDir
}
```

If an existing folder causes a stop, choose a new `$pilotRoot`; do not overwrite old
evidence. Locate `iw4l.exe` inside each extracted folder. Keep its bundled converter
and notices together. Record archive layout differences rather than guessing paths.
Do not invoke an updater. Existing runtime `.env` files may contain personal paths;
keep them local and never include them in recipe exchange.

Before launch, capture a complete local-only inventory and SHA-256 manifest of the
original game folders; compare file additions, removals and changed hashes after
exit. Stop and record a blocker if capture fails. The first MW2 manifest is already
in ignored `.private/c003a/mw2-before.json`; it covers 178 files. A before manifest
alone does not prove preservation; record the after comparison explicitly.

## 3. Establish prerequisites independently of gameplay

Launch the first trial's `iw4l.exe` manually. Confirm the MW2 folder; select the
extracted Skate file when requested. Record every prompt, retry and conversion
duration. Upstream may start Minecraft data downloads during initial startup even
when the first selected world is MW2. Record network/content preparation time separately.

For the later Minecraft skating test, repeat setup in a second trial if needed, preserving isolation. Record the duplicate
conversion cost as a possible usability problem, not an assumed opportunity.
Do not edit implementation files or add undocumented settings to make a test pass.

## 4. Exercise the candidates (30 minutes total)

| Stage | Task | Evidence |
| --- | --- | --- |
| Minutes 0–10: MW2/Skate | Select Rust in Create Game. Move, aim/fire and exercise available local combat. Press J to enter/leave skating ten times. Move over edges, attempt a grind and recover after a fall/death when possible. | Record actual map, bot count, input model, failed transitions, board visibility and frame-time/FPS observations if an existing counter is available. |
| Minutes 10–25: Minecraft/MW2/Skate | In the second trial select Minecraft → overworld. Move, shoot mobs and blocks, place/break blocks, use inventory. Skate across changed terrain, try an edge grind, then return to shooting. | Record stale collision, stuck input, visual errors, crashes and reproducible steps. |
| Minutes 25–30: replay | Exit and relaunch both trials without changing versions. Repeat world selection and one skating transition. If content preparation completed, test offline replay separately. | Record setup prompts recurring, missing content, unexpected network dependency and successful/failed replay. |

If the time is consumed by errors, record that honestly and schedule a separate
retest; do not count troubleshooting as thirty minutes of gameplay. If a feature
cannot be triggered, label it `not tested`, not `pass`.

For recipe exchange, give only a JSON recipe and this runbook to another eligible
tester. They must independently select the same world and modes on the pinned
runtime. A second machine is required before claiming cross-machine reproduction.
The runtime does not load Combine JSON directly.

## 5. Failure matrix

Use disposable trial folders, never corrupt or delete original game data.

| Scenario | Expected observation / acceptance |
| --- | --- |
| Wrong or missing MW2 folder | Clear correction request; cannot be reported as ready |
| Skate skipped/cancelled or files unavailable | Record upstream behaviour; both skating recipes remain unmet even if on-foot play works |
| Network unavailable during first preparation | Record error/retry behaviour; never mark preparation complete on partial data |
| Interrupted download/conversion | Close the trial during preparation, preserve logs, restart; record whether recovery succeeds or needs a fresh trial |
| Wrong archive/version | Stop before execution; record mismatch instead of substituting latest |
| No controller or alternate controller | Record effect separately from runtime crash; supported devices remain unverified until exercised |
| Crash or stuck skating after mode change/death | Save redacted reproduction and exact version; compare with inherited release claims |
| Original installation changed | Stop trial and investigate; do not restore/delete automatically |

The current checker only covers recipe input failures. Runtime behaviours in this
matrix are acceptance targets to measure, not behaviours Combine has implemented.

## 6. Record and hand off

Copy [the result template](../templates/baseline-result.md) into ignored `.private/`
for raw notes. Put only a manually redacted report under `research/results/` when
ready; include no usernames, absolute private paths, game files, tokens or participant
identities. Update C-003 with pass/partial/fail/blocked and evidence location.

Acceptance: verified archive identity, actual hardware/build details, both candidate
results, thirty minutes of gameplay observations, failure cases, original-file
preservation evidence or its explicit limitation, and remaining uncertainty. First
successful local play is not owner acceptance, business validation or public release.
