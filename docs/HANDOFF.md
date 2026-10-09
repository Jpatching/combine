# Current context

## Current task

Reviewed: 2026-10-09

Task: bounded real-street collision experiment for [#20](https://github.com/Jpatching/combine/issues/20), following the owner's reaffirmed real-GTA-plus-Skate direction.

Source branch: `prototype/gtaiv-street-collision`

Source revision: `00fd570d98b86c3479c9607b75eb299172095221`

This is the synchronized main starting revision. The experiment branch and #20
own the preserved result revision; this snapshot does not identify a new runtime.

Disposition: preserved experiment; blocked at composite collision decoding and transforms, before placement or gameplay. No PR exists for this experiment.

The owner selected a real street demonstration: visible board and recognisable
Skate animation, push/steer, ollie onto pavement, wall contact, dismount and GTA
car use. Traffic/pedestrians remain active; riding contact with moving objects
is deferred. The existing host decision is reaffirmed. The current request
supersedes the inspector-only task selection, without merging its candidate.

## Evidence

The [experiment record and reproduction](../tools/gtaiv-street-prototype/README.md)
distinguish acquisition, authored checks, owned-file inspection and untested
runtime behavior. A reviewed private adaptation read one local archive and
acquired one owned WBN. The original inspector rejected its valid zlib trailer;
an authored fixture reproduces that framing defect. A temporary framing
correction reaches an unsupported composite root on the owned resource.
No geometry was decoded and no child transform or world placement was proved.
The pinned reference's composite reader omits child matrices.

Private acquisition code, source snapshots, input and result records are retained
under ignored `.private/gtaiv-street-collision/`. Do not upload them. The public
reproduction uses authored data and loads the exact inspector Git object; its
optional owned-file mode prints verdicts only. A successful reproduction exit
is not a supported-resource or runtime verdict.

Latest runtime evidence: the earlier candidate `b403377481a33e407aeb81b78b8d38984aac4735` refused a guarded mount at `over-0.05-metres`; this experiment did not run GTA. A read-only Windows process check found GTA closed.

Inspector [#34](https://github.com/Jpatching/combine/issues/34) and draft
[#37](https://github.com/Jpatching/combine/pull/37) remain unmerged. Their seven
synthetic tests and 61-test gate were earlier source checks, not owned-resource
compatibility. The prior no-extracted-resource blocker has been resolved locally;
framing and unsupported composite layout now explain the owned-file refusal.
The inspector candidate itself has not been changed by this experiment.

## Next step

Use the reproduction to correct zlib framing through the existing inspector's
review flow. Establish bounded composite and child-transform support before
feeding this resource to Skate. Then validate a selected street's world placement
against GTA physical contact before claiming a collision connection.
Stop on unsupported required layouts or unexplained placement; do not flatten
children, substitute synthetic surfaces or relax the retained flatness guard.
If transform semantics cannot be established, reconsider acquisition.

Preserve `integration/gtaiv-skate-loop`, draft
[#23](https://github.com/Jpatching/combine/pull/23), the separate worker candidate
and recovery branches. No permanent process architecture was selected. The full
visible street milestone remains outstanding; #21/#22 remain blocked. Reconcile
follow-on specifications/tickets with #20 rather than creating a competing backlog.

## Session close

Read the live #20 experiment update and #34 defect evidence, then follow
[workspace conventions](agents/issue-tracker.md) before edits. Continue from this
experiment only for its bounded question; promote any useful fix through a
reviewed source slice. Keep resources, keys, identities, private scripts and
recordings out of Git and AI uploads. Runtime proof, owner acceptance and merge
are separate. No game launch, staging or runtime capture occurred in this trial.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[physical collision research](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md).
Research #31/#32 is merged; its source evidence did not establish geometry or
runtime compatibility. Earlier inspector handoff is preserved on
`implement/gtaiv-collision-inspector` at `fcb4acc0c643d7244a8cae1db83c9e08b1a07887`.
