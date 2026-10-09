# Current context

## Current task

Reviewed: 2026-10-09

Task: [#25 — workbench approval-flow follow-up](https://github.com/Jpatching/combine/issues/25).
The owner requested automatic local evidence presentation, explicit approval before
merge and fewer bookkeeping commits. #25's original source setup is closed;
this requested follow-up does not reopen its completed setup criteria.
Fetch its body and comments for the current PR disposition.

Source branch: `fix/evidence-before-approval`

Source revision: `b983ee2d0c1d68dedbd809dad8a138f189d9b5dd`

This is the base revision; the follow-up candidate is identified by the branch
and its PR, avoiding a self-referential commit.

Disposition: candidate awaiting owner approval. No PR exists at preparation;
publication and the final revision are recorded on #25. Earlier setup merged in
[PR #26](https://github.com/Jpatching/combine/pull/26).

## Evidence

Latest runtime evidence: the automatic evidence command requested Windows viewers
for the existing synthetic walkthrough and screenshot. The owner confirmed that
the evidence opened; acceptance remains pending. This is not GTA gameplay.
The new command opens local evidence by default and retains `--print-only`.
Source checks cover viewer routing, literal filenames, invalid files and failures.

The [GTA diagnosis](https://github.com/Jpatching/combine/issues/20#issuecomment-6078907484)
remains tied to `b403377481a33e407aeb81b78b8d38984aac4735`.
A fresh read-only check using the preserved branch's status module returned
unknown native state and `CanTest=false`. The current checkout lacks that module,
so the old runtime helper cannot be used unchanged. No new successful ride or
surface root cause is established by this follow-up.

## Next step

Present evidence, obtain explicit owner approval, then squash merge the reviewed
candidate and synchronize main using the [workflow](agents/issue-tracker.md).
Keep owner confirmation separate from a successful viewer launch.

The next gameplay behavior remains [#20 — Mount -> move -> dismount](https://github.com/Jpatching/combine/issues/20).
Use `diagnosing-bugs` with the current refusal and the same scenario after a fix.
Retain `integration/gtaiv-skate-loop` and [draft PR #23](https://github.com/Jpatching/combine/pull/23).
#21/#22 remain blocked. Follow the [workbench guide](WORKBENCH.md) for the reviewed
Universal Modder and Reverse Engineer Anything tooling and private evidence rules.

## Session close

Follow [context maintenance](agents/current-context.md). Bundle handoff updates
with the source slice; record the final merge revision on the issue.
Preserve private evidence, tools, original installations and recovery branches.
Source checks, runtime observation, owner acceptance and release are separate.

## Historical reference

The [retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md),
[host decision](adr/0001-preserve-offline-gta-gameplay.md) and
[glossary](../GLOSSARY.md) retain the integration constraints and prior evidence.
