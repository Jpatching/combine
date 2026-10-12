# Context maintenance

## Start or resume

1. Read `docs/HANDOFF.md` for the selected issue and source branch. The owner's
   current request takes precedence over the snapshot.
2. Read the live issue body, especially its current summary and acceptance
   criteria. Read comments or linked evidence only for a named question; a later
   explicit correction supersedes the historical claim it identifies.
3. Verify the workspace using [workspace conventions](issue-tracker.md).
   For runtime trials, check source and installed runtime identities separately.
   Reuse qualified setup until a changed prerequisite requires another check.

## Finish or transfer

Update the live issue's current summary when the verdict changes: passed behavior,
remaining blocker, candidate revision and one next action. Retain comments as
history. Keep HANDOFF a short pointer and resume note; link evidence rather than
copying trial chronology. Use glossary entries for resolved domain terms and ADRs
only for consequential decisions, following [domain rules](domain.md).

Follow [workspace conventions](issue-tracker.md) for verification, publication
and approval. The repository gate checks tracked document links and the issue
pointer; it cannot establish factual freshness or gameplay acceptance. Review
staged public content; keep private measurements, identities and media local.

## Context boundaries

Use Matt's `ask-matt` phase-boundary guidance. Continue when the next phase needs
the reasoning already here; use fresh context for independent implementation
work after preserving its result. Read historical snapshots and research by
specific question or anchor. Their old next steps do not select current work.
