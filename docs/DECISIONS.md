> Process note: D-034 supersedes earlier custom workflow, routing and closure rules.
> Historical entries retain their original context; product and safety decisions remain.

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

Use the checkpoint contract in docs/archive/AGENT-ROLES-2026-10-07.md. The owner authorizes a concrete
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

See [workflow configuration](archive/WORKFLOW-2026-10-07.md) and
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


## D-014: exact-build review handoff and public repository — 2026-10-04

The approved implementation plan selects local checkpoint commits before final
build/test handoff, one Intervention branch, Windows test/files/checklist
shortcuts and a local evidence manifest. Shared helpers belong in the existing
global workflow directory; Combine holds its adapter, checklist and evidence.
One lead continues; automatic task pickup is deferred until an owner-tested
handoff works. Failed checks keep the slice in Phase 5. Phase 6 requests Trial,
not assumed acceptance. Actual starts are recorded; target dates are deliberate.

The owner then requested a public repository to attract users and a public
repository default for new projects. `Jpatching/combine` was created PUBLIC with
ADMIN access and connected as origin. Global instructions now carry the default,
with project privacy overrides and existing private repositories preserved.
The subsequently refreshed project instructions retain replacement acceptance
before source publication. Repository creation is complete; source push, PR,
merge and release remain separate and have not occurred. No game assets, private
logs, recordings or settings enter the source repository. Later priority: finish
the usable Windows trial and production evidence before more workflow work.


## D-015: execute Synergy itself — 2026-10-04

After seeing native Intervention previews, the owner said "i don't want our menu
i want that new one", then confirmed "yes synergy its self". This settles the
identity of the requested replacement: the pinned Synergy GSC menu, including
its own presentation and options. A Combine-native imitation or labels over the
old panel is not the requested delivery. The earlier native-port mechanism and
bounded-menu presentation are superseded; preserve their commits and results.

Check compatibility using the mashup's existing script compiler, runtime and HUD
support. Synergy's MW2 README requires IW4x, so direct compatibility is not yet
established. Keep adaptations narrow and traceable to the pinned source; do not
silently replace its menu with ours. Opening the actual menu and equipping the
Intervention is the first observable integration check. Existing full-menu and
hit-radius requirements remain; gameplay and individual feature support require
evidence. This does not authorize a universal loader, new engine or production
launcher. No corrected trial, owner acceptance or source publication occurred.


## D-016: menu completion, Fortnite qualification and reviewed source branches — 2026-10-04

The owner supplied the plan “Finish Synergy and add a Fortnite map to the existing
mashup” for implementation. Finish input isolation and its first trial, then the
agreed menu inventory and hit radius. Qualify legitimate access and export of
Windows Fortnite Release-3.1-CL-3917250, starting with one Tilted building and
surrounding ground; only then implement the existing-world adapter and expand to
bounded Tilted Towers. The selected build is a research target, not verified local
data or successful conversion. The plan's defaults and exclusions are preserved
in docs/archive/WORKFLOW-2026-10-07.md; menu requirements remain in docs/TRICKSHOT_MENU.md.

The plan authorizes reviewed source-branch commits and pushes, with private assets,
original installs and older builds preserved, checks before a versioned trial,
and a stop at ready for owner test. This supersedes the earlier source-publication
acceptance condition for these branches. It does not authorize asset distribution,
merge, release, spending, online services or automatic gameplay acceptance.

## D-017: one resume entry point and bounded model/agent routing — 2026-10-04

The owner requested a workflow that resumes the latest work without remembering
skill order or repeatedly choosing /model. Use “Continue Combine” and the existing
matt-workflow router; reconcile live Git, the current board card and concise
handoff before selecting the next missing check. Load targeted current context;
archives stay historical. Record failed sync explicitly and read back writes.

Personal model/agent configuration and reusable policy stay in global Codex
storage. Start with Sol medium as lead, bounded read-only scout/reviewer/specialist
roles, one writer and at most two helpers when independent work justifies them.
This is an initial policy, not a measured speed guarantee. No background worker
or automatic change of the current conversation model is claimed.

