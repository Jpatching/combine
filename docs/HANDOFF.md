# Handoff — actual Synergy integration, 2026-10-04

The owner explicitly wants **Synergy itself**, not our native imitation. D-015
records the correction. The current source patch runs the original pinned GSC
through the mashup's existing engine. A Windows diagnostic observed its HUD,
open/navigation, Intervention equip/hold, back and close. An offline match-data
script error remains; this is **implementation in progress**, not ready for an
owner trial, accepted, published, merged or released.

Read [actual-script evidence](../research/results/2026-10-04-synergy-gsc.md),
[menu requirements](TRICKSHOT_MENU.md) and the same
[C-016 draft](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=261972158).
The private Project owns status. Owner choice is settled; Codex acts next.

```text
Pinned Synergy GSC -> existing compiler + local game scripts -> actual menu
                           | error -> fix and rerun checks
                           v
                verified exact build -> owner review folder -> verdict
```

Branch `slice/intervention-review`; prior tested native commit
`730b11354934b43c2ca703aec615ea31d3e77f2e`; actual-script patch follows it.
Use `git log -1` and `git status --short` for the checkpoint containing this
handoff. Source pins remain unchanged. Public `origin` is
`https://github.com/Jpatching/combine`; creation and access were verified, but no
source push/PR/merge/release occurred. Current project instructions require owner
replacement acceptance before source publication. Private assets/logs/settings
and earlier trials are preserved. Deferred Hide HUD is unchanged and excluded.

The earlier native build and three local commits are documented in
[preserved Intervention evidence](../research/results/2026-10-04-intervention-review.md).
Its 17 native tests and 720p/1080p previews do not verify the new GSC integration.
Shared helper checks passed: 15 Python board/hook and 14 Windows bundle fixtures.
No further workflow setup is needed to continue the menu work.

Next: fix and verify the actual-script integration's offline error and input
handling, then supply a fresh exact-build trial with launch/files/checklist
shortcuts. Do not prepare the rejected native build as the replacement. Baseline
recovery/replay, the earlier possible freeze and audio listening acceptance remain
inherited gaps; use their existing result records only when relevant.
