# Proposed next slice: one repeatable launch on Rust

After the replacement menu is accepted, give the player one loop:

```text
Save launch point -> set stationary target -> launch on foot -> attempt shot
        ^                                                        |
        +------------------------ reset -------------------------+
```

Reuse Positions and Targets. Add one typed action that applies a fixed impulse
after confirming local authority, a valid saved launch point and an on-foot,
living player. Use one measured impulse; no tuning screen in this slice.
Reset returns to the saved point. Missing point/target, map changes or a blocked
launch produce menu feedback and no impulse. Map changes invalidate the launch.

First implementation step: inspect the upstream movement/authority path for a
supported impulse action and demonstrate a single local launch. Do not simulate
it with teleport loops or invent a new networking interface. Record the chosen
impulse and landing behavior before adding menu controls.

Acceptance: on Rust, the owner completes three attempts with the controller,
without console commands: save, target, launch, attempt shot, reset. Verify no
unintended firing, original files unchanged, clear failure feedback and map
invalidation. Synthetic input tests supplement those three observed attempts.

Exclude firing while skating, map editing, another game integration, variable
launch presets and shared/public matches. This proposal is recorded only; no
stunt-launch action is implemented or accepted.

## Owner's broader direction

After seeing the replacement, the owner asked for more gameplay options,
including “EB”, and a bigger crossover using their game library. The owner confirmed EB means explosive bullets;
preferred titles remain open. The first launcher scope above remains
unimplemented; do not infer authorization to add arbitrary Synergy features.

A promising separate research candidate is classic GTA San Andreas + Skate 3 +
MW2, documented by PipeLink. City skating into rooftop trickshot attempts is a
proposed experience, not verified compatibility with our current menu. See the
[research findings](RESEARCH.md#bigger-crossover-ideas-after-the-menu--2026-10-03).
