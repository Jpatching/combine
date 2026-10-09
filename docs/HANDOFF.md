# Current context

## Current task

Reviewed: 2026-10-09

Task: [#30 — enable bounded public-source research in Sandcastle](https://github.com/Jpatching/combine/issues/30).
The owner approved three tickets to distribute the next GTA/Skate investigation.
[#31](https://github.com/Jpatching/combine/issues/31) assesses an exact-version
collision-query route; [#32](https://github.com/Jpatching/combine/issues/32) assesses
physical collision extraction. Both have native dependencies on #30 and may run
independently after its research execution route is ready.

Source branch: `feat/sandcastle-research`

Source revision: `fb2be7fb852cb3985b5af31dda54bbb18acac4e9`

This is the synchronized main base. Fetch #30 for candidate revision, validation
and publication status.

Disposition: source candidate prepared; no PR exists yet. Live research
qualification is blocked on subscription reauthentication. The approach reports
remain preserved on `research/integration-approach-review` at `d6f6725` in
[draft PR #29](https://github.com/Jpatching/combine/pull/29), pending owner approval.
They are not merged into this branch's main base.

## Evidence

The owner selected Universal Modder's rebuilt-Skate-in-real-GTA route and the
world-collision investigation. Read the
[prepared next proof](https://github.com/Jpatching/combine/blob/d6f6725/research/results/2026-10-09-world-collision-next-proof.md)
and its interface-audit references. The limited flat patch remains a diagnostic;
no permanent choice between worker and in-process placement is made.

Latest runtime evidence: on the retained staged candidate
`b403377481a33e407aeb81b78b8d38984aac4735`, restoring the minimized GTA window
recovered fresh gameplay status. One guarded mount attempt refused at
`over-0.05-metres` before playback with fresh GTA control retained. A later
owner-requested window change was verified at 1280x720 with fresh status.
No accepted ride, world-collision capability or publisher code defect was proved.
These earlier observations are not runtime tests of the Sandcastle change.

Sandcastle preflight for #30 passed pinned tools, Docker access and existing
subscription login. This alone does not establish a working research job. The
new candidate adds research profiles for #31/#32 and a fixed public-source
qualification command. The first actual qualification failed before researcher
completion with `refresh_token_reused`; the source workspace and private failure
evidence were preserved. Host credentials have not changed since that failure,
so retrying the same credentials is not useful. No report or research-readiness
pass was produced. Research execution must preserve
source-only isolation, reviewed task profiles, source evidence, independent
reviews and bounded cancellation/preservation; no game/private-data access.

## Next step

Complete source review and publish #30 as a draft. Renew the host Codex
subscription login locally, then rerun `npm run research-smoke` from
`tools/sandcastle`. Do not expose login tokens or private logs. Require a real
accepted research qualification and owner approval before merge. Only then dispatch #31/#32 when all readiness checks pass. They
require Matt's original research skill and pinned Universal Modder guidance;
record actual delegation and evidence, not just a successful fixture test.

The separate research-capable Sandcastle prerequisite on
[#20](https://github.com/Jpatching/combine/issues/20) remains unmet until the
required investigation actually runs and returns its report. Native REA provider
readiness and GTA 1.2.0.59 collision-query compatibility remain unestablished.
Keep all runtime activity in the local controlled environment.

Retain `integration/gtaiv-skate-loop`, [draft PR #23](https://github.com/Jpatching/combine/pull/23),
both gameplay candidates and recovery branches. #21/#22 remain blocked. Do not
resume retired Fortnite work or loosen the flatness guard to manufacture a pass.

## Session close

Follow [context maintenance](agents/current-context.md) and the
[workspace/slice conventions](agents/issue-tracker.md). Record source tests,
container/inference qualification and actual research-job results separately.
Keep authentication, raw logs, game assets and private diagnostics outside Git
and AI uploads. No automatic merge or owner gameplay acceptance is implied.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md),
[workbench guide](WORKBENCH.md), [Sandcastle guide](../tools/sandcastle/README.md)
and [glossary](../GLOSSARY.md) retain supporting facts and execution boundaries.
