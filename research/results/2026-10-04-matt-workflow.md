> Historical setup record. The later global skill/board setup supersedes its
> installation and authority claims; see docs/archive/WORKFLOW-2026-10-07.md for Combine configuration.

# Shared workflow installation and validation — 2026-10-04

Outcome: Matt Pocock's actual skills are installed across projects, with a small
Codex entry point and Combine configuration preserving existing authorities.
The owner's subsequent instruction excludes the Hide HUD pilot. No gameplay
implementation, owner acceptance, new commit, remote or publication is claimed.

## Source and installation

- Source: [mattpocock/skills](https://github.com/mattpocock/skills/tree/24fe0ef7737efae15c87225755e9f6f5965e4888).
  One observed and installed revision: `24fe0ef7737efae15c87225755e9f6f5965e4888`.
- Download: `https://codeload.github.com/mattpocock/skills/zip/24fe0ef7737efae15c87225755e9f6f5965e4888`.
  Archive SHA-256: `c3078c46d6f4d92e361866533d2da07b7ed0395da6b602a4b4e9bac2e441e75a`.
- Licence inspected: MIT, Copyright (c) 2026 Matt Pocock. Licence copied into every
  upstream skill; original ZIP/licence retained in the router's provenance folder.
- Destination: `~/.codex/skills`. Installed `matt-grill-me`, `grilling`,
  `codebase-design`, `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `implement`,
  `tdd`, `code-review`, plus local `matt-workflow`.
- All supporting files copied. Source ZIP safely extracted and skills validated/
  copied with the inspected system skill-installer helpers. No downloaded scripts
  were run. Local preparation/install scripts ran from `/tmp/matt-workflow-20261004`;
  they refuse existing destination names and verify existing-file hashes.
- The sandbox blocked initial GitHub DNS and global writes required filesystem
  escalation. Approved operations downloaded public instructions and wrote the
  prepared new global skill folders; no existing skill was overwritten.
- Durable provenance: `~/.codex/skills/matt-workflow/provenance/source.json`
  records original file hashes and adapted paths; `install.json` records installed
  and pre-existing hashes; `upstream.zip` retains original source. The custom skill
  backup stores its entry point as `SKILL.md.original` to avoid duplicate discovery.

Original custom `grill-me/SKILL.md` before/after SHA-256:
`db34e4648b4ff75dc35083e539acee0e8e8250ce414c6afd61b9afb07216cc46`.
Its `agents/openai.yaml` before/after SHA-256:
`5389196224e36e927b031b89b6dc7e0ad6378b158655df1225a01f9071bdd5ce`.
All pre-existing skill source/configuration files, including system skills,
matched their saved hashes; generated Python bytecode caches were excluded.

Local adaptations are documented in installed `matt-workflow/ADAPTATION.md` and
[the project guide](../../docs/archive/WORKFLOW-2026-10-07.md). Each installed upstream entry point
loads the same adaptation, including when invoked directly. This prevents the
router being the only place where project constraints are enforced.

## Verification

An inline Python validation imported the system skill-creator's
`scripts/quick_validate.py` and called `validate_skill` on each installed folder.
It also checked frontmatter names against folder names, every local Markdown
link, source-supporting-file hashes, installed hashes and preserved-existing-file
hashes. Result: **10 valid skills; all references/hashes passed**.
`python3 /tmp/matt-workflow-20261004/validate-stage.py` also passed before install.
The UI metadata generator successfully produced the router's `agents/openai.yaml`.

Required invocation chain checked against actual installed files:

```text
matt-workflow -> matt-grill-me -> grilling
              -> to-spec / to-tickets -> setup-matt-pocock-skills
              -> implement -> tdd -> codebase-design
                           -> code-review -> setup-matt-pocock-skills
```

All nine are present. Optional references to triage, domain-modeling, wayfinder,
grill-with-docs and improve-codebase-architecture in setup/reference material are
outside this selected workflow, explicitly not automatic installation dependencies.
Matt's original slash invocations for required skills now use Codex `$name` syntax;
references to the unavailable Claude Skill tool now read sibling skill files.
Existing upstream Codex implicit-invocation policies are preserved. `$matt-workflow`
is discoverable normally; the custom `$grill-me` retains its original policy.

Manual routing exercises, performed by the lead against the installed router,
adaptation and upstream instructions (not independent agent or end-to-end trials):

| Scenario input | Routed behavior / output | Result |
| --- | --- | --- |
| Substantial feature: add a user-visible export with unresolved format/scope | Clarify consequential choices via matt-grill-me; to-spec captures examples/exclusions; to-tickets proposes one usable export slice and demo; implement/TDD at the agreed observable interface; Standards and Spec review; demonstrate for owner verdict | Phase route and dependencies resolve; no feature built in this dry run |
| Trivial correction: fix a misspelled control label | Inspect authoritative text, make the narrow edit, run relevant existing link/check tools; no mandatory PRD/interview/new automated test | Lightweight route explicitly takes precedence over full-cycle defaults |
| Uncertain integration: can an existing adapter pass one synthetic input through to an observable result? | Establish the smallest tracer bullet with success/failure evidence before broader feature work; record failed prerequisite rather than expanding scope | Uncertainty gets a thin end-to-end check, not separate full UI/backend layers |
| Required behavior test fails | Keep technical status incomplete; report failure, fix/recheck only relevant evidence | Failure cannot be called completion |
| All automated checks pass; owner has not tried result | Report coverage and “verified within these checks”; experience acceptance and release remain pending | Green tests cannot supply the owner's verdict |
| Existing uncommitted work is submitted for review | Resolve known base; inspect tracked diff and relevant untracked patch; read current spec; keep Standards and Spec distinct in a sequential one-lead review | Avoids the upstream three-dot-HEAD empty-diff trap |

These exercises check the written routing and decision rules. They do not prove
automatic skill triggering in a future session or sustained quality/satisfaction.
The two-completed-slice retrospective remains pending in the existing backlog.

`python3 scripts/verify.py` passed once at handoff: **16 tests, two recipes, lock
structure and local links in 14 documents**, exit 0. A separate link check covered
all four new documents, including nested configuration and evidence omitted from
the gate's root-document glob. `git diff --check` passed, exit 0. No new automated
tests were added for these instructions/configuration changes. Only recording
these results followed the gate; no code, dependency or test changed.

Standards review of the setup: existing project authorities, one-lead rules,
provenance and private-data boundaries are retained; no unresolved violation
identified. Spec review: requested skills/supporting files, rename, global router,
local configuration and proportional verification are present. Pilot exclusion
follows the latest owner instruction. Future-session triggering and the two-slice
experience assessment remain explicitly unverified. Reviews were by the lead,
not independent agents; installation checks cannot establish future model behavior.

## Pilot scope correction

Before the owner asked to leave Hide HUD alone, cached native build/test checks
completed: 24 console practice tests and 4 audio regressions passed; the native
preview generated 11 images at each of 1280×720 and 1920×1080. Seven 720p states
were visually inspected. The 1080p images and remaining 720p states were not
visually reviewed before the stop; no full native visual acceptance is claimed.
Synthetic class/pause fixtures are not gameplay checks. No game was launched or
trial deployed, and no Hide HUD source was changed in this session.

Commands already run were the existing `.private/hide-hud/build.sh` with locked,
offline `play` builds for `launcher` and the console preview, and console/audio
test compilation; the asset-free Windows binaries ran via a reviewed private
PowerShell script. Sandbox cache access needed escalation. Existing upstream
`must_use`/private-interface warnings and preview dead-code warnings remain.
An optional contact-sheet attempt lacked Pillow; no dependency was installed.

The pilot was stopped on the owner's instruction and is not a setup completion
requirement. The existing Hide HUD patch was preserved at SHA-256
`31568ed152da16aecd4a93194c602e9a8fe05af29744a52e45936e7dbf3e780a`.
Private generated previews/logs remain ignored. This record preserves what
occurred without resuming, accepting or finishing the withdrawn pilot.

## Handoff and boundaries

Branch `slice/hide-hud`; HEAD/base
`bfcb6073a829cb7b7f1b314a66c7006213ef0917`. Working tree is dirty, including inherited
DECISIONS/RESEARCH/TRICKSHOT_MENU edits and the untracked Hide HUD patch. No commit
or project remote was created. Source authority remains Git plus explicitly
uncommitted edits; status authority remains BACKLOG.md.

`git ls-remote` refreshed the public skills HEAD, runtime HEAD/v0.4.0, and Synergy
HEAD on October 4. They matched the skills pin above and project pins
`f608f85e407ff1b7689d54a9aafdd16e95711ac4` and
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4`; pins were not moved.

No CI/CD, Sandcastle, publication, spending, external messaging or game-file upload
is part of this setup. Other repositories are not bulk-edited: configure them
against their own authorities when first used.

Next concrete step: invoke `$matt-workflow` on the next chosen non-Hide-HUD slice.
For Combine, retain the full trickshot-menu goal, read the existing inventory and
settled decisions, and identify one desired behavior/demo without restarting the
whole design interview. After two completed owner-reviewed slices, assess clarity,
objective progress and satisfaction before changing the workflow.
