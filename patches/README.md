# Native trickshot menu patch

`trickshot-v0.4.0.patch` applies to the mashup runtime at
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. It carries the local practice actions,
typed menu state, input isolation, native renderer, tests and preview example.
It contains source only. Follow [build and trial steps](../docs/TRICKSHOT_MENU.md).

The navigation and presentation derive from Synergy MW2 at
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`, by SyndiShanX. Synergy credits M203 by
Xeirh and the Apparition Structure Team (CF4_99, Extinct, ItsFebiven, Joel).
Adapted functions: initial_variables, create_menu, input_manager, open_menu,
close_menu, set_menu_visibility, new_menu, scroll_cursor and set_options.

The patch adds COMBINE-NOTICE.md and a verbatim GPLv3 licence to the runtime;
the licence is also [preserved here](../licenses/Synergy-GPL-3.0.md). The console
crate containing the adapted menu declares GPL-3.0-only. Existing runtime
Apache-2.0 LICENSE/NOTICE and source notices remain unchanged. No Synergy GSC,
IW4x binaries, shaders, retail data or unrelated gameplay modifications are added.
This is a source-derived native port, not an unchanged Synergy installation.

`skate-audio-v0.4.0.patch` is a separate follow-on: apply it **after** the menu
patch. It adds native skating-event cues and optional local WAV playback. It
contains no samples, music, recordings, extractor code, new recipes or network
interface. Existing runtime licences/notices remain in force. The music cue
starts on entering skating or Christ Air and never overlaps itself. See the
[audio result record](../research/results/2026-10-03-skate-audio-highlights.md) for
setup, tests and the still-unverified listening assignment.
