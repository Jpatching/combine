# Research record — 2026-10-03

## Assessment

A supported mashup catalogue is technically plausible because an existing runtime
already integrates the candidate systems. Demand for configuring and sharing these
combinations, their maintenance cost, and a commercial distribution path are unproven.
The next useful evidence is an observed Windows baseline and user setup sessions.

Evidence labels: **documented** = publisher/maintainer statement; **inspected** =
source or metadata examined; **reproduced** = observed execution with recorded
conditions; **hypothesis** = proposed explanation/product value. Minecraft play is now owner-reported; skating, replay and stability remain
unverified. Online descriptions are not proof of runtime fidelity or legal clearance.

## Pinned candidate

- Repository: [2010 Rust Rewrite Mashup](https://github.com/chasmlol/2010-rust-rewrite-mashup).
- Source: `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, dated 2026-10-02.
- [Release v0.4.0](https://github.com/chasmlol/2010-rust-rewrite-mashup/releases/tag/v0.4.0), published 2026-10-02 02:28:19 UTC.
- Source fetched with Git; HEAD and the release tag independently resolved to the
  same full commit. Fifteen inspected source files have hashes in the
  [lock](../research/upstream.lock.json). No upstream code is copied into this repo.
- Release metadata advertises a 70,231,384-byte Windows ZIP and SHA-256
  `f7c02cfb4dd5650be29762947a0b17d3e6f9b9f1259025ee89a99bd031e1ebca`.
  These values were subsequently matched by local Linux and Windows hash/size checks
  on 2026-10-03; see [first attempt](../research/results/2026-10-03-first-launch.md).
- The verified archive was launched on Windows on 2026-10-03. No source build
  has been attempted; process launch alone does not establish gameplay.

Sources: [release API](https://api.github.com/repos/chasmlol/2010-rust-rewrite-mashup/releases/tags/v0.4.0),
[exact source tree](https://github.com/chasmlol/2010-rust-rewrite-mashup/tree/f608f85e407ff1b7689d54a9aafdd16e95711ac4).
Record future refresh dates without silently changing this baseline.

## How this combination works

```text
Local MW2 assets --------> IW4L world/rendering/combat
                                   ^       |
Local Skate assets -> converter -> skating worker
                                   |       ^
                            pose / input / collision bridge
                                   |
MinecraftOSS + downloaded data -> voxel world and changing collision
```

The inspected adapter feeds map collision and input into a skating simulation,
receives poses, and maps them back into the host. Voxel collision is rebuilt as the
player moves or blocks change. That is bespoke integration, not arbitrary executable
merging. [Pinned adapter source](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs)

| Finding | Evidence and consequence |
| --- | --- |
| IW4x and IW4L are different projects | Documented: [IW4x](https://github.com/IW4x/iw4x-client) extends MW2; [IW4L](https://github.com/vladtrc/iw4L) is an experimental reimplementation. Do not describe the pilot as an IW4x mod. |
| Upstream already has a setup wizard | Inspected: [first_run.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/launcher/src/first_run.rs) locates MW2, invokes the Skate converter and writes local settings. A wrapper needs demonstrated additional value. |
| First-run content acquisition is part of the runtime | Inspected: [minecraft_setup.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/minecraft_setup.rs) downloads versioned content using curl, checks hashes and stages files. Do not promise a network-free first launch, even for a MW2 test. |
| Prior research matters | Documented: [Skate engine history](https://github.com/SK8-ENGINE/skate-3-rust-engine) credits years of reverse engineering and describes incomplete parity. AI usage does not demonstrate universal conversion. |
| Embedded revisions need provenance follow-up | Inspected: Skate files name short revision cb79689; MinecraftOSS names 4013a68. The containing commit pins the bytes, but the original full revisions and MinecraftOSS origin URL are not verified. |

## Contradictions and inherited limitations

- The pinned skating guide still lists bodies accumulating after death; v0.4.0
  release notes report that fixed. Test it rather than treating either as observed.
- That guide asks for an Xbox/XInput controller, while v0.3.2 release notes report
  other controller support. Prefer an XInput controller for the first comparison;
  test other devices separately. See [v0.3.2 notes](https://github.com/chasmlol/2010-rust-rewrite-mashup/releases/tag/v0.3.2).
- v0.4.0 reports invisible boards on some maps and lower bot-match frame rates than
  v0.2.0. Neither has been measured here; record them as inherited candidate defects.
- The build guide says the toolchain is pinned, but the inspected file selects
  `stable`. A future source-build report must record the exact Rust version.
- The portable Windows guide describes generic IW4L packaging; use the mashup release
  instructions for this baseline. Do not mix its updater with a pinned trial.

## Alternatives and traction

| Alternative | Established capability | Hypothesis to test for Combine |
| --- | --- | --- |
| [Wabbajack](https://github.com/wabbajack-tools/wabbajack) | Reproduces curated mod setups | Cross-game settings and compatibility might add value beyond installation |
| [Nexus Collections](https://help.nexusmods.com/article/115-guidelines-for-collections) | Curated collections installed through Vortex | Players may want shareable gameplay combinations, but a catalogue alone is not differentiation |
| [s&box](https://sbox.game/dev/doc) | Tools for creating and publishing games | Simpler supported configuration may suit players who do not want to develop games |
| The mashup's own wizard | Existing discovery/conversion/launch flow | Measure where it fails ordinary users before replacing any part |

Working acquisition hypothesis: compelling gameplay -> clear prerequisites -> successful
first session -> shared recipe -> repeat play. No traffic, conversion, retention or
revenue was measured. Creator interviews should establish willingness to maintain
integrations; player enthusiasm alone does not solve the supply side.

## Rights/provenance questions (C-006)

This is an evidence checklist, not legal clearance. No public distribution is approved.

| Material | Evidence now | Required resolution before proposed distribution |
| --- | --- | --- |
| Host runtime | Root Apache-2.0 text inspected | Inventory redistributed files/dependencies and preserve required notices |
| Skate code and converter | Imported source present; guide mentions converter-specific licences | Inspect actual converter bundle, origin revisions and applicable licence terms; do not infer coverage from root licence alone |
| MinecraftOSS | Vendored files and short origin revision present | Establish origin and applicable source licence/provenance |
| Fonts | NOTICE identifies embedded font notices | Confirm release carries the required licence texts |
| MW2/Skate assets | Runtime expects local user data | Assess publisher terms, extraction/use and any proposed distribution separately; do not host game data |
| Minecraft content | Downloader code inspected | Assess this use and any commercial service against current EULA/usage guidelines; official hosting is not blanket permission |
| Branding, clips and user uploads | No permission evidence collected | Establish permitted marketing and sharing policy for the intended public pilot |

Sources: [pinned NOTICE](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/NOTICE),
[Minecraft EULA](https://www.minecraft.net/en-us/eula).
Publisher terms can change; refresh the applicable sources before making a release
decision. If affordable rights cannot be established, evaluate original/licensed
content as a different pilot rather than silently changing the promise.

## Skate acquisition follow-up — 2026-10-03 (historical; superseded)

The owner previously confirmed they do not own Skate 3. MW2 Multiplayer is now
confirmed installed. Skating became the immediate priority on 2026-10-03. The [official
Xbox listing](https://www.xbox.com/en-GB/games/store/skate-3/BNKDKQXMXRR2) advertises
Xbox One, Series X|S and cloud play. It does not establish a PC download yielding
the extracted Xbox 360 files required by this runtime. No suitable official extracted
asset download was verified, and no Skate game was downloaded or purchased. Do not
recommend a purchase solely for this pilot without establishing a usable acquisition
route. C-003a can establish a partial MW2-only baseline while skating remains blocked.


## How skating and AI fit together — 2026-10-03

The mashup retains IW4L for rendering and the match. Its adapter sends map collision
and controller input into a skating simulation worker, then maps the returned pose
onto the soldier. The collision adapter changes axes and units; grindable map edges
become rails. Setup converts the player's Skate data into the model, animation and
configuration data used by that simulation. Missing assets block this route.

```text
Owned Skate files -> converter -> skating simulation
                                      ^       |
MW2 map collision + controller -------+       v
                                    pose -> MW2 soldier/rendering
```

This bridge lets one simulation operate in another game's map. It does not combine
arbitrary retail executables. Sources at the selected mashup commit:
[skating guide](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/docs/SKATE.md),
[inspected adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate.rs),
[collision conversion](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs).

The Skate engine authors say AI coding tools helped turn prior research into the
Rust/Bevy implementation. They credit more than two years of reverse engineering
and tools by dumbad. Their README does not quantify a speedup or supply a complete
prompt/model/workflow record. Therefore “AI massively sped it up” remains an
unquantified claim, not our measurement. Reusing established engines, known formats
and tools is a plausible accelerator; the amount attributable to AI is unknown.
[Author account at 7ae67f269c024ed0b1aa945701e04fa5bf419848](https://github.com/SK8-ENGINE/skate-3-rust-engine/blob/7ae67f269c024ed0b1aa945701e04fa5bf419848/README.md)
(the documentation revision observed today, not a replacement for vendored cb79689).

For acquisition, the pinned mashup guide expects an already extracted Xbox 360
base game. A disc-image extraction tool processes an existing image; the guide does
not establish how this owner's PC would read a retail disc. The current Xbox store
lists console/cloud play, not an extracted PC asset download. Establish the owner's
copy/backup and hardware first; do not recommend a purchase based only on that listing.
No asset source or extraction route has been verified for this owner.


## Free-content search and readiness follow-up — 2026-10-03 (historical; superseded)

**Result: no verified compatible free Skate asset package acquired.** This does not
mean free listings do not exist. Searches found third-party full-game/XEX listings,
but their pages/downloads could not be validated with the browsing tool. No game
archive from those listings was downloaded or executed, and no distribution-rights
claim is made. Distinguish advertised availability, obtainable bytes, compatibility
and authorization rather than treating any one as evidence for all four.

- **Official free demo:** [Xbox's 2010 announcement](https://news.xbox.com/en-us/2010/04/15/demo-skate-3/)
  confirms that a free demo existed. Its Marketplace link could not be retrieved.
  [Xbox's closure announcement](https://news.xbox.com/en-us/2023/08/17/xbox-360-store-will-close-july-2024/)
  explains the old store/Marketplace changes from 2024-07-29. Neither establishes
  a currently obtainable PC package or compatibility with the pinned converter.
  No demo compatibility evidence was found in the targeted project searches.
- **Owner's lead, [mchughalex/skate3recomp](https://github.com/mchughalex/skate3recomp):**
  its README explicitly excludes retail game files and asks the user to select an
  existing ISO. This is a standalone native recompilation with an extraction flow,
  not a source of the base game and not the skating engine integrated into IW4L.
  HEAD observed with `git ls-remote`: `f6e0ae87fdfecbadb5c1e36c55d66a744187a3cd`.
  README inspected through the current main URL; fetching the revision URL through
  the browser failed. No release downloaded, built or executed; extraction output
  compatibility with our converter is untested. Keep the existing mashup baseline.
- **Exact converter input, source-inspected at the selected mashup commit:**
  `default.xex`, `data/big/miscload.big`, `data/big/miscboot.big`,
  `data/big/db.big`, and `data/content/createacharacter.big` are required by the
  initial checks. Presence is necessary, not sufficient: conversion can still fail.
  [Converter source](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/converter/iw4l_skate_convert.py)
- **Local checks:** runtime/converter present; trial configuration has skating off;
  converted `skater.glb` absent. Targeted filename search in the Windows Downloads
  folder found no Skate-named downloads or required input files (not a whole-PC scan).
  Windows device-name inspection found only a virtual gamepad emulation bus among
  matching names; that does not confirm a connected working controller.
- **Minecraft:** the 26.3 completion marker, pinned metadata/client SHA-1 values and
  metadata-declared asset-index SHA-1 match. Four catalogs and pack paths exist.
  Individual extracted assets were not rehashed; stability/replay remain unverified.

Next: inspect a legitimately obtained candidate's required files before running the
bundled converter in a fresh trial. A demo remains an unproven candidate, not a
recommended substitute. No purchase is recommended until content access is established.

## Learning while using a coding agent — 2026-10-03

Keep the existing small-slice, what/where/why and verification approach. Add active
practice selectively: predict one behavior, explain a function in your own words,
or make a small change and inspect the test result. This is a recommendation for
our workflow, not a proven optimal curriculum; no new learning tracker is needed.

- [Shen and Tamkin, How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245)
  studied developers learning an unfamiliar Python library. The authors report
  lower immediate quiz scores with AI assistance; this does not establish long-term
  effects or directly evaluate our Codex workflow. Their interaction-pattern analysis
  associates conceptual inquiry/explanation with stronger scores, without establishing
  causality between those patterns and learning.
- [Karpicke and Blunt, 2011](https://pubmed.ncbi.nlm.nih.gov/21252317/) found benefits
  from retrieving knowledge over concept mapping for science-text learning.
  Applying that to a brief code explanation from memory is our inference.
- [Official Codex best practices](https://learn.chatgpt.com/guides/best-practices)
  recommends concise, practical instructions, clear task context and verification.
  Keep detailed project evidence in existing records rather than expanding global
  instructions for every task.

Current runtime learning example: follow the converter → launcher → controller
adapter in [the runbook](WINDOWS_BASELINE.md#trace-the-approach-what-where-and-why).
Local Xbox extraction/conversion now passed; this supersedes earlier missing-file
readiness findings. Human skating and replay remain pending, as recorded in the
[preparation report](../research/results/2026-10-03-skating-preparation.md).

## Bigger crossover ideas after the menu — 2026-10-03

Owner follow-up: the replacement retains the same options; asks about “EB” and
what larger addition could use their game library. No replacement acceptance was
given. The owner confirmed EB means explosive bullets; preferred games were requested.
No EB implementation or new integration started.

Primary-source documentation checked (not built, installed or gameplay-tested):

- [PipeLink Launcher](https://github.com/Sm1jjj/PipeLinkLauncher/blob/e0f3014889ad4acd7239e2d973dcab6da33c3fc1/README.md),
  main revision `e0f3014889ad4acd7239e2d973dcab6da33c3fc1` fetched via GitHub API.
  Creator describes Skate 3 and MW2 modes inside classic GTA San Andreas 1.0 US,
  using an ASI plugin, Skate bridge and IW4L-derived runtime. The launcher repo
  documents converters and an IW4L patch, but its build expects a separate mod
  project for native binaries. Source completeness and compatibility with our
  menu are unverified. Its setup modifies GTA files; do not run it on originals
  or invoke version-conversion tools without a separately reviewed trial plan.
- [GTA San AnSkateas](https://github.com/ryglizzy/GTA-San-AnSkateas): creator
  documents Skate physics/tricks on classic San Andreas streets. Separate
  plugin/bridge integration, not a drop-in map for our runtime. README inspected;
  exact revision not pinned because it is not selected as a baseline.
- [FalloutCraft](https://github.com/zeyvu/FalloutCraft): creator describes Minecraft
  movement/building/combat inside Fallout 4 via F4SE and a Fabric process. Early
  experimental project; a separate host integration, not evidence that Skate or
  our MW2 menu works there. README inspected; no selected baseline pin.

Recommendation for investigation if the owner owns compatible GTA: city-scale
skating and MW2 trickshot attempts in San Andreas. A launch/reset loop is our
proposed addition, not a claimed existing PipeLink feature. Keep the first fixed
on-foot launcher on Rust as the smallest separately testable step. A larger
Minecraft stunt arena can later reuse the selected runtime's documented block
building, bullet damage and grenade destruction; cross-mode acceptance still
needs observation. No binaries/assets downloaded or launched for this research.

## Current shortcut and conversion trace — 2026-10-04

The current **Combine Skate Audio** shortcut targets `skate-audio-dev/iw4l.exe`
with `map mp_rust`; its SHA-256 matches the recorded audio build
`2319178a836247efaff4b99852eebaf920e0697e1b894a7310739a0c06470807`.
Its working-directory configuration selects that trial's converted Skate assets.
All four converter-required outputs match the original `mw2-skate` conversion
byte-for-byte (SHA-256 comparisons). The preparation metadata records converter
exit 0, 41.53 seconds and required outputs present on October 3. Synergy and
older Trickshot shortcuts also remain, pointing to their recorded builds.

This traces today's audio shortcut to the previously converted Xbox data. It does
not establish demo versus full-game edition or distribution provenance. No edition
manifest was found at the assets root; do not infer edition from a folder name.
Earlier demo-acquisition and missing-input guidance above is superseded for this
prepared setup. Preserve the historical evidence and all local files; no new demo,
asset acquisition or reconversion is needed for Hide HUD. Private paths and raw
configuration remain outside Git; redacted trace is local under `.private/hide-hud`.
