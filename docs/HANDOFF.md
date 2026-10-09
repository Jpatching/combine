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
The [guide-driven proof](../research/results/2026-10-09-guide-driven-proof.md)
selects the next investigation using the owner-delegated technical judgment.
It preserves both candidates; permanent process placement remains undecided.

Latest runtime evidence: fresh read-only checks found one GTA process, a stale
status file and `Scene=unknown` / `CanTest=false` from the source-matched reader.
The installed public publisher script matches retained source; 32-bit inspection
found the adapter and CLEO loaded. The cause of stale publication is unresolved.
No game launch, input, staging or riding trial occurred. See the guide-driven proof
for scope and limitations. Earlier mount refusals remain tied to
[their dated revision](https://github.com/Jpatching/combine/issues/20#issuecomment-6078907484).

## Next step

The owner delegated technical selection to the guides; do not repeat the
integration-versus-fidelity-versus-world-interaction questionnaire. Use the
[guide-driven proof](../research/results/2026-10-09-guide-driven-proof.md): reuse the
dated fixed-input/pose evidence, then qualify the complete real-host handover.
First diagnose stale status publication, with a fresh process-bound observation
as the feedback condition. Do not infer collision or mount failure from unknown
state. REA is reserved for a specific shipped-artifact/native question source
cannot settle; no native provider or analysis session is claimed ready.

Keep rebuilt-Skate behavior distinct from original-game equivalence. Research PR
approval accepts the findings; live game actions and installation changes remain
subject to the runtime task boundary. No permanent architecture is selected.

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
For a fresh session, read this handoff, #28 including comments, PR #29 and its linked
research reports before acting; do not infer that the cited repositories contain
everything needed to reproduce the desired gameplay.
Preserve private evidence, tools and original installations. Source checks,
runtime observation, owner acceptance and release are separate claims.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md),
[workbench guide](WORKBENCH.md) and [glossary](../GLOSSARY.md)
retain the integration constraints and prior evidence.
