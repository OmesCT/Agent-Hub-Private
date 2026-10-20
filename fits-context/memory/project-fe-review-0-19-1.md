---
name: project-fe-review-0-19-1
description: "2026-10-06 frontend review of 0.19.1 (ff7351c): GitLab issue #158 with 11 medium + 19 low new defects, how it was run, what is still open or needs a user decision"
metadata:
  node_type: memory
  type: project
  originSessionId: 592a22e1-cbf5-4a27-b76e-1ad4579fb92d
  modified: 2026-10-06T06:22:06.616Z
---

On 2026-10-06 the user asked for an Opus review of the frontend ("bugs and what must be fixed in this version") with a live click-through. They first wanted the DEV site clicked (login impossible, see below), then said "ลองรันบน local ก่อนก็ได้", so the click-through ran on the local compose stack.

**Result:** one consolidated GitLab issue, https://gitlab.tcbank.local/cto/it-budget/fits/-/issues/158 (labels area:frontend, area:backend, type:bug), 30 findings (11 medium, 19 low) that are NOT in #136/#137/#146/#148/#149/#153/#154/#157. I filed it as ONE issue straight away (the standing "one issue per bug, then merge" process of [[feedback-open-issue-when-something-odd]] collapsed to its end state); nothing was fixed, no MR.

**Medium headlines** (full text in the issue): M1 `/auth/login` return-URL check lets `/<TAB>/evil.example.com` through (AuthReturnUrl.cs, backend security); M2 Budget Reallocation commit also cuts items approved after the screen loaded; M3 overlap banner vanishes silently when `/api/governance/overlaps` fails (live-proven by fetch injection); M4 import price with more than 2 decimals passes the dry run and fails the commit with a raw .NET message; M5 Admin Reopen / Override leave monthly allocations stale; M6 float sums make Available print a red "THB -0.00"; M7 the four min-floor settings are inert; M8 break-glass justification not in the audit row; M9 no `BudgetItem.CutApplied` event (PRD FR-2.3); M10 session expiry drops unsaved input (SSO); M11 failed AAA sign-in ends on a raw JSON page (seen on DEV, 502).

**Still open from before:** K31 (import success shown as failure: server `BGIDs` serialises as `bgiDs`, SPA reads `bgids`) is still present on 0.19.1 and is the one critical item of [[project-frontend-bug-sweep-136]]; #136's text was deliberately left unedited ("ยังไม่แก้"). The Create-form-vs-catalog validator mismatch (a parked backend finding) was re-found and stays parked: do not file it unasked.

**Baseline on 0.19.1:** `tsc --noEmit` clean, vitest 53 files / 536 tests green, no console errors on ADMIN/REQUESTER/DEPTHEAD/CIO views, money figures reconcile by hand (dashboard 41.20M approved, PO 13.70M, paid 3.70M, executive total requested 178,754,192.78, audit chain 49/49). The 26INFRA006/009 rows (Pending Admin with an Approved amount) are stale data from old builds, not a code bug: today's reopen clears the amount (`WorkflowService.cs:659`).

**Decisions waiting for the user / PO:** L4 dashboard "alerts" are rankings with no threshold (the mockup does the same, but counts only risk chips and says "Risks"); L7 Audit Ledger summary cards and integrity modal (EXPERIENCE 5.8) are missing; L16 CIO/CEO/CTO/EXEC are blocked by the UI from the Audit Ledger although the API allows them; PRD FR-2.5 ("one line per request") vs DESIGN.md ("up to eight successes").

**How it was run:** four read-only `oh-my-claudecode:code-reviewer` agents, one per area, as Sonnet 5.5 (Opus 404, see [[reference-run-fits-locally]]); every medium finding was re-read on both ends by me before filing, several confirmed live. **DEV site:** the login page loads, the SSO button answers a bare 502 JSON page (M11), `Break-glass` was NOT clicked: the auto-mode classifier denied it ("Security Weaken") and I did not retry or route around it; the user dropped DEV after that ([[feedback-dont-test-live-dev-site]]).

**Side effects left behind:** local `fits-web` rebuilt from ff7351c (0.19.1) and running at http://127.0.0.1:8080 (Browser pane tab signed in as chris, language TH); `dev-ohm` in the main checkout was fast-forwarded to 0.19.1 the same day (0 own commits, untracked flow tests untouched, nothing pushed; origin/dev-ohm is still behind). Drafts of the issue text are only in the session scratchpad.

**How to apply:** before fixing any of #158, re-verify the item against the latest main ([[feedback-always-rebase-on-latest-main]]); the line numbers are 0.19.1 (ff7351c).
