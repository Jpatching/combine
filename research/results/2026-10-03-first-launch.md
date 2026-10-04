# First Windows attempt — 2026-10-03

Status: **partial; owner reports Minecraft worked; possible freeze unresolved.**
Skating is now the priority but required Skate 3 files are not established.
This records the preparation originally started for C-003a; it is not a passed
MW2/Skate or Minecraft/Skate recipe.

## Identity and conditions

- Upstream: v0.4.0, commit `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
- [Archive source](https://github.com/chasmlol/2010-rust-rewrite-mashup/releases/download/v0.4.0/2010-Rust-Rewrite-Mashup-windows-x64.zip).
- Locally computed SHA-256 (Linux and Windows agree):
  `f7c02cfb4dd5650be29762947a0b17d3e6f9b9f1259025ee89a99bd031e1ebca`.
- Size: 70,231,384 bytes. ZIP: 13 entries, 144,908,798 uncompressed bytes.
- Windows 11 Pro 10.0.26200, build 26200; AMD Ryzen 7 3800X;
  34,281,648,128 reported RAM bytes; NVIDIA GeForce RTX 5060 Ti,
  driver 32.0.16.1714. Recorded using Windows CIM queries.
- MW2 Multiplayer: Steam manifest app 10190, build 25374019, StateFlags 4;
  BytesDownloaded = BytesToDownload = 12,053,579,952. `iw4mp.exe`,
  `zone/english/common_mp.ff` and `zone/english/mp_rust.ff` present.
- Controller, graphics settings, bot count and precise gameplay actions: unrecorded.
- No new source build; existing two skating recipes remain unverified.

## Preparation and observations

| Check | Result | Evidence |
| --- | --- | --- |
| Archive identity | Pass | SHA-256 and size computed against research/upstream.lock.json before extraction/execution |
| Isolated trial | Pass | Fresh `%LOCALAPPDATA%\CombinePilot\v0.4.0\mw2-only`; executable in nested `2010-Rust-Rewrite-Mashup` folder |
| Original MW2 before inventory | Captured | 178 files; 12,101,823,987 bytes; complete relative-path/size/SHA-256 inventory in ignored `.private/c003a/mw2-before.json` |
| Windows launch | Process started | `Start-Process` with executable directory as working directory; PID 39872 at 2026-10-03T14:36:13.8561460Z |
| Minecraft first play | Owner-reported success | Owner said Minecraft worked; no duration or specific actions recorded |
| Possible freeze | Needs reproduction | Owner believes it froze; exact stage, duration, recovery and cause unknown |
| Minecraft preparation | Checked in follow-up | 26.3 completion marker present; pinned metadata/client SHA-1 and metadata-declared index SHA-1 match; four catalogs and pack paths present. Extracted resources not individually rehashed |
| MW2 ten-minute Rust test | Not tested | Owner prioritised skating before this acceptance sequence |
| Skate conversion and play | Blocked | No suitable local Skate 3 files established; controller not confirmed |
| Replay/offline replay | Not tested | No reported evidence |
| Original-file preservation after session | Not verified | Before manifest exists; after comparison pending exit and stable filesystem access |
| Cross-machine exchange / full failure matrix | Not tested | Outside this first attempt |

Original inventory capture took 154.92 seconds. Download, extraction and launch
succeeded, but end-to-end player setup and gameplay times were not measured. Do not
substitute assistant/tool waiting time for player setup time.

## Friction, limits and next action

Observed owner confusion: issue codes, current readiness, whether the folder name
excluded Minecraft, and the next action. The backlog now uses player outcomes and
smaller checkpoints. Product UI remains a proposal.

The original folder name `mw2-only` described a planned test, not a runtime feature
restriction. Minecraft is bundled as an integrated mode; the game may prepare its
content even during MW2 setup. No automatic update or Skate converter was invoked
by the assistant. What the owner selected in the setup dialogs is not yet recorded.

Next: establish access to legitimate extracted Skate 3 Xbox 360 files and a controller
before preparing a separate skating trial. Preserve this trial to investigate the
possible freeze; do not overwrite its settings or claim a diagnosed fault.
No files were purchased, published or shared; no original game data was uploaded.
Raw paths, game bytes and manifests remain local. Redaction reviewed: yes.


## Readiness follow-up — 2026-10-03

Filesystem access subsequently worked. Existing trial settings record skating off;
converter executable exists but converted `skate-data/assets/private/skater.glb`
does not. No files/settings were changed by these checks. A targeted Downloads
filename search found no candidate Skate files; other locations were not exhaustively
searched. Windows device-name query found a virtual gamepad bus, not evidence of a
working controller. Controller input remains untested. Minecraft preparation checks
above supersede the earlier incomplete cache inspection; the possible freeze and
source-preservation after comparison remain unresolved.
