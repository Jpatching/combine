# Current context

## Current task

Reviewed: 2026-10-09

Task: fix checksummed resource framing in [#34](https://github.com/Jpatching/combine/issues/34), following the bounded street experiment for #20.

Source branch: `implement/gtaiv-collision-inspector`

Source revision: `fcb4acc0c643d7244a8cae1db83c9e08b1a07887`

This is the inspector revision before the framing fix. The issue and existing
PR own the final publication revision and review evidence.

Disposition: framing fix prepared for existing draft PR [#37](https://github.com/Jpatching/combine/pull/37); source approval and merge remain pending. Owned resource remains unsupported because its root is composite.

The owner authorized this focused fix using implement and TDD at the existing
command/parser boundary. The broader selected goal remains real GTA IV plus
Skate: one street with visible board/animation, curb/wall contact, dismount and
ordinary GTA driving. Traffic/pedestrians stay active; riding contact with moving
objects is deferred. No full-city or composite implementation is part of this fix.

## Evidence

The [inspector](../tools/gtaiv-collision/README.md) now validates the full zlib
stream, including its checksum, within the existing decompression bounds.
The previous parser skipped the zlib header and rejected the valid checksum as
trailing junk. Authored fixtures now include a real checksum: the existing
command test failed before the correction and passed afterward. The added
invalid-framing command regression fails against the original revision's
acceptance of a missing checksum. Corrupt/missing/truncated checksums, appended
data and concatenated streams return invalid after the correction.
Eight focused command/parser tests and the repository gate's 62 tests passed;
link/context checks passed across 59 documents. No separate Python typechecker
is configured in this repository.

The separate [street experiment](https://github.com/Jpatching/combine/issues/20#issuecomment-6087765258)
is preserved at `a4fec7364c957bd4bf80e3fb6eb80e04ba6eb054` on
`prototype/gtaiv-street-collision`. It acquired one owned WBN in private storage.
The corrected inspector was run on that same input and returned
`unsupported / unsupported-root` with exit 2. The experiment classified the root
as composite. No geometry, child transforms or world placement were decoded.
Private input remains under ignored `.private/gtaiv-street-collision/` and must
not be uploaded. This fix does not incorporate the archive-reading experiment.

Latest runtime evidence: the earlier gameplay candidate `b403377481a33e407aeb81b78b8d38984aac4735` refused a guarded mount at `over-0.05-metres`. No GTA launch, staging, input or runtime test occurred for this framing fix.

## Next step

Review the corrected source candidate in draft #37. Its framing defect is fixed;
its geometry support is still deliberately narrow. Keep #34 open until approved
and merged. Synthetic success and an unsupported owned-file verdict do not
establish gameplay acceptance.

The street experiment's next technical blocker is composite collision and child
transforms. Establish bounded decoding and independently validate selected street
placement before feeding triangles to Skate. Do not assume identity transforms,
silently skip shapes, substitute a synthetic floor or relax flatness guards.
If placement cannot be established, reconsider acquisition. Preserve the runtime
candidate, worker evaluation, draft [#23](https://github.com/Jpatching/combine/pull/23)
and recovery branches; #21/#22 remain blocked.

## Session close

Use [context maintenance](agents/current-context.md) and
[workspace conventions](agents/issue-tracker.md). Read #34's latest fix evidence
before resuming its candidate, and #20's experiment record before further street
work. Keep resources, keys, geometry, settings, identities and raw logs private.
Source approval, merge, gameplay verification and owner acceptance are distinct.
No merge or runtime launch is implied by this fix.

## Historical reference

[Host decision](adr/0001-preserve-offline-gta-gameplay.md),
[glossary](../GLOSSARY.md), [workbench](WORKBENCH.md),
[physical collision report](../research/results/gtaiv-120059-physical-collision-feasibility.md),
[retained GTA context](archive/HANDOFF-2026-10-09-gta-context.md).
The full street experiment and reaffirmed demonstration scope are preserved on
`prototype/gtaiv-street-collision`; they are not merged by this source fix.
Research #31/#32 is merged; its source findings did not establish runtime compatibility.
