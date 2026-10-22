---
name: code-review
description: Review git diff against a fixed point (commit/branch/tag/main) across Standards (repo conventions & Fowler code smells) and Spec compliance (requirements & issue tracking).
---

# Code Review Skill

Reviews the diff between `HEAD` and a fixed point you name (`<fixed-point>...HEAD`, e.g. `main`, `HEAD~1`, `origin/main`, tag, or commit hash) along two separate axes: **Standards** and **Spec**.

## Core Rules & Guardrails
- **Ref Validation First**: Check that the fixed point resolves (`git rev-parse --verify <fixed-point>`) and that the diff is non-empty (`git diff <fixed-point>...HEAD`) before running analysis.
- **No Recursive Spawning**: Do not recursively invoke `/code-review` or spawn additional agents. Perform this review directly.
- **Two Independent Axes**: Keep Standards and Spec findings strictly separate. Never blend or merge them into a single score or single winner.
- **Strict Evidence Requirement**: Every Standards finding must cite a documented repo rule or named Fowler smell plus code hunk. Every Spec finding must cite the spec line/requirement.

---

## The Two Axes

### Axis 1: Standards (Is it built right?)
- **Primary Source**: Repository conventions and documented standards (`GEMINI.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `README.md`). Repo rules always override generic heuristics.
- **Smell Baseline (Fowler Refactoring Ch.3 Floor)**:
  1. *Mysterious Name*: Unclear function, variable, or module names.
  2. *Duplicated Code*: Identical or near-identical code blocks across components.
  3. *Feature Envy*: A function accessing data/methods of another object more than its own.
  4. *Data Clumps*: Bunches of data hanging around together that belong in a dedicated type.
  5. *Primitive Obsession*: Overusing primitives instead of domain-specific objects.
  6. *Repeated Switches*: Duplicated conditional logic switching on the same type flag.
  7. *Shotgun Surgery*: A single conceptual change requiring small edits across many files.
  8. *Divergent Change*: A single module modified for multiple unrelated reasons.
  9. *Speculative Generality*: Over-engineered abstractions not needed by actual requirements.
  10. *Message Chains*: Long chains of navigation calls (`a.getB().getC().getD()`).
  11. *Middle Man*: Classes delegating all their work with no added value.
  12. *Refused Bequest*: Subclasses ignoring/overriding inherited methods inappropriately.
- Format each smell as: **What it is** ➔ **How to fix**.

### Axis 2: Spec (Is it the right thing?)
- Locates the spec in:
  1. Issue/Ticket references in commit messages (`#123`, `WO#...`).
  2. A path passed by the user.
  3. Spec files under `wiki/specs/`, `docs/`, `specs/`.
  4. Prompt requirements from the conversation.
- If no spec exists or is findable, report **"No spec available"** instead of inventing requirements.
- Flags: Missing requirements, partially implemented specs, scope creep, wrong behavior.

---

## Output Report Structure

```markdown
# Code Review Report (<fixed-point>...HEAD)

## Standards
- **[Rule/Smell Name]** `file:line`:
  - **Issue**: <Exact problem description>
  - **Evidence**:
    ```language
    <code hunk>
    ```
  - **Remedy**: <Actionable fix or refactoring move>

## Spec
- **[Requirement / Spec Line]**:
  - **Status**: Satisfied | Missing | Partial | Scope Creep
  - **Detail**: <Explanation with citation to spec and code>

## Worst Issues
- **Worst Standards Issue**: <Highest priority standards/smell violation, or None>
- **Worst Spec Issue**: <Highest priority spec discrepancy, or None>
```
