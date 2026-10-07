# Combine development loop

Choose one observable outcome from the [private board](https://github.com/users/Jpatching/projects/5/views/8)
and [current handoff](HANDOFF.md). Read only that task's requirements and relevant
decisions. Existing contracts settle prior choices. Historical backlog and
handoffs are evidence to consult when needed, not mandatory orientation.

```text
Choose one observable outcome
  -> resolve only the uncertainty blocking it
  -> implement a small complete change
  -> test and review
       failure -> fix and recheck
       blocked -> retain evidence and stop that attempt
  -> publish reviewed source when authorized
  -> demonstrate; obtain acceptance where required
```

Keep Doing to one card. Before editing, state the outcome, exclusions and acceptance
check. Inspect existing behavior, preserve unrelated work and use focused checks.
A blocked attempt ends with a precise missing prerequisite and next action.
Use Matt's original skills at the relevant step; explicit-only skills need explicit
invocation. Skill execution is not board progress. Specifications and tickets are
useful when work spans sessions; the next task must stand alone. Global skills and
utilities remain unchanged; Combine no longer uses the seven-phase board helper.

Use one branch per coherent outcome. Refresh origin, inspect the base and checkpoint
inherited work separately. At handoff review the slice diff and explicit source
list/history for private data, run `python3 scripts/verify.py` once plus relevant
runtime/link checks, and make a reviewable commit. Repeat gates only after relevant
changes or failures. Ignored runtime changes need a reproducible reviewed patch.

D-027 and the October 7 reset authorize reviewed source branches to Jpatching/combine
before gameplay acceptance. Push completed reviewed changes, verify the remote SHA,
and read back the updated card. Record routine synchronization and SHA confirmation
on the card or PR, without a follow-up commit just to describe the prior commit.
Report a concrete blocker and unpushed count if publication cannot finish.

The reset branch inherits 24 commits beyond main at its starting revision
`676998711eadebdb2297a320cad9171e888f6fe5`. Review inherited changes separately before
any merge; [PR #1](https://github.com/Jpatching/combine/pull/1) and existing branches
remain intact. No squash, merge, CI deployment or release is authorized by this reset.

For an owner trial, follow the relevant gameplay guide: prepare the exact verified
build, versioned launch/files/checklist shortcuts and limitations; preserve its
predecessor and stop ready for the owner's test. Launch requires authority. Passing
source checks or a published branch does not establish gameplay or acceptance.

Maintain one current handoff with goal, evidence/blocker and next action. Move prior
substantial handoffs into the linked archive, repairing relative links. Preserve
requirements and evidence when parking work: inactive never means accepted or done.
For board operations and unavailable-service recovery, use [tracker instructions](agents/issue-tracker.md).
