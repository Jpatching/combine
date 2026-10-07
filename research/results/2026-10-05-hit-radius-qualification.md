# Hit-radius qualification — initial source trace, 2026-10-05

Purpose: identify the authoritative seams for the D-013/D-019 near-pass slice
inside actual Synergy. This is source-inspected evidence, not a feasibility,
implementation, launch or gameplay result. Requirements and expected cases remain
in docs/TRICKSHOT_MENU.md; active progress belongs on the private board.

Runtime: `https://github.com/chasmlol/2010-rust-rewrite-mashup` at
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Local source checkout HEAD matches
that pin. `git show <pin>:<path>` byte comparisons match the five files below;
this excludes unrelated ignored runtime modifications from these observations.
Links use pinned public source; private logs/assets were not read or uploaded.

| Question | Source-inspected evidence | Remaining qualification |
| --- | --- | --- |
| Accepted shots and range | [combat.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/sim/src/combat.rs), `phase_emit` (1040 onward) creates emissions with shot/pellet IDs, spread direction and weapon bullet range; `phase_trace` (1089 onward) obtains lag-compensated poses | Trace sniper classification, skating exclusion and private-session authority before enabling settings |
| Travel and penetration | [bullet_collision.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/sim/src/bullet_collision.rs), `BulletTraceSegment` (882), `bullet_trace_segments_filtered` (1505), `fire_extended`/`fire_penetrate` carry start/end, damage multiplier, exit flag and collider | Classify forward reachable intervals versus exit/reverse bookkeeping; reject invalid/start-solid/exhausted travel; prove target-side cover independently of centreline reach |
| Normal body volume | Same file: `PlayerCollisionPose` (934); player trace loop (1305 onward) uses collision-bone oriented boxes when present, otherwise the pose AABB | Match distance computation to exactly this authoritative representation; shield bones must not become damageable body assistance. Confirm actual pose producers, stance and history behavior |
| Units | [skate/collision.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs) converts runtime coordinates to Skate using 0.0254 and axis remapping | Evidence supports inches-to-metres conversion; prove the same units at shot/body boundaries with calibrated geometry before setting radius |
| Damage ordering | `combat.rs` (1259 onward) computes range damage times segment multiplier and sends player hits through `apply_damage_attempt`; [bullet.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/sim/src/bullet.rs) owns range falloff; [damage.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/sim/src/damage.rs), `apply_damage_attempt` (687) checks living/current life and applies hit-location scale before script damage | Trace script damage/team/God Mode behavior, upper-body hitloc, lethal One-shot amount and deduplication across all emissions/ricochets of a shot. Preserve any direct hit/collateral without an extra assist |
| Menu setting seam | Our `patches/synergy-gsc-v0.4.0.patch` embeds the original source in `crates/session/src/synergy/Synergy.gsc`; input patch redirects its input manager | Qualify a typed GSC-to-authoritative-simulation setting operation with acknowledgements, private-only enforcement, match reset and failure feedback. A menu label is not activation evidence |

```text
Accepted shot -> lag-compensated trace -> ordinary direct hits/collaterals
                                       | any direct hit -> no assistance
                                       | otherwise miss
                                       v
Reachable forward intervals + body gap + target-side cover + session eligibility
      | absent/invalid capability -> explicit blocker; leave assistance Off
      | qualified -> closest eligible body -> one authoritative damage attempt
```

A reachable centreline beside a wall does not prove a shielded nearby target is
reachable. Next concrete check: inspect `fire_penetrate` interval construction and
player pose producers, then establish a side-cover qualification using existing
collision/penetration queries without mutating glass or duplicating normal damage.
If these APIs cannot supply the required witness, record that precise missing
capability rather than substituting final-impact distance. No hard blocker has
been proven yet; these are unresolved integration checks.

Rainy qualification is inherited from the owner-supplied plan: preceding source
inspection reported IW4x/Bot Warfare dependencies and unsupported function
replacement. No Rainy source revision/evidence file was found in the existing
tracked evidence index in this session, so that conclusion is recorded as a
reported prior finding, not independently reproduced source inspection. Rainy
has not been installed, launched or gameplay-tested and is outside this slice.
