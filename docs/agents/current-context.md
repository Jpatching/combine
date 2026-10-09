# Context maintenance

## Start or resume

1. Read `docs/HANDOFF.md`, then fetch its linked live issue body and comments.
   The owner's current request selects work. If it differs from the snapshot,
   use the current request and report the discrepancy.
2. Verify the directory, branch, revision and local changes using the
   [workspace conventions](issue-tracker.md). Check the source and installed
   runtime revisions separately when a runtime trial is authorized.
3. Read the issue's current verdict first. Consult linked evidence for the
   behavior being changed. Reuse qualified setup until a changed prerequisite
   or observation gives a reason to repeat it.

## Finish or transfer a task

1. Preserve source-safe decisions in the glossary/ADRs and observations in dated
   research. Link existing artifacts rather than copying transcripts. Review
   public content before staging; private runtime data stays outside Git.
2. Update the existing issue's current status when new evidence changes it.
   Identify the revision, passed behavior, blocker and next step. Keep acceptance
   criteria separate from isolated trial passes. Retain comments as history.
3. Update HANDOFF when the selected task or verdict changes. Keep these sections:
   `Current task`, `Evidence`, `Next step`, `Session close`, `Historical reference`.
   Include `Reviewed`, `Task`, `Source branch`, `Source revision`, `Disposition`
   and `Latest runtime evidence`. Link the issue and PR, or explicitly state
   that no PR exists. The snapshot points to evidence; the issue owns acceptance.
4. Stage only reviewed source-safe files and run `python3 scripts/verify.py`.
   Its context check flags untracked Markdown in `docs/`, `research/results/`
   and the root glossary without reading ignored/private files. It checks
   HANDOFF structure and links, not the truth or freshness of runtime claims.
5. Report one disposition: merged and synchronized; pushed but blocked with the
   exact blocker; or a preserved experiment with its question and verdict.
   State any remaining uncommitted work. Follow the existing review/merge gate.

## Fresh context

Use Matt's original `ask-matt` phase-boundary guidance. Continue when the next
phase needs the current reasoning. Start each independent implementation ticket
with fresh context after preserving its durable result. Compact at a boundary
when relevant context must survive and continuing is no longer practical.
Use a temporary handoff for transfer to another directory, tool or person, or
a side task; link the issue, decisions and evidence instead of duplicating them.

README and AGENTS point to HANDOFF for current status. Historical snapshots and
dated research remain references; they do not select the next task.
