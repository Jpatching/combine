# Fortnite + Skate-only wayfinding — 2026-10-05

Outcome: begin source/access/export qualification for the owner's separate
Fortnite scenery + Skate movement experience. No MW2 combat or Synergy. No
Fortnite files were read, copied, exported or uploaded. No adapter, launch,
gameplay result or distribution clearance is claimed.

> Scope update, October 6: D-022 selects the full island. Building-only language
> below is historical. See the [current adapter qualification](2026-10-06-fortnite-adapter-qualification.md)
> for the specification, startup changes and missing input witness.

## Primary-source findings

A bounded read-only research helper checked official Epic/GitHub sources and
returned facts/unknowns to the lead. Source findings:

- Epic's [v3.1.0 notes](https://www.fortnite.com/news/v3-1-0-patch-notes?lang=en-US)
  date that release to February 28, 2018. The local selected changelist
  `Release-3.1-CL-3917250` was not independently confirmed by an Epic source.
- [UEFN migration](https://dev.epicgames.com/documentation/fortnite/migrating-assets-from-unreal-engine-to-unreal-editor-for-fortnite)
  documents UE/UEFN project migration, including current-version restrictions;
  it does not establish a supported export from the selected legacy retail client
  into Combine. [UEFN import documentation](https://dev.epicgames.com/documentation/en-us/fortnite/importing-assets-in-unreal-editor-for-fortnite)
  similarly describes importing custom assets into UEFN, not legacy extraction.
- [UEFN terms](https://legal.epicgames.com/epicgames/uefn) distinguish developer-owned
  content from Epic content; [Epic terms](https://legal.epicgames.com/epicgames/tos?lang=en_US)
  constrain use of licensed products/content. Ownership or UEFN availability does
  not establish external-engine use or redistribution authority. This flags an
  unresolved access/rights prerequisite, not a legal determination.

## Asset-free Rust integration trace

Lead inspected existing runtime source at local HEAD
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. Struct declarations were read, not
executed or tested as a Fortnite importer:

- `crates/assets/src/lane/mod.rs:32`, `LoadedWorld`: scripts, prepared world,
  material pool, optional collision, spawn points and explicit capability gaps.
- `crates/assets/src/session_load/mod.rs:94`, `PreparedWorld`: draw data, static
  meshes/instances, lighting, bounds and draw policy. `PreparedMatch` also carries
  weapon/script resources; reusing it does not yet prove a combat-free experience.
- `crates/asset_world/src/clip_collision.rs:36`, `ClipCollision`: brushes, BSP
  nodes/leaves, mesh tables, triangle material indices and placed collision models.

These are potential adapter destinations, not a generic import API or sufficient
export schema. Next check: inspect producers/validation and Skate activation to
identify minimum map, collision, spawn and player dependencies; prove how MW2
combat, weapon UI and Synergy stay excluded. A synthetic fixture can validate a
contract but cannot prove Fortnite compatibility or gameplay.

## Precise current prerequisites

No verified lawful local selected-build access/identity or compatible authorized
one-building export witness is available in the evidence. No supported legacy
export route was established by official documentation. Therefore a genuine
Fortnite adapter trial cannot proceed on this evidence. Preserve the selected
scope; do not invent a map or substitute another source without a decision.
Source-only engine tracing and planning remain possible.

The existing private board owns the map and open decisions. Public direction,
reproduction and researched traction proposals are in docs/ROADMAP.md,
docs/REPRODUCING.md and docs/GROWTH.md. The general source licence/contributor
policy and public task surface require review before broad contributor promotion;
only Synergy component attribution is currently evidenced in licenses/.

## Existing adapter precedent in the pinned Rust runtime

The runtime already supports a separate custom world beside the Call of Duty map
loader. This proves an adapter-shaped extension exists as a technical pattern:

- `crates/assets/src/minecraft_map.rs` recognizes the namespaced zone
  `minecraft:overworld`, selects local Minecraft data and returns an IW4 Rust map
  `ZoneFile` as a proxy. That proxy lets existing match startup find shared
  scripts/content. In `crates/session/src/match_apply.rs`, Minecraft uses the
  proxy map's script identity.
- `crates/render_anim/src/minecraft_world.rs::load` reads Minecraft registries
  and resource packs and creates an independent terrain stream/scene. Its update
  system listens for match-installed/torn-down events and runs a separate world
  lifecycle. `render_anim/src/plugin.rs` registers both Skate and Minecraft
  world systems.
- The Minecraft world converts each block state's collision boxes into interned
  shape IDs and streams chunk collision through `sim::voxel::set_chunk`; removed
  chunks call `remove_chunk`, shutdown calls `deactivate`. `sim/src/voxel.rs`
  supplies the collision-query handoff while using the proxy map's brush table.
  Coordinate conversion and scale are explicit there (`BLOCK = 36` map units per
  block; block Y-up maps to runtime coordinates).

This is more than a declaration-only seam: existing source contains a custom
world reader, renderer, streaming loop, coordinate mapping and simulation
collision feed that coexists with the Skate plugin. It demonstrates how a *new
world adapter can be shaped*. It does **not** show that Fortnite's asset format
can be read, that its legacy build may lawfully be exported, or that Fortnite's
geometry and materials match Minecraft's voxel interface.

The Skate interface is more concrete: `crates/render_anim/src/skate/collision.rs::extract`
consumes `asset_world::ClipCollision`, extracting collision mesh triangles,
brush faces and placed static-model collision surfaces. It filters to solid/player
clip contents (`0x10001`), transforms coordinates with `to_skate`, detects grind
rails from walkable lips, and returns triangles/rails to the Skate host.
`crates/render_anim/src/skate.rs::preload_map` passes the extracted geometry to
`skate_host::Session::new`. Minecraft additionally supplies streamed voxel faces
through `sim::voxel::collision_triangles` so its generated blocks can become
Skate collision/rails.

This gives us a demonstrated target contract for static imported geometry:
produce a correct `ClipCollision` (or a deliberately narrow equivalent consumed
by the Skate host), preserving solid contents, units/axis conversion and useful
walkable edges. The source decoder remains unknown. The normal match session still
requires game startup/script/content; the Minecraft precedent supplies an IW4 proxy
map for these. That proxy may retain MW2 weapons, combat rules and Synergy systems.
Therefore Fortnite + Skate needs an explicit no-MW2 capability/configuration
boundary at match setup; a custom renderer alone cannot establish the requested
composition.

A voxel bridge only fits if the authorized Fortnite export can be represented at
that granularity. For a static Tilted building, translating its solid surfaces to
the existing `ClipCollision`/Skate extraction path looks like the first seam to
qualify. Neither choice is proven compatible or complete. Keep Fortnite + Skate
free of visible/collidable proxy Rust geometry, weapons, combat and Synergy menu.

```text
Minecraft precedent: custom world -> voxel simulation + block-face Skate collision
Fortnite proposal:   lawful building export -> decoder/transform -> Rust world render
                                           -> ClipCollision -> Skate triangles/rails
                                           -> match config suppresses MW2 combat/UI
No export/format witness -> decoder contract remains unknown -> no playable claim
```

Observation type: source-inspected at the exact pinned upstream commit, not built
or gameplay-tested during this check. Fortnite source/export compatibility and
a no-MW2 match configuration remain unproven. Paths: `crates/assets/src/minecraft_map.rs`,
`crates/render_anim/src/minecraft_world.rs`, `crates/render_anim/src/plugin.rs`,
`crates/sim/src/voxel.rs`, `crates/session/src/match_apply.rs`.
