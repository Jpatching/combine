# Context maintenance

## Start or resume

1. Read the owner's selected issue and its acceptance criteria. For the GTA ride,
   read [#61's current summary](https://github.com/Jpatching/combine/issues/61)
   and [#20](https://github.com/Jpatching/combine/issues/20).
2. Verify the directory, branch, revision and local changes using
   [workspace conventions](issue-tracker.md). Check installed runtime identity
   separately before a runtime trial; a source revision is not loading evidence.
3. Consult historical comments or Git history for a specific question. Reuse
   qualified setup unless a changed prerequisite calls for a fresh check.

## Task boundary

Update the existing issue's current summary when evidence changes the verdict:
candidate revision, passed behavior, blocker and next action. For GTA, #61 owns
that summary and #20 owns acceptance criteria. Keep routine diagnostic progress
in private run records; preserve historical comments without duplicating them.
Source checks, observed gameplay and owner acceptance remain separate claims.

Keep unique build procedures in [reproduction instructions](../REPRODUCING.md),
resolved terms in the glossary and consequential decision rationale in ADRs.
Code and behavior tests explain implementation. Do not create permanent progress
snapshots or test-audit narratives.

Follow [workspace conventions](issue-tracker.md) for review, publication and owner
approval. `python3 scripts/verify.py` checks tracked links and behavior tests;
it cannot establish factual freshness or gameplay acceptance. Review public
content before staging; keep private measurements, identities and media local.

## Context transfer

Use Matt's `ask-matt` phase-boundary guidance. A temporary handoff may transfer
work to another session, directory or person; link the owning issue and durable
evidence rather than copying status. Recheck Git and runtime state on arrival.