After a newly supplied AGENTS repeated the old restrictions, Codex asked whether
to allow reviewed source pushes and bounded helpers or retain those restrictions.
The owner replied “allow - reviewed source branch proceed”. Apply the selected
routing policy and reviewed branch publication; retain explicit owner-test,
merge/release and private-data boundaries. Skill/helper selection is the lead's
job. A missing asset/access/verdict remains a real dependency, not a model problem.

## D-018: useful menu batches and exact-build release states — 2026-10-05

The owner supplied the ordered batch plan now recorded in docs/archive/WORKFLOW-2026-10-07.md:
finish the Intervention/input checkpoint, then basic loadout, weapons,
presentation/adjustments, complex movement, killstreaks/private players and
the agreed trickshot hit radius. Keep one batch active. Split only on a
demonstrated integration problem; unsupported entries remain completion
requirements while independent entries continue. Hide HUD stays deferred.

Record effects, reversals, failures and interactions against committed source,
upstream pins, patch and executable hashes. Versioned local reviews supply
Launch, Files, Checklist and newly working options; preserve predecessors.
Experimental source publication, checked local trial, exact-build owner-accepted
local release and public full-menu release are distinct. Public release needs
complete coverage, hit-radius checks, acceptance, reproducibility/permissions
review and explicit publication authority; assets remain excluded.

The owner reports on October 5: only Intervention worked in the most recent
trial; other options were missing. No exact build identity or full-menu
acceptance was provided. Retain this successful Intervention report separately
from automated diagnostics and the missing option coverage.

## D-019: hit radius first and resume reconciliation — 2026-10-05

The owner-supplied reconciliation plan puts hit-radius assistance first,
superseding D-018's batch order where it put hit radius last. Preserve D-013's
geometry, damage and cover contract and D-015's actual pinned Synergy execution.
The existing exact-build physical input trial remains prepared and unaccepted;
Codex can qualify the hit-radius integration independently of that verdict.
Rainy remains a research candidate: the preceding source investigation reported
IW4x/Bot Warfare dependencies and unsupported function replacement. It has not
been installed, launched or gameplay-tested; this session has not re-inspected
Rainy source and does not claim runtime compatibility.

Reconcile the board, current requirements, evidence and latest owner correction
before selecting one missing check. Persistent guidance describes responsibilities
and authorities; current work stays on the board and exact-build evidence in the
handoff. Keep separate mashup experiences and their evidence distinct.

Preserve inherited unfinished scripts/prepare_experience.py and
tests/test_experiences.py outside this correction. No commits or pushes are
authorized for this work. Amend the existing global router/policy using filesystem
approval; keep the static reminder hook unchanged. Defer new hooks, dashboards,
automatic task pickup and skill upgrades. Passing checks do not confer acceptance,
publication, merge or release.

## D-020: Fortnite with Skate only and an open-source experience hub — 2026-10-05

The owner requests starting Fortnite-with-Skate work, a polished README and clear
reproduction guide, and a substantial open-source project with a compelling
multi-game roadmap and a tested player hub. The owner explicitly selects
**Fortnite + Skate only**: no MW2 combat or Synergy in this experience. This
supersedes the earlier Fortnite composition in D-016/WORKFLOW.md; actual Synergy
and hit-radius work remain a separate experience, incomplete and unaccepted.

Start wayfinding/qualification now on the existing private board. Reuse the
previously selected Windows build and one Tilted building + ground scope until
source access/export evidence justifies a change. Reuse the existing Rust engine
where suitable, while explicitly isolating inherited combat/UI. No adapter or
playable Fortnite build exists. The unfinished scaffolding does not settle
architecture or prove progress. No universal merger, new engine, marketplace,
asset redistribution, outreach, spending, site publication, commits or pushes
are authorized by this planning request.

The roadmap should distinguish research candidates, prepared exact builds and
play-tested experiences. A hub means a player-facing catalogue with prerequisites,
reproduction/launch instructions, evidence, limitations and recovery for each
experience, rather than a claim all combinations work. Its implementation,
hosting and public status workflow require a later bounded spec; current work is
planning. Traction means measurable player success/repeat use and contributor
reproducibility, not a promised audience or download total. Source/community
publication remains separate from game-data rights and owner acceptance.


