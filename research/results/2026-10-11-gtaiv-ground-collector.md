# Bounded GTA ground collector preparation

Reviewed: 2026-10-11

The owner selected a focused child branch, `implement/gtaiv-ground-collector`,
stacked on retained `implement/gtaiv-qualified-ground` at
`4677e1616b8d41e218f08bdbf13139b73f3ab45d`. This is the authorized exception to
the normal new-slice-from-main convention. The source-safe collection work
advances [#39](https://github.com/Jpatching/combine/issues/39); it does not activate
blocked [#54](https://github.com/Jpatching/combine/issues/54) or replace draft #57.
Reviewed implementation: `3fef129c39e61e97c278c156562e6a85719f53d7`, published in
[draft PR #58](https://github.com/Jpatching/combine/pull/58). Owner acceptance
and live qualification remain pending; the issue records publication follow-ups.

The [collection command](../../tools/gtaiv-collision/README.md#collect-qualified-ground-readings)
checks the complete candidate inventory and exact prepared script before one
guarded trigger. Its observation adapter reuses the reviewed current-run log
reader's byte boundaries and quoted-record handling. The diagnostic reuses the
existing plugin-owned guarded float buffer and pairs actual native boolean
success with the written height. It has no movement or camera writes and never
classifies loading/layer from character flags or height agreement.

The command keeps one private bundle, including partial observations and failed
attempts. It invokes the unchanged comparator for R1/P1/H1/H2 only. Additional
named points preserve their own coordinates/evidence without entering that gate.
An optional exact-hash private recovery script uses the retained transaction;
all retained artifact bytes must match after cleanup. Restoration failure
remains explicit. Compatible repeats require no new plugin installation or
restart; replacing a loaded plugin still requires normal shutdown/restart.

## Independent evidence remains unresolved

All 16 existing checkpoint views were requested through the repository's local
evidence viewer. No pixels were uploaded to the AI. The repository prohibits
private media uploads, so exact R1/P1/H1/H2 surface/layer interpretation still
requires local owner inspection. A viewer request is not interpretation,
viewing confirmation or owner acceptance. No new capture was made.

Ordinary physical support is a candidate independent loading witness, not an
accepted flag. The diagnostic retains character position, velocity, height,
air/stopped/waiting/dead/water/injured state before and after queries. A stopped
character, `waiting=false` or agreement with character height can occur without
identifying the intended floor; the height native may depend on the same ground
mechanism. Observations at the player's position also cannot establish loading
at another checkpoint. A validated method must distinguish unloaded/wrong-layer
cases at independently associated unchanged points. No such validation or
owning-issue acceptance decision has occurred. Verdict: **inconclusive**.

The source refuses live execution before complete intended surface/layer
associations. Missing independently established loading/layer witness references
remain unavailable in the comparison, regardless of native success. The frozen
three readings, 0.02 m spread and 0.05 m per-reading error rules are unchanged.

## Source verification and limits

The first authored public-command test failed because the command was absent,
then passed after implementation. Later command tests caught and corrected
decimal readings retained as strings, restoration failure lacking a failed
status, and unintended writes into an existing bundle directory. Twelve command
tests currently pass, covering complete/missing/unavailable observations,
coordinate mismatch, unknown evidence, stale process/status, lost focus,
interruption, artifact mismatch before execution, restoration failure, additional
points, non-executing preparation and existing-bundle preservation. Review
follow-ups require complete additional-point collection and confirmed observer
exit before restoration. An authored external-process adapter verifies timeout
refusal without running Windows or sending keys. The native input guard now
checks focus immediately before key-down, refuses a held F8 and releases only
an accepted command-owned press.

`node --check tools/gtaiv-collision/ground_probe.js` and Python compilation pass.
Actual Windows PowerShell parsing initially found a multiline condition error;
the corrected observer parses. Its C# window/input interop also compiles without
executing input or the observer. These checks do not execute CLEO native calls,
the log protocol, staging or recovery against the game.

The command retains Python preflight, backend wait and total duration, plus
Windows setup before the pulse and observation duration. Its restart
metric observes the before/after process identity across recovery, rather than
assuming an exit-zero recovery script restarted GTA. Missing final identity
remains unknown; prior setup and intermediate restarts are outside this metric.
No live timing baseline,
new checkpoint measurements or demonstrated speed improvement exists yet.
Foreground sampling cannot exclude changes between samples; file hashes/times
do not instrument loaded process memory. Exact retained-byte restoration is
distinct from fresh restarted gameplay. No new staging, game restart, ground
agreement, riding, board/rider acceptance, merge, deployment or release occurred.
Independent Standards and Spec reviews found several input/cleanup and evidence
reporting defects, all corrected. Final staged source reviews have zero remaining
actionable findings on each axis. They inspected source and authored tests;
they did not reproduce private runtime checks. The repository gate passed 91
tests and 70 document/context checks; final publication results remain on the
issue/PR.
