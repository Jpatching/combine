# Combine workbench

Combine should make selected integrations repeatable, observable and reusable.
Use Reverse Engineer Anything (REA) and Universal Modder as investigation and
modding guides. Each supported product still needs its own adapter, tests and
acceptance evidence. A future hosted catalogue can list those products and their
actual status. This setup prepares the workflow; it does not deploy that catalogue.

## Where to look

```text
Goal and intended behaviour -> issue acceptance criteria
Investigation              -> exact target/version + one question + evidence
Implementation             -> adapter + regression check
Visible result             -> private clip/screenshots + measured observations
Review                     -> source checks / runtime verdict / owner acceptance
Next session               -> issue evidence + HANDOFF pointer
```

Start from [current context](HANDOFF.md), then read the live issue and comments.
For [Mount -> move -> dismount](https://github.com/Jpatching/combine/issues/20),
the intended sequence is normal GTA walking, mount, push, left/right steering,
dismount, then normal walking/vehicle use. The recorded blocker is a mount refusal
above 0.05 metres; its surface root cause remains unknown. Keep the guard and
preserved candidate. Fixing a blocker and accepting a complete ride are separate.

The existing GTA and Fortnite issues remain integration experiments. This guide
connects them to the broader reusable workflow; it does not claim that open issues
already specify the hosted catalogue or select another gameplay task.

## Use the two guides

The [reviewed guide revisions](../research/tool-guides.json) are separate from
the [runtime pins](../research/upstream.lock.json); no existing runtime pin moved.
Local snapshots and tools live under ignored `.private/tool-guides/` and
`.private/tooling/`. Do not commit those folders.

- [REA investigation instructions](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/skill-src/reverse-engineer-anything/SKILL.md):
  use source tools for complete source repositories. Use REA when a question needs
  shipped-artifact, decompilation or requested runtime evidence. A CLI installation
  does not establish native-provider readiness or an active MCP connection.
- [Universal Modder reconnaissance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/game-recon/SKILL.md):
  establish version, existing community route and isolated lab before modifying.
- [Reverse engineering](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/reverse-engineering/SKILL.md):
  test each interpretation against the real behaviour; retain reusable findings.
- [Recording guidance](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/skills/showcase-video/SKILL.md):
  make takes repeatable and capture only the target window. For acceptance retain
  an uncut sequence with timing; an edited showcase is supplementary.

Matt's `ask-matt` chooses the engineering flow. These upstream guides supply
target-specific methods; repository boundaries and the owner's request govern use.
Read the relevant guide before invoking a new command. Remote asset generation,
scanning, input automation, backup restoration and publishing are distinct actions.

After local installation, run from the repository:

```sh
python3 scripts/workbench.py guide universal-modder kb search 'gta iv' --limit 3
python3 scripts/workbench.py guide rea --help
```

The wrapper checks the guide checkout revision and clean state before execution.
REA uses an isolated Node 24.11.0 and exact package 6.1.0. Installation instructions
are in [REA setup](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/docs/installation.md).
A fresh checkout needs those ignored local tools prepared separately; the wrapper
reports missing setup and does not silently download or register anything.

## See intended behaviour and proof

Open [the local comparison page](../tools/workbench/evidence.html) in your browser,
or run `python3 scripts/workbench.py evidence` for its location. Select a reference
and candidate clip or screenshot, record the expected/observed behaviour, and save
the private JSON record beside the original media. The page previews local files,
computes their SHA-256 when browser support allows, and makes no network requests.
It defaults to untested and owner acceptance pending. Reloading clears the page;
save the record first. This comparison page is a review aid, not a game recorder.

Use a 20–40 second uncut clip for movement, camera and recovery. Use paired
screenshots for a static visual change. Use a trace or numerical comparison for
timing, physics and file-format claims. Pair visual evidence with the relevant
test result; a pleasing clip alone does not prove scale, collision or recovery.

Before a trial, write this record in a new private trial folder:

```text
Issue and acceptance criterion:
Question or hypothesis:
Source revision and installed runtime identity:
Scenario and starting state:
Action sequence and expected visible behaviour:
Observed result: passed / refused / failed / unavailable / untested
Recording/screenshot filenames and timestamps:
Measurements and automated checks:
What this evidence does not establish:
Owner acceptance: pending / explicitly accepted
Next step:
```

Retain assets, recordings, screenshots, identities, settings, raw traces and
decompiled output in private local storage. Do not upload them to AI or GitHub.
Use `.private/evidence/<trial>/` for local records, or private storage outside the
checkout. Public issues carry only reviewed source-safe findings and check results.
Keep failed/refused takes as evidence, rather than presenting them as a success.

For an authorized Windows capture, review Universal Modder's `um/win.py`,
`um/ps1/ProcLoopback.ps1` and `skills/game-automation/SKILL.md` first. Its
`win record` captures a selected process; `video contact` produces a timestamped
frame grid. This Linux terminal setup does not establish Windows capture readiness.
Watch local clips in a local player such as ffplay; compare images locally.
Do not start a game or take input control merely by opening these views.

Public catalogue entries should distinguish proposed, source-tested,
runtime-observed and owner-accepted status. Record source licences and attribution
separately from target/asset permissions. No new target has general rights
clearance from using these tools. Keep game data and copied proprietary code out
of public entries; source publication and visual publication need their own review.

## Terminal views

```sh
python3 scripts/workbench.py open
```

This adds `combine-git` (lazygit), `combine-issues` (live issue list and comments),
`combine-behaviour` (this guide), and `combine-checks` (an explicit source-gate run).
It preserves existing panes, the selected window and any existing named views.
Use tmux's window selector, normally prefix then `w`, to switch. Neovim's installed
git plugins offer `:LazyGit`, `:DiffviewOpen` and `:DiffviewFileHistory` when loaded.
Issue commands use the explicit `Jpatching/combine` repository; no issue plugin is
required. The checks pane reports the checkout identity before offering a run.

Run `python3 scripts/verify.py` for the repository gate. Run relevant adapter and
runtime checks for changed behaviour. Keep test, build, launch, gameplay,
owner acceptance and release claims separate. At the task boundary, follow
[context maintenance](agents/current-context.md) so the next session can recover
the goal, evidence, exact blocker and next action without relying on memory.
