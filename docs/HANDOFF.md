# Foundation handoff — 2026-10-03

## Objective and implemented behaviour

Validate a Windows-first supported-mashup business before building a platform.
This revision creates the research foundation, pinned upstream evidence, project
instructions/agent work packages, two candidate recipes, an offline checker, a
Windows baseline procedure, study materials and an authoritative local backlog.

```text
Recipe JSON + trusted release lock
               |
         offline validation
           /          \
  reject with reason   accept metadata only
                              |
                  Windows runbook (pending)
                              |
                real observations -> decision
```

No runtime is downloaded or executed by the checker. No game assets are stored in
this repository. There is no site, launcher, public service, billing or automated
outreach. Project agent roles are documented, not spawned or configured globally.

## Revision and evidence

- Branch: `main`; initial repository, no predecessor/base commit and no remote.
- Repository-local Git author metadata uses the verified connected GitHub account
  and its public no-reply address. GitHub access was already authenticated; missing
  local author metadata was a separate issue. No global Git identity was changed.
- Local issues: C-001 through C-009 in BACKLOG.md.
- Determine the containing revision with `git log -1 --format=%H`; verify clean state
  with `git status --short`. Do not infer a commit from this document's existence.
- Upstream candidate: v0.4.0 / `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
- Exact source fetched into temporary research storage and inspected without running
  upstream code. HEAD and release tag resolved to the selected commit.
- Fifteen inspected files have computed SHA-256 values in research/upstream.lock.json.
- Windows ZIP SHA-256/size are publisher-declared metadata; local byte verification
  and execution remain pending. No reproducible source-build claim is made.

## Validation evidence and commands

- `python3 -m unittest discover -s tests -v`: **16 tests passed** on Linux/Python 3.12.3.
  An earlier run exposed a JSON nesting-limit assumption; explicit depth validation
  fixed it. Overflowing JSON floats are also rejected.
- Full local gate: `python3 scripts/verify.py`: **passed**, including lock structure,
  both recipes, local links in 11 Markdown documents and all 16 tests. It is offline; external link
  freshness, game prerequisites, gameplay and rights are outside this gate.
- Manual use: `python3 scripts/check_recipe.py recipes/mw2-skate.json` (same command
  for minecraft-skate.json). Expected output explicitly retains unverified status.
- At a new handoff, check `git diff --check` and refresh public upstream refs without
  changing the selected baseline. There is no project remote to fetch.

The three agreed global instruction refinements were applied to
`/home/patch/.codex/AGENTS.md` and verified after writing; this file is outside the
project's Git history. They qualify fresh-project defaults and scale explanations.

## Limits and inherited debt

Windows hardware execution and legitimate local game files are unavailable in this
Linux workspace. The owner reports a Windows PC and MW2 downloading, and confirms
they do not own Skate 3. A suitable Skate content acquisition route is unresolved.
Participant recruitment, interviews, repeat-use
observations and payment interest have not happened. Rights/provenance questions
remain unresolved and block public redistribution.

The selected upstream reports map-dependent invisible boards and bot-match performance
regression. Some skating documentation is stale relative to release notes. Rust uses
a moving stable toolchain. None of these are independently reproduced here. See
docs/RESEARCH.md for sources and docs/DECISIONS.md for explicit decision thresholds.

## Next concrete step

Owner/runtime role: start **C-003a** using docs/WINDOWS_BASELINE.md on Windows when
MW2 Multiplayer finishes downloading. Verify the archive and establish on-foot
movement/combat/relaunch with optional skating declined; no IW4x is needed. This is
only a partial baseline. Full C-003 needs a controller, legitimate extracted Skate
3 files and a decision on upstream content acquisition. Record all outcomes with
templates/baseline-result.md; keep raw logs private.

Acceptance: genuine version/hardware/timing evidence, thirty minutes of gameplay,
recorded failures and preservation checks. Cross-machine sharing remains unverified
until a second eligible tester reproduces the recipe. Only then investigate a guided
improvement from actual friction; do not skip directly to a marketplace.

Owner sense-check: confirm that a supported catalogue, existing-game research pilot,
Windows-first target and small-budget validation remain the intended direction.
Foundation implementation is not owner acceptance or permission to release. Future
product work follows the vertical slices in BACKLOG.md and the owner checkpoint
contract in docs/AGENT_ROLES.md. No custom skill, MCP server or plugin was installed.