## D-021: GitHub catalogue and evidence before roadmap expansion — 2026-10-05

The owner selected the GitHub experience catalogue as the first player hub. An
experience may be called community-tested only with an identified exact build
and recorded participant results; no minimum participant count or statistical
claim is settled. Add additional game candidates to the public roadmap after
Fortnite + Skate reaches its first playable milestone. Fortnite + Skate remains
a separate Skate movement experience without MW2 combat or Synergy. These answers
resolve the hub-format/readiness portion of C-021; the pilot threshold remains open
in C-022. The private board is the detailed status authority.

## D-022: full Fortnite island and a source-backed adapter specification — 2026-10-06

The owner's supplied implementation plan makes the full selected Fortnite island
the destination, with Skate movement and no MW2 combat or Synergy. The earlier
one-building destination/expansion gate is superseded: smaller areas are test
cases within the island integration. Keep `Release-3.1-CL-3917250` and runtime
`f608f85e407ff1b7689d54a9aafdd16e95711ac4`; a Fortnite version change needs an explicit
decision. Spatial streaming is a qualification question, not excluded from the
destination and not yet justified by measurements.

This bounded deliverable is the source-backed adapter specification, ordered
implementation work, and precise input/startup blockers. It permits independent
runtime research when input access is missing, not invented export formats or
playable claims. Parser/exporter components can be reused without a finished
third-party mashup. Preserve actual Synergy, its physical trial and hit-radius
requirements separately. See the [qualification report](../research/results/2026-10-06-fortnite-adapter-qualification.md).

The supplied plan excluded commits/pushes; the owner's later concern about dirty
work and request for a clear branch/merge workflow supersede that for local
reviewable checkpoints. Record actual Git results in the handoff; no push/merge
result or broad auto-merge authority is inferred. Board maintenance remains
authorized; publication, owner acceptance and release remain separate.


## D-023: concise live resume and input-first reconciliation — 2026-10-06

The owner's implementation plan retains the existing full-island specification
and eight dependency-linked slices; planning/slicing are complete, integration is
not. Keep C-021 and C-023 Done, and preserve the pending Synergy physical trial.
Check Fortnite island input (C-024) first, then render standalone skating (C-025)
after its asset prerequisite check when input is externally blocked. Broader
ambitions remain milestones; later dependent work stays Later.

Fresh board evidence records permission to choose a suitable accessible Fortnite
build. This supersedes D-022's requirement for another version-choice approval;
record the actual selected build and identity before changing requirements. Local
metadata still identifies Release-3.1-CL-3917250; no replacement has been selected.
No bypass or redistribution authority follows from version-choice permission.

The existing global Projects helper gains a read-only live summary, not another
saved status list. Preserve untracked exporter work and local main. Remote main
and qualification source publication are verified; PR #1 remains open with local
checks and no attached automated checks. Full diff review precedes any merge
proposal. No CI, protection, automatic merge or deployment in this slice. Check
resume usefulness at the next two returns and retire the helper if it adds friction.


## D-024: qualify existing tools before custom Fortnite conversion — 2026-10-06

The owner's supplied plan makes reuse assessment the next bounded outcome.
Compare existing Fortnite exporters, Blender importers and Skate map pipelines
with completing Combine's adapter; source claims do not establish local
compatibility. Require an identified private export with terrain and a building,
placements, materials and collision evidence before choosing serialization or
writing a custom decoder. Qualification ends with an evidenced route or precise
blocker; further research needs a named question that changes that choice.

The full selected island remains the destination. First prove movement, jump,
solid collision, a representative grind, recovery, exit and relaunch in one real
area. Measure content/resource costs before choosing full residency or streaming.
Keep the pinned runtime and existing skater. Another runtime requires comparison
and an explicit owner decision. No Fortnite/MW combat, Synergy, character
retargeting, new engine, asset redistribution or protection bypass.

Update existing C-019 specification, C-020 map and dependent tickets; park
route-dependent custom work pending qualification. Preserve inherited commits,
patches and exporter scaffolding. The reproduced PR #1 rail validation defect
remains a repair obligation before merge. Separate Synergy requirements/trial
are preserved and parked outside this active milestone. Global custom-router
retirement remains separate. See the [qualification](../research/results/2026-10-06-fortnite-adapter-qualification.md).


