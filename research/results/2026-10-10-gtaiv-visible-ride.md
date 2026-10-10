# GTA visible ride and presentation gap — 2026-10-10

The owner selected visible ride proof before completing street checkpoint
qualification. Reuse the preserved adapter and unchanged mounting guard. This
supersedes the previous trial sequence, not the frozen street comparison rules.

## Actual observations

The first ordinary launch request left GTA closed with Rockstar Launcher present.
GTA subsequently reached on-foot gameplay, enabled native player control, a
connected controller and ready adapter. A 32-bit inspection verified the executable
and all three native modules belonged to the staged runtime. Runtime source is
`b403377481a33e407aeb81b78b8d38984aac4735`; runtime files were not changed.

A private 32-second frame take started before mounting. The existing evaluator
observed a fresh worker mount, but no fresh push/steer attempt verdict arrived.
Lifecycle messages recorded `surface/input/time unavailable - GTA restored`;
actual native player control and owned-camera destruction then passed. This
message does not identify which prerequisite failed. The owner reported entering
Skate briefly, with no board or skating animation; later they reported forward
movement and unreliable triggering on apparently flat ground. This is partial
owner-reported behavior, not measured both-direction steering or full acceptance. The take was encoded with its original frame timing and opened in the PC evidence viewer. It has low frame rate
and no audio; it is an incomplete trial, not accepted sustained riding.

A second recording/playback attempt refused its prerequisites before input. GTA
was still running but native status was unknown/stale. A later read-only health
check twice found the window responsive, minimized and not foreground; CPU time
advanced while the snapshot remained stale and matched the same process. This
does not establish a crash or diagnose the earlier ride termination. The owner
was asked to restore and focus GTA; no window manipulation was automated. No valid clip came from that second attempt.

A later focused take sustained
mount until requested F6 cleanup, with native GTA control/camera restoration, but
still no F8 observer-start marker. Its 31.84-second timeline was retained. The
next take refused mounting above 0.05 m, retained GTA control, and preserved a
31.76-second timeline. Both clips were encoded with original timing and opened
locally; low frame rate/no audio remain limitations. A longer F8-hold experiment
could not run because mounting refused, so its hypothesis remains untested. No
restart repeat passed. All attempts have private SSH-readable records. No paired
GTA checkpoint readings were collected; street agreement remains inconclusive.

Universal Modder's official shot/record help passed from isolated source revision
`550651675153070cce68066e07c3c8f95df86d08`. The bounded Windows FFmpeg lookup found
none; no UM recording or dependency installation was performed. Existing screen
capture plus Linux encoding supplied the first take. Shared mouse automation stays
stopped; private trial keyboard helpers refuse unless GTA is already focused.

The installed private observer was checked against its manifest, current source
and startup reference: all matched, and it uses the reviewed Windows evaluation
key command. This rules out that specific old-observer mismatch, not every input
or native-return issue. The 5×5, 8-unit surface guard supports a narrow flat patch;
one unit equalling one metre remains an assumption. A visually flat road can
include grade, curb or edge within the wider sampled square. No such cause was
independently measured for a refused location.

## Why presentation is missing

The pinned Skate Session already evaluates root and solved bone poses. The GTA
worker validates the complete pose but reduces its response to `[x,y,z,heading]`.
The GTA script positions a stock pedestrian and chase camera; it creates no board
and applies no solved bones. This explains the owner's visual observation.

At upstream pin `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, MW2 retains the full pose,
[retargets its soldier rig and skins the board](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rig.rs),
then [adds board geometry to rendering](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/occupancy/remote_body.rs).
Five inspected public source files matched that exact Git pin. No private asset
availability was inferred from their loaders. MW2 material/vertex output and bone
names are specific to its host; importing animation files alone supplies neither
a GTA drawable nor a GTA skeleton mapping.

## Next bounded objectives

The owner invoked ask-matt and wayfinder to chart reliable ground, board and
rider presentation, and GTA recovery. First acceptance scope and rider appearance
remain questions for the owner; no GTA map/tickets have been published. Existing
riding tickets and the retired Fortnite map remain preserved. The map should
resolve contact, drawing and observation decisions before producing a new spec.

The existing implementation still needs to complete and record the guarded push/both-steering/dismount/normal-walking loop,
then repeat after normal restart. Retain failures and source/gameplay acceptance
separately; #20 remains open and #21/#22 remain blocked.

For presentation, first prove a supported drawing interface on GTA IV 1.2.0.59.
Then show a visible board driven by the same accepted Session pose and remove it
on dismount or failure. Follow with solved rider animation and feet/deck alignment.
The exact GTA drawing/skeleton interface remains unresolved. This report does not
authorize a version downgrade or select an invented native API. Actual street mesh,
curb/wall contact and ordinary vehicle recovery remain separate requirements.
