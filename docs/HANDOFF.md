# Current context

## Current task

Reviewed: 2026-10-13

Task: consistent riding on the correct floor under [#64](https://github.com/Jpatching/combine/issues/64), with usable-ride prerequisite [#20](https://github.com/Jpatching/combine/issues/20) and evidence workflow [#61](https://github.com/Jpatching/combine/issues/61). Current experiment: shorten startup and qualify dismounted JavaScript-only reload without restarting GTA.

Source branch: `integration/gtaiv-skate-spec64`

Source revision: `5b5f6dd57a8b7e1608baecafcc1702ce75afda02`

Worktree: `.private/worktrees/gtaiv-skate-spec64` under the primary checkout.
The candidate PR owns its final publication revision. Preserve the unrelated
`tools/workbench/hub.js` edit in the primary checkout.

Disposition: [draft PR #69](https://github.com/Jpatching/combine/pull/69), awaiting runtime qualification and owner acceptance; retain earlier candidates including [#62](https://github.com/Jpatching/combine/pull/62).

## Evidence

Latest runtime evidence: reload qualification stopped at startup. Fresh checks found GTA closed, tested keys released and installed files matching the retained manifest. One guarded windowed launch returned `window-not-ready`; the monitor timed out waiting for a process. No gameplay keys, termination or script replacement occurred; reload remains unqualified.

The latest candidate PR records a prior no-video mount followed by conflicting
evaluation and restored normal controls. Its auxiliary pose was invalid; it does
not prove a floor defect or a successful ride. This supersedes the stale F8-held
blocker previously in this handoff. Owner-observed mounting remains bounded to
the teleport spot; prepared surfaces have 3 m radii and do not establish coverage
elsewhere. Earlier H2 stacked-floor qualification remains reusable. Installed
riding source remains the earlier staged candidate; terminal-stop labels in this
branch are source-only. Prior recovery and independent-script backup are retained.

## Next step

Resolve the launch boundary first: the ordinary launch did not establish a
stable game window; its cause is unknown. Preserve the private launch record
and change one diagnostic variable before another attempt. Then recheck
released keys, windowed operation, installed identities, dismounted
controls/camera and watchdog readiness. Reuse the qualified floor. Back up the
installed riding script, atomically replace only a temporary startup log marker,
and establish CLEO executed it in the same GTA process. Prove remount, movement,
dismount and control restoration, then restore the original script through the
same path and verify its hash/readiness. Stop at the first failure and diagnose
that boundary. Native plugin, worker and definition changes require closed-game
staging. Record a proven reload procedure in the [adapter guide](../tools/gtaiv-skate/README.md).

## Session close

Follow [context maintenance](agents/current-context.md). Publish source-safe
checks and trial verdicts on the existing candidate; retain private evidence
locally. Owner acceptance remains required before merge.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [coverage/presentation research](../research/results/2026-10-13-gtaiv-coverage-and-presentation.md).
Earlier evidence remains in the linked issues and retained records.
