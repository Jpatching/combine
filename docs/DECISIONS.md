# Decisions and milestone outcome

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

## Continue / change / stop — pending

Current recommendation: **continue the bounded private feasibility study only**.
No launch or investment recommendation is justified yet.

| Evidence | Threshold / interpretation | Current result |
| --- | --- | --- |
| Technical reproduction | Both candidates reproducible and exchangeable without editing code | Not run |
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
