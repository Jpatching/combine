# Automatic GTA floors and Skate presentation

Researched 2026-10-13. Source-only findings for the owner's request for automatic
floor coverage, a visible board, GTA character animation and Skate tricks.
No game assets, private diagnostics or settings were inspected or reproduced.
No runtime trial, tracker change or implementation is claimed here.

## Verified current boundaries

The owner reports mounting works. That is separate from acceptance of movement,
all-floor support, board rendering or skeletal animation. The inspected source
baseline is Combine `50bdc0207a3c35ea931c5d1e061e741dff9398f9`; local preparation
reporting changes were already in progress and are outside this investigation.

- `SURFACES` is empty in the tracked adapter. With no prepared surfaces it samples
  a 5×5 ground grid, refuses height changes over 0.05 m, and constructs a flat
  patch. Prepared surfaces require a unique matching layer. There is no automatic
  nearby geometry provider in this route. [Mount script][script]
- Flat riding is bounded to 3.5 m from the origin in each horizontal direction.
  Triangle support also assumes one height at each horizontal position: two
  distinct heights differing by more than 0.001 m cause refusal. Loading a whole
  city mesh unchanged therefore does not solve bridges or stacked floors.
  [Surface contract][surface]
- There is no fixed world-height ceiling in the riding acceptance contract.
  The 3 m vertical check is relative to local support, so it can restrict airborne
  tricks; it is different from banning high roofs. Broad numeric validity bounds
  are also different from a gameplay altitude limit. [Surface contract][surface]
- Triangle replacement already exists, including revision and rider-support
  checks. The JavaScript riding loop does not feed it an automatic moving window.
  [Replacement][replace], [script][script]
- Presentation sets a frozen GTA ped's coordinates and heading plus a chase
  camera. It does not apply Skate skeleton matrices or show a Skate board.
  The worker response contains only `x,y,z,heading` and timing/identity fields.
  [Script][script], [wire][wire]
- The plugin reads sticks and triggers, but both simulation routes deliberately
  mask buttons to A/X push and pass only the left stick. Worker messages do not
  transport the right stick or triggers. Keyboard input currently provides push
  and left/right steering only. [Plugin][plugin], [worker][worker],
  [in-process][inprocess], [wire][wire], [keyboard][keyboard]

## Existing Skate and MW2 capabilities

The pinned Skate Session accepts triangles and rails, supports collision built
off-thread and installed later, and accepts complete Xbox-style controls. Its
pose contains named bone matrices, root, velocity, camera, tick and state.
It does not expose a dedicated public trick-name/score result in that pose.
[Pinned Session interface][session]

MW2 presentation maps soldier bones to the Skate skeleton, aligns bind poses,
and inherits unmapped bones from mapped ancestors. Its board renderer skins a
locally supplied model using named Skate joints and reference inverse binds.
This is the useful reference for the requested appearance. It runs inside a
renderer the rewrite owns; it is not an existing GTA bone-write adapter.
[Pinned retargeting and board rendering][rig]

## Concrete collision routes

**Recommended first route: locally prepared static collision plus an automatic
spatial index and moving window.** Reuse Combine's strict decoder and established
placement facts, catalogue locally available resources, query nearby geometry
at the actual rider position, select the supporting floor, and refresh through
the existing replacement interface. Keep obstacles in the window rather than
reducing the city to sampled flat ground. Actual resource coverage and street
placement must be established; this recommendation is an architectural inference,
not proof of whole-map coverage. [Decoder][decoder], [surface][surface],
[replacement][replace]

The pinned GTA4Unity parser is a source reference for resource decoding, not an
automatic host provider. Its builder enumerates WBN files, combines vertices and
polygons, and places generated Unity colliders at identity. Its composite parser
reads child bounds without applying the matrix arrays it documents; the builder
uses geometry and ignores parsed primitive shapes. Copying that path would
inherit material gaps. [Builder][builder], [composite parser][composite]

**Alternative: extract nearby active host collision.** This could account for
current placement/loading and later moving objects, but the inspected current
plugin provides no mesh API. Version-compatible host access remains a concrete
feasibility question, especially on the retained Complete Edition baseline.
A ground-height query alone supplies neither walls nor floor identity.
Do not present this route as ready. [Current plugin][plugin], [mount][script]

## Recommended ticket boundaries and dependencies

1. **Automatic nearby floor coverage:** mount at the player's current supported
   location without named spots, then ride across refreshed local collision.
   The goal is the whole playable map, including ordinary roofs, bridges and
   interiors, with no spot whitelist or gameplay height cap. Use automatically
   refreshed supporting-floor patches, not all world triangles in one ambiguous
   collection, and preserve verified host/mesh agreement. Include slopes,
   road/bridge separation, obstacles and cache boundaries in
   acceptance. Resolve static resource inventory/placement first; change the
   single-height support assumption explicitly. Dynamic vehicle collision and
   grind rails remain separately declared work, not implicit static coverage.
2. **Visible Skate-driven board:** transport the required Skate joint transforms,
   render a local board from that pose in GTA, and remove it on dismount/failure.
   Include the necessary renderer feasibility proof in this slice. Independent
   of automatic coverage; uses the established riding location for verification.
3. **GTA model animated from Skate:** map GTA bones and bind poses to Skate,
   apply live push/steer/stance animation and preserve the GTA model. Establish a
   compatible bone/render hook before claiming delivery. Depends on the board
   slice's coherent presentation transport; verify feet/board alignment and
   normal GTA animation after dismount. Do not substitute unrelated GTA clips.
4. **First Skate tricks and results:** enable full input transport and deliver
   ollie plus one flip with live board/body motion, landing and failure outcome.
   Depends on board and character presentation. Adjust airborne support checks
   deliberately: existing ground-height/pose bounds are not a general jump
   contract. Accept valid Skate airborne poses without requiring them to equal
   floor height, and preserve landing/failure recovery. Use engine-derived
   outcomes; if named/scored results need a new
   upstream-facing API, record that as part of this behavior, not fabricated UI.
5. **Grinds and wider trick coverage:** follow the first trick slice, adding
   validated GTA rails and engine outcomes. Depends on automatic coverage and
   first tricks; do not imply triangle ingestion already creates grind rails.

Board/animation work need not wait for city-wide collision. Public behavior test
seams should cover F6 → Skate Session, solved pose → visible GTA presentation,
and trick input → landing/recovery. Each implementation
ticket should carry its own reproducible source checks, one representative live
clip and restoration acceptance. Approval of the proposed breakdown is required
before publishing tickets under the repository's tracker convention.

[script]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/combine_skate.js
[surface]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/src/connection.rs
[replace]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/src/worker_parent.rs
[wire]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/src/wire.rs
[plugin]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/plugin.cpp
[worker]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/src/bin/worker.rs
[inprocess]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/src/in_process.rs
[keyboard]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-skate/riding_input.h
[decoder]: https://github.com/Jpatching/combine/blob/50bdc0207a3c35ea931c5d1e061e741dff9398f9/tools/gtaiv-collision/inspect_resource.py
[session]: https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs
[rig]: https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rig.rs
[builder]: https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/IVUnity/CollisionBuilder.cs
[composite]: https://github.com/Infinity-Loops/GTA4Unity/blob/c107e46cf8ab4e3d42f9c0bf685f80bb732a3609/Assets/Scripts/RageLib/Collision/PhBoundComposite.cs
