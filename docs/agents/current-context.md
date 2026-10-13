# Context maintenance

## Start or resume

1. Use HANDOFF to locate the current task/worktree; the owner's request selects
   work. Verify the workspace using [AGENTS.md](../../AGENTS.md).
2. Load the relevant issue, implementation and one or two evidence references.
   Compare dates and source/runtime revisions before relying on a status claim.
   A live issue can contain an old verdict; verify runtime state before acting.
3. Retrieve older comments or research only to answer a named uncertainty.
   Reuse qualified evidence until a changed prerequisite gives reason to repeat it.

## Keep one source of truth

- Code and focused tests explain implementation behavior. Comments capture
  non-obvious reasons and constraints, not a second implementation description.
- Issues own requirements and acceptance. Update the existing issue when a
  meaningful result changes its verdict, blocker or next action; link evidence.
  Routine diagnostic attempts stay in existing private records.
- Durable documentation changes only when a durable fact or decision changes.
  Keep resolved terminology in the glossary and consequential architectural
  decisions in ADRs. Correct an affected operational instruction when necessary.
  Completing a task creates no obligation to write research, a report or an ADR.
- Existing research, licences and recovery records remain retrievable history.
  Consult them selectively; old plans do not select or authorize work. New
  research must answer a specific unresolved question needed for the next step.

## Transfer only when needed

Update HANDOFF when another session needs a changed task pointer or a necessary
recovery fact. Point to the latest issue/result and exact worktree; keep only
unrecorded information necessary to resume. Preserve the existing fields required
by the repository check, without duplicating the issue, logs or research.
Handoff maintenance is not progress or evidence of gameplay success.

Report the observed result, remaining blocker, next action and uncommitted work
in the conversation. Keep source checks, runtime evidence and owner acceptance
separate. Follow the existing [publication checks](issue-tracker.md) when publishing;
no additional documentation phase is required at every task boundary.
