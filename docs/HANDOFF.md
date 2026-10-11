# Current context

## Current task

Reviewed: 2026-10-11

Task: make GTA IV testing repeatably windowed and resume automated [ground qualification #39](https://github.com/Jpatching/combine/issues/39).

Source branch: `fix/gtaiv-current-context`

Source revision: `844fcdad69be245c4a8df9c36a6c1f1019599d5f`

This is the synchronized-main starting point for the documentation correction.
The draft PR owns the final publication revision.

Disposition: [draft PR #60](https://github.com/Jpatching/combine/pull/60) awaits
owner source approval; private runtime observations are separate.
[PR #59](https://github.com/Jpatching/combine/pull/59) is merged at
the revision above. Its earlier awaiting-approval snapshot is superseded by the
[merge record on #39](https://github.com/Jpatching/combine/issues/39#issuecomment-6113398089).
Retain ground [PR #57](https://github.com/Jpatching/combine/pull/57), collector
[PR #58](https://github.com/Jpatching/combine/pull/58) and riding
[PR #23](https://github.com/Jpatching/combine/pull/23); this branch does not
integrate those implementations.

## Evidence

Latest runtime evidence: the pinned GTA IV runtime had no persistent windowed
startup request. A read-only inspection found a minimized captioned window,
not a reproduced fullscreen transition. The owner confirmed the Rockstar
launcher and authorized restart, restore and focus for testing. Windows denied
an ordinary write to the protected runtime folder; the reviewed administrator
action then created the exact windowed startup setting. Independent byte and
executable-hash verification passed. Private recovery records preserve the
prior absent configuration. The game then launched as a new pinned process with
a captioned window. Initial activation was refused; targeted activation later
verified foreground without sending keys. The owner confirmed live gameplay.
An immediate read-only check after activation independently reported fresh
gameplay, ready/unmounted adapter, enabled player control and connected controller.
The heartbeat resumed after activation; no adapter failure was demonstrated.
This is one startup/readiness observation, not a repeatability or riding pass.

The retained private startup preflight imported a root module absent from main.
Its module pointer was corrected to the verified retained adapter checkout, with
the original backed up. The bounded menu automation ended without verified
readiness and sent no input. The owner temporarily requested free keyboard/mouse,
then explicitly revoked that restriction: use keyboard/mouse for testing with
GTA focused. Guarded testing input and controlled restore/focus are authorized;
lost focus still refuses input.

The retained F6 diagnostic first stopped before input because its transient
staging pointer was missing. Every staged and retained runtime hash matched the
saved manifest; only the missing pointer was reconstructed. Runtime bytes were
unchanged. A reviewed private runner now pins the retained clean source checkout,
uses its status module, binds key pulses to process/start identity, refuses held
keys and releases only accepted owned presses. Python and emitted PowerShell
syntax passed; the compiled key guard refused an invalid owner without input.

The repeated live attempt accepted one owned F6 pulse and observed the exact
default-route refusal `over-0.05-metres`. A sampled height differed from the centre
by more than the default flat route permits; this does not prove that the actual
floor is uneven rather than queried incorrectly. Fresh unmounted GTA control was
retained. The private clip was verified, remuxed without changing its 155 frames,
and requested in the local evidence viewer; owner viewing remains unverified.
No successful mount, push/steer or ground qualification is claimed.

The owner already [confirmed the retained checkpoint pictures show the intended
surfaces](https://github.com/Jpatching/combine/issues/39#issuecomment-6112509746).
That supersedes earlier viewing-unverified claims. Reuse the confirmation.
Independent per-point loaded collision and intended-layer evidence remain
unqualified. The prepared stationary probe leaves contact/loading/layer unknown
and cannot qualify that method alone. No qualified checkpoint readings or
skating pass have been recorded in this slice.

[Windowed iteration research](../research/results/2026-10-11-gtaiv-windowed-iteration-tools.md)
records available capabilities and qualification gaps, not required tool
installations or passed reload trials. No measured speed improvement exists.

## Next step

Resolve the observed default flat-route refusal, distinguishing a real uneven
patch from unqualified ground queries. Reuse the retained non-flat implementation
after its independent ground and source-acceptance prerequisites; do not relax
the flat-route guard or infer loaded/layer witness flags from this refusal.
Verify a normal Rockstar restart repeat when authorized to interrupt the game. Keep
collectors' lost-focus refusal and owned-input cleanup; this session's
owner-authorized restore/focus does not remove them.
Retain failures and private recovery. Resolve the independent support/layer
observable at one checkpoint under #39, then reuse collector #58 for all four.
Require three valid readings per point, at most 2 cm spread and 5 cm per-reading
mesh error, with independent loading/layer evidence. Keep geometry fixed.

[#54](https://github.com/Jpatching/combine/issues/54) retains qualification and
source-acceptance blockers before riding activation, recovery and restart trials.
Board #55 and rider #56 follow; full riding acceptance remains under #20.
Implement a focused tooling fix only for a demonstrated gap.

## Session close

Follow [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Keep GTA windowed as required
by [AGENTS.md](../AGENTS.md). Source checks, private setup, runtime observations
and owner acceptance remain distinct. Preserve original binaries, retained
branches and recovery. Settings, identities, coordinates, raw logs and media
stay private; open actual evidence locally without AI upload.
Repository verification passed 62 tests and 60 document/context checks; whitespace
checks passed. Independent Standards and Spec review found zero remaining
actionable findings; reviewers did not inspect private runtime evidence.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md),
[collector source](https://github.com/Jpatching/combine/blob/a1e456cebcebdbc2b3a59033edfbc4629db0f0ab/tools/gtaiv-collision/README.md),
[retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md).
Historical methods do not add requirements to the current task.
