# Synergy menu requirements, build and trial

The destination is the proper pinned Synergy menu plus **trickshot hit radius**,
without Combine-specific save/return, target practice, aim-lock/preset or stunt
launcher additions. Existing patches and trials are preserved as earlier work.
They do not establish feature parity or acceptance of this destination.

The [source coverage record](../research/results/2026-10-04-menu-coverage.md)
rechecks the inventory and supports the first demonstrable slice below. Hide HUD
is deferred and is not an active slice or prerequisite.

## Owner correction — use Synergy itself, October 4

The owner explicitly confirmed **Synergy itself** after rejecting the custom
native menu previews. The pinned GSC source must drive the menu's appearance,
navigation and options. Changing the labels or restyling our practice menu does
not satisfy that request. Use the existing runtime script engine to establish
compatibility with Synergy's IW4x requirements; do not assume copying the mod
folder is enough. D-015 records this correction.

The native-port implementation details and bounded Intervention contract below
are historical where they conflict with this correction. Preserve their source
and test evidence, but do not prepare that build as the requested replacement.
The first integration check remains opening the actual Synergy menu, navigating
to Intervention and equipping it. The full menu destination and agreed hit-radius
requirements remain; individual options need execution evidence before claiming
support. No Synergy-script trial is prepared or gameplay-tested.

## Preserved native Intervention build and review adapter — October 4

Apply `trickshot-v0.4.0.patch`, then `skate-audio-v0.4.0.patch`, then
`intervention-v0.4.0.patch` to the pinned runtime. Do not apply deferred Hide HUD.
The new root contains six Synergy sections; only Weapon Options → Give Weapons →
Sniper Rifles → Intervention is enabled. Requests use the native weapon catalogue
and simulation acknowledgement; "equipped" also requires the actual held weapon
and inventory. Previous practice patches/trials are preserved.

Build with the pinned tools below. Run the console tests with `practice`, build
`launcher --bin iw4l` and `console --example practice_menu_preview`, then run
720p/1080p previews. The preview now captures root, Intervention, failure and
closed states. These are synthetic checks, not play or acceptance.

The adapter is verified with synthetic fixtures. The command below documents
its interface; do not prepare the rejected native build for owner acceptance.
For a future corrected build, prepare the folder only after required checks pass:

```powershell
.\scripts\prepare-trickshot-trial.ps1 -Source '<prepared runtime>' `
  -Binary '<built iw4l.exe>' -Destination '<new versioned trial>' `
  -ExpectedSha256 '<build SHA-256>' -ReviewDirectory '<new versioned review folder>' `
  -EvidenceFile '<local evidence.json>' `
  -ChecklistFile '.\templates\intervention-checklist.txt' `
  -WorkflowDirectory '<shared solo-development workflow directory>'
```

Evidence JSON contains `issue`, full `sourceCommit`, `upstreamPins`, ordered
`patches` (name/hash) and `checks` (command/result, all pass). The shared Windows
helper creates **Test Intervention**, **Open trial files**, **Read checklist**
and `evidence.json`, marked prepared/unaccepted. The launcher validates the hash,
checks for an existing game and holds a mutex through process exit so concurrent
shortcuts cannot start another trial. Errors are shown explicitly. Launch history
stays local and never claims gameplay. Do not use `-Launch` for the owner handoff;
it is an explicit combined operation requiring the review bundle.

The [Intervention checklist](../templates/intervention-checklist.txt) replaces the
earlier practice sense-check for this trial. Report keyboard/controller equip,
fire, input release, relaunch and the exact build in chat. Record the verdict
against that build; revised binaries require a new folder and verdict. No raw
logs, machine paths or game content go to the Project. Reviewed source-branch publication is now authorized by D-016/D-017; owner
acceptance, merge and release remain separate.

The sections below retain reproduction/history for the earlier menu and the
agreed full-menu contract. [Current evidence](../research/results/2026-10-04-intervention-review.md)
separates automated checks, preparation, launch and owner acceptance.

## Existing development build

This slice gives the existing local practice actions a Synergy-derived native
menu. [README](../README.md) is the player guide; this document owns developer
reproduction and acceptance steps. No console commands are needed to use the menu.

```text
Physical buttons -> menu state (page, history, cursor, repeat, release barrier)
                          | closed / unavailable -> no menu UI
                          | open
                          +-> native proportional-font panel
                          +-> typed action -> local-host checks -> existing queues
                                                  | unavailable -> menu feedback
