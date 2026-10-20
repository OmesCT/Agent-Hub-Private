---
name: feedback-flow-tests-stay-uncommitted
description: "The three flow-completeness test files written 2026-10-05 must never be committed or pushed; they stay untracked in the working tree"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b51447ab-922e-401e-ac78-e04468240da4
  modified: 2026-10-05T08:48:17.821Z
---

On 2026-10-05, while I was building the flow-completeness report, the user said "แต่ไม่ต้องเอาที่เทสอัพขึ้น git นะ": do not put the tests up on git. The files are `backend/Fits.Tests/Unit/WorkflowFlowCompletenessTests.cs`, `backend/Fits.Tests/E2E/FullLifecycleJourneyE2E.cs` and `frontend/src/shell/flowContract.test.ts`.

**Why:** the tests were written to answer "is the whole flow covered?" and to feed a report; the user wants to look at them first and does not want them in the repo history on their own.

**How to apply:** leave them untracked. Never `git add -A` / `git add .` on dev-ohm while they exist: stage explicit paths only, and keep these three out of every commit, tag and push (alpha tags are cut from dev-ohm, so check `git status` before tagging). Do not add them to `.gitignore`. Only commit them if the user later says so. Run recipe and numbers are in [[reference-run-fits-locally]]; branch rules are in [[feedback-dev-ohm-issue-first-no-mr]].
