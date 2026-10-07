# Combine domain documentation

Start with the current board and `docs/HANDOFF.md`; load only relevant domain documents:

- `research/results/2026-10-06-fortnite-adapter-qualification.md`: active Fortnite + Skate gameplay contract.
- `docs/TRICKSHOT_MENU.md`: menu requirements, pinned feature inventory, build,
  trial and acceptance procedures. The parked menu destination is Synergy plus trickshot hit
  radius; Hide HUD is deferred and is not a prerequisite.
- `docs/DECISIONS.md`: consequential decisions, including the superseding scope/tracker decision D-012.
- `docs/WINDOWS_BASELINE.md`: gameplay/recovery procedure.
- `research/upstream.lock.json`: runtime and menu-source pins.
- `docs/HANDOFF.md` and linked `research/results/`: evidence and reproduction.

This uses existing project documents rather than adding a glossary or ADR store.
Follow their terms. “Prepared”, “launched”, “gameplay-tested”, “verified” and
“owner-accepted” are distinct. Synthetic fixtures and successful builds do not
establish play. Source licences do not establish asset or publisher clearance.

Our repository stores patches against pinned upstream. Distinguish changes to
those patches from private build checkouts, generated binaries and runtime trials.
Record source hash, patch order and commands for review. Private assets, recordings,
settings and raw logs remain outside Git and are never uploaded to AI services.

Use original skills when relevant; the custom shared adaptation was retired.
Respect one-lead coordination and existing acceptance/publication boundaries.
Use small plain-text diagrams where helpful and define unfamiliar terms plainly.
