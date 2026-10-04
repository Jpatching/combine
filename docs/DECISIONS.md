# Decisions and milestone outcome

## D-009: board audio and a private highlight edit — 2026-10-03

The owner requests board pop/landing sounds in the game and highlights from the
latest OBS recording. They clarify that “Tony Hawk” means music, then identify
the desired reference as the Christ Air/Jesus skating meme. Research identifies
Pearl Jam's Even Flow. Both the game and video should use the cue when a local
audio file is available; no new game integration is authorized by that wording.

Use native skating events and the existing audio output. Keep a separate source
delta after the menu patch and a separate development trial. Extracted collision
samples and recordings remain local; provisional event assignment needs an
owner listening check. No new recipe, network interface or assets in Git.
On October 4 the owner supplied a local MP3. Use it privately for the comedy
edit and ten-second game cue; preserve the original file and previous exports.
This removes the missing-file blocker without changing runtime source or
authorizing publication. The [result record](../research/results/2026-10-03-skate-audio-highlights.md)
separates implementation, synthetic checks, music mixing, startup decoding and
remaining listening/gameplay acceptance.

## Accepted direction — 2026-10-03

- Validate a business, with one owner plus Codex and a small budget.
- Investigate an existing-game pilot on Windows; the owner reports a Windows PC.
- Long-term product: discovery hub plus local configuration/launch companion.
- Near-term scope: reproduce the existing mashup and establish unmet user friction.
- Reuse the pinned runtime. Do not write an engine, arbitrary-game merger or platform
  before the baseline and user evidence justify it.
- Keep one local backlog; no paid hosting, remote publishing or recruitment automation.
- Global AGENTS.md received the three agreed refinements: proportional explanations,
  named verification gates with explicit handling when absent, and Git/remote/tracker
  requirements conditional on those facilities existing. This project names its own
  local gate and status authority. No other global settings were changed.

## D-001: baseline selection

