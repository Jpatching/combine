# Sandcastle for Combine

Run one approved coding issue in a private source-only clone, check it without
credentials, then review it in two fresh sessions. The host owns GitHub, PRs and
merging. The runner stops after that issue.

## Setup

Use WSL Ubuntu with Docker Desktop running and Ubuntu WSL integration enabled.
Docker commands need access outside Codex's workspace sandbox. From the repository:

```sh
cd tools/sandcastle
npm ci --ignore-scripts
npm run check
npm run doctor
npm run build-image
npm run integration
npm run smoke
```

`doctor` checks pinned host tools, Docker access and ChatGPT login. `build-image`
records the image ID and verifies its tools. `smoke` performs actual inference
using the existing subscription; authentication or account limits stop execution.
There is no API billing fallback.

Dependencies are locked to Sandcastle 0.12.0 and TypeScript 6.0.3. The image uses
digest-pinned Node 24.10.0 and Python 3.10.19 bases with Codex 0.160.1. The model
is `gpt-6.1-sol` at medium effort. Setup time is recorded separately from task time.
The host needs Matt's original `implement`, `tdd` and `code-review` skills under
`~/.codex/skills/`; their unmodified instructions are supplied to the sessions.

## Start one task

Fetch and synchronize `main` first. Use a clean primary checkout on `main` or
the exact task branch at that same revision. Read the issue and settle its scope,
checks and blockers before running:

```sh
npm run run -- --issue 12 --branch fix/markdown-angle-links
```

The host fetches the full selected issue and comments from `Jpatching/combine`
and requires `OPEN`, `ready-for-agent` and zero open native blockers. Missing
dependency information fails readiness. An issue also needs a reviewed entry in
the `TASKS` table in `scripts/settings.mjs`, defining allowed source files and
checks. Issue text never supplies executable check commands. The initial entry
is the approved Markdown-link proof; future tasks need their own reviewed entry.

The runner clones committed `main` from Combine's public remote and removes the
clone's remote before inference. It does not copy the host working tree, private
directories or other worktrees. If remote `main` has moved, synchronize and run
again rather than overriding the revision check.

The implementer uses a fresh Sandcastle Docker container and commits scoped task
changes. Separate verification runs `python3 scripts/verify.py`, focused task
checks and external acceptance. Standards and Spec review run in parallel fresh
containers with read-only source and Git metadata. Both must approve the checked
revision. Findings stop acceptance; corrections require another bounded run
after preserving the previous result. The host coordinates the original review
skill's two axes, with one axis per reviewer.

The coding container receives source, dedicated Git metadata and minimal copied
ChatGPT authentication. Sandcastle's permission bypass operates inside Docker;
Docker is that execution boundary. Verifiers have no authentication or network,
read-only source and a writable temporary directory. Reviewers have read-only
source and their own authentication copies. Containers receive neither host
home/configuration nor the Docker socket, project credentials, game assets,
profiles or unrelated private files. Generated tests run inside containers.

## Results and recovery

Each run has a 30-minute limit and one implementer iteration. There are no automatic
retries, issue selection, pushes, merges or deployments. Ctrl-C requests cooperative
cancellation and allows up to 45 seconds for preservation and cleanup.

Private records live under ignored `.private/sandcastle/`:

- `setup.json` and `smoke.json` identify the built and authenticated image.
- `runs/<run-id>/job.json` preserves the issue, profile, base, image, dependency-lock
  hash and supplied skills. `result.json` records checks, reviews and elapsed time.
- `source.patch`, `status.txt` and private logs support diagnosis. Source branches
  remain in `repos/<run-id>`; dirty worktrees and untracked/ignored source remain
  in place after failure/cancellation. Sandcastle may remove a clean successful
  worktree; its branch and commits remain in the dedicated clone.

Inspect `coordinator-error.txt` locally when preflight fails. Keep authentication,
raw logs and private records outside Git and AI uploads. Inspect the recorded
branch before recovery; the runner never resets or overwrites an existing task
workspace. Preserve the only retained copy before any cleanup.

An `accepted` result means source checks, scope/branch invariants and both agent
reviews passed. Host review and publication are pending. Follow Combine's
[slice conventions](../../docs/agents/issue-tracker.md): inspect/import task commits
into the primary task branch, push, open a PR, require CI, merge and synchronize
clean `main`. Reviewed corrections require affected checks and fresh review again.

Hands-on time, interruptions and owner acceptance start as `null`; record only
observed values. This does not establish Windows gameplay, game integration,
owner gameplay acceptance or supervision improvement. Upstream Skate host-test
debt remains outside this source-only proof.

## Maintainer checks

`npm run check` checks syntax and unit tests without Docker or inference.
`npm run integration` uses Docker without credentials/inference to prove isolation,
defect detection and cancellation/source preservation. Run these for runner
changes, and `python3 scripts/verify.py` for every source slice.

Source: [Matt Pocock's Sandcastle](https://github.com/mattpocock/sandcastle).
