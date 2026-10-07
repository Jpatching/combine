# Domain docs

Use a single context: `GLOSSARY.md` at the repository root and architecture
decision records (ADRs) under `docs/adr/`.

Before exploring, read the glossary if it exists and any ADRs relevant to the
area being changed. If they are absent, proceed silently. `domain-modeling`
creates them only when terms or decisions are resolved; setup creates no empty
glossary or ADR directory.

Use the glossary's terms in issue titles, proposals, hypotheses and tests.
If a needed concept is missing, reconsider the wording or note the gap for
`domain-modeling`. Surface conflicts with an existing ADR explicitly instead
of silently overriding it.

The historical [decision log](../DECISIONS.md) remains available for technical
evidence and product constraints; its retired workflow does not select new work.
