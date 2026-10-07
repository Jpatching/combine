# Resume reconciliation evidence — 2026-10-06

This slice makes the current outcome and next action visible from the existing
private board and Git. Planning and ticket slicing are complete; runtime integration,
physical trials, owner acceptance, merge and release remain incomplete.

## Live observations and reproduction

Observed 2026-10-06 around 08:04 UTC. Source reads:

```sh
git fetch origin
git ls-remote origin
git rev-list --left-right --count main...origin/main
gh pr view 1 --json state,headRefName,headRefOid,baseRefName,statusCheckRollup,body
python3 ~/.codex/workflows/solo-development/projects.py summary 5 /path/to/combine
```

Fetch was part of reconciliation, not the summary command. Remote main is
`a5593d671142f31653d45caeaad7b926d40ff855`; qualification branch is
`b399c55b3abff6fc864fd3158f7df36b17906eac`. Local main comparison: `0 9`
(zero ahead, nine behind). Local main remains
`bfcb6073a829cb7b7f1b314a66c7006213ef0917`. PR #1: OPEN, qualification into main,
empty statusCheckRollup. Its body records 13 local focused Rust tests, patch replay
and the repository gate at b399c55; these are recorded evidence, not newly rerun
runtime checks. Full PR diff review is required before any merge proposal.

The board was read with the existing helper's snapshot API. C-024 is Now, C-025
Next; C-019/C-020 next-action pointers agree. C-021 and C-023 remain Done; C-016
physical trial remains pending. C-026 through C-030 are Later with unchanged
contracts/dependencies. Outcome-first titles retain identifiers. Fields, bodies,
titles and unrelated state were read back after mutation; custom views preserved.
The helper's old strict view validator rejected extra owner-visible columns;
validated field writes and exact read-back were used without resetting the views.

## Bounded private metadata check

No raw parser log or game asset was sent to an AI service. Reproduction reads only
small identity/inventory/failure JSON records in the owner's private input folder.
Set `COMBINE_INPUT_ROOT` locally; do not publish its value. The exact query used
these filenames and selected fields (paths are deliberately absent from output):

```python
import json, os
from pathlib import Path
root = Path(os.environ['COMBINE_INPUT_ROOT'])
for record in root.rglob('identity.json'):
    d = json.loads(record.read_text())
    print({k: d[k] for k in ('build', 'manifestFiles', 'archiveFiles',
                             'missingFiles', 'extraFiles')})
    print('Shipping hash matches:', d['shippingSha1'] == d['shippingReferenceSha1'])
for record in root.rglob('inventory.json'):
    d = json.loads(record.read_text())
    print({k: d.get(k) for k in ('mounted', 'unmounted', 'encryptedUnmounted',
        'files', 'worlds', 'completeIsland', 'collisionQualified')})
for record in root.rglob('failure.json'):
    d = json.loads(record.read_text())
    print('Failure type:', d['type'])
```

Identity: `++Fortnite+Release-3.1-CL-3917250-Windows`, 3,323 manifest/archive files,
empty missing/extra lists, matching shipping hash. This verifies what metadata
records; it does not rehash all assets or establish acquisition rights. Six recorded
parser inventories all mount 0 of 10 containers, list 0 files and no worlds, and
leave completeIsland/collisionQualified false. Three include encryptedUnmounted=10;
this is a parser report, not proof of the cause. Six failures are
InvalidDataException; recorded message: “Unmounted containers or no worlds:
inventory is incomplete.” The untracked exporter was not executed or modified.
No serialization/export/collision witness exists. Actual replacement version choice
remains unrecorded; permission to choose one is already present on the live board.

Asset prerequisite discovery used bounded directory queries: project private area
to depth six for `private/stock`, depth four for `stock`, and the existing Windows
owner-profile area to depth four for `stock`. No matching prepared tree found.
Earlier extracted Skate Xbox data exists; that is not a prepared host asset root.
The inspected host loads stock input, GameAssets, graphs, physics, skater, camera
and markers. Confirm the existing prepared Windows trial root and these resources
before C-025 rendering. Searches do not prove absence elsewhere; no conversion,
game launch or new gameplay verification occurred.

## Verification boundaries

Global `test_summary.py`: seven tests pass, covering dirty/untracked files, missing
remote branch, unavailable reads, conflicting Now and parent-in-Next pointers,
private path formats, open PR visibility from a fresh branch, and byte comparison
of a fixture repository before/after summary. Global `test_workflow.py`: final rerun passed all 15 tests. Tests use
synthetic fixtures and do not upload private input. The summary does not fetch,
write Git/board state, store status snapshots, merge or launch games.

The repository gate tests research/scaffolding, recipes and document links. The
recorded focused Rust tests establish native world validation/error behavior only.
The full host all-target suite is blocked by inherited missing
`src/tests/map_startup.rs`; a reviewed correction and full rerun are needed before
broader host verification. Windows rendering, controller, real-data collision,
performance, recovery and gameplay need separate exact-build trials and verdicts.
No CI, branch protection, automatic merge or deployment added. Two one-minute
resume experience checks remain future work, with retirement if the helper adds friction.

Final repository gate: PASS, 27 tests, 2 recipes, links in 17 documents;
`git diff --check`: PASS. Upstream handoff read: HEAD and v0.4.0 remain
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`; no pin moved.

Installed global artifact SHA-256 (outside Combine Git):
- `projects.py`: `2d7ece369b89d705a106fa3d161fb95d369498df03c635eb8e5ab42926316f9c`
- `test_summary.py`: `135afb40941d63a93a4570a282b4476796abf32761f131f0dcd96cd79ebcf81d`
