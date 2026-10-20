---
name: project-work-split-2026-10-07
description: "2026-10-07 split of the open GitLab issues between the user (A) and one friend (B) by file ownership so nothing conflicts; who does what, corrections found, where the data is"
metadata:
  node_type: memory
  type: project
  originSessionId: 653b489e-e167-408b-adaa-cb678d8f75cd
  modified: 2026-10-07T03:34:01.445Z
---

On 2026-10-07 the user asked how to split every open issue between them and one other friend without merge conflicts, then for a short "ฉันทำ issue ไหน เพื่อนทำ issue ไหน" to send. The friend's identity and GitLab name are unknown (T650669 is a guess, unconfirmed). Nothing was assigned in GitLab and nothing was sent.

**Split** (A = the user, B = the friend; swappable). Computed on main e2d1f5c (0.20.0), refreshed on 3a18727 (0.20.1): all five open MRs (!174 !159 !172 !171 !163) had merged and #157/#159 had closed, 18 open issues left.
- A whole issues: #74, #129, #137, #138, #162 (the user runs the owner decisions and edits prd-fits.md). B whole issues: #128, #132, #154, #164.
- By item: #130 (A 1,6,7 / B 2,3,4,5,8); #146 (A 2,3 / B 1); #153 (A 1,2,4 / B 3); #158 (A M3-M6, L1-L3, L9, L10, L12, L14, L18, L19 / B M1, M2, M7-M11, L4-L8, L11, L13, L15-L17); #160 (A N2, N5, N8, N9 / B N1, N3, N4, N6, N7); #136 (A 78 items incl. K31 / B 91, of which K2 was fixed by #157).
- Docs #161/#163/#165 by file: A 33 files (AGENTS, README, PRODUCT, process docs, design-D, UX, prd-fits.md), B 60 files (summaries, WORKFLOW/CLASS diagrams, AAA guide, specs, epics/stories). 69 items touch only A files, 56 only B, 35 need both (each edits own files).
- Why it does not conflict: one owner per file (80 code files, 40 each); hubs FitsShell.tsx, client.ts, fitsCanvas.css only via tiny serialized MRs; VERSION, package.json, tags, release.sh, AGENTS.md, README.md only the user; new e2e specs as new files; never touch tickets.toml.
- Waiting for the business owner: #130-1/#137, #160 N3/N5/N8, #158 L4/L16, #128, #129, #162.

**Corrections made on the way:** the first docs split said 80/79 (majority family); by file it is 69/56/35. #130 item 7 (missing tests) moved from B to A. The in-flight MRs merged cleanly with each other (`git merge-tree`), so "the second author must rebase !171/!172" was wrong. !159's branch was 76 commits behind main yet mergeable.

**Where:** `.omc/research/work-split-2026-10-07/`: plan md (written at e2d1f5c with the pre-merge MR order, so stale: regenerate with `build_friend_plan.py` before anyone sends it), `work-split-items.csv` (229 code items), `work-split-docs.csv` (160 doc items), `graph.json`, `ownership2.json`, scripts, and `work-split-plan.html` (rendered, never published: the user wanted the short list only).

**Why:** the user wants two people fixing issues in parallel with no merge conflicts; file ownership was the only workable cut because #136, #158 and #160 touch the same few frontend files.

**How to apply:** if asked again, `git fetch`, `glab issue list`, `glab mr list`, re-derive from the CSV, and answer with the short list. See [[feedback-keep-answers-simple]], [[project-docs-conflict-check-2026-10-06]], [[project-frontend-bug-sweep-136]].