## D-025: separate playable-map needs from exporter-comparison needs — 2026-10-06

The owner confirms no additional local Fortnite build/export is available and
asks us to find online input, then challenges whether a matching build and
Blender are needed for the goal. Neither is a runtime requirement. Preserve the
pinned Skate host and full-island destination; assess a public world package by
actual content, dimensions, placements, materials and usable collision. A
particular Fortnite build is not required merely to inspect a model.

The proposed paired-export experiment requires the same source world/build for
a fair comparison; a pre-exported mesh cannot prove either upstream exporter's
fidelity. Blender is a conversion/authoring tool for the proposed SK8 pipeline,
not part of gameplay. Another converter is possible but unqualified. Newly
authored collision must be labelled and tested, never called preserved source
collision. No route or replacement is selected by this clarification.

Public Chapter 1/Tilted/Chapter 6 listings are concrete leads; their metadata is
available, but anonymous official download checks return 401 and content has
not been inspected. No account action, asset acquisition or spending occurred.
Keep the paired comparison conditional on accessible raw input and the
downstream package assessment distinct. Evidence and exact source conditions:
[qualification follow-up](../research/results/2026-10-06-fortnite-adapter-qualification.md#paired-route-follow-up--2026-10-06).

The owner's subsequent question also reopens whether Combine is necessary.
Upstream SK8 documents a complete custom-map load/render/collision/grind/session
path; it is a candidate to assess rather than implementing that bridge anew.
This is a recommendation from source/documentation, not a runtime switch or
Fortnite gameplay result. Owner host selection remains pending; preserve Combine
and its separate Synergy work. See the qualification's runtime-necessity section.

The owner then requests GitHub examples and asks whether different runtimes
should serve different experiences. Investigate existing standalone map hosts
before new Combine session work; preserve the full island + Skate-only outcome.
The standalone Rust Engine and SK8 Custom Engine Layer are documented candidates.
ReSkate's author-documented GTA III map port is an existing cross-game example
for the newer skate. game, not a verified Skate 3 substitution. Final host
selection remains open; no universal-runtime architecture is selected.


## D-026: interactive Fortnite world with Skate simulation — 2026-10-06

The owner's implementation plan corrects the export-first approach: retain
Fortnite building, editing and destruction while Skate supplies movement,
tricks and grinds. Static scenery is insufficient. Combine, Blender and a
particular Fortnite version are not mandatory. The complete selected island
remains the destination; the first demonstration builds/edits on foot then
switches to skating. Simultaneous building while skating is deferred.

Investigate Project Reboot 3.0 first, pin inspected source, establish accessible
compatible client and a reviewed isolated launch route without protection
bypass, then qualify live collision/lifecycle, controls/pose and rendering seams.
Server functionality alone is insufficient. Reuse existing Skate Session seams
where compatible; no generic bridge API/schema is selected. The bounded slice
may finish with a precise evidence-backed prerequisite blocker. No static
substitution, gameplay recreation, multiplayer, spending, redistribution,
publication, merge or release is authorized. Preserve original/private data and
separate Synergy requirements. Existing C-019/C-020/C-024 and dependency records
are revised in place; conflicting static requirements become historical.

The [current specification](../research/results/2026-10-06-fortnite-adapter-qualification.md)
owns requirements and acceptance. D-026 supersedes conflicting static-world
scope in D-020 through D-025, not their recorded observations or unresolved debt.


## D-027: same-process adapter reuse and source-publication policy — 2026-10-06

The owner asks to establish the existing integration architecture, try methods
per game, and use same-process reuse unless required otherwise. Pinned source
shows IW4L hosts MW2, Skate and Minecraft in one Bevy app; Skate uses internal
thread channels, not cross-process IPC. The separate public Minecraft crossover
uses two programs and shared memory. Neither supplies a qualified Fortnite host
adapter. Prefer the existing Skate Session inside the selected host process.
Only introduce IPC after a demonstrated host constraint justifies the change;
keep one measured live-host experiment active and retain explicit blockers.
The current specification and linked process-model evidence own the details.

The owner also directs reviewed source branch publication and saving a global
default that avoids accumulating local commits. At each completed authorized
slice, review, run required checks, commit, push the branch, verify remote SHA
and synchronize the tracker. Pending gameplay acceptance alone does not hold
experimental source locally. This supersedes D-026's slice-specific no-publication
restriction. Private data/assets remain excluded; acceptance, merge and release
remain separate. Global Codex instructions now favor the smallest useful workflow
and an explicitly requested skill rather than chaining unrelated workflows.


## D-028: selected modding guidance informs qualification, not runtime authority — 2026-10-06

The owner's supplied plan uses research to qualify an interactive Fortnite route,
Reboot first, retaining the existing Skate Session and same-process preference.
Any qualified interactive island is acceptable. Universal Modder reconnaissance,
Unreal and mashup guidance is pinned and read as reference material; installing
its tools or following its generic injection instructions is not part of this
slice. Review tools before installation/execution. Its Unreal reference itself
excludes Fortnite's EAC/BattlEye route. The guidance does not override project
boundaries or establish a permitted host extension.

The [qualification report](../research/results/2026-10-06-fortnite-guidance-qualification.md)
records fresh source evidence: Reboot's inspected launcher suspends EAC; Era's
inspected launcher requests protection-disabling options and an unreviewed DLL;
Rift's inspected catalogue establishes packaging, not a qualified native host.
No candidate selected for execution. Unknown exact compatible clients/dependencies
stay explicit. Offline status or removed protection is insufficient qualification.

First live experiment remains a real player/camera value correlated with movement,
after a permitted client/extension route is established. Preserve build ramp →
skate/jump/grind → edit/collision → destroy/removal → recover/relaunch acceptance.
No runtime API or universal framework is introduced. Extract scripts only for
proven repetition; create a reusable skill after success on a second case, in
global storage. D-027 publication policy remains; no merge/release or gameplay
acceptance follows from source research or passing repository checks.

## D-029: actual Skate connection before observation-only diagnostics — 2026-10-06

During grill-with-docs the owner selected option A: assess whether a Fortnite route
can actually connect to the existing Skate simulation before spending effort on
an observation-only diagnostic. Reading player/camera coordinates alone is not
sufficient progress toward this selected outcome. Preserve actual Skate physics,
the interactive island and same-process preference; no substitute simulation or
static-world route is selected.

The [connection assessment](../research/results/2026-10-06-fortnite-guidance-qualification.md#actual-skate-connection-assessment--owner-choice-a-2026-10-06)
compares official UEFN native/transport/editor APIs and input/collision/animation
capabilities with the pinned Session. Documented observation and editor automation
do not establish a creator-provided native runtime call path. No supported native
or local-transport connection was established in the inspected sources. This is
a documentation result, not a universal impossibility claim or an observed
constraint selecting IPC. Existing Reboot/Era protection/dependency blockers remain.

Continue only on concrete primary-source evidence for the missing runtime seam;
do not create a coordinate-only demo, speculative bridge, hosted backend or
rewritten skating system to conceal the gap. Existing acceptance sequence and
publication/asset/merge/release boundaries remain unchanged.


## D-030 Original Matt skills restored — 2026-10-06

The owner requested Matt’s original skills and Ask Matt flow map globally,
removing the custom workflow layer. Restore the existing 21 skills unchanged
from upstream v1.3.1 (`24fe0ef7737efae15c87225755e9f6f5965e4888`), including
supporting files and invocation settings. Retire the custom `matt-workflow`
router, adaptation rules, shared routing policy and automatic reminder.
This supersedes earlier requirements to use that custom layer.

The original archive checksum and all 62 restored files were verified. A complete
pre-restoration backup is retained outside active skill discovery. Standalone
board/review utilities, project records and unrelated personal preferences remain.
Combine’s tracker, gameplay requirements and acceptance/publication boundaries
are unchanged. Fresh-session skill discovery remains a separate check.

## D-031: isolated Fortnite 12.41 acquisition before startup review — 2026-10-06

The owner selected the supplied plan to download Windows 12.41 **CL12905909**
from the reachable 42.5 GB archive into ignored private Linux storage. Download
authorization is explicit. Preserve the working mashup and existing Fortnite
copies; check extraction size, safe paths, ZIP integrity, exact-build manifest
file hashes and executable version/signature in a fresh isolated directory.
Stop on corruption or identity mismatch and retain diagnostics privately.

This slice ends at downloaded/integrity-checked files. It authorizes no game
launch, account login, protection changes, public asset upload or runtime API
changes, and establishes neither playability nor ban safety. After successful
verification, review the matching local-server startup path before preparing
a gameplay trial. The [acquisition evidence](../research/results/2026-10-06-fortnite-12-41-preparation.md)
records exact provenance, checks and limitations. Existing qualification,
source-publication, owner-acceptance, merge and release boundaries remain separate.


## D-032: one Fortnite outcome and a lightweight workflow — 2026-10-07

The owner selected a reset to reduce administration: retain the private Project,
keep only the Fortnite destination C-019 and qualification task C-024 visible,
and archive other work as inactive without changing acceptance claims. Replace
phase views with Ready → Doing → Blocked → Done, with at most one Doing task.
A separate Work status field preserves every historical Status/Phase/skill value;
old views and full item bodies are snapshotted privately before replacement.

The next task diagnoses the selected executable's integrity failure and original-client
availability, ending with matching verified input or a precise unresolved blocker.
The reset itself includes no new download or launch. Synergy, its unaccepted trial,
hit radius and static-world work remain parked with requirements/evidence intact.

Use one short development loop, task-relevant context and one current handoff with
linked historical archive. Stop using the seven-phase helper for Combine; retain
Matt's original skills and global configuration unchanged. This supersedes earlier
phase machinery, mandatory backlog/history reading and conflicting publication wording.
Reviewed reset source publication is authorized; routine SHA/board confirmation stays
on the card or PR. Preserve branches/history and review inherited changes separately
before any merge. No CI deployment, squash, merge, release or gameplay acceptance.


## D-033: finish routine source changes through main — 2026-10-07

The owner selected routine agent merges after review and checks, then instructed
Codex to proceed with the workflow correction and existing-branch reconciliation.
Keep one branch per ticket/coherent outcome, created from updated main; continue
the same task on its existing branch. The complete procedure and completion
criteria live in [workflow](archive/WORKFLOW-2026-10-07.md#branch-to-main).

This supersedes earlier separate-approval requirements for ordinary source PR
merges, including D-032's reset restriction, subject to the workflow's review,
verification and synchronization conditions. This is the owner's Combine policy,
not a claim about Matt Pocock's personal merge practice. The owner subsequently
clarified that Matt's skills should guide feature work without a second prescribed
Combine workflow. Keep WORKFLOW.md limited to source completion and project
boundaries; no mandatory skill sequence, custom router or phase system. Gameplay acceptance,
launch, spending, redistribution, deployment and release keep their boundaries.

The pre-existing backlog remains separately controlled: reconcile unique local
history, review accumulated changes and present a concrete proposal for owner
merge authorization. Preserve published history and unique local work. Continue
the workflow-reset branch for this correction; do not add another dependent branch.


## D-034: Matt's original skills only — 2026-10-07

The owner selected Matt's original skills as the only engineering process and
approved removing the competing global and Combine workflow layers. Global
instructions retain communication preferences and evidence honesty. Project
instructions retain requirements, test commands, tracker operations and runtime/privacy
boundaries; archived process documents are historical evidence, not instructions.
This supersedes the custom phase, agent-role, mandatory handoff and source-closure
procedures in earlier decisions, including D-032/D-033. It does not expand existing
authority: routine source merge permission remains subject to review/checks and
repository protections; inherited PRs #1/#2 require separate owner merge approval.

The private Project remains the ticket store. Install original triage with default
roles represented as Project metadata; use it only for incoming requests. Glossary
and ADR documentation uses Matt's lazy single-context convention. Preserve existing
requirements and evidence. Reconcile accumulated branches without rewriting
published history or discarding unique work. No new launcher, gameplay trial,
download, deployment or release is authorized by this change.
