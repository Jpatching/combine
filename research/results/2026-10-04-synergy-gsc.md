# Actual Synergy GSC integration — 2026-10-04

The owner confirmed Synergy itself. The integration executes the pinned MW2 GSC
through the mashup's existing compiler, simulation and HUD. An automated Windows
diagnostic observed its HUD creation, open, root → Weapon Options → Give Weapons
→ Sniper Rifles navigation, Intervention equip/hold, back and close. An offline
script error remains. This is implementation evidence, not owner acceptance.

## Source

Apply `patches/synergy-gsc-v0.4.0.patch` after menu, audio and Intervention.
Base source: `730b11354934b43c2ca703aec615ea31d3e77f2e`; runtime pin:
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`.

The patch embeds unchanged [Synergy MW2 source](https://github.com/SyndiShanX/Synergy-GSC-Menu/blob/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2/Synergy/maps/mp/Synergy.gsc),
SHA-256 `2c7be615f2e435c34ad7e1ee4bc9d1b1682ff08b909dea911abc6819e4a484d9`.
The session crate declares GPL-3.0-only; attribution and the complete existing
licence are preserved. No retail scripts or assets are embedded.

`COMBINE_SYNERGY_GSC=1` overlays that one module and starts its connection
watcher before admitting players. Our native panel is disabled in this mode.
`isarray` is added to the IW4 compiler catalogue using its existing native
implementation. This is not a generic mod discovery/loader feature.

`COMBINE_SYNERGY_GSC_PROBE=1` adds an authored diagnostic observer. It reads
Synergy state and logs booleans, fixed page identifiers and cursor positions.
It does not create a menu, change menu state or equip a weapon. Ordinary timed
button commands drive the original script's input manager.

## Observations

1. A compile-only probe parsed the whole menu and enumerated fourteen imported
   helper symbols using placeholder modules. This established syntax and
   dependencies only; it was not treated as runtime support.
2. First Windows diagnostic executable SHA-256:
   `b616025547b7497d713a6beb8f92213589bc5987a53e1e19a4c443bfed00616f`.
   Rust map scripts installed: 273 modules, 2,938 functions, 463 natives, four
   startup entries. No script fault was found during that bounded observation.
   The diagnostic closed its own process; no interaction was established.
3. Interaction diagnostic executable SHA-256:
   `2a015528530f3d8d5fcfc69d9ac515a0d09a604fa8102114468600e4c8277a2f`.
   Actual script HUD creation, open, all three hierarchy transitions, Intervention
   inventory presence then held-weapon state, back and close were observed. The
   process ended after scripted quit; its exit code was not captured reliably.

The interaction run also reported:

```text
maps/mp/_matchdata:10:3 in init:
setmatchdatadef: unavailable: IW4 definition schemas are not supported by the local match-data store
```

Synergy `init` sets `level.rankedmatch = 1`; whether that enables this unsupported
offline statistics path requires controlled reproduction. Do not suppress the
error or mark the check passed. Input leakage, firing, relaunch, controller input,
720p/1080p presentation and remaining options are unverified. No corrected owner
review bundle exists. Diagnostic copies preserve earlier trials and originals.

Build command with the previously recorded pinned Windows toolchain:

```sh
cargo +1.95.0 xwin build --offline --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l
```

Both builds passed with inherited render/skate warnings. The second took 14.97
seconds from the warm cache. It preceded the source notice/licence declaration
edit; no executable behavior changed in that edit. Raw manifests, logs and
commands remain local under `.private/synergy/`.

## Review and next check

Standards review: explicit source list, unchanged menu bytes, licence/notices
preserved, isolated opt-in behavior. The checkpoint is intentionally incomplete.
Spec review: actual menu execution and Intervention path observed; offline error
and missing input/recovery evidence prevent the owner handoff. Both reviews were
performed by the lead; no independent subagent review is claimed.

Next: reproduce and fix the offline error, verify input isolation and the
Intervention flow, then prepare the exact-build owner trial.
