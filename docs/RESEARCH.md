# Research record — 2026-10-03

## Assessment

A supported mashup catalogue is technically plausible because an existing runtime
already integrates the candidate systems. Demand for configuring and sharing these
combinations, their maintenance cost, and a commercial distribution path are unproven.
The next useful evidence is an observed Windows baseline and user setup sessions.

Evidence labels: **documented** = publisher/maintainer statement; **inspected** =
source or metadata examined; **reproduced** = observed execution with recorded
conditions; **hypothesis** = proposed explanation/product value. No gameplay is yet
reproduced. Online descriptions are not proof of runtime fidelity or legal clearance.

## Pinned candidate

- Repository: [2010 Rust Rewrite Mashup](https://github.com/chasmlol/2010-rust-rewrite-mashup).
- Source: `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, dated 2026-10-02.
- [Release v0.4.0](https://github.com/chasmlol/2010-rust-rewrite-mashup/releases/tag/v0.4.0), published 2026-10-02 02:28:19 UTC.
- Source fetched with Git; HEAD and the release tag independently resolved to the
  same full commit. Fifteen inspected source files have hashes in the
  [lock](../research/upstream.lock.json). No upstream code is copied into this repo.
- Release metadata advertises a 70,231,384-byte Windows ZIP and SHA-256
  `f7c02cfb4dd5650be29762947a0b17d3e6f9b9f1259025ee89a99bd031e1ebca`.
  This is publisher metadata, not a hash computed from downloaded archive bytes.
- No archive has been executed and no source build has been attempted here.

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

## Skate acquisition follow-up — 2026-10-03

The owner confirms they do not own Skate 3 and is downloading MW2. The [official
Xbox listing](https://www.xbox.com/en-GB/games/store/skate-3/BNKDKQXMXRR2) advertises
Xbox One, Series X|S and cloud play. It does not establish a PC download yielding
the extracted Xbox 360 files required by this runtime. No suitable official extracted
asset download was verified, and no Skate game was downloaded or purchased. Do not
recommend a purchase solely for this pilot without establishing a usable acquisition
route. C-003a can establish a partial MW2-only baseline while skating remains blocked.