After closing -> wait for physical release -> gameplay controls resume
```

Navigation and practice actions are separate. The native panel has seven row
slots (unused slots remain blank). Action results remain visible until the next
action; an accepted queue request is labelled requested, not completed.

## Pinned source and build

Use runtime `f608f85e407ff1b7689d54a9aafdd16e95711ac4` (v0.4.0) and
Synergy `33bcc80f5446e7543a2eb68b17c798e29d3f27c4`. The pins and observed source
hashes are in [upstream.lock.json](../research/upstream.lock.json).
The patch contains the prior local practice implementation and its replacement
UI. Apply it to a clean checkout of the selected runtime, not over the old patch:

```sh
git apply --check /path/to/combine/patches/trickshot-v0.4.0.patch
git apply /path/to/combine/patches/trickshot-v0.4.0.patch
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p launcher
```

Established cross-build tools: Rust 1.95.0, cargo-xwin 0.23.1, Clang/LLVM 19.1.1
for native dependencies, and Rust's bundled rust-lld linker. The Windows SDK and
CRT are the existing cargo-xwin cache; retain Cargo.lock. Upstream's moving
`stable` is not the reproduction pin. No upstream updater is built or published.
See the [result record](../research/results/2026-10-03-synergy-menu.md) for exact
local build commands, hashes, verification results and inherited warnings.

## Focused verification

The two pure Rust modules can be tested without dependencies or game assets:

```sh
rustc +1.95.0 --edition 2024 --test crates/console/src/practice_menu.rs -o /tmp/menu-tests
/tmp/menu-tests
rustc +1.95.0 --edition 2024 --test crates/console/src/practice_core.rs -o /tmp/practice-tests
/tmp/practice-tests
```

Build the actual input/action integration tests, then run the resulting console
test executable on Windows with the `practice` filter:

```sh
cargo +1.95.0 xwin test --locked --profile play --target x86_64-pc-windows-msvc -p console --lib --no-run
cargo +1.95.0 xwin build --locked --profile play --target x86_64-pc-windows-msvc -p console --example practice_menu_preview
```

The preview executable takes `width height fresh-output-directory`. Run it once
at `1280 720` and once at `1920 1080`. It renders the production UI on a plain
background, captures root/Aim/error/closed states and exits. It loads no game
assets or profile and opens no network interface. Keep generated images local.
This verifies native rendering, not gameplay or owner acceptance.

## Fresh Windows trial

Build `target/x86_64-pc-windows-msvc/play/iw4l.exe`, calculate SHA-256, and use
[scripts/prepare-trickshot-trial.ps1](../scripts/prepare-trickshot-trial.ps1):

```powershell
.\scripts\prepare-trickshot-trial.ps1 -Source '<prepared baseline runtime>' `
  -Binary '<built iw4l.exe>' -Destination '<fresh development folder>' `
  -ExpectedSha256 '<64-character build hash>'
