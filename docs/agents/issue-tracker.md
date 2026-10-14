# Issue tracker: GitHub

New specs and tickets live in [Jpatching/combine Issues](https://github.com/Jpatching/combine/issues).
Use the `gh` CLI with `--repo Jpatching/combine` for issue operations.
The repository is public: publish source-safe task descriptions and acceptance
criteria; keep private diagnostics, logs, settings, identities and game assets
outside Issues and Git.

## Conventions

- Create: `gh issue create --repo Jpatching/combine --title "..." --body-file <file>`.
  Prepare multiline bodies in a temporary file and review them before publishing.
- Read current status: `gh issue view <number> --repo Jpatching/combine --json body,title,state`.
  Fetch `--comments` for a named evidence question or when the selected skill
  requires the full ticket.
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

**One observable behavior → implement and test → review → commit and push → draft PR with evidence → owner approval → squash merge → synchronize local `main`.**

Before requesting approval for a visible change, capture and automatically open
the actual clip or screenshots locally with `python3 scripts/workbench.py evidence
<file> [<file> ...]`. Identify the demonstrated behavior and its limitations.
Keep private media local; the draft PR records source-safe evidence descriptions
and checks. A file path, passing test or viewer launch is not owner acceptance.
Wait for explicit approval of the presented candidate before marking the PR ready
and merging. Material behavior changes after approval require renewed evidence
and approval. Do not enable automatic merge while acceptance is pending.

Bundle source, tests and durable documentation into one focused commit when practical.
Use additional commits for meaningful fixes or review responses, then squash the
finished PR into one commit on `main`. Record the final merged revision on the
issue; the issue summary owns the final revision.
Preserve published history and retained recovery branches. A superseded PR may
be closed after verifying its commits are contained in the selected candidate,
or preserving its useful findings in the owning issue or durable reference.
Link the replacement when closing; closure does not mean gameplay acceptance.

For the owner-approved GTA evidence workflow (#61), keep retained riding,
collector and workflow changes in one integration candidate and draft PR.
Present source checks, runtime verdicts, unresolved criteria and private clips
for one explicit owner decision. Bounded diagnosis requires current runtime
authority; stop unchanged scenarios after two identical failures. This exception
replaces fragment-by-fragment approvals, not ground or gameplay acceptance.

Use one focused branch and PR per other implementation slice. Resume existing
unfinished issues/branches/PRs and reuse their worktree with explicit command
working directories and edited paths. Before edits, after handoff and before
commit/push, verify `git rev-parse --show-toplevel`, `git branch --show-current`,
`git rev-parse HEAD` and `git status --short --branch`. Match the exact selected
directory and task branch; stop writes on a wrong target, `main` or detached HEAD.
Preserve unrelated changes; never force-switch, reset or stash them. Pass the
same directory and branch to delegated agents. A different chat attachment or
UI branch label does not block verified worktree operations; report the mismatch
without claiming the UI moved. Create new slice branches from synchronized `main`.

Before pushing, inspect the remote and destination branch; publish the task branch,
not a refspec targeting `main`.

Work only on slices whose blockers are complete. When blocked, record the exact
blocker on the existing issue/PR and preserve the branch. The owner may select
independent work while it is blocked. Review, required checks and owner approval must pass before
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
