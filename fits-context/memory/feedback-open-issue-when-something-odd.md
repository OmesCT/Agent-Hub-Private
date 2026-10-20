---
name: feedback-open-issue-when-something-odd
description: "When anything odd/inconsistent is found in the repo, open a GitLab issue (with the release version) instead of just mentioning it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b51447ab-922e-401e-ac78-e04468240da4
  modified: 2026-10-06T13:21:46.390Z
---

User (2026-10-03): "ถ้าเราเจออะไรแปลกๆ ก็ควรจะเปิด issue ขึ้นไปก่อน" — when we notice something odd (spec conflict, stale docs, dead code, wrong numbers), open a GitLab issue first rather than only reporting it in chat. Include the version found (e.g. 0.17.0 + origin/main short SHA) in the body; write in English with Problem / Goal / Scope / Not in scope / AC; check `glab issue list --search` for duplicates first.

**Why:** keeps an issue trail and lets the team (who are debugging FE/BE in parallel) see and own the finding.

**How to apply:** open the issue for real findings; do NOT implement it unless asked. Exception: ticket statuses in `tickets.toml` — user said the team closes those themselves, don't touch. Examples: #137 (Reject in queue, K6), #138 (README/AGENTS drift). Related: [[feedback-dev-ohm-issue-first-no-mr]], [[project-frontend-bug-sweep-136]], [[feedback-always-rebase-on-latest-main]].

Process the user asked for (2026-10-03, mid re-verification of #136): "ถ้าเจอบัคอะไรก็ให้เปิด issue ทิ้งไว้ ถ้าตรวจเสร็จให้ทำการรวม issue เป็นอันเดียว" — open one issue per NEW bug the moment it is found (do not stop the check, do not ask), and when the check is finished merge all of those issues into ONE issue: create the consolidated issue with every finding's full text, then close each per-bug issue with the quick action `/duplicate #<consolidated>` (GitLab has no real merge). Bugs already listed in #136 are not re-filed. The target of the merge is a new consolidated issue, NOT an edit of #136 (user declined extra #136 edits on 2026-10-03; offer folding into #136 instead of doing it). Used on 2026-10-03: #147 (exception-handler texts) was folded into #146 (rewritten as the consolidated 'user-facing messages' issue, label area:backend added) and closed with `/duplicate #146`; folding into the oldest per-bug issue avoids an extra issue number. Guard with a read-compare before any PUT (an issue could have been edited meanwhile).

Caveat (2026-10-03): `glab issue create --label X` silently creates label X when it does not exist (#138 created `documentation`, id 909). Run `glab label list --per-page 100` first and prefer an existing label; tell the user if a new one was created.

2026-10-06 (docs conflicts): the user ruled "เรายึดตาม prd — ถ้าเจออันไหนไม่ตาม prd.md ก็เปิด issue ไป" (the PRD is the arbiter; a doc that does not follow it gets an issue) and "ตอนเปิด issue เช็คด้วยนะว่ามี issue ไหนเหมือนกันหรือป่าว". Duplicate check = download ALL issues (open and closed) once with `glab api --paginate "projects/cto%2Fit-budget%2Ffits/issues?state=all&per_page=100"`, search them locally by the distinctive terms of each finding, read the candidates, then leave out what an existing issue already covers (#138 covered README/AGENTS drift) and link it instead (`--linked-issues`, a "Related:" line). Do not edit someone else's issue. Split a big result by what the reader must do (documents that deviate / owner decisions where the PRD cannot simply win / dead references), not into one 100-item issue; item ids shared across the issues. See [[project-docs-conflict-check-2026-10-06]].
