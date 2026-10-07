# Combine issue tracker

Tickets and specs live in the private [Combine Project](https://github.com/users/Jpatching/projects/5/views/8),
owner `Jpatching`, number `5`. Git owns source and repository PRs own source review.
Repo Issues are not this project's ticket store; keep private planning private.

## Skill operations

Use `gh project` and GitHub's Projects GraphQL API. Inspect current IDs/options
before writes and read back changes. Avoid the retired custom phase helper.

- **List/fetch:** `gh project item-list 5 --owner Jpatching --limit 100 --format json`.
  Read the full matching C-identifier body and fields. For complete inventory,
  query `user(login: "Jpatching") { projectV2(number: 5) { items(first: 100, after: $cursor) } }`
  through `gh api graphql`; page until `hasNextPage` is false and include `isArchived`.
  Search archived cards before creating duplicates or allocating the next C-number.
- **Publish a ticket/spec:** `gh project item-create 5 --owner Jpatching --title ... --body ...`.
  Preserve C-identifiers. Include result, acceptance checks, evidence/blocker,
  next action and relevant links. Use structured arguments or a subprocess argument
  list for multiline bodies, never interpolate bodies into shell commands.
- **Edit/read notes:** draft cards have no issue comments. Use `gh project item-edit`
  with the draft content ID to edit title/body, retaining prior discussion and dated
  notes. For triage, retain Matt's AI disclaimer on generated text and append reporter
  replies with author/date; do not invent reporter activity or send outreach.
- **Fields/claim:** discover fields with `gh project field-list 5 --owner Jpatching --format json`.
  Use `gh project item-edit` with Project ID, item ID, field ID and option ID for
  Work status, Triage state and Triage category. Set Doing to claim work; use the
  draft's assignees via `updateProjectV2DraftIssue` when a skill needs an assignee.
  Never treat draft content IDs as Project item IDs.
- **Dependencies/maps:** record linked `Blocked by: C-xxx` and `Part of: C-xxx` lines
  in bodies, with a linked child list on the map. Drafts lack native issue dependency
  endpoints. A ready frontier excludes assigned tasks and tasks with unresolved
  prerequisites; a rejected prerequisite does not satisfy an acceptance check.
- **Complete/close:** set Work status Done with evidence only when the acceptance
  check passes. For a rejected request, record reason and `wontfix`, then archive;
  archiving is not completion or gameplay acceptance. Read archived items via the API.

Work status options are Ready, Doing, Blocked, Done. Historical Status/Phase fields
are retained evidence, not active process. Current selection belongs on the board.
If GitHub fails, report the failed operation and pending update without claiming sync.

## Triage

PRs as a request surface: no.

Use [triage labels](triage-labels.md). Apply triage to incoming reports/requests,
not prepared tickets. Discover candidates with Triage category/state metadata or
an explicit `Incoming request` body marker; do not treat every unlabeled planned
card as incoming. For imported reports, retain reporter, reported date and replies
in the body. Sort by reported date (or creation date if unavailable).
Record brief/notes in the draft body. Keep private rejection knowledge in the private
tracker; only non-sensitive reusable rationale may go into public `.out-of-scope/` files.

Bare `#N` denotes a repository PR/issue: resolve with `gh pr view N`, then
`gh issue view N`. `C-NNN` denotes a Project ticket. An explicitly requested PR
can be triaged using `gh pr` operations; maintainers' ordinary PRs are not an intake queue.
