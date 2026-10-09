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

Latest runtime evidence: on the retained staged candidate `b403377481a33e407aeb81b78b8d38984aac4735`,
restoring the minimized GTA window changed stale status into fresh validated
gameplay with testing available. A bounded mount attempt then refused at
`over-0.05-metres` before movement playback; fresh GTA control remained available.
The game and three expected native modules were observed under the staged runtime.
A subsequent owner-requested window change was verified at 1280×720 with fresh
gameplay status. These are isolated observations, not completed riding acceptance.
No runtime source or tolerance was changed. Private evidence remains local.

## Next step

The owner selected Universal Modder's rebuilt-guest-in-real-host route and asked
us to assess the missing world-collision connection. The existing route already
fits that classification; this selects the investigation direction, not a new
engine or a permanent choice between worker and in-process placement.

Use the [world-collision next proof](../research/results/2026-10-09-world-collision-next-proof.md)
to distinguish reusable source from exact-version gaps and qualify the smallest
host-geometry observation before designing a broader adapter. Preserve the flat
patch as a limited diagnostic. Do not repeat its unchanged mount refusal or
relax its 5 cm guard as a substitute for world collision. The earlier
[guide-driven proof](../research/results/2026-10-09-guide-driven-proof.md) remains
useful for control handover and recovery, but its stale-status diagnosis is no
longer the immediate next task.

Keep rebuilt-Skate behavior distinct from original-game equivalence. Retain
[#20](https://github.com/Jpatching/combine/issues/20),
`integration/gtaiv-skate-loop`, [draft PR #23](https://github.com/Jpatching/combine/pull/23),
both candidates and recovery branches. #21/#22 remain blocked. The separate
research-capable Sandcastle prerequisite recorded on #20 remains unmet: this
session exposes no such connected tool. Public-source preparation does not
satisfy that prerequisite or establish a working collision bridge. REA native
provider/session readiness is also unestablished.

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
