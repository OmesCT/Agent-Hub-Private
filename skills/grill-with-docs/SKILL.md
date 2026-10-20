# grill-with-docs

Interviews you about a plan, writes resolved terms to `GLOSSARY.md` and gated decisions to `docs/adr/` during the session. Requires `grilling` + `domain-modeling` skills installed.

Key points:
- Single-session tool for fuzzy plans in a repo
- Terms land in glossary immediately; ADRs need 3 gates (hard to reverse, surprising, real trade-off)
- Most decisions stay in conversation only — feed to `to-spec` after
- Fails silently inside orchestration layers (known bug)
- Loads `grilling` + `domain-modeling` via one-line `SKILL.md` delegation

Chain: `grill-with-docs → to-spec → to-tickets → implement`

> "The glossary is the point. Domain language is the thing this skill is actually building."

Use `/wayfinder` for multi-session efforts.
