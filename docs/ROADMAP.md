# Combine roadmap: separate experiences, shared reproducibility

The ambition is a substantial open-source home for game mashup experiments:
interesting combinations that contributors can reproduce and players can test.
Each experience declares its world, movement and optional combat separately.
Rust runtime capabilities are reused where verified; this is not a universal merger.

## Player destinations

| Experience | Destination | Evidence boundary |
| --- | --- | --- |
| MW2 world + Skate | Repeatable skating in an existing MW2 map | Owner reports skating; recovery/replay baseline incomplete |
| Minecraft world + movement/combat modes | Separately selectable documented combinations | Minecraft play reported; changed-terrain skating unverified |
| Actual Synergy trickshots | Original GSC menu and agreed near-pass hit radius | Exact input trial prepared/unaccepted; hit radius unimplemented |
| Fortnite world + Skate only | Build, edit and destroy structures on the complete selected island with Skate movement/tricks/grinds; recover and relaunch | Live gameplay base/client/bridge qualification; no playable integration |
| More game combinations | Add candidates after Fortnite + Skate reaches its first playable milestone | Candidate names and scope follow verified engine capability |

The [private planning board](https://github.com/users/Jpatching/projects/5/views/4)
owns active tasks, decisions and dependencies. [Decisions](DECISIONS.md) owns
scope corrections; this public roadmap describes destinations without invented
release dates. The Fortnite request starts wayfinding now; hit radius remains
first within the separate menu implementation track. The pending physical
Synergy trial remains visible independently.

## Build trust before widening the catalogue

1. **Qualify one integration.** Identify exact source/build, legitimate inputs,
   live gameplay/client access and collision lifecycle requirements; publish only source-safe
   findings, including an honest blocker if the inputs are unavailable.
2. **Demonstrate one playable slice.** For Fortnite + Skate only, start with the
   live building and terrain as a test within the full-island integration.
   Build a ramp on foot, skate/jump/grind, edit and destroy it, then recover and
   relaunch. Qualify matching visible shape and current skating collision.
3. **Make it repeatable.** Pin code/tools, preserve originals, prepare a versioned
   review, test setup and relaunch, and record an owner verdict for that build.
4. **Offer a useful hub.** Proposed first format: a source-backed catalogue linking
   each experience's prerequisites, reproduction, exact-build evidence, limitations
   and recovery. A launcher/download service is a later decision.
5. **Invite focused contributions and expand.** The first hub is a GitHub
   experience catalogue. “Community tested” requires a named exact build and
   recorded participant results; sample-size/threshold claims remain undecided.
   Add other game candidates after Fortnite + Skate reaches its first playable
   milestone. Outreach needs separate authority.

```text
Candidate -> source/access qualification -> exact build ready to try -> play tested
   | missing support -> visible blocker         | fails -> revise       | verdict
   +------------------- no playable claim ------+-----------------------+
```

“Play tested” must name who tested what build and which behavior; a prepared
folder or successful fixture does not qualify. Automatic launch/acceptance,
asset redistribution and multiplayer integration remain excluded.
Building, editing and destruction are required by D-026; static export work is historical.
Full-island loading and any needed spatial streaming require measured qualification;
this specification slice does not implement them. A live hosted hub is not implemented.

Start with [reproduction](REPRODUCING.md). Proposed discoverability and community
work is in the [growth plan](GROWTH.md); detailed qualification evidence stays in
research/results/ and the [handoff](HANDOFF.md).

## Fortnite adapter qualification order

Pin an accessible client; establish a permitted host extension route; read one
host value; connect controls/pose/camera to the existing Skate Session; qualify
collision geometry/rails and live structure lifecycle; demonstrate on-foot build,
skate, edit/destroy, recover and relaunch. A reusable host/guest bridge is the
method; process placement and transport follow inspected interfaces. No universal
framework is selected. Stock-client startup alone cannot qualify this bridge.
