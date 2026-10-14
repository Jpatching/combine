# GTA IV Complete Edition presentation interfaces

Source findings retained from [research PR #50](https://github.com/Jpatching/combine/pull/50).
These describe inspected interfaces, not current installed behavior. [#55](https://github.com/Jpatching/combine/issues/55)
owns solved board presentation; [#56](https://github.com/Jpatching/combine/issues/56)
owns the exact-version bone interface and [#67](https://github.com/Jpatching/combine/issues/67)
owns GTA rider animation. Current candidate and runtime evidence belong to [#61](https://github.com/Jpatching/combine/issues/61).

## Solved pose and converted data

At upstream `f608f85e407ff1b7689d54a9aafdd16e95711ac4`, the [Skate Session](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/skate/crates/skate-host/src/physics/bridge.rs)
returns root and bone matrices, names, camera and deck velocity. Deck velocity
alone does not define deck orientation. The [board exporter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/assets/src/skate_board.rs)
derives rig and weighted board geometry from the private GLB; those intermediate
files are not GTA-native models.

The [MW2 rig adapter](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/rig.rs)
skins board vertices from solved joints and retargets the rider using host bind
frames. Its bone names and proportions are host-specific. The [MW2 conversion](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/f608f85e407ff1b7689d54a9aafdd16e95711ac4/crates/render_anim/src/skate/collision.rs)
uses inches-to-metres scale `0.0254`; that is not evidence for GTA scale.

## Exact-version limits

- [CLEO Redux documentation at bbf6773](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/docs/en/introduction.md)
  explicitly lists CE 1.2.0.43/1.2.0.59. Its [SDK](https://github.com/cleolibrary/CLEO-Redux/blob/bbf6773fe8cc1bfa95c73509a25928f97b0d8d13/SDK/cleo_redux_sdk.h)
  supplies script/plugin callbacks, not a documented arbitrary bone-palette or
  render-thread interface.
- [Sanny Builder definitions at 34bedee](https://github.com/sannybuilder/library/blob/34bedee0be2f57047ed8f0705c81f137ede3d3ce/gta_iv/gta_iv.json)
  declare model/object lifetime and transform calls, animation tasks and bone-position
  queries. A bone-position getter or clip-time setter does not apply solved joint
  matrices. Definitions alone do not qualify signatures or lifecycle on CE.
- [IV-SDK at dddbd3f](https://github.com/Zolika1351/iv-sdk/blob/dddbd3f54b146bdb3a9852809e48e5cb169af3cd/README.md)
  supports 1.0.7.0/1.0.8.0 EFIGS. [LibertyCraft at 83dcdfe](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/README.md)
  targets 1.0.8.0. Its [render code](https://github.com/mrborghini/libertycraft/blob/83dcdfe2dd710d1b51d65dd7f3644f82b365e406/asi/src/Render.cpp)
  illustrates render-thread scheduling, depth and state restoration; it supplies
  no CE-qualified draw hook or skeleton setter.

Asset conversion can supply a model, but does not supply live pose transport,
retargeting or resource cleanup. A rigid board can demonstrate solved deck
orientation without establishing weighted truck/wheel deformation. Full GTA rider
presentation still needs an exact-build write phase, joint/bind mapping and
restoration of ordinary GTA animation. These are bounded source conclusions,
not proof that every possible external interface has been exhausted.
