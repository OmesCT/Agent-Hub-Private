---
name: project-approval-authority-requirement
description: "Requirement from the business (2026-10-06): approval authority ladders by position (in budget / no budget), 300,000 = procurement-committee screening; the route-designer flow the user had already sent; what differs, what the system has today, what is still open"
metadata:
  node_type: memory
  type: project
  originSessionId: 592a22e1-cbf5-4a27-b76e-1ad4579fb92d
  modified: 2026-10-06T07:23:19.395Z
---

On 2026-10-06 the user relayed a business reply ("อ้างตามประกาศอำนาจอนุมัติในแผนงบประมาณ") that arrived AFTER he had sent the business an approval-route flow (four screenshots he pasted: route of 26INFRA041, route designer with palette/validation, org chart by level, route-instance flowchart by amount range S/M/L). Amounts in THB, "ไม่เกิน" = up to and including.

**Table A, budgeted (มีงบในแผน):** VP, FVP 100,000 · SVP, FSVP 300,000 · EVP, FEVP 1,500,000 · SEVP 3,000,000 · CEO 10,000,000 · Excom committee and Board unlimited.
**Table B, "ไม่มีงบประมาณ" (not specified in the budget plan):** no position has approval authority except CEO up to 2,000,000; Excom up to 20,000,000; above that the Board of Directors.
**300,000:** only a screening threshold for the procurement committee (คณะกรรมการจัดซื้อ), not an approval limit.

**The flow he had sent (his own design, ITEM_GROSS_TOTAL basis D1, A1 requester-VP self-approves then escalates, D11 vacant position = BLOCK, D12 CEO records the committee resolution, "stale" re-route when the amount grows after the first approval)** used example numbers VP <= 200,000, SEVP <= 300,000, CEO unlimited after an ITSC resolution (quorum 4/6). Differences with the business reply: 7 real levels instead of 4; real limits; 300,000 was an authority boundary in the flow but is only a procurement screen; CEO is limited to 10,000,000 (above: Excom/Board decide); no Table B in the flow; the business names Excom, Board and the procurement committee, not ITSC. With the real table 26INFRA041 (350,000 + 7% = 374,500.00) ends at CIO-01 (SEVP) plus a procurement screen, no ITSC/CEO.

**What the system has today (0.19.1, 69503e9):** none of it. Users have only a role; Stage 4 (`PendingApproval`) is approved by CIO or ADMIN for ANY amount; the only amount rules are the THB 500,000 quotation notice (UI text, not enforced, #129 q7) and the THB 300,000,000 board cap setting. No 300,000 anywhere in code or PRD. This is a new feature (route engine + positions + two authority tables + committee resolution record), not a constant to change. It answers part of my open questions B1 (ADMIN approving as CIO stand-in: in his org chart the budget admin is AVP, a control step, "not an approval authority"), B3 and B5 in [[reference-fits-e2e-flow-artifact]].

**Artifact:** board 5 "เส้นทางอนุมัติตามอำนาจ" was added to the E2E canvas (https://claude.ai/artifact/EHUV4S6PEghGMfdcyV8sQz, version 6) with both tables, the 6-step resolver, nine worked examples (sample line INFRA-HEAD VP -> CIO-01 SEVP -> CEO-01), the differences list and the questions below. Boards 1-4 stay as-is of the current system.

**Open, to ask the business:** (1) what "no budget" means in FITs (out-of-plan item opened mid-year, PO above Available, both); (2) amount basis: gross incl. non-refundable VAT? total contract or annual share? before or after the cut; (3) Table A above 10,000,000: Excom or Board or split by size; (4) Table B: may other positions join as "เห็นควร" (recommend); (5) 300,000 "over" or "from", who screens, does it replace the 500,000 quotation rule; (6) who records an Excom/Board resolution in the system and with what attachment; does ITSC still exist.

**Why:** the user owns PRD/flow changes; the PRD (`_bmad-output/initiative-fits/prd-fits/prd-fits.md`) is the single source of truth, so the change goes PRD first, then an issue/story (BMad). **How to apply:** do not edit PRD or code until the open points are answered and the user says go; limits must be configurable (Settings, audited ADMIN write, versioned with the announcement reference and effective date), enforced on the server, amounts with `THB ` prefix and 2 decimals. Related: [[project-fe-review-0-19-1]].
