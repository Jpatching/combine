# Current context

## Current task

Reviewed: 2026-10-14

Task: implement the owner's ground-responsive riding, solved Skate animation and faster mounting request under [#64](https://github.com/Jpatching/combine/issues/64), with usable riding [#20](https://github.com/Jpatching/combine/issues/20) and evidence workflow [#61](https://github.com/Jpatching/combine/issues/61). The integrated source adds in-process warm remount, measured mount observation, chat-focus return and strict WBD dictionary inspection. Full ground coverage and visible animation remain incomplete.

Source branch: `integration/gtaiv-skate-spec64`

Source revision: `307ff7d7d1e21b714b8fefe5fdf6d9939831d3f6`

Worktree: `.private/worktrees/gtaiv-skate-spec64` under the primary checkout.
The candidate PR owns its final publication revision. Preserve the unrelated
`tools/workbench/hub.js` edit in the primary checkout.

Disposition: [draft PR #69](https://github.com/Jpatching/combine/pull/69), awaiting runtime qualification and owner acceptance; retain earlier candidates including [#62](https://github.com/Jpatching/combine/pull/62).

## Evidence

Latest runtime evidence: the retained installed worker candidate passed two F6-to-mounted observations at 439.9 ms and 475.1 ms after reuse of the retained checkpoint, with verified dismount recovery each time. These are upper bounds including key delivery and status polling, not cold Session initialization times or whole-ride acceptance. A longer ride observer refused `evaluation-observation-unavailable`; independent fresh normal control and released keys reconciled its named recovery record. A measurement persistence error was corrected and its original completed result retained and independently reconciled. Chat typing focus was restored after the bounded trials. Final read-only status found one responding windowed GTA process outside foreground, with fresh gameplay/control state unknown. No new candidate artifacts, reload, restart or animation were installed; the retained no-video option means no new representative clip or owner acceptance is claimed.

Exact-source standalone in-process trials measured 27,119.066 ms cold and 17.875 ms normal remount. Fresh slope collision, idle pose/tick refusal and reset from another thread passed; deliberately retaining old collision failed the regression. The complete authored native ramp/fault/recovery suite passed. First cold initialization remains unchanged, and this alternative backend has not been staged into the running worker candidate.

An owned WBD now passes structural dictionary inspection, including explicit box metadata. Complete polygon supply still refuses `unsupported-box-geometry`; box contact semantics, instance placement and automatic floor selection remain unresolved. Structural parsing does not supply a qualified live floor or moving coverage.

Candidate overlap replacement is source-tested, not staged: prepared patches
have no qualified neighbors. The focused local collision query traced the ground
native and two helpers in an analysis matching the isolated executable, but did
not qualify a nearby-geometry interface or callable native contract. Private
verdict: `.private/tooling/ground-query-analysis/verdict-private.json`.

Parallel worktrees: `.private/worktrees/gtaiv-board-presentation` owns named solved
pose transport; `.private/worktrees/gtaiv-character-presentation` owns character
feasibility and has no source changes. Board/rig assets exist; GTA model conversion,
bind qualification and the exact-version per-ped bone-write phase remain unresolved.
Transport checks do not establish visible rendering or usable riding.

## Next step

Resolve complete geometry and its instance placement, then the actual supporting floor, before claiming #65/#66. Prove the exact-version GTA character bone-update interface before #56/#67; solved pose transport alone is insufficient. First cold preparation needs a separate measured improvement; normal remount caching is now source-tested. Preserve the current worker architecture until a matching, reviewed runtime comparison establishes a reason to change it. The complete ride/camera/ordinary walking baseline and owner acceptance remain open.

Reuse the retained focused analysis rather than repeating full executable import. Keep
native staging and game input with one operator. Preserve the existing unfinished
launch/reload tooling; it is not a qualified deployment path. Board transport
requires matching parent and worker wire versions when staged.

## Session close

Follow [context maintenance](agents/current-context.md). Publish source-safe
checks and trial verdicts on the existing candidate; retain private evidence
locally. Owner acceptance remains required before merge.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [coverage/presentation research](../research/results/2026-10-13-gtaiv-coverage-and-presentation.md).
Earlier evidence remains in the linked issues and retained records.
