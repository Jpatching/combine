# Synergy menu requirements, build and trial

The destination is the proper pinned Synergy menu plus **trickshot hit radius**,
without Combine-specific save/return, target practice, aim-lock/preset or stunt
launcher additions. Existing patches and trials are preserved as earlier work.
They do not establish feature parity or acceptance of this destination.

The [source coverage record](../research/results/2026-10-04-menu-coverage.md)
rechecks the inventory and preserves earlier source coverage. Hide HUD
is deferred and is not an active slice or prerequisite.

## Owner correction — use Synergy itself, October 4

The owner explicitly confirmed **Synergy itself** after rejecting the custom
native menu previews. The pinned GSC source must drive the menu's appearance,
navigation and options. Changing the labels or restyling our practice menu does
not satisfy that request. Use the existing runtime script engine to establish
compatibility with Synergy's IW4x requirements; do not assume copying the mod
folder is enough. The [Synergy decision](adr/0002-execute-pinned-synergy.md) records this correction.

Earlier native menu patches remain available for reproduction; the requested
replacement is actual Synergy.
The original integration checkpoint was opening actual Synergy, navigating
to Intervention and equipping it; its automated evidence is preserved. The full menu destination and agreed hit-radius
requirements remain; individual options need execution evidence before claiming
support. The owner reports Intervention worked in the most recent trial, with other
options missing; exact-build acceptance is not recorded. See the
[reference build identities](REPRODUCING.md#preserved-synergy-reference-build).

## Actual Synergy input build — October 5

Apply the five source patches in order to runtime
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`: trickshot, skate-audio,
Intervention, synergy-gsc, then synergy-input. Do not apply deferred Hide HUD.
The last patch redirects only the original GSC input manager and reports capture
state; the embedded pinned menu bytes, presentation and option actions remain
Synergy's. It blocks gameplay commands and stale button history through the
neutral release frame. New physical input after release resumes ordinary play.

Build with Rust 1.95.0, cargo-xwin 0.23.1, Clang/LLVM 19.1.1 and rust-lld,
using the existing Windows SDK/CRT cache and unchanged Cargo.lock:

```sh
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p launcher --bin iw4l
cargo +1.95.0 xwin test --locked --profile play --target x86_64-pc-windows-msvc -p sim -p console --lib --no-run
```
Run sim with `synergy` and console with `practice` on Windows. These cover scripted open/close, held Fire, keyboard/pad
capture, skating shortcuts, focus/reconnect and fresh input. They are synthetic
integration evidence, separate from owner gameplay.

The reproducible bounded diagnostic uses a fresh copy and quits its own process:

```powershell
.\scripts\run-synergy-diagnostic.ps1 -Source '<prepared runtime>' `
  -Binary '<exact iw4l.exe>' -Destination '<new diagnostic runtime>' `
  -Report '<new private report.json>' -Resolution '1920x1080'
py -3 scripts/check-synergy-diagnostic.py '<private report.json>' `
  --baseline '<private Synergy-disabled report.json>'
```

Use `-Baseline` for the disabled-menu comparison. Keep raw logs/screenshots,
settings and assets private. Confirm captured PNG pixel dimensions: requested
resolution alone is insufficient. The checker requires hierarchy, held weapon,
close and a post-close shot in order, rejects any observed menu-open shot and
requires normal exit. The fixed runner releases then freshly presses Fire;
synthetic recovery tests separately exercise the held-close boundary.

Actual controls and physical checks are in the [Synergy checklist](../templates/synergy-checklist.txt).
Prepare with the trial adapter's Source/Binary/Destination/ExpectedSha256,
ReviewDirectory/EvidenceFile/ChecklistFile/WorkflowDirectory parameters and `-Synergy`.
Evidence JSON contains issue, full sourceCommit, upstreamPins, ordered patches
(name/hash) and checks (command/result, all pass). Launch/files/checklist shortcuts
use the exact checked build; use `-VerifyOnly` to check availability without launch.

Only after required checks pass, prepare a versioned owner review using the
[trial adapter](../scripts/prepare-trickshot-trial.ps1) with `-Synergy` and `templates/synergy-checklist.txt`. The wrapper
forces actual Synergy on, observer/console stdin off and no diagnostic commands.
Use `-VerifyOnly` to verify launch availability without starting the owner trial.
The trial's manifest identifies source commit, pins, patch hashes and executable.
Previous builds remain preserved; owner verdict, merge and release are separate.

## Full menu milestone

### Problem and solution

Run the reachable pinned Synergy GSC menu through the existing runtime, preserving
its own presentation/options, and add the agreed near-pass control. Each option
requires effect, reversal, failure and lifecycle evidence; visibility is insufficient.
This parked contract does not select new work. Resume only at the owner's
request, using the [workspace conventions](agents/issue-tracker.md).

### Agreed behavior — C-017, 2026-10-04

The owner-approved requirements settle the hit-radius, noclip and private-player
scope. The [Synergy decision](adr/0002-execute-pinned-synergy.md)
records why the original menu executes. These are requirements for actual Synergy and the runtime extension;
source inspection and this document do not establish implemented behavior.

| Area | Required behavior |
| --- | --- |
| Near-pass detection | A sniper bullet passing close to an eligible target can count regardless of its eventual impact. Do not move aim, redirect the shot or add an explosion. |
| Weapons | Scoped and unscoped sniper bullets. Other weapon types do not receive radius assistance. |
| Targets | Living enemies, including bots and friends playing as enemies in private sessions. Exclude self, teammates, dead players and spectators. |
| Radius | Off by default. When enabled, select 0.25–5 metres in 0.25-metre steps. Measure the additional distance outside the target's normal damageable body volume, not from its origin/centre. |
| Initial and match defaults | Normal damage initially; 0.25 metres on first enabling. A new match resets assistance to Off. |
| Damage | Normal applies the weapon's upper-body damage, including distance and penetration reductions. One-shot makes a qualifying assisted hit lethal. This toggle does not alter ordinary direct-hit damage. |
| Cover and reach | Both modes respect ordinary bullet reach and penetration. The radius cannot reach around, through blocked cover or beyond the bullet's supported travel. One-shot changes damage only after qualification. |
| Multiple targets | Only assist an otherwise missed shot. Choose the eligible enemy closest to the reachable bullet path, using the gap to its damageable body volume. At most one assisted hit per shot. Preserve ordinary direct hits and collateral behavior without an additional assisted hit. |
| Frag No Clip | Include Synergy's option, superseding the earlier exclusion. Restore ordinary movement and weapons on exit and remove only temporary noclip invulnerability, preserving a separately enabled God Mode. Clean up on death, disconnect and map/match changes. |
| All Players | Include the player list, name display, Kill, menu-access grants and Kick. The host controls administration. Granted guests receive personal menu access, not authority over other players or shared session settings. Protect the host from Kick. |

```text
Sniper shot -> ordinary bullet travel, penetration and direct-hit resolution
                  | direct hit(s) -> preserve damage/collaterals; no assist
                  | miss
                  v
       assistance on + eligible enemy + within radius + cover/reach valid?
                  | no -> ordinary miss
                  | yes
                  v
       closest eligible enemy -> one Normal or One-shot assisted hit
New match -> assistance Off
```

The radius extends hit tolerance around a body's normal damageable shape along
the bullet's reachable path. A wall far beyond the target does not invalidate a
near pass; a wall shielding the target does. This requires native path/cover
evidence, not just distance from an impact point.

### Acceptance examples for the full menu

These are expected results, all **not yet tested** for the new behavior. Record
actual setup, selected radius/mode, weapon, target state, observed damage and
pass/fail in later implementation evidence. Distances below are measured from
the body's damageable surface; avoid relying on visual estimates for boundaries.

| Example | Expected result |
| --- | --- |
| Radius 1 m; missed sniper bullet passes 0.5 m from an enemy and impacts a distant wall | One assisted hit qualifies even though the impact is far away. Aim and bullet direction stay unchanged; no explosion. |
| Radius 1 m; otherwise identical passes at 0.99 m and 1.01 m | Inside qualifies, outside misses. Exercise the exact boundary with native geometry/tolerance tests. |
| Assistance Off; same 0.5 m near pass | Miss, with no assisted damage. Direct hits continue normally. |
| First enable, adjustments at both ends, then a new match | Starts at 0.25 m and Normal; controls step by 0.25 m within 0.25–5 m; assistance is Off in the new match. |
| Scoped and unscoped sniper shots; a non-sniper near pass | Both sniper modes qualify under the same rules; the non-sniper receives no assist. |
| Normal versus One-shot against an enemy with more health than normal upper-body damage | Normal matches an equivalent upper-body hit at that distance/penetration and can leave the enemy alive; One-shot kills a qualifying target. |
| Near pass after permitted penetration through a suitable surface | Assist only where ordinary bullet reach/penetration permits it. Normal includes attenuation; One-shot is lethal only after the same cover check passes. |
| Impenetrable cover, exhausted penetration/reach, or a target around a corner but within the selected radius | No assistance in either damage mode. |
| Two living enemies 0.4 m and 0.7 m from the path with radius 1 m | Assist only the 0.4 m enemy, regardless of list order. Equal-distance candidates still produce at most one hit with a repeatable tie result. |
| Direct hit or ordinary penetrating collateral, with another enemy nearby | Preserve the ordinary result; no duplicate damage and no extra assisted target. |
| Self, teammate, dead player or spectator is closer than an eligible enemy | Ignore excluded targets when selecting the assisted enemy. A private friend on the enemy side and an enemy bot are eligible. |
| Noclip enabled: enter with Frag, move, then exit with melee in free space | Restore movement/collision and weapons; remove temporary invulnerability. A prior separate God Mode remains as it was. |
| Attempt noclip exit inside solid geometry | Do not strand the player or re-enable collision inside solid geometry. Reject the unsafe exit with feedback and allow movement to free space before retrying. This is the native port's safe-exit policy. |
| Death, disconnect or map change during noclip | No stale movement mode, disabled weapons or temporary invulnerability reaches the next life/session; temporary state is disposed of. |
| Host selects a current player; guest with and without a menu grant tries the same administrative actions | Host can display the name, Kill, grant personal access and Kick a non-host. Ungranted guests cannot use the menu; granted guests can use personal options but cannot Kill/Kick/grant access or change shared settings. Check enforcement at execution, not just visibility. |
| Host selected for Kick, including a forged/stale action request | Reject Kick with feedback and keep the host connected. |
| Selected player disconnects, list changes, or another connection reuses the name/slot before execution | Reject stale selections, refresh the list and apply nothing to the replacement connection. Revalidate target identity and caller permission; an old grant does not transfer to a new connection. |

### Implementation research still required

These tasks remain under the full-menu milestone; they do not reopen the agreed
product choices or assert runtime feasibility.

- **Native compatibility:** map every reachable option/catalogue entry to pinned
  runtime support; demonstrate effect, failure and lifecycle cleanup. An unsupported
  entry stays a visible parity gap with explicit feedback.
- **Near-pass integration:** establish authoritative bullet segments, body volumes,
  metres-to-runtime units, distance/penetration damage, cover tests, direct-hit
  ordering and deterministic target/tie handling. Validate the examples above at
  the simulation boundary before claiming this is feasible or implemented.
- **Noclip lifecycle:** establish movement/weapon state restoration and collision
  clearance checks for safe exit, including death and map teardown. The GSC
  reference alone does not prove cleanup in the native runtime.
- **Private-session synchronisation:** establish host-side authorization,
  connection identities, grants and invalidation, acknowledgements and replicated
  effects. Classify personal versus shared options before exposing them to guests;
  unsupported private-session capabilities must fail explicitly.

No new game integration, public-match assistance, redistribution or general
GSC-loader implementation is included. Hide HUD remains deferred. Native tests,
an isolated Windows trial and explicit owner acceptance are separate later gates.

### Historical Hide HUD contract — C-014 (deferred)

The following records the earlier bounded contract only. Its source patch stays
untouched; it is neither the current slice nor a prerequisite for another slice.
The former HUD-first ordering and Combine practice milestone are superseded.

Before coding, the Hide HUD contract is:

- Outcome: Menu → Appearance → Hide HUD, OFF by default. Turn ON, close the menu,
  skate without gameplay HUD/crosshair/routine skating banner; reopen and turn
  OFF to restore. Existing keyboard/controller navigation and release barriers apply.
- Preserve practice feedback, pause/settings, class selection, Minecraft inventory
  and actionable skating errors, controller and preparation prompts. Preserve the
  choice through menu, pause, class, respawn and skating transitions. New map/session
  or returning to main menu resets it to OFF. No disk persistence.
- Allowed runtime files: frame presentation contracts; console menu/input/banner/
  tests/preview; HUD renderer and UI layer policy. Deliver a third source patch
  after the unchanged menu/audio patches, plus relevant docs and redacted evidence.
- Dependencies: pinned runtime/Synergy, existing audio patch and recorded Windows
  cross-build tools. No recipe/network, movement/audio, assets or integration changes.
  Broad console `ui` retains its separate diagnostic meaning.
- Acceptance evidence: toggle/lifecycle/recovery behavior tests, real keyboard/pad
  input integration, native asset-free previews at 720p/1080p, Windows build/hash,
  repository gate; then owner controller play and explicit design verdict.
- Stop for a design decision if preserving recovery controls requires gameplay or
  network changes. Record failed/missing prerequisites explicitly. Publication
  remains conditional on owner acceptance. This historical contract is inactive.

### Hit-radius vertical slice — D-019

Outcome: open actual Synergy → enable/adjust hit radius → close → fire an eligible
sniper near miss → observe qualifying damage → disable → ordinary shooting resumes.
Inputs are captured Synergy controls, match/session authority, an accepted sniper
shot, lag-compensated body volumes and ordinary penetration/cover facts. Output is
at most one ordinary damage attempt after an otherwise missed shot qualifies.

Qualification work belongs inside this slice: trace authoritative path segments,
body volumes and units; damage ordering; cover from path to target; private-session
eligibility; and the actual GSC-to-simulation setting seam. Record missing capability
precisely before implementation. Use the [initial source trace](../research/results/2026-10-05-hit-radius-qualification.md)
as evidence navigation, not proof of feasibility. No impact-distance substitute.

Keep the defaults, boundaries and examples above. Verify Off/first enable/steps/
match reset; scoped/unscoped snipers; living enemy bots/private players and excluded
targets; Normal/One-shot; permitted/blocked cover and reach; direct-hit/collateral
preservation; closest target/ties; and menu input isolation. Unsupported settings
must report failure without activating assistance; stale/dead/session-invalid
requests must apply nothing. Public matches, skating fire, aim movement, added
explosions, Combine practice additions and new menu candidates are excluded.

After simulation and input checks pass, build an isolated Windows trial and a
separate versioned Launch, Files and Checklist review folder with exact source,
ordered patch hashes, upstream pins and executable hash. Physical gameplay and
owner acceptance remain separate. Preserve the current Synergy trial.

### Pinned MW2 Synergy feature inventory

Source: `MW2/Synergy/maps/mp/Synergy.gsc` at
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`, SHA-256
`2c7be615f2e435c34ad7e1ee4bc9d1b1682ff08b909dea911abc6819e4a484d9`.
Catalogs: `initial_variables` lines 19–90. Reachable features: `menu_option`
1105–1345. `hide_ui` 1446–1449 sets `cg_draw2d`.

This is a source/technical coverage snapshot dated October 4, 2026, not a second
status tracker. **pending**: no native implementation evidenced; **implemented**: code exists, checks
remain; **verified**: named technical checks pass, owner play verdict still needed;
**blocked**: scope/dependency stated. This historical snapshot does not establish acceptance or current publication status.
Each grouped row's state applies to every named feature. Existing upstream class
selection alone does not establish Synergy loadout-menu parity.

| Feature | State | Evidence / delivery |
| --- | --- | --- |
| Native menu, seven slots, submenus/history, controller/keyboard input capture | verified | Existing 18 menu tests and native previews; owner acceptance pending |
| God Mode | pending | Loadout/practice |
| Frag No Clip | pending | Included by C-017/D-013; native lifecycle and safe-exit checks required |
| Infinite Ammo and grenades | pending | Loadout/practice |
| Give All Perks; Take All Perks; Give Perks; Take Perks | pending | Individual catalog below |
| Forge Mode | pending | Visual/fun; integration unestablished |
| Set Speed (190–990, step 20) | pending | Movement/session |
| Set Timescale (1–10, step 1) | pending | Movement/session |
| Set Gravity (120–900, step 20) | pending | Movement/session |
| Fullbright; Third Person; Visions / None | pending | Visual/fun; catalog below |
| Move Menu X (−600–20); Move Menu Y (−50–50) | pending | Appearance |
| Rainbow Menu; Red; Green; Blue | pending | Appearance; fixed cyan is not parity |
| Hide UI | deferred | C-014 preserved; not an active slice or dependency |
| Hide Weapon | pending | Separate visual option |
| Give Weapons; Take Current Weapon; Drop Current Weapon | pending | Loadout/practice; catalog below |
| Equip Attachment | pending | Current-weapon restrictions need native checks |
| Equip Camo (1–8); Cycle Camos | pending | Excludes launchers, machine pistols, shotguns, pistols, extras |
| Give Killstreaks | pending | Native support requires per-entry evidence |
| All Players list; Print name; Kill; Verify menu access; Kick | pending | C-017 settles host administration/personal guest access; native authority and synchronisation still require evidence |
| Save starting spot; Return to starting spot | excluded from destination | Earlier implementation preserved |
| Add stationary bot; Place latest bot; Freeze bots | excluded from destination | Earlier implementation preserved |
| Bot aim lock; Smooth controller preset; Restore settings | excluded from destination | Earlier implementation preserved |
| Trickshot hit radius | pending | C-017 specifies near-pass geometry, defaults, damage and cover; no native implementation yet |
| Added explosion / blast damage for hit assistance | excluded | D-013 selects near-pass assistance without an added explosion; ordinary Synergy weapons remain in inventory |
| Stunt launcher | excluded from destination | Earlier proposal preserved; not a dependency |

Individual catalog entries follow. “Death streaks” are declared in the source but
not exposed by `menu_option`; they are not silently added to the M1 promise.

| Catalog | Entry | State |
| --- | --- | --- |
| visions | AC-130 | pending |
| visions | AC-130 inverted | pending |
| visions | Aftermath | pending |
| visions | Airplane | pending |
| visions | Airport | pending |
| visions | Airport Death | pending |
| visions | Airport Exterior | pending |
| visions | Airport Green | pending |
| visions | Airport Intro | pending |
| visions | Airport Stairs | pending |
| visions | Ambush | pending |
| visions | Armada | pending |
| visions | Armada Water | pending |
| visions | Big City Destroyed | pending |
| visions | Blackout | pending |
| visions | Blackout Nvg | pending |
| visions | Bog | pending |
| visions | Boneyard | pending |
| visions | Bridge | pending |
| visions | Cargo Ship | pending |
| visions | Cheat BW | pending |
| visions | Cheat BW Contrast | pending |
| visions | Cheat BW Invert | pending |
| visions | Cheat Chaplin Night | pending |
| visions | Cheat Contrast | pending |
| visions | Cheat Invert | pending |
| visions | Cheat Invert Contrast | pending |
| visions | Cliff Hanger | pending |
| visions | DC | pending |
| visions | DC EMP | pending |
| visions | Default | pending |
| visions | Default Night | pending |
| visions | Default Night MP | pending |
| visions | End Game | pending |
| visions | Intro Screen | pending |
| visions | MP Afghan | pending |
| visions | MP Nuke | pending |
| visions | MP Nuke Aftermath | pending |
| visions | MP Outro | pending |
| visions | Near Death | pending |
| visions | Near Death MP | pending |
| visions | Thermal MP | pending |
| weapons / assault rifles | M4A1 | pending |
| weapons / assault rifles | Famas | pending |
| weapons / assault rifles | Scar-H | pending |
| weapons / assault rifles | Tar-21 | pending |
| weapons / assault rifles | FAL | pending |
| weapons / assault rifles | M16A4 | pending |
| weapons / assault rifles | ACR | pending |
| weapons / assault rifles | F2000 | pending |
| weapons / assault rifles | AK-47 | pending |
| weapons / assault rifles | AK-47 Classic | pending |
| weapons / sub machine guns | MP5K | pending |
| weapons / sub machine guns | UMP45 | pending |
| weapons / sub machine guns | Vector | pending |
| weapons / sub machine guns | P90 | pending |
| weapons / sub machine guns | Mini-Uzi | pending |
| weapons / sub machine guns | AK-74u | pending |
| weapons / sub machine guns | Peacekeeper | pending |
| weapons / light machine guns | L86 LSW | pending |
| weapons / light machine guns | RPD | pending |
| weapons / light machine guns | MG4 | pending |
| weapons / light machine guns | AUG HBAR | pending |
| weapons / light machine guns | M240 | pending |
| weapons / sniper rifles | Intervention | implemented; see current Intervention evidence |
| weapons / sniper rifles | Barrett .50cal | pending |
| weapons / sniper rifles | WA2000 | pending |
| weapons / sniper rifles | M21 EBR | pending |
| weapons / sniper rifles | M40A3 | pending |
| weapons / sniper rifles | Dragunov | pending |
| weapons / machine pistols | PP2000 | pending |
| weapons / machine pistols | G18 | pending |
| weapons / machine pistols | M93 Raffica | pending |
| weapons / machine pistols | TMP | pending |
| weapons / shotguns | SPAS-12 | pending |
| weapons / shotguns | AA-12 | pending |
| weapons / shotguns | Striker | pending |
| weapons / shotguns | Ranger | pending |
| weapons / shotguns | M1014 | pending |
| weapons / shotguns | Model 1887 | pending |
| weapons / pistols | USP .45 | pending |
| weapons / pistols | .44 Magnum | pending |
| weapons / pistols | M9 | pending |
| weapons / pistols | Desert Eagle | pending |
| weapons / pistols | Gold Desert Eagle | pending |
| weapons / launchers | AT4-HS | pending |
| weapons / launchers | Thumper | pending |
| weapons / launchers | Stinger | pending |
| weapons / launchers | Javelin | pending |
| weapons / launchers | RPG-7 | pending |
| weapons / extras | Riot Shield | pending |
| weapons / extras | Default Weapon | pending |
| weapons / extras | Frag Grenade | pending |
| weapons / extras | Semtex | pending |
| weapons / extras | Throwing Knife | pending |
| weapons / extras | Claymore | pending |
| weapons / extras | C4 | pending |
| weapons / extras | Flash Grenade | pending |
| weapons / extras | Stun Grenade | pending |
| weapons / extras | Smoke Grenade | pending |
| attachments | Reflex Sight | pending |
| attachments | Holographic Sight | pending |
| attachments | Acog Scope | pending |
| attachments | Thermal Scope | pending |
| attachments | Grip | pending |
| attachments | Grenade Launcher | pending |
| attachments | Shotgun | pending |
| attachments | Tactical Knife | pending |
| attachments | Heartbeat Sensor | pending |
| attachments | Silencer | pending |
| attachments | Extended Mags | pending |
| attachments | Rapid Fire | pending |
| attachments | Akimbo | pending |
| attachments | FMJ | pending |
| perks | Marathon | pending |
| perks | Slight of Hand | pending |
| perks | Scavenger | pending |
| perks | Bling | pending |
| perks | One Man Army | pending |
| perks | Stopping Power | pending |
| perks | Lightweight | pending |
| perks | Hardline | pending |
| perks | Cold-Blooded | pending |
| perks | Danger Close | pending |
| perks | Commando | pending |
| perks | Steady Aim | pending |
| perks | Scrambler | pending |
| perks | Ninja | pending |
| perks | SitRep | pending |
| perks | Last Stand | pending |
| death streaks | Copycat | blocked: not reachable |
| death streaks | Painkiller | blocked: not reachable |
| death streaks | Martyrdom | blocked: not reachable |
| death streaks | Finalstand | blocked: not reachable |
| killstreaks | UAV | pending |
| killstreaks | Care Package | pending |
| killstreaks | Counter-UAV | pending |
| killstreaks | Sentry Gun | pending |
| killstreaks | Sentry Gun Care Package | pending |
| killstreaks | Predator Missile | pending |
| killstreaks | Precision Airstrike | pending |
| killstreaks | Harrier Strike | pending |
| killstreaks | Attack Helicopter | pending |
| killstreaks | Emergency Airdrop | pending |
| killstreaks | Pave Low | pending |
| killstreaks | Stealth Bomber | pending |
| killstreaks | Chopper Gunner | pending |
| killstreaks | AC-130 | pending |
| killstreaks | EMP | pending |
| killstreaks | Nuke | pending |
