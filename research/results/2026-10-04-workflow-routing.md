# Resume and model routing repair — 2026-10-04

The owner requested one way to resume current Combine work, visible synchronized
states and saved model/agent choices. This change updates project instructions,
removes stale publication restrictions under D-016/D-017 and records the selected
menu-then-Fortnite dependency path. No gameplay source or assets are changed.

## Findings and configuration

The live private Project identifies C-016 input isolation as sole Now/Phase 5.
Diagnostic 05's menu-open firing regression and incomplete lifecycle checks remain;
statistics debt was reproduced without Synergy. The old handoff named an earlier
branch and omitted dirty runtime work. Remote head listing succeeded and returned
no branches before this repair. A local commit had not published source.

The saved local Codex default was Astra/xhigh. It is now Sol/medium, with at most
two spawned helpers and personal read-only roles: Luna/high scout, Sol/high reviewer,
Astra/medium specialist. Model availability/effort was checked against the installed
catalog. The router reaches a shared resume/routing policy, applies current owner
instructions, loads focused evidence and requires remote SHA and board read-back.
Backups were made before installation; unrelated configuration was preserved.

These are new-session defaults on clients honoring local configuration. Current
or resumed conversations may keep explicit model choices. No speed benchmark,
background task pickup, automatic current-model switch or owner acceptance is
claimed. Named roles are TOML/model validated; cross-client role discovery and
long-run routing behavior require observation. On clients with explicit spawn
settings, the policy uses the equivalent model/effort and bounded task brief.

## Verification

- Installed Codex CLI: 0.160.0. Its app-server config/read, with strict config,
  confirmed Sol/medium, helper cap two and default helper Sol/medium before and
  after installation. No model turn or gameplay was started by that check.
- Skill validator: passed for matt-workflow. Three personal role files parse,
  declare read-only sandbox, and use catalog-supported models/efforts.
- Shared helper/hook suite: 15 tests passed. This validates existing read-back,
  failure and reminder behavior, not universal future agent compliance.
- Independent standards and spec reviews each found one issue: missing runnable
  check commands and a stale next-check instruction. Both are corrected here.
  The revision-specific project gate and publication/board results belong on
  the live C-016 card; resolve that revision before relying on the results.

Reproduce the local configuration checks from a trusted project directory:

```sh
python3 ~/.codex/workflows/solo-development/check_routing.py
python3 ~/.codex/workflows/solo-development/test_workflow.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/matt-workflow
python3 scripts/verify.py
```

The routing check parses the three installed roles, checks cached model/effort
support, then uses `codex --strict-config app-server --stdio` and its
`initialize`/`config/read` requests to assert effective defaults and helper limit.
It starts no model turn. It needs local Codex state-directory write access; a
restricted subprocess failed that initialization before the approved local run
succeeded. Global setup lives outside the product repository and is not installed
by cloning Combine. The named project gate covers metadata/recipes/links/tests,
not gameplay or model routing.

The installed shared policy is `~/.codex/workflows/solo-development/ROUTING.md`.
Official [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference),
[subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents)
and [model guidance](https://developers.openai.com/api/docs/models) were read on
2026-10-04. Local CLI/catalog/config evidence, rather than model marketing,
establishes which settings this installation actually loads.

## Resume and safety

Four inherited trial-script/checklist changes stay in the product checkout on
slice/synergy-input-isolation. Ignored runtime input edits stay in their original
checkout and must be captured as source patches before claiming checkpointed code.
This repair is on the isolated chore/workflow-routing branch; no patch or runtime
code was changed. Game data, logs, settings and prior trials are preserved.

Next: integrate the reviewed workflow documentation locally, preserve inherited
work, then resume the same input-isolation regression and its Windows checks.
The repository gate cannot prove menu play or Fortnite conversion. Board and
publication operations are reported only after their own read-back succeeds.
