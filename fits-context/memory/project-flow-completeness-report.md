---
name: project-flow-completeness-report
description: "2026-10-05 flow-completeness work: three uncommitted test files, run numbers, report artifact, findings and the issue it produced (#153)"
metadata:
  node_type: memory
  type: project
  originSessionId: b51447ab-922e-401e-ac78-e04468240da4
  modified: 2026-10-05T09:43:37.093Z
---

On 2026-10-05 (dev-ohm eeb4e4a = 0.19.0 + the two #150 Dockerfile commits) the user asked via `/design` for unit tests that show whether the whole flow is complete, with screenshots and an explained report file.

**Files (untracked on purpose, see [[feedback-flow-tests-stay-uncommitted]]):** `backend/Fits.Tests/Unit/WorkflowFlowCompletenessTests.cs` (157 cases: 7x5 transition table, reachability / no dead end, role matrix per review stage, submit gate, queue routing), `backend/Fits.Tests/E2E/FullLifecycleJourneyE2E.cs` (4 journeys, real HTTP + PostgreSQL, no SQL status shortcut: one item through all six stages, send-back loop from stages 2/3/4, reject at 3/4 plus admin reopen, self-certified submit incl. the cross-team duplicate check), `frontend/src/shell/flowContract.test.ts` (47 cases: FE submit/executive/export gates and status chips vs the server rules). Trait `Category=FlowCompleteness` selects all 161 backend tests.

**Results:** backend 981/981 in the repo's Docker test image (Unit 511, Integration 398, E2E 72; before: 820, and on this Mac 2 attachment tests fail only because `/app/attachments` is not writable), frontend 583/583 (before 536; run with `--exclude 'src/__bugverify__/**'`). Five deliberate breaks of production rules (Stage 3 skips Stage 4, other-team Dept Head, PO gate open, everyone self-certifies, executive version guard removed) were all caught by the new tests AND by the old suite (the old suite is already tight); production files were restored and `git diff` stayed empty. An independent reviewer found 5 medium issues in the first draft (vacuous duplicate check, CIO refused by the wrong policy, exports only checked as zip, SignalR enum spellings, "documented" overclaim); all fixed before the final run. Recipe: [[reference-run-fits-locally]].

**Report:** private Design artifact https://claude.ai/artifact/LK35VeufcFnfnLBqUuew5u ("FITs Flow Coverage", Thai, 25 screenshot crops from a local pod-like replica; the live DEV site was not touched). Screenshot dataset was throwaway; the capture scripts are only in the session scratchpad.

**Findings:** ADMIN can take an ITPN item from Draft to Approved alone (Pending CTO accepts CIO or ADMIN; ties to !155, a PO decision); the executive Portfolio Sign-off only writes an audit row, nothing reads it; the THB 500,000 quotation rule is UI text only (known: #129 open question 7), so the golden-path journey submits a THB 1,200,000 item with no attachment, update it if the rule becomes enforced; on a 384 MiB replica the API was OOM-killed once under UI use (supports #132; amplified by #136 R3-session-3 reload storm); the audit trail shows the nginx pod IP unless `ForwardedHeaders__KnownProxies/KnownNetworks` are set (docs/DEPLOY_ON_PREM.md, "Reverse proxy trust"), worth checking on DEV. Four new minor UI nits were filed as one issue **#153** (Itemized tab clipped, send-back button padding, hard-coded "PRD 2026-09-24" eyebrow in DashboardView.tsx:643, register Committed column under the sticky action column); K22 and R1-contract-7 in #136 already cover the PO date default / stale available panel and the "Over budget" label on the PO gate.

Login guide (asked right after the report, 2026-10-05): private artifact https://claude.ai/artifact/1Y3LGV1tbUqDzAnDWwcMjt, Thai, mock sign-in on DEV and local: 7 seeded users with roles, any non-empty dummy password (never a real AD password), order of users for one full run, how to switch user (sessionStorage per tab), troubleshooting, what changes with SSO (#78).

Not done: the 76 Playwright specs (config hard-codes localhost:8080, some specs need the dev-auth bundle), no check of the live DEV site. Related: [[project-frontend-bug-sweep-136]], [[feedback-open-issue-when-something-odd]], [[feedback-dont-test-live-dev-site]].