```

The script refuses an existing destination or a mismatched binary, copies the
prepared baseline, rewrites internal runtime references, verifies the deployed
hash and checks the source executable remained unchanged. Failed preparation
retains the incomplete folder for inspection. It does not compare every original
game file; the baseline runbook's post-session hash check remains outstanding.

Close the prior game, then run `iw4l.exe map mp_rust` in the new folder. Optional
`-Launch` now requires the review-bundle inputs above and uses its verified launcher.
Preparation, a started process and successful play are distinct results.

## Owner sense-check

At both 1280×720 and 1920×1080:

1. Launch on Rust: no practice panel/banner. Open with L2+R3 and F6; confirm the
   right-side layout and readable proportional text, arrows and cyan selection.
2. Enter each submenu and go back. Hold D-pad and triggers; selection repeats
   without firing. Cross/Square select; Circle/R3 go back. Escape closes only this menu.
3. Hold fire/jump/melee/skate buttons while closing: gameplay waits for release.
   Close with aim lock enabled: no practice overlay remains.
4. Try Return before saving and Place before adding a bot: error inside menu,
   menu stays open. Save, move, return; repeat while skating and confirm exit first.
5. Add/place/freeze a bot. Apply and restore the controller preset. Enable aim
   lock deliberately, verify release stops it, then turn it off.
6. Change maps: save cleared and aim lock off. Confirm recovery/relaunch.

Record pass/fail/not tested, readability and controller feel in the result record.
The old panel's rejection is not acceptance. D-016/D-017 now authorize reviewed
source branches and notices on Jpatching/combine before replacement acceptance;
owner trial, merge and release remain separate.

## Full menu milestone

### Problem and solution

The existing build gives players a Synergy-looking menu around earlier practice
actions, so selecting the familiar Synergy loadout, fun or player options is not
yet possible. Port the reachable pinned menu and add the agreed near-pass control
so a player can configure the supported private mashup through controller or
keyboard. Keep unfinished native capabilities explicit until demonstrated.

Port the reachable pinned Synergy menu: Basic Options, Fun Options, Weapon
Options, Give Killstreaks, Menu Options and All Players, plus a separately
specified trickshot hit-radius control. Port native behavior in small slices;
do not infer that an option works because its name appears in a menu.

The current native build implements presentation/navigation and earlier Combine
practice actions. It does not implement this full menu. Catalogue identifiers
must resolve against the pinned runtime; unsupported entries need explicit
feedback and remain gaps in parity. Death streaks are declared but unreachable
in the pinned menu and are outside the source-parity promise.

### Agreed behavior — C-017, 2026-10-04

The owner-approved requirements settle the hit-radius, noclip and private-player
scope. [D-013](DECISIONS.md#d-013-near-pass-assistance-and-full-menu-scope--2026-10-04)
records the consequential changes. These are requirements for the native port;
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
product choices or block the bounded Intervention slice below.

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

### Earlier native slice contract — equip Intervention (C-016)

The first slice solves one visible gap: a living local host on Rust can equip
the Intervention through Synergy's weapon hierarchy without console commands.
It is a tracer bullet: a narrow working path from input through simulation to
visible feedback, before extending the remaining catalogue. C-017 supplies the
settled requirements. `to-spec` consolidated the contract and `to-tickets`
finalised this one independently demonstrable slice. Implementation and its
acceptance checks are tracked separately in the current evidence; the [C-016 draft](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=261972158)
owns active status. C-017 is the completed prerequisite; no other gameplay slice
blocks starting C-016. The existing plan supplies the agreed granularity and
test boundary, so no new interview or duplicate ticket is needed.

#### User stories

1. As a player, I want the six Synergy root sections so the menu matches the
   promised destination, with unfinished options clearly unavailable.
2. As a controller player, I want to reach Weapon Options → Give Weapons →
   Sniper Rifles → Intervention using the existing controls.
3. As a keyboard player, I want the same path and result without the console.
4. As a living local host, I want the selection to grant and equip `cheytac_mp`
   with supported ammo so I can close the menu and fire it on foot.
5. As a player, I want feedback to distinguish a queued request from a completed
   grant so an unavailable or rejected action cannot report false success.
6. As a player, I want an unavailable world, dead state or unsupported weapon
   to explain failure inside the still-open menu so I can recover and retry.
7. As a player, I want repeated selections and late replies to refer to the
   correct action, and a map change to discard pending old-session feedback.
8. As a player, I want selecting and closing the menu to suppress held gameplay
   inputs until release so equipping does not accidentally fire, jump or skate.
9. As the owner, I want a separate reproducible Windows trial and explicit
   controller/keyboard verdict before the replacement is accepted or published.

#### Implementation decisions

Reuse the native menu/input capture, typed weapon catalogue/request and matching
simulation result interfaces. The menu issues a typed action, never a console
string. Revalidate availability at dispatch and use authoritative rejection on
state changes between request and execution. Correlate replies with the requesting
player, request and current match; unrelated or late replies cannot claim success.
Verify the held weapon as well as the acknowledgement before claiming equip.

Implementation entry points: native `practice_menu.rs` navigation,
`weapon_dispatch.rs` catalogue resolution and `ClientAction::GiveWeapon`, with
simulation acknowledgement through `apply_give_weapon`. Reuse inventory checks.
The runtime/menu pins and isolated build/trial procedure are existing prerequisites.
Synergy's delayed 999-round clip fill remains a named follow-on parity gap;
this slice uses standard supported ammo/inventory behavior.

#### Testing decisions and acceptance evidence

Test the highest existing behavior boundary: physical menu input → typed action
→ simulation result → held weapon and menu feedback. Existing pure menu/policy
tests and Windows input/action integration tests provide prior art; only add
lower-level cases where integration cannot isolate a boundary. Do not test source
text or infer success from a queued request. Implementation must provide:

- Controller and keyboard reach the specified hierarchy, grant/equip the
  Intervention and keep useful feedback in the open menu. Only this weapon
  action is enabled; the six root sections are present with unfinished paths
  clearly unavailable and without the earlier Combine practice pages.
- Missing world/catalogue, dead player, unsupported weapon, queue failure and
  simulation rejection do not equip or claim success; a later valid retry works.
- Repeat selections, unrelated/out-of-order replies and map teardown do not
  duplicate actions or apply stale feedback to a new match.
- Input capture and release barriers pass; Windows build/hash and native previews
  at 720p/1080p pass; the full repository gate passes at the handoff revision.
- In a fresh isolated Rust trial, the owner selects, equips and fires on foot with
  keyboard and controller, checks recovery and confirms that closing leaks no input.
  Record actual results and the explicit verdict separately from automated checks.

Out of scope: the other catalogue entries and menu actions, delayed 999-round
clip parity, hit radius, noclip, private-player administration/synchronisation,
Hide HUD, skating fire, new audio, assets and publication. Full-menu acceptance
examples above belong to later slices and do not expand this first slice.

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

### Pinned MW2 Synergy feature inventory

Source: `MW2/Synergy/maps/mp/Synergy.gsc` at
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`, SHA-256
`2c7be615f2e435c34ad7e1ee4bc9d1b1682ff08b909dea911abc6819e4a484d9`.
Catalogs: `initial_variables` lines 19–90. Reachable features: `menu_option`
1105–1345. `hide_ui` 1446–1449 sets `cg_draw2d`.

This is a source/technical coverage snapshot dated October 4, 2026, not a second
status tracker. **pending**: no native implementation evidenced; **implemented**: code exists, checks
remain; **verified**: named technical checks pass, owner play verdict still needed;
**blocked**: scope/dependency stated. No feature is owner accepted or published.
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
