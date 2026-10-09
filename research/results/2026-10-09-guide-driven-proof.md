# Apply the guides: prove the existing-game handover

For [research requirement #28](https://github.com/Jpatching/combine/issues/28), 2026-10-09.
The owner asked the agent to use Universal Modder and REA to select the next technical
step. This supersedes the pending request to choose between integration, fidelity
and world interaction. The retained product goal and prior rough-presentation
acceptance remain the starting point; no new permanent architecture is selected.

## Subsequent owner decision and runtime observation

Later on 2026-10-09, restoring the minimized GTA window produced fresh validated
gameplay status. A guarded mount trial at staged revision
`b403377481a33e407aeb81b78b8d38984aac4735` refused at `over-0.05-metres`
before playback and retained fresh GTA control. A requested live window change
was verified at 1280×720 with fresh gameplay status. This does not establish a
publisher defect, accepted riding or the cause of the surface refusal.

The owner then selected assessment of the missing world-collision connection,
using Universal Modder's rebuilt-guest-in-real-host route. The
[world-collision next proof](2026-10-09-world-collision-next-proof.md) and
[handoff](../../docs/HANDOFF.md) now select the next action. The handover contract
below remains a later integration check; the stale-status investigation and
unchanged flat-patch mount retries are no longer the immediate task.

## Selected investigation

Use Universal Modder's **rebuilt guest engine in a real host** route. Its first-slice
table calls for fixed inputs and poses against a fake host, followed by a real-host
mount/ride/dismount and guest crash/stall check. That independently supports testing
the whole handover contract; it does not establish that the mount refusal's cause
is the right engineering task or that collision acquisition must come first.
[Route and first-slice table](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/choosing-a-mashup-route.md),
[ownership and process placement](https://github.com/rehan-remade/universal-modder/blob/8370faa8e114baf33acdb23079aff552a7728c4b/knowledge/techniques/rebuilt-guest-engine-inside-a-host.md).

Reuse the [dated synthetic Session/worker evidence](2026-10-08-separate-skate-worker.md)
instead of rerunning it to manufacture progress. It supports the fixed-input/pose
boundary, not GTA gameplay. Retain the pinned Session, GTA IV 1.2.0.59 and both
existing candidates. The [source-interface audit](2026-10-09-repository-interface-audit.md)
found no ready replacement that avoids the missing host integration.

REA supplies the question/evidence discipline. Use public source first; open a
specific shipped artifact only when a concrete native behavior remains unresolved.
Do not run REA readiness, install a provider or decompile a game merely to claim
use of the tool. No REA native analysis is claimed by this investigation.
[REA instructions](https://github.com/morluto/rea/blob/f085589957922eaf421db814399e88e415712050/skill-src/reverse-engineer-anything/SKILL.md).

## Proof contract

Question: can the retained rebuilt Skate Session control movement visibly inside
the existing GTA game and return ownership reliably, without replacing the host?
The limited proof does not establish full-city interaction or original Skate parity.

- **Baseline:** reconcile source, installed adapter and helper identities before a
  trial. Reuse the qualified game baseline; preserve original installations and
  private trial evidence. Start with the already-staged candidate if its identity
  matches, rather than replacing it to run a comparison.
- **Scenario:** one clear, bounded real GTA patch. Begin with normal walking,
  deliberately enter riding, push, steer left and right, stop riding, walk and
  enter/drive a vehicle. Rough rider presentation is sufficient; input-driven
  position, heading and usable camera must be visible.
- **Repeatability:** propose three consecutive complete cycles from a recorded
  starting state. This is a new investigation criterion, not prior acceptance.
  A refusal is recorded separately and does not count as a completed cycle.
- **Recovery:** for an already-authorized worker trial, interrupt only its owned
  worker and observe restored GTA control, unfrozen player and camera cleanup.
  The existing source uses a response-gap threshold above 250 ms and a separate
  two-second no-frame rescue; record detection and visible recovery separately.
  Those source thresholds are not measured end-to-end recovery guarantees.
- **Evidence:** uncut local recording plus timestamped input, pose freshness and
  ownership verdicts. Keep media/raw diagnostics private. Save source-safe pass,
  refusal, failure or unavailable summaries. Show the actual result to the owner
  before asking for acceptance.
- **Stop:** failed restoration, stale observations or mismatched runtime identity
  stops a live trial. After repeated identical refusals, retain the evidence and
  investigate one discriminating hypothesis; do not relax the guard, change
  placement or build a broad scene extractor simply to continue.

The source thresholds and ownership behavior are described in the
[retained adapter](https://github.com/Jpatching/combine/blob/c87e59471c34aff6ffcae5f23b8afc320ca6bd09/tools/gtaiv-skate/README.md).
This contract prepares a bounded experiment; it does not authorize launch,
staging, input automation or termination of any process. Those actions need the
existing runtime workflow and task authority. #20 remains the existing gameplay
issue; do not create a duplicate ride ticket. Its separate collision-research
prerequisite remains applicable if that investigation is selected.

## Decision rules

A passing loop supports continuing this integration route, not choosing its final
process placement. A failure becomes an identified boundary to investigate using
matching source or, where necessary, REA artifact/runtime evidence. If a required
interface cannot meet the contract on this baseline, return to the audited
alternatives with that evidence. A clear mismatch in reconstructed-Skate behavior
is recorded as a simulation limitation, not silently fixed by changing the goal.

## Checks in this follow-up

The pinned Universal Modder knowledge searches for `rebuilt guest` and `gta iv`
completed through `scripts/workbench.py`, returning the route, ownership and
collision guidance used above. No upstream installation or runtime pin changed.
Fresh read-only Windows checks returned:

- One GTA process; status file not recent (file timestamp older than three seconds).
- The retained status module returned `Scene=unknown`, `CanTest=false`.
- The installed status-publisher script matched the preserved public source hash.
- A 32-bit process inspection reported the adapter and CLEO modules loaded.

The status reader was taken from the retained worker worktree and matched the
integration branch's source, rather than the stale helper path on main. Initial
module import was blocked by PowerShell policy; the reviewed read-only module ran
with an explicitly approved process-only execution-policy override. No persistent
policy or game files changed. Only fixed labels and booleans were returned; private
status contents, process identities and raw logs were not published.

These observations establish a stale observation channel, not its cause. Loaded
modules and matching script bytes do not prove the script is executing or the
installed plugin matches the intended candidate. No launch, game input, staging,
worker interruption or ride trial occurred.

**Immediate next action:** diagnose why the matching publisher does not produce a
fresh validated status. The feedback condition is a fresh, process-bound report
with explicit native state; `unknown` is not readiness. Compare the publisher's
execution/registered-command path and bounded write failures before changing code
or installation. Resume the selected proof only after runtime identity and fresh
observations are established. This replaces repeating a mount attempt under stale
telemetry. Repository checks validate these documents, not the proof.
