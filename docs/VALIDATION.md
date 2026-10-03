# Player and creator study — C-005 / C-007

Test whether Combine would solve a recurring problem, not just attract curiosity.
Target ordinary Windows players interested in game mashups and creators already
maintaining mods or runtimes. This protocol is prepared; no recruitment, interviews,
consent, observations or payment commitments have occurred.

## Recruitment and consent

The owner recruits ten players and three creators. Seek players with varied modding
experience, including people who previously abandoned setup. Record how many were
invited, eligible, prerequisite-ready and completed; never hide prerequisite drop-off.
Do not purchase files or bypass access requirements for participants.

Suggested owner-sent invitation:

> I'm researching whether a simpler way to configure and share game mashups would
> help players. Would you discuss your last attempt and, if eligible, try a short
> setup task? This is research, not a released product or a sales commitment.

Explain what will be recorded, ask permission for notes, and separately ask before
recording a screen. Participation is voluntary; avoid minors for this small study.
Use pseudonyms P01–P10 and C01–C03. Keep contact details and raw recordings outside
Git and separate from answers. Share aggregate/redacted findings only; delete raw
identifiable material within 30 days after synthesis unless separately agreed.

## Player interview (before showing the concept)

1. Tell me about the last game/mod/mashup you tried to set up. What actually happened?
2. Which step took the most time? What did you try when it failed?
3. What did you play again a week later, and why?
4. Which combination would you use? Which parts must behave like the original game?
5. Which tools do you already use, and have you paid for setup or creator services?

Then show the proposed supported-catalogue flow. Ask what they believe it does,
what they expect to supply, and what would make them distrust it. Correct any belief
that it can combine arbitrary games or supply paid game content.

## Observed task

Prerequisite: C-003 establishes usable baseline behaviour and applicable rights
questions for involving testers are addressed. Do not promise a guided launcher:
only upstream software, a runbook and research recipes currently exist.

- Ask the participant to reach the target combination using upstream instructions.
  Record questions, mistakes, interventions and time; do not rescue them silently.
- Ask them to save/exchange a recipe and reproduce its world/modes without code edits.
  Record whether manual application is understandable and whether sharing is useful.
- Compare with a paper/click-through guided-flow proposal after the task. This
  comparison measures comprehension, not proven software onboarding improvement.
- Once a working guided improvement exists, test it with fresh participants or
  counterbalance task order; repeat testers benefit from learning. Label the cohort
  and flow version before claiming the 8/10 threshold applies to Combine.
- Invite a second session within seven days without promising rewards for returning.
  Record voluntary return separately from a prompted research appointment.

## Creator interview

1. Demonstrate your last integration or release workflow. Where did maintenance hurt?
2. What can users safely configure today, and what needs engineering?
3. Would you publish or maintain a compatible recipe/integration here? Under what terms?
4. What provenance, support, versioning and revenue conditions would you require?
5. What ongoing effort would each release require? What would make you leave?

Record interest, concrete next commitment, constraints and estimated effort separately.
Three conversations are discovery evidence, not a guaranteed content pipeline.

## Money and traction experiments

Ask which specific convenience/creator service is valuable and what existing spend it
would replace. If a price concept is tested, record the exact price, service and
answer; do not treat hypothetical willingness as paid demand. No payments or paid
game access are implemented. Any future monetisation must pass C-006.

Hypothesis for a later public test: owner-approved gameplay clip → one clear recipe
page → prerequisite check → actual play → recipe share → return. A dedicated hub is
the proposed destination; it is not yet built or published. Use only permitted media.
Measure every step and acquisition source. Views and sign-ups alone are insufficient.

## Recording and decision

Copy [the CSV template](../templates/participant-results.csv) into ignored `.private/`.
Use blank numeric cells for missing data, never zero. Record seven-day follow-up due
date and whether a return was observed; unanswered follow-up is not evidence of return.
Contact details do not belong in the CSV. Keep creator findings as redacted notes.

Report all ten enrolled players, prerequisite attrition, unaided completions, median
time among completers, failure reasons, support minutes, return count and cohort/flow
version. Time to gameplay after readiness and total prerequisite/setup time must both
be reported. Early dropouts and assisted completions do not count as unaided success.

Use the [decision record](DECISIONS.md): 8/10 unaided within 15 minutes once ready,
5/10 observed returns within seven days, technical reproducibility and resolved
distribution questions. These are tentative go/no-go criteria for a tiny study,
not statistical validation. Record a negative or inconclusive result without changing
the threshold after seeing the data.
