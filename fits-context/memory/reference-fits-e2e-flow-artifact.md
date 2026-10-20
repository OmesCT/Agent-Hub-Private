---
name: reference-fits-e2e-flow-artifact
description: "2026-10-06 private Design artifact 'FITs End-to-End Flow' (my understanding of the whole flow, 4 boards) and the 8 open questions B1-B8 it asks the user"
metadata:
  node_type: memory
  type: reference
  originSessionId: 592a22e1-cbf5-4a27-b76e-1ad4579fb92d
  modified: 2026-10-06T06:50:50.146Z
---

On 2026-10-06 the user asked "ในความเข้าใจของนาย ฉันอยากรู้ว่านายเข้าใจ flow แบบ End2End เป็นแบบไหน ลองทำเป็นไฟล์ HTML" (via `/design`). Result: private Design artifact https://claude.ai/artifact/EHUV4S6PEghGMfdcyV8sQz ("FITs End-to-End Flow", Thai, built from the repo's own DESIGN.md colours, Sarabun + JetBrains Mono; no design system was listed for the account).

**Boards:** 1 swimlane of the 6 stages with the roles per step, self-certify shortcut, exits (Send Back / Reject / Reopen) and the PO release gate (2464x1760, hand-placed cards and arrows); 2 the 7 statuses x 5 actions matrix with role gates (from `WorkflowService.CreateStateMachine`/`ValidateTransition`); 3 money flow with the real figures of 26DEM401 from the local DB (30,000,000.00 approved, 12,500,000.00 committed, 2,750,000.00 paid, 17,500,000.00 available, burn 41.67%); 4 what I am sure of plus eight questions B1-B8.

**The eight questions (unanswered when written, the user has not replied):** B1 ADMIN(ITPN) can take an item Draft to Approved alone (self-certify, approve at Pending Admin, approve as CIO stand-in); B2 CIO Sign-Off only writes an audit row and gates nothing; B3 THB 500,000 quotation rule is UI text only (#129 q7); B4 no Reject button in the approval queue although API/docs have it (#137); B5 Returned -> Submit always lands on PendingDeptHead, so a Dept Head can approve their own resubmission; B6 docs say "Batch Consolidate" at Stage 3 but code approves item by item and packages only overlap pairs; B7 Export and PO booking do not depend on each other (D365 export needs Approved items, PO needs the FY cut committed); B8 Audit Ledger hidden in the UI from CIO/CEO/CTO/EXEC though the API allows them (#158 L16).

**Caveats:** per the Design type's own rule I did not render or screenshot the canvas, so the layout is unchecked visually; the board files are `.dc.html` (need the type's support.js), not standalone HTML; only the owner can open the link until shared. Related: [[project-fe-review-0-19-1]], [[project-flow-completeness-report]].
