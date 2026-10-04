# Source coverage and first Synergy slice — 2026-10-04

The requested destination is the proper Synergy menu plus trickshot hit radius,
without Combine-specific practice additions. This record is source inspection,
not a gameplay test. Requirements and the first slice contract live in
[TRICKSHOT_MENU.md](../../docs/TRICKSHOT_MENU.md); active status lives in the
configured tracker.

Inputs: runtime `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, Synergy
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`, existing menu/audio patches and the
inherited deferred Hide HUD patch. Branch `slice/hide-hud`, source HEAD/base
`bfcb6073a829cb7b7f1b314a66c7006213ef0917`; dirty state predates this work.

The pinned [Synergy source](https://github.com/SyndiShanX/Synergy-GSC-Menu/blob/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2/Synergy/maps/mp/Synergy.gsc)
has six root sections in `menu_option` (1105–1345): Basic Options, Fun Options,
Weapon Options, Give Killstreaks, Menu Options and All Players. `initial_variables`
declares 42 visions, 58 weapons across nine categories, 14 attachments, 16 perks
and 16 killstreaks. Four death streaks are declared but not reachable from the
menu. Local SHA-256 matches the lock:
`2c7be615f2e435c34ad7e1ee4bc9d1b1682ff08b909dea911abc6819e4a484d9`.

The existing native `practice_menu.rs` root uses Positions, Targets, Aim and the
inherited Appearance/Hide HUD work. That is navigation/presentation reuse, not
the six-section Synergy menu. Catalogue presence alone proves no runtime support.
The menu guide retains the individual catalogue and explicit parity gaps.

The first tracer bullet is selecting Intervention from the Synergy weapon
hierarchy. Source `give_weapon` (1720 onward) grants and switches a weapon, then
sets 999 clip rounds after a delay. The first native slice deliberately covers
grant/equip with runtime-supported ammo; the delayed clip fill remains a named
parity gap. This avoids claiming the entire Synergy action is reproduced.

The original coverage pass left requirements and PRD/slicing incomplete. The
C-017 follow-up below records the now-agreed requirements and source limits.
The existing menu guide remains the requirements authority; the board records
the subsequent `to-spec` and `to-tickets` handoff for Intervention.

The pinned runtime already resolves weapon names and queues typed
`ClientAction::GiveWeapon` in
[weapon_dispatch.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/console/src/weapon_dispatch.rs),
with accepted/rejected results in
[step.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/sim/src/step.rs).
`apply_give_weapon` rejects dead clients, zero/unknown IDs, unsupported weapons
and empty combat profiles. These upstream files have no local diff in the build
checkout. Reuse is source-supported; the new menu path remains unimplemented.

```text
Synergy menu selection -> typed weapon ID/request -> existing simulation
                            | unavailable                  | rejected -> error
                            +-> menu error                 | accepted
                                                          v
                                                 matching menu feedback
```

A queue acknowledgement must be matched to the request before the menu reports
success. The implementation must check actual equip behavior, recovery and input
capture in a Windows trial; the diagram does not establish those results.

Reproduction used `sha256sum` on the pinned GSC and inherited Hide HUD patch,
`sed -n '1105,1350p'` / `sed -n '1710,1755p'` on the GSC, an in-memory Python
`strTok` catalogue count, `rg -n --no-ignore` for GiveWeapon/GiveAccepted/
GiveRejected, and `git diff --` on the three upstream weapon request files.
Runtime checkout HEAD matches the pin. No upstream code was edited or game run.
Hide HUD SHA-256 remains
`31568ed152da16aecd4a93194c602e9a8fe05af29744a52e45936e7dbf3e780a`.

## C-017 follow-up — 2026-10-04

The approved plan now settles near-pass geometry/defaults/damage/cover, includes
Frag No Clip, and scopes host administration with personal menu access for granted
guests. See [the requirements and acceptance examples](../../docs/TRICKSHOT_MENU.md#agreed-behavior--c-017-2026-10-04)
and [D-013](../../docs/DECISIONS.md#d-013-near-pass-assistance-and-full-menu-scope--2026-10-04).
These are required behavior, not native or gameplay results.

### Synergy references and gaps

At the pinned [Synergy source](https://github.com/SyndiShanX/Synergy-GSC-Menu/blob/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2/Synergy/maps/mp/Synergy.gsc#L1467),
`frag_no_clip` / `frag_no_clip_loop` (1467–1525) enter on Frag, move using attack/
aim and exit on melee. They disable weapons, move a linked script origin and
temporarily enable God Mode if needed; the ordinary exit deletes that origin,
restores weapons and removes temporary God Mode. This does not establish safe
exit inside solid geometry or native death/map cleanup.

`All Players` / `Player Option` (1165–1199) select by player name and expose Print,
Kill, Verify and Kick. Host targets are excluded from Kick in menu construction.
The callbacks (1652–1667) print, suicide, grant Verified access/start a menu and
kick by entity number. `initialize_verified_menu` (169 onward) starts granted
menus. These references do not establish execution-time host-only administration
or safe identity handling for disconnects, duplicate names and reused slots.
The native requirements deliberately add those checks; source labels alone are
not security or synchronisation evidence.

### Trickshot Dummy is an impact-distance reference

Inspected public file: [_funStuff.gsc](https://github.com/timwaldron/trickshot-dummy-mod-OG/blob/958d54a503be4e4a7f0aab4539aa72e5642d7e26/maps/mp/gametypes/_funStuff.gsc#L61)
at `958d54a503be4e4a7f0aab4539aa72e5642d7e26`, raw-byte SHA-256
`4a73c7ab06353b25643f6295f3dd7d86edc04bb50e9b05c2af1d2d58b27314eb`.
In `doInstaKill` (61–122), `destination` comes from `BulletTrace(...)["position"]`.
The `301` branch compares `Distance(destination, player.origin) <= 150`, then
calls the damage callback with a large lethal value. It also checks a head-to-head
trace; the `302` branch omits the impact-distance condition. Neither is evidence
for the selected closest-body near-pass behavior, normal damage with penetration,
or one assisted target per otherwise missed shot. No code from this reference
was copied into the native patch or executed.

### Reproduction and remaining evidence

Commands used for this follow-up:

```sh
curl -fsSL --max-time 30 https://raw.githubusercontent.com/timwaldron/trickshot-dummy-mod-OG/958d54a503be4e4a7f0aab4539aa72e5642d7e26/maps/mp/gametypes/_funStuff.gsc -o /tmp/combine-c017-funStuff.gsc
sha256sum /tmp/combine-c017-funStuff.gsc .private/trickshot/synergy/MW2/Synergy/maps/mp/Synergy.gsc patches/hide-hud-v0.4.0.patch
sed -n '60,127p' /tmp/combine-c017-funStuff.gsc
sed -n '1160,1210p' .private/trickshot/synergy/MW2/Synergy/maps/mp/Synergy.gsc
sed -n '1460,1528p' .private/trickshot/synergy/MW2/Synergy/maps/mp/Synergy.gsc
sed -n '1646,1674p' .private/trickshot/synergy/MW2/Synergy/maps/mp/Synergy.gsc
sed -n '1341,1430p' .private/trickshot/upstream/crates/sim/src/step.rs
```

The public file fetch succeeded after sandbox DNS failure and an approved network
retry; browser retrieval had returned a cache miss. Synergy and deferred Hide HUD
hashes above were reproduced unchanged. The typed weapon dispatch and simulation
rejection path were re-read for the Intervention contract.

Explicit implementation research remains: native support per catalogue entry;
bullet/body geometry, unit conversion and penetration-aware damage; safe noclip
cleanup; and host-authoritative private-session grants, identity and replicated
effects. The menu guide names acceptance examples for each. No game was launched,
no new native behavior was tested, and no owner gameplay verdict was obtained.
Publication remains conditional on explicit replacement acceptance; no assets,
recordings, private settings or logs are included in this evidence.

### Requirements handoff verification

`to-spec` consolidated the existing guide and the C-011 milestone; `to-tickets`
finalised the existing C-016 draft without creating more items. C-017 is Done;
C-016 is the sole Now item in Phase 5, Status Todo, with phases 1–4 evidenced and
5–7 unchecked. All three bodies/fields were read back, then refreshed once more.
The 17 private drafts, unrelated items and all four views/fields were preserved.
Field-filter counts are Now 1, Milestones 2, Needs you 4. The extra roadmap view
has no configured start/target-date fields. The standard helper's layout guard
stopped before writing; a targeted temporary updater preserved that view.

`python3 scripts/verify.py` passed: 16 tests, two recipes, lock structure and links
in 14 documents. Additional checks covered local links in all nine task documents
and preserved archived backlog text; `git diff --check` passed. No new tests were
needed for this documentation-only change. Menu/audio/Hide HUD patch hashes are
unchanged. `git ls-remote` refreshed runtime HEAD/v0.4.0 and Synergy HEAD/main;
both still match their pins. Branch/base and continuation are in the handoff.
