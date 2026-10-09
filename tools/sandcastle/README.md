# Sandcastle for Combine

Run one approved coding or public-source research issue in a private source-only clone, check it without
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
checks. Issue text never supplies executable check commands. Coding #12 retains its Markdown-link proof. Research #31 and #32 have reviewed
profiles allowing only their respective reports. Future tasks need their own reviewed entry.

The runner clones committed `main` from Combine's public remote and removes the
clone's remote before inference. It does not copy the host working tree, private
directories or other worktrees. If remote `main` has moved, synchronize and run
again rather than overriding the revision check.

The implementer or background researcher uses a fresh Sandcastle Docker container
and commits scoped task changes. Separate verification runs `python3 scripts/verify.py`, focused task
checks and external acceptance. Standards and Spec review run in parallel fresh
containers with read-only source and Git metadata. Both must approve the checked
revision. Findings stop acceptance; corrections require another bounded run
after preserving the previous result. The host coordinates the original review
skill's two axes, with one axis per reviewer.

The coding container receives source, dedicated Git metadata and minimal copied
ChatGPT authentication. Sandcastle's permission bypass operates inside Docker;
Docker is that execution boundary. Verifiers have no authentication or network,
read-only source and writable temporary directories. The checkout's `.private`
directory is shadowed by an empty, user-owned tmpfs for synthetic header-test
fixtures; it exposes no host private data and retains no fixture writes. A symlink
or non-directory scratch mountpoint is rejected. Reviewers have read-only
source and their own authentication copies. Their Codex CLI uses `danger-full-access`
inside Docker to avoid an unsupported nested namespace sandbox; Docker's read-only
root/source/Git mounts, dropped capabilities and no-new-privileges enforce the review
boundary. This CLI setting is never used for a host review process. Containers receive neither host
home/configuration nor the Docker socket, project credentials, game assets,
profiles or unrelated private files. Generated tests run inside containers.

## Public-source research

After runner acceptance and all native issue blockers are closed, dispatch one
approved research issue through the same `run` entrypoint:

```sh
npm run run -- --issue 31 --branch research/gtaiv-native-collision
npm run run -- --issue 32 --branch research/gtaiv-physical-collision
```

Each invocation runs independently and still requires a clean checkout at
synchronized committed `main`, current smoke/image identity and issue readiness.
Use separate attached task workspaces for parallel host work. The approved paths
are `research/results/gtaiv-120059-native-collision-feasibility.md` and
`research/results/gtaiv-120059-physical-collision-feasibility.md` respectively.

The host supplies Matt's unmodified original `research` skill and delegates the
researcher's steps to a separate background worker process. The host remains
available to coordinate other work while that process reads. There is no nested
agent claim: the separate completed researcher process is the delegation. Missing
skills or pinned guidance stop preflight before copying authentication or starting
inference. The public Universal Modder snapshot must match the existing reviewed
revision and be clean. Only four allowlisted public text files and their hashes
are supplied in the prompt; the private snapshot directory is never mounted.
No UM CLI, native analysis provider, game assets or Windows access is installed
or exposed to the research container.

The researcher fetches public primary-source text and records immutable revisions.
Reports distinguish verified source facts, inference, unknowns and the next local
proof. One bounded evidence record lists immutable public file citations,
inaccessible sources and a verdict: `source-feasible`, `requires-local-proof`, or
`blocked`. `runtimeVerified` must be false. The credential-free external report
check rejects missing/oversized reports, symlink paths, incomplete citations and
unsupported verdicts. It checks structure; the fresh reviewers assess actual
source support and ticket completeness. A reviewed `blocked` report is an honest
accepted research output, not a claim that world collision works. Result records
identify the background role, completed researcher and evidence verdict.

Before dispatch readiness, qualify the actual research path with:

```sh
npm run research-smoke
```

This runs actual subscription inference, report checks and fresh reviews on a
fixed public-guide question, using a separate source-only clone of committed
`main`. It permits testing candidate runner source while the primary checkout is
being edited. Its synthetic qualification brief and report path are fixed host
configuration; it cannot select, unblock or complete #31/#32. The generated
qualification report and branch stay in private recovery records and need not be
published. Passing fixtures alone does not establish research readiness. A successful actual
qualification records `research-smoke.json` with the image, model and a fingerprint
of runner implementation, dependency lock and supplied skills/guidance. Production
research requires that matching marker; a generic login smoke is insufficient.
Starting qualification invalidates the previous marker, so a failed retry cannot
leave the candidate qualified. Unrelated handoff edits do not change its identity. The
same authentication/image requirements, 30-minute limit, cancellation and output
preservation apply. Run qualification again if the inference/acceptance path
changes materially; do not bypass production issue or checkout guards.

## Results and recovery

Each run has a 30-minute limit and one implementer iteration. There are no automatic
retries, issue selection, pushes, merges or deployments. Ctrl-C requests cooperative
cancellation and allows up to 45 seconds for preservation and cleanup.

Private records live under ignored `.private/sandcastle/`:

- `setup.json` and `smoke.json` identify the built and authenticated image.
- `runs/<run-id>/job.json` preserves the issue, profile, base, image, dependency-lock
  hash and supplied skills. `result.json` records checks, reviews and elapsed time.
- `source.patch`, `status.txt` and private logs support diagnosis. A `source/`
  snapshot preserves tracked, untracked and ignored files before cleanup, retaining
  symlinks without following them. Source branches and worktrees remain in
  `repos/<run-id>`. Container shutdown never removes source, even if snapshotting
  fails. Inspect the retained worktree when recovery artifacts are incomplete.
- Accepted runs also export `export/task.bundle` inside a credential-free container.
  Import this bundle on the host instead of fetching worker-controlled Git metadata.

Inspect `coordinator-error.txt` locally when preflight fails. Keep authentication,
raw logs and private records outside Git and AI uploads. Inspect the recorded
branch before recovery; the runner never resets or overwrites an existing task
workspace. Preserve the only retained copy before any cleanup.

Worker-controlled Git inspection runs inside credential-free, network-disabled
containers, keeping configured executable helpers inside Docker. Container teardown
is separate from upstream worktree cleanup. Every phase uses the immutable image ID.
The inherited host Git environment also disables lazy object fetching and all
transport protocols for upstream's remaining commit enumeration.

An `accepted` result means source checks, scope/branch invariants and both agent
reviews passed. Host review and publication are pending. Follow Combine's
[slice conventions](../../docs/agents/issue-tracker.md): inspect/import task commits
into the primary task branch, push, open a PR, require CI, merge and synchronize
clean `main`. Reviewed corrections require affected checks and fresh review again.

Use `git fetch <run-directory>/export/task.bundle <task-branch>` and fast-forward the
primary task branch to `FETCH_HEAD` after inspecting the accepted result. The
bundle retains the exact reviewed commits without executing a donor repository's
configured Git helpers on the host.

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
