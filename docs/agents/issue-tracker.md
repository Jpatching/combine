# Issue tracker: GitHub

New specs and tickets live in [Jpatching/combine Issues](https://github.com/Jpatching/combine/issues).
Use the `gh` CLI with `--repo Jpatching/combine` for issue operations.
The repository is public: publish source-safe task descriptions and acceptance
criteria; keep private diagnostics, logs, settings, identities and game assets
outside Issues and Git.

## Conventions

- Create: `gh issue create --repo Jpatching/combine --title "..." --body-file <file>`.
  Prepare multiline bodies in a temporary file and review them before publishing.
- Read: `gh issue view <number> --repo Jpatching/combine --comments`;
  also fetch `--json number,title,body,labels,comments,state` when structured data is needed.
- List: `gh issue list --repo Jpatching/combine --state open --json number,title,body,labels,comments`,
  with appropriate label and state filters.
- Comment: `gh issue comment <number> --repo Jpatching/combine --body-file <file>`.
- Apply/remove labels: `gh issue edit <number> --repo Jpatching/combine --add-label "..."`
  or `--remove-label "..."`.
- Close: `gh issue close <number> --repo Jpatching/combine --comment "..."`.

When a skill says “publish to the issue tracker”, create a GitHub issue.
When it says “fetch the relevant ticket”, read its full body, labels and comments.
GitHub shares issue and PR numbers; resolve ambiguous references before acting.

**PRs as a request surface: no.** External PRs are not part of the triage queue.

## Implementation slices

Follow `ask-matt`: larger, multi-session work goes through `to-spec` and
`to-tickets`; small, clear work can go directly to `implement`.
Use `to-tickets`' existing rules: each slice delivers a complete behavior that
can be verified independently, fits one fresh context window, and declares
acceptance criteria and blockers. Obtain the owner's approval of the breakdown
before publishing tickets. Tickets produced by `to-tickets` are already ready
for implementation; apply `ready-for-agent` without sending them through triage.

Complete each authorized source slice through:

**Implement → test → review → commit → push → PR → merge → synchronize local `main`.**

Use one focused branch and PR per implementation slice. For a single active chat,
switch its clean checkout to the task branch before editing. Use a separate
worktree when parallel work or retained experiment state needs isolation, and
attach the working chat to that checkout. A worktree is a separate folder checked
out on a branch; creating one or using `git -C` does not move a chat into it.

Before edits, after a handoff and before committing or pushing, verify the chat's
workspace with `git rev-parse --show-toplevel`, `git branch --show-current`,
`git rev-parse HEAD` and `git status --short --branch`. Match the exact task branch
and directory; any non-main branch is not enough. Stop writes on a mismatch,
`main` or detached HEAD and align the checkout first. Preserve local changes;
never force-switch, reset or stash unrelated work to satisfy this check. Pass the
same task branch and working directory explicitly to delegated agents.

Create new slice branches from synchronized `main`. Resume existing unfinished
issues/branches/PRs instead of creating duplicates. If a branch is already checked
out elsewhere, use that existing worktree rather than forcing a second checkout.
For app-managed worktrees, use the app's workspace/handoff controls; for an existing
manual worktree, open that folder as the chat workspace. Treat the displayed branch
as a useful cross-check; Git in the actual working directory supplies the evidence.
In Codex CLI, start or resume with `codex -C <worktree>` or
`codex resume -C <worktree>` and select the intended saved session. A shell command's
`cd` does not retarget the running CLI. Its branch footer can be cached: if the
display disagrees with Git, report the discrepancy, verify the actual directory
and branch, and use `/statusline` or restart/resume to check the display. Do not
claim the label refreshed without observing it or receiving user confirmation.
Before pushing, inspect the remote and destination branch; publish the task branch,
not a refspec targeting `main`.

Work only on slices whose blockers are complete. When blocked, record the exact
blocker on the existing issue/PR and preserve the branch. The owner may select
independent work while it is blocked. Review and required checks must pass before
merging. Start the next new slice from updated `main` after completion.
Verify completion with a clean working tree, a merged PR, and identical local
`main` and `origin/main` revisions after fetching. Source integration does not
establish gameplay acceptance or authorize launch, deployment or release.
Keep experimental checkpoints on a separate `prototype/<name>` branch and link
its question and verdict from the issue. A preserved experiment need not merge;
promote useful implementation through a reviewed source slice. Verify branch,
worktree and starting revision before edits. Remove completed worktrees only
after preserving commits and checking ignored local files.
This convention supplements Matt's original skills without modifying them.
If a routed skill is unavailable, report that fact and inspect its upstream
availability before installing or choosing an applicable installed skill. Never
claim an unavailable skill ran.

The old Project cards and deleted plans remain historical. Leave the cards
untouched and do not import old plans or use them to select new work.

## Blocking and wayfinding

Publish approved tickets in dependency order. Use native GitHub issue dependencies:
fetch the blocker's database ID with
`gh api repos/Jpatching/combine/issues/<number> --jq .id`, then add it with
`gh api --method POST repos/Jpatching/combine/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`.
The database ID is not the issue number or node ID. If dependencies are unavailable,
record `Blocked by: #<number>` in the ticket body. A ticket is ready only when every
blocker is closed; the native `issue_dependencies_summary.blocked_by` counts open blockers.

When `wayfinder` is selected, its map is an issue labelled `wayfinder:map`; children
use `wayfinder:<type>` and native sub-issue links. If sub-issues are unavailable,
use a task list in the map and `Part of #<map>` in each child. Create those additional
labels only when needed. Choose an unassigned open child with no open blockers,
in map order; claim with `gh issue edit <number> --repo Jpatching/combine --add-assignee @me`.
Resolve with an answer comment, close the child, and add its result link to the
map's decisions. Preserve `to-tickets`' rule against changing or closing its parent issue.
