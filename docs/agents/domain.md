# Combine domain docs

Single-context: read root `GLOSSARY.md` and relevant `docs/adr/` entries when present.
If absent, proceed silently; domain-modeling creates them lazily as terms and
architectural decisions are resolved. Use glossary vocabulary in issues and code.

Existing decisions remain in `docs/DECISIONS.md`. Consult relevant entries, surface
conflicts explicitly, and link existing decisions instead of copying them into ADRs.
Project requirements are linked from AGENTS.md.

Distinguish repository patches against pinned upstream from private build checkouts,
generated binaries and runtime trials. Preparation, launch and owner acceptance
are separate claims.
