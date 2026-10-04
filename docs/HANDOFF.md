# Handoff — resume Synergy input isolation

The actual pinned Synergy GSC runs in the mashup and automated interaction reached
Intervention equip/hold and close. Input isolation is unfinished: diagnostic 05
recorded a shot while the menu was open. No corrected owner trial is ready or
accepted. Full menu coverage and trickshot hit radius remain, followed by the
Fortnite qualification and map slices in the [agreed order](WORKFLOW.md).

The live [C-016 card](https://github.com/users/Jpatching/projects/5?pane=issue&itemId=261972158)
was read on 2026-10-04: Phase 5 Implementation, sole Now item, Codex next,
input isolation first. Its current evidence identifies the statistics error as
inherited debt reproduced with Synergy disabled; an older section still called
it the integration blocker. Preserve that distinction when reconciling evidence.
The board remains status authority; this file is a recovery/evidence pointer.

```text
Physical input -> actual Synergy script -> menu action
       | menu captured / held after close -> block gameplay input
       | released after close -> ordinary gameplay
       v
Regression checks -> committed exact build -> owner trial -> explicit verdict
```

## Source and inherited work

- Product checkout: branch `slice/synergy-input-isolation`, HEAD
  `3f2e70d6b9be401251373a61f55cd0616c150a57` at the workflow audit.
  Actual-script checkpoint is `71d5025d15ebbeb79985f54cc653745922e0bed6`;
  runtime and Synergy pins remain unchanged in `research/upstream.lock.json`.
- Four inherited paths remain dirty: `scripts/prepare-trickshot-trial.ps1`,
  `scripts/check-synergy-diagnostic.py`, `scripts/launch-synergy-trial.ps1`,
  `templates/synergy-checklist.txt`. They are not validated or included in this
  workflow-only change.
- Runtime input edits are in the ignored `.private/intervention/upstream`
  checkout, including console and simulation `synergy_input.rs`. They are not
  captured by a Combine commit. Inspect/reproduce before editing, then capture
  the reviewed source delta as a patch. Private reproduction helpers and
  diagnostics are under `.private/synergy/`; never publish their raw contents.
- Workflow repair is isolated on `chore/workflow-routing`, based on `3f2e70d6b9be401251373a61f55cd0616c150a57`
  in a separate worktree. Resolve its exact commit with Git. Before resuming in
  the product checkout, bring over this reviewed documentation commit while
  preserving the four inherited paths and runtime checkout; this is local
  integration, not a GitHub merge or release.
- Read [workflow evidence](../research/results/2026-10-04-workflow-routing.md)
  for installed defaults and verification. Remote branch read on 2026-10-04
  returned no heads before this repair. Resolve publication and synchronization
  from the remote branch SHA and latest live card; do not infer them from this file.

## Next check

Resume the input regression, covering open/navigation, held release, skating
shortcuts, focus loss and controller reconnect. Recheck actual Intervention flow,
fresh closed-menu firing, presentation and relaunch; record failed/missing checks.
Only then prepare a versioned exact-build trial and stop for the owner to test.
The native imitation remains rejected; no synthetic check establishes play.

Earlier [actual-script evidence](../research/results/2026-10-04-synergy-gsc.md)
and [menu requirements](TRICKSHOT_MENU.md) remain relevant. Baseline recovery,
possible freeze, audio listening and original-file comparisons are inherited gaps.
Fortnite access/build identity/export remain unverified; no Fortnite assets or
adapter have been added. Preserve assets, logs, prior trials and original installs.
