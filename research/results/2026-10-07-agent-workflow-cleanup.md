# Agent workflow cleanup — 2026-10-07

The owner requested a review of project documentation and global Codex setup after
an experiment branch existed in a separate worktree while the active chat still
showed `main`, then authorized the identified corrections. The approved scope is
workflow/documentation maintenance, original-skill restoration and verification;
no game/runtime implementation or trial is part of this change.

## Corrections

- Align a chat's working directory with its task branch before editing or committing.
  A single active chat may switch its clean checkout to a task branch; use separate
  worktrees for isolation and attach their working chats. Preserve the existing
  Fortnite experiment and all unrelated work.
- Replace obsolete recovery/setup instructions with completion evidence: PR #3
  merged at `7f152713a24402ccb74560066f62d8f39afb6800`. Live issue #4 owns the
  experiment; dated investigation reports do not select tasks.
- Extract the current Fortnite contract, retaining full interactive-world acceptance
  while keeping the one-surface first proof and prerequisites on issue #4.
- Remove retired tracker operations from live runbooks. Permit owner-selected
  independent work while another task is blocked; dependent work remains blocked.
- Extend the repository gate to all tracked Markdown documents, excluding ignored
  private data and other worktrees. Add focused regression tests and CI using the
  existing Python gate. Native runtime and gameplay validation remain separate.
- Restore the five missing router targets without modifying existing skills:
  `implement-spec`, `improve-codebase-architecture`, `pr`, `wizard`, `to-questionnaire`.
  Install from the previously recorded Matt revision
  `24fe0ef7737efae15c87225755e9f6f5965e4888`; all 13 added files were compared
  byte-for-byte against the inspected originals. Fresh-session discovery is a
  separate check from successful file installation.
- Remove only the retired board-updater allow rule and inactive session-start hook
  trust record from global Codex settings. Back up both files; preserve other
  permissions, model preferences, status-line configuration and original skills.

## Verification and scope of evidence

The new documentation-link tests reproduce nested agent/research link failures,
accept valid relative links, and exclude untracked private Markdown. Full check
and independent Standards/Spec review outcomes belong on the cleanup PR at its
reviewed revision; they are not native-runtime or gameplay evidence.

Global skill installation and settings cleanup are local setup, not files delivered
by this repository PR. The global hook file was empty; removing its stale trust
record did not disable an active hook. The CLI status line already included the
working directory and Git branch; no display setting needed changing.

During cleanup, the owner clarified the interface is Codex CLI and reported that
the footer still displayed `main` after Git in the chat's own checkout verified
`chore/agent-workflow-cleanup`. Installed CLI version: 0.160.0. Its
[status-surface source](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/tui/src/chatwidget/status_surfaces.rs)
caches branch state by working directory and uses asynchronous refreshes. An
[open upstream report](https://github.com/openai/codex/issues/30930) describes stale
branch labels after a switch on an earlier version. This supports investigating
the display cache; it does not prove the exact cause in the owner's running TUI.
No live TUI reproduction or confirmed refresh was obtained. Desktop-project advice
was inapplicable to the reported CLI interface; Git state and UI state must be
reported separately. This repository change does not patch the Codex binary.

The source change adds CI but does not itself configure GitHub branch protection.
After a passing PR run, require that check and PR-based updates on `main`, apply
protection to administrators, and retain force-push/deletion restrictions. No
independent approving reviewer is required for this sole-maintainer workflow.
Remote protection cannot prevent local file edits; workspace checks remain necessary.

## Primary references

- [Matt skills at the retained revision](https://github.com/mattpocock/skills/tree/24fe0ef7737efae15c87225755e9f6f5965e4888): original router, implementation and retrospective workflows.
- [OpenAI worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees): worktree creation, chat handoff and branch ownership.
- [OpenAI project folders](https://learn.chatgpt.com/docs/projects): primary working directories for new chats.
- [OpenAI best practices](https://learn.chatgpt.com/guides/best-practices): concise practical instructions and verification.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): PR/check requirements and administrator enforcement.