Use upstream v0.4.0 at `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
The release tag and HEAD resolved to that commit on 2026-10-03. The GitHub release
metadata identifies a Windows archive and SHA-256 (see the lock). Prefer this exact
archive for initial reproduction; upstream's Rust `stable` channel is not an exact
toolchain pin. This selects a candidate, not a tested or legally cleared product.

## D-002: recipe scope

Implement an offline validator and two data-only candidate recipes. Manual runtime
selection is documented; no launcher API or automatic recipe application is promised.
Baseline candidate A is MW2 Rust map with optional skating; candidate B is Minecraft
overworld with MW2 combat and optional skating. Both pilot recipes require skating.

## D-003: public distribution gate

Public distribution and charging remain blocked by unresolved rights/provenance.
Local research and writing interview materials continue. No claim that game ownership,
an open-source root licence or an official download URL resolves all relevant rights.

## D-004: deliver vertical slices

The foundation is enough to begin, not enough to validate a product. Deliver one
player outcome end to end, including failures and evidence, before expanding breadth.
First reproduce MW2 on-foot while Skate prerequisites are unresolved; then add
skating and the voxel world. Product slices, if justified by observations, are play
one combination, reopen it, and reproduce a shared recipe on another PC. This follows
the end-to-end increment approach described by [Agile Alliance](https://agilealliance.org/resources/experience-reports/a-tale-of-slicing-and-imagination/).

## D-005: repeatability and owner control

Keep deterministic checks in scripts and project expectations in AGENTS.md. Once a
workflow has been exercised and stabilised, a focused skill can guide repeated slice
delivery. Existing connected tools cover current GitHub research; no new MCP server
or plugin installation is needed. MCP becomes useful for controlled external actions;
a plugin packages reusable skills/tools for distribution. See the [official plugin
architecture](https://developers.openai.com/plugins/concepts/plugins).

Use the checkpoint contract in docs/AGENT_ROLES.md. The owner authorizes a concrete
slice; routine work inside it continues without repeated proceed prompts. Present
observable evidence before expanding scope. Publishing/spending/outreach remain
separate boundaries, and environment-enforced approvals cannot be waived by a skill.

## D-006: skating first and understandable progress — 2026-10-03

The owner explicitly prioritised skating over the MW2-only ten-minute acceptance
run. C-003b is the current priority, blocked on legitimate Skate 3 files and controller
confirmation. Preserve C-003a preparation evidence; do not force its deferred play
check before preparing skating. Minecraft first play is owner-reported with a
possible freeze, not a completed Minecraft/skating baseline.

Use plain-language player outcomes before issue IDs. Keep one authoritative backlog
with a readiness table and one next action; split skating into file readiness,
first skating, and recovery/replay checkpoints. Minecraft first play/replay and
Minecraft skating are distinct checks. Record setup confusion as evidence for C-005;
no product UI, website or new management system is implemented yet.

The short vertical-slice default was added to global AGENTS.md and read-back verified.
It remains outside project Git history. Windows access through WSL was demonstrated
with sandbox approval, superseding the earlier claim that this workspace could not
launch Windows programs. Gameplay still needs the owner's observations.

## D-007: isolated skating preparation and traceable learning — 2026-10-03

The supplied local Xbox candidate passed extraction and bundled conversion. Prepare
and launch a separate `mw2-skate` trial using the pinned v0.4.0; preserve the older
trial and original installs. This supersedes the missing-input blocker in D-006.
DualSense detection passed; human skating/replay acceptance is still pending.
Preparation was agent-assisted and cannot measure unaided-player onboarding.
Asset distribution provenance is unresolved; no redistribution is authorized.
See the [preparation report](../research/results/2026-10-03-skating-preparation.md).

The owner's global explanation preference now includes what changes, where behavior
lives, why the approach fits, and traceable inputs/outputs/evidence. It was read-back
verified outside Git. Keep learning proportional: one useful concept and optional
prediction or small exercise, with no mandatory quiz or extra tracking system.

## Continue / change / stop — pending

Current recommendation: **continue the bounded private feasibility study only**.
No launch or investment recommendation is justified yet.

| Evidence | Threshold / interpretation | Current result |
| --- | --- | --- |
| Technical reproduction | Both candidates reproducible and exchangeable without editing code | Windows process launched; owner reports Minecraft worked; skating/replay unverified |
| Onboarding | At least 8/10 complete unaided in 15 minutes after prerequisites are ready | No participants |
| Repeat use | At least 5/10 return within seven days; missing follow-up counts as no observed return | No observations |
| Creator supply | Three interviews establish willingness, conditions and maintenance cost | No interviews |
| Payment interest | Record specific service, price response and commitment strength; intent is not revenue | Not measured |
| Rights | Relevant source/converter/asset/distribution questions resolved for the proposed release | Unresolved |
| Maintenance | Measure support minutes and integration effort; owner assesses solo affordability | Not measured |

Continue toward a narrow prototype only if technical reproduction works and observed
friction supports a specific improvement. Launch a business pilot only after the
usability/return thresholds and distribution gate are met. Change direction if users
only want discovery/installation, or rights require original content. Stop if neither
repeat value nor an affordable permission path exists. Inconclusive evidence remains
inconclusive; thresholds are small-sample decision aids, not market proof.

## D-008: Synergy-native menu replaces the rejected panel — 2026-10-03

The owner-selected plan authorizes porting Synergy MW2 presentation/navigation at
`33bcc80f5446e7543a2eb68b17c798e29d3f27c4` into the pinned mashup's native UI and
reusing the local practice actions. It supersedes the earlier text panel and the
older no-new-UI exclusion for this bounded slice. Preserve GPLv3 and attribution;
import no GSC loader, unrelated gameplay changes or IW4x binaries.

The UI is hidden at launch and destroys all its elements when closed. Navigation
uses a separate state machine and typed actions, with a physical-button release
barrier before gameplay resumes. Position/map policy, local-only bot conditions,
return-after-leaving-skating and default-off aim lock are preserved. Feedback
remains in the menu; actions do not auto-close it. The font comes from the existing
runtime. The smooth preset persists in the separate trial profile; its restore
snapshot is available only in the current process.

Use the named Windows build, synthetic tests and asset-free native previews to
verify implementation. Owner controller/gameplay acceptance remains separate.
Source publication to Jpatching/combine is authorized only after explicit
replacement acceptance. No binaries/game data, OBS/recordings, private logs or
local settings enter Git. The stunt launcher is a separate recorded proposal;
three repeatable on-foot attempts on Rust are its future acceptance criterion.

Project instructions now point to one player guide, one reproduction guide and
one evidence/status source per purpose. Do not replicate controls or setup in
handoffs or add formulaic what/where/why headings to player docs.

## D-010: full menu milestone and gameplay-only Hide HUD — 2026-10-04

The selected plan makes the full controller-friendly menu M1, beginning with Hide
HUD. The pinned MW2 inventory and slice contract are in TRICKSHOT_MENU.md. M2
covers stronger skating atmosphere, M3 private sessions, and M4 independently
repeatable curated setups. Red Dead is research only; edition/bridge unestablished.

Checkpoint inherited work before coding: `bfcb6073a829cb7b7f1b314a66c7006213ef0917`,
then branch `slice/hide-hud`. This is a local checkpoint, not owner acceptance.
The new feature remains uncommitted pending the owner's verdict, following the
plan's review → accept → commit sequence. No remote/publication is configured.

Use session-local gameplay visibility and existing native HUD/layer machinery.
Broad `ui 0` also hides class selection, so it is unsuitable. Keep recovery/menu
surfaces separate from gameplay geometry and preserve actionable skating prompts.
New map/session or main menu resets the setting; ordinary menu/skating/class/
respawn transitions preserve it. No network, recipe, movement or audio changes.
A third patch preserves the checkpoint menu/audio artifacts and their evidence.

## D-011: shared workflow, repository-specific authority — 2026-10-04

Install Matt Pocock's nine requested/dependency skills from the single source pin
`24fe0ef7737efae15c87225755e9f6f5965e4888`, preserving supporting files and MIT
attribution. Preserve the custom `grill-me`; Matt's version is `matt-grill-me`.
A small global `matt-workflow` router and shared Codex adaptation translate
invocation, tracker, review and commit defaults without replacing Matt's content.

The reusable standard is outcome → one usable slice → checks → review/demo →
owner verdict, scaled down for trivial changes. Per-project configuration keeps
existing requirements, checks, status and release authority. Combine uses
BACKLOG.md, TRICKSHOT_MENU.md and DECISIONS.md; no parallel tracker or PRD is added.
Routine authorized implementation continues autonomously. Failed/missing required
checks block technical completion; green checks do not imply owner acceptance.

The owner clarified that the goal is the full trickshot menu plus Combine practice
controls, then asked to leave Hide HUD alone. Stop the proposed Hide HUD workflow
pilot and leave its implementation untouched. This setup implements no gameplay
feature and grants no publication, deployment, asset upload or external messaging
authority. Keep one lead and local verification. Assess demonstrated friction
after two completed owner-reviewed slices before adding Sandcastle or automation.

See [workflow configuration](WORKFLOW.md) and
[installation/validation evidence](../research/results/2026-10-04-matt-workflow.md).

## D-012: proper Synergy destination and private board authority — 2026-10-04

The owner selected the proper Synergy menu plus trickshot hit radius, without
Combine-specific practice additions. This supersedes the earlier D-010/D-011
HUD-first ordering and practice-controls destination. Preserve existing menu,
audio and Hide HUD work; Hide HUD is deferred and blocks no current slice.
Source coverage and a bounded Intervention candidate are recorded in the menu
guide. Remaining choices must precede final PRD/slicing; a candidate draft does
not prove those phases complete or authorize invented behavior.

The verified private Combine GitHub Project owns active status. Seventeen draft
items preserve current/deferred outcomes with named dependency links; completed
old records remain in the frozen backlog. Requirements, decisions and technical
evidence retain their existing local authorities. If GitHub is unavailable,
record sync pending in the handoff rather than create a competing tracker.

The owner explicitly requested a clean seven-phase visualization and confirmed
that only Combine-specific corrections belong here. Reusable workflow material
lives in global Codex storage. Private board maintenance is authorized; source
publication, assets, recordings/logs, outreach, spending and CI/CD are separate.
Publication still requires explicit acceptance of the replacement menu. No new
gameplay implementation, gameplay test, commit or source publication occurred.

## D-013: near-pass assistance and full-menu scope — 2026-10-04

The approved C-017 plan settles the remaining product choices in D-012. Keep the
full reachable pinned Synergy menu plus near-pass hit radius, without Combine
practice additions. The [menu guide](TRICKSHOT_MENU.md#agreed-behavior--c-017-2026-10-04)
owns the detailed contract and acceptance examples. A bullet passing near an
eligible living enemy can qualify independently of its eventual impact; radius
is extra distance outside the normal damageable body volume. This is neither
aim movement nor added blast damage. The inspected Trickshot Dummy impact-distance
implementation does not establish this behavior.

Cover scoped/unscoped sniper bullets, bots and private enemy players; exclude
self, teammates, dead players and spectators. Assistance starts Off, with Normal
damage and 0.25 m on first enabling; adjust 0.25–5 m in 0.25 m steps and reset
assistance to Off for a new match. Normal uses upper-body weapon damage with
distance/penetration reductions; One-shot is lethal only for a qualifying hit.
Both respect ordinary reach and cover/penetration. Assist only an otherwise
missed shot, at most once, selecting the closest eligible enemy; retain ordinary
direct hits and collateral behavior.

Include Frag No Clip, superseding the earlier C-011 no-noclip exclusion. Restore
movement/weapons and only temporary invulnerability on exit, with death/map
cleanup. The native safe-exit policy rejects an exit inside solid geometry with
feedback until the player moves clear. Include All Players/name display/Kill/
menu grants/Kick with host administration, personal-only guest grants and host
Kick protection. Revalidate permissions and connection identity when executing
actions so stale selections or reused names/slots cannot affect another player.

Synergy supplies behavior references, not proof of native compatibility or
private-session synchronisation. Those remain explicit implementation research.
Proceed through to-spec and to-tickets for the agreed Intervention tracer bullet;
requirements agreement does not establish gameplay, owner acceptance or release.
Hide HUD stays deferred, and source publication still requires explicit acceptance
of the replacement menu. No runtime change or new trial is part of C-017.
