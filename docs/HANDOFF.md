# Current context

## Current task

Reviewed: 2026-10-11

Task: research windowed GTA IV iteration alongside [ground qualification #39](https://github.com/Jpatching/combine/issues/39).

Preserve the owner's windowed testing preference and investigate existing tools
for faster local AI-assisted iteration. This is a source-only research side
task; the live ground experiment remains pending.

Source branch: `research/gtaiv-windowed-iteration`

Source revision: `82d35ad1e43620389abb69fa6bcb591cca1d6279`

This is the synchronized-main starting point; the draft PR owns the final
publication revision.

Disposition: source-only research in progress; no PR exists yet. The standing
window-mode instruction is in [AGENTS.md](../AGENTS.md). Runtime settings and
installed binaries have not been changed by this research task.

The current request selects this work instead of the older Sandcastle task
snapshot. Retained source branches and drafts stay preserved: ground
[PR #57](https://github.com/Jpatching/combine/pull/57), collector
[PR #58](https://github.com/Jpatching/combine/pull/58), and parent riding
[PR #23](https://github.com/Jpatching/combine/pull/23). The newer implementations
are on those retained branches; this research branch starts from main and does
not integrate them.

## Evidence

The research report is
[windowed iteration tools](../research/results/2026-10-11-gtaiv-windowed-iteration-tools.md).
It separates upstream capabilities, retained source, prior execution evidence,
local qualification gaps and recommendations. Documented hot reload is not a
passed trial on the installed runtime. No tool installation, script reload,
runtime staging, keyboard input or gameplay trial occurs in this source task.

The owner has already
[confirmed that the retained checkpoint pictures show the intended surfaces](https://github.com/Jpatching/combine/issues/39#issuecomment-6112509746).
Reuse that confirmation. Independent loaded collision and intended-layer
evidence remain unqualified. The prepared physical-state probe observes the
actual player position and leaves contact, loading and layer unknown; it does
not associate that position with a checkpoint by itself.

Latest runtime evidence: a read-only Windows check found one responding GTA IV
process, minimized and outside the foreground. Fresh unmounted gameplay and
player control were not established. Window mode itself was not verified.
Earlier retained runtime, diagnostic candidate and recovery backup hashes
matched; no active staging transaction was present at that check. These are
separate observations, not a live support or riding pass. Private raw evidence
stays local. Persistent Windows execution policy was not changed.

## Next step

Finish source review and the repository gate, publish the research as a draft,
and keep owner approval and merge separate. Qualify existing hot reload and
observer capabilities on the exact retained runtime before claiming a faster
loop; measure setup, trial, recovery and total time against the previous loop.
The proposed capability qualification is future runtime work, not an execution
claim or an instruction to install a different hook.

Resume the one-checkpoint support experiment through `grill-with-docs`. The
independent contact/layer observable remains unresolved. The owner restores
and focuses GTA; testing preflight must establish windowed gameplay readiness.
Keep the existing collector's foreground refusal and input ownership. Once the
support method is qualified explicitly on #39, collect three valid readings at
each of R1/P1/H1/H2 with the unchanged maximum 2 cm spread and 5 cm mesh error.
Ambiguous evidence remains inconclusive. Geometry placement stays fixed.

[#54](https://github.com/Jpatching/combine/issues/54) retains its qualification
and source-acceptance blockers before triangle-route activation and the recorded
mount, push, steering, dismount, recovery and restart repeat. Board #55 and
rider #56 remain downstream; complete riding acceptance stays under #20.

## Session close

Follow [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Keep GTA IV windowed during
testing as required by AGENTS. Preserve installed runtime files, private recovery,
retained branches, collector bundles and resource placement. Keep assets,
coordinates, identities, media, settings and raw logs outside Git and AI uploads.
The repository gate passed 62 tests and 60 document/context checks; whitespace
checks passed. Independent Standards and Spec reviews reported zero actionable
findings. Source research, capability qualification, ground qualification,
gameplay and owner acceptance remain separate claims.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[retained native proof](https://github.com/Jpatching/combine/blob/45d409a1b6e8bb72d6f5361355c44c58228892c4/research/results/2026-10-11-gtaiv-native-refusal-proof.md),
[collector source](https://github.com/Jpatching/combine/blob/a1e456cebcebdbc2b3a59033edfbc4629db0f0ab/tools/gtaiv-collision/README.md),
[physical collision report](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md).
