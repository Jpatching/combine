# Actual Synergy input checkpoint — October 5, 2026

The actual pinned GSC remains the menu implementation. The input adapter keeps
navigation buttons available to Synergy while consuming gameplay commands and
stale button history through closing and the neutral release frame. Fresh input
after release restores ordinary gameplay. No native imitation or new engine.

Owner report: Intervention worked in the most recent trial, all other options
were missing. The report supplies no exact build identity or full-menu verdict.
This is successful Intervention experience evidence, not acceptance of all options.

## Source and reproduction

Base Combine revision: `b52c28f6fe1a21c81f610a7d96a7e48d7f953650`, branch
`slice/synergy-input-isolation`. Apply trickshot, skate-audio, Intervention,
synergy-gsc, synergy-input in order to runtime
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`. The pinned menu remains
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4` from
[Synergy MW2](https://github.com/SyndiShanX/Synergy-GSC-Menu/tree/33bcc80f5446e7543a2eb68b17c798e29d3f27c4/MW2).
Upstream HEAD/tag/main observations on October 5 still match both pins.

Input patch SHA-256:
`00af9a992b9ce7b04c1ce3a89a37734377a129093dbff3f6e04aa7453e091527`.
Observed executable SHA-256:
`e06c7f1fc217523485363fe156fe448ea94b2cba8b14c52cb66a3d4fff5e9268`.
The existing executable was built by the preceding work; source replay below
checks its current source delta. Commit/build-linked review preparation remains
pending required runtime checks.

## Checked evidence

- Input patch replay: `git apply --check`, apply in a fresh temporary copy of
  the committed four-patch base, then byte comparison: all 16 runtime files match.
- Windows sim lib test executable, filter `synergy`: 4 passed, 0 failed.
- Windows console lib test executable, filter `practice`: 20 passed, 0 failed;
  includes keyboard/pad capture, held close/fresh fire, skating controls and
  focus/reconnect state coverage. Synthetic integration, not physical gameplay.
- `python3 -m unittest discover -s tests -p test_synergy_diagnostic.py -v`:
  7 passed after reproduced failures for invalid baseline/provenance fixtures.
- Windows `tests/test-synergy-diagnostic.ps1`: passed chronological repeated
  observations, imported/unclassified faults and private-argument redaction.
- Shared `test_review_bundle.ps1 -Adapter scripts/prepare-trickshot-trial.ps1`:
  14 behavior checks passed with synthetic fixtures. The Synergy wrapper still
  passes synthetic Synergy-specific isolation/automation/shortcut/environment tests;
  exact trial preparation/read-back is the remaining delivery check.
  Forward-slash profile rewriting was corrected and tested; source settings stay
  unchanged. Synthetic review verification was refused while the diagnostic ran,
  then passed after its exit, demonstrating duplicate-process protection.

Diagnostic 09 historically recorded the menu hierarchy, Intervention held,
close and fresh closed-menu firing, normal exit 0, and the inherited statistics
fault. Its old checker passed. Independent review exposed weak evidence handling:
merged/deduplicated streams, faults limited to maps/mp, private error arguments,
and an exemption without a successful same-build disabled baseline. The new
runner uses one chronological runtime latest.log and redacts fault arguments;
the new checker rejects old reports without provenance. Do not upgrade historical
09 evidence to a new checker pass.

Diagnostic 10 exited 0 but did not complete the navigation sequence. Diagnostic
11 exited `-1073741510` (Windows control/close termination) before relevant
observations. Neither passes. The requested 1080 capture files from earlier work
are actually 2560x1351; 720 captures are 1280x720. Actual 1920x1080 presentation
were then checked in corrected diagnostics 12/13. Disabled 12 exits 0 and
reproduces statistics on the same binary. Enabled 13 exits 0 and passes the
corrected checker: hierarchy/equip/close/fresh fire, no observed open-menu shot.
All four PNG headers from 13 report 1920x1080. Extra reopen/close observations
remain visible in the chronological stream; no physical owner interaction is
inferred from automated commands.

## Review and boundaries

Independent review of the inherited source found one Standards issue (private
arguments) and three Spec issues (fault omissions, ordering and baseline identity).
Focused fixes and regressions are recorded above; re-review found all four addressed; no remaining actionable source defect in its bounded scope.
The world's existing offline statistics/schema fault is inherited debt, but its
exemption now requires a successful disabled run of the same executable.

Raw logs, machine paths, captures, game assets and local settings remain private.
Diagnostic launch is a bounded test and supplies no owner verdict. Source checkpoint `c5910860c57b69c7e7c8dc2edae88f3cf99a31f7` was committed.
The repository gate passes: 23 tests, 2 recipes, 14 linked documents. The pinned
Windows launcher rebuild succeeds with the same executable hash; inherited
compiler attribute/private-interface warnings remain. The versioned desktop
review folder **Combine Synergy - 2026-10-05 - c591086** is prepared and
unaccepted. Read-back verifies source/hash/three shortcuts; `-VerifyOnly` passes
without starting the owner game. Its checklist states the closed-capture gap.
The 1080 capture labelled closed still shows the menu open; it cannot establish
closed presentation. The chronological stream proves an earlier close and fresh
shot; synthetic capture tests cover close/release and closed native rendering.
Owner checks must confirm reliable physical open/close and presentation.
No local release, merge or public full-menu release is claimed.
Basic loadout is the first coverage batch after this checkpoint; all untested
menu options and hit radius remain requirements. Hide HUD stays deferred.
