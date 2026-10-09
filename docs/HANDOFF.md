# Current context

## Current task

Reviewed: 2026-10-09

Task: [#28 — review the integration approach and investigation process](https://github.com/Jpatching/combine/issues/28).
The owner requested research into Reverse Engineer Anything (REA) and Universal
Modder before deciding how Combine should shift. Do not assume that diagnosing
mount refusal is the right next task. The existing goal remains actual Skate
mechanics inside offline GTA IV with ordinary host gameplay preserved.

Source branch: `research/integration-approach-review`

Source revision: `fb2be7fb852cb3985b5af31dda54bbb18acac4e9`

This is the synchronized main base. The research candidate is identified by its
branch and PR; fetch #28 for publication and final revision.

Disposition: [draft PR #29](https://github.com/Jpatching/combine/pull/29) awaits
owner approval. The source-interface audit extends the same research requirement;
publication and review status are recorded on #28. The earlier workbench follow-up
was owner-approved and squash-merged in [PR #27](https://github.com/Jpatching/combine/pull/27),
as recorded on [#25](https://github.com/Jpatching/combine/issues/25#issuecomment-6082420092).

## Evidence

The [approach review](../research/results/2026-10-09-integration-approach-review.md)
compares the two guides, the preserved candidates and evidence-supported
alternatives. The follow-up [repository interface audit](../research/results/2026-10-09-repository-interface-audit.md)
checks concrete source interfaces, exact revisions and remaining replication gaps.
Recommendations are research findings, not an architecture decision.

Latest runtime evidence: no new runtime trial belongs to this research task.
The [GTA diagnosis](https://github.com/Jpatching/combine/issues/20#issuecomment-6078907484)
remains tied to `b403377481a33e407aeb81b78b8d38984aac4735`; mount refused above
0.05 metres and no surface root cause or complete accepted ride was established.
The later workbench check reported unknown native state and `CanTest=false`;
its old helper depends on a status module absent from main. Reconcile source,
helper and installed runtime before any separately authorized live trial.

## Next step

Review the research and source-interface audit with the owner using `grill-with-docs`.
Keep the distinction between the reused rebuilt Skate simulation and the original
Skate executable explicit; behavior parity is not established. Decide which
uncertainty to test before choosing further implementation. Research
PR approval accepts the written findings; it does not authorize a proposed runtime
experiment or select a permanent architecture. If the findings reveal a larger
unresolved effort, use `ask-matt` to route the next phase before creating build tickets.

Retain [#20](https://github.com/Jpatching/combine/issues/20),
`integration/gtaiv-skate-loop` and [draft PR #23](https://github.com/Jpatching/combine/pull/23).
#21/#22 remain blocked. Preserve the in-process and worker candidates, prototypes
and recovery branches. The separate collision-feasibility research prerequisite
recorded on #20 is not satisfied by this public-source survey.

## Session close

Follow [context maintenance](agents/current-context.md) and the
[issue/branch/approval workflow](agents/issue-tracker.md).
Bundle research and handoff updates; record final publication/merge state on #28.
Continue this research/decision phase in the current context while practical.
For a fresh session, read this handoff, #28 including comments, PR #29 and both
research reports before acting; do not infer that the cited repositories contain
everything needed to reproduce the desired gameplay.
Preserve private evidence, tools and original installations. Source checks,
runtime observation, owner acceptance and release are separate claims.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md),
[workbench guide](WORKBENCH.md) and [glossary](../GLOSSARY.md)
retain the integration constraints and prior evidence.
