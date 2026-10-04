# Combine domain documentation

Read `README.md` and `BACKLOG.md` first, then documents relevant to the task:

- `docs/TRICKSHOT_MENU.md`: menu requirements, pinned feature inventory, build,
  trial and acceptance procedures. The destination is Synergy plus trickshot hit
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

Read the skill's shared Codex adaptation before following upstream defaults.
Respect one-lead coordination and existing acceptance/publication boundaries.
Use small plain-text diagrams where helpful and define unfamiliar terms plainly.
