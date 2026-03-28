# Assumptions Log
## AP Value Framing Business Case — All Assumptions Documented

> **Purpose**: This document records every assumption used in the business case calculation.
> In a real Celonis engagement, this log is reviewed and signed off by the AP Team Lead and Finance Controller
> during the Value Validation Workshop before values are committed.

---

## How to Read This Log

Each assumption is classified as:
- **Type A — FTE Cost**: Labor-related financial inputs
- **Type B — Effort**: Time estimates for manual activities
- **Type C — Realization**: Expected improvement percentages
- **Type D — Volume**: Event/case counts from data analysis
- **Type E — Scale**: Enterprise extrapolation parameters

Risk levels: 🟢 Low | 🟡 Medium | 🔴 High (higher risk = more likely to be challenged in sign-off)

---

## GLOBAL ASSUMPTIONS (Apply to Both Opportunities)

| ID | Assumption | Value | Type | Risk | Source | Sign-Off Status |
|----|------------|-------|------|------|--------|----------------|
| A1 | Annual FTE cost | $90,000 | A | 🟡 Medium | Celonis lecture note example (standard benchmark) | ⬜ Pending |
| A2 | Working days per year | 250 | A | 🟢 Low | Standard calendar convention | ⬜ Pending |
| A3 | Working hours per day | 8 | A | 🟢 Low | Standard working day | ⬜ Pending |
| A4 | **FTE cost per minute** | **$0.42** | A | 🟢 Low | Derived: $90,000 ÷ (250 × 8 × 60) | ⬜ Pending |
| A5 | Dataset represents typical process behavior | Yes | D | 🟡 Medium | Assumed — no seasonality filter applied | ⬜ Pending |
| A6 | Each deviation event = one manual intervention | Yes | B | 🟡 Medium | One-to-one assumed; multi-step interventions not modeled | ⬜ Pending |

**Note on A4**: The FTE cost per minute formula is:
```
$90,000 ÷ 250 days ÷ 8 hours ÷ 60 minutes = $0.4167/min ≈ $0.42/min
```
This is the same formula used in the Celonis Value Framing Guide automation example.

---

## OPPORTUNITY 1: PAYMENT & PO BLOCK RESOLUTION

| ID | Assumption | Value | Type | Risk | Source | Validation Notes |
|----|------------|-------|------|------|--------|-----------------|
| B1 | Total block events | 58 | D | 🟢 Low | P2P-Activities.csv: Set Payment Block (20) + Block PO Item (38) | Verified from data |
| B2 | Effort per payment block removal | 15 min | B | 🟡 Medium | Celonis Value Framing Guide published benchmark | Validate with AP team |
| B3 | Effort includes: identify reason, coordinate with departments, edit SAP, communicate to vendor | Yes | B | 🟡 Medium | Celonis guide step breakdown | Validate with AP team |
| B4 | Realization potential | 80% | C | 🟡 Medium | Conservative estimate; assumes 20% of blocks require extended manual investigation | Validate with process owner |
| B5 | Automated block removal requires 30% residual manual effort | Yes | C | 🟡 Medium | Celonis recommendation: "if 100 blocks automated, 30 include manual effort" | Per Value Framing Guide |
| B6 | Both Set Payment Block AND Block PO Item are in scope | Yes | D | 🟢 Low | Both activities delay invoice processing and require manual resolution | Confirm scope with AP lead |
| B7 | Enterprise scale factor | 343.6x | E | 🔴 High | Linear extrapolation: 279,000 ÷ 812 cases | Business volume confirmation needed |

**Sensitivity**: At 60% realization and 10 min effort: $146. At 90% realization and 20 min: $441 (sample dataset).

---

## OPPORTUNITY 2: PRICE DEVIATION REWORK ELIMINATION

| ID | Assumption | Value | Type | Risk | Source | Validation Notes |
|----|------------|-------|------|------|--------|-----------------|
| C1 | Total Change Price events | 110 | D | 🟢 Low | P2P-Activities.csv: ACTIVITY_EN = 'Change Price' | Verified from data |
| C2 | Effort per price correction | 10 min | B | 🔴 High | Industry estimate — not from published benchmark | Must validate with AP team |
| C3 | Effort includes: identify discrepancy, contact vendor/buyer, update SAP record, re-validate | Yes | B | 🟡 Medium | Standard price correction workflow | Validate with AP team |
| C4 | Realization potential | 70% | C | 🟡 Medium | Achievable through vendor master data sync + process change | Validate with process owner |
| C5 | Top 2 vendors (0000001001 + R1000) account for 50% of Change Price events | Yes | D | 🟢 Low | Confirmed from data analysis | Verified |
| C6 | Price corrections are independent events (one correction per event) | Yes | B | 🟡 Medium | Some cases may require multiple rounds — not modeled | Validate with AP team |
| C7 | Realization split: 50% from master data fix (no tech), 50% from process automation | Assumed | C | 🔴 High | Not verified — Phase 1 vs Phase 2 assumption | Must confirm with IT |

**Sensitivity**: At 50% realization and 10 min effort: $231. At 90% realization and 15 min: $496 (sample dataset).

---

## QUALITATIVE IMPACTS (Not Quantified)

These impacts are real but excluded from the monetary calculation.

| Impact | Opportunity | Why Not Quantified |
|--------|-------------|-------------------|
| Improved vendor relationships | OPP_02 | No data to model relationship value |
| Reduced AP team stress / burnout | OPP_01 + OPP_02 | No baseline data |
| Better cash flow timing and DPO improvement | OPP_01 | Would require Days Payable Outstanding baseline |
| Improved financial close accuracy | OPP_01 | Requires finance team input |
| Reduced audit risk from process non-conformance | OPP_01 + OPP_02 | Risk quantification requires separate assessment |
| Increased reputation as reliable payer | OPP_01 | Qualitative only |

---

## ASSUMPTION SIGN-OFF TRACKER

| Assumption ID | Reviewer | Role | Status | Date | Comments |
|--------------|----------|------|--------|------|---------|
| A1–A6 | — | Finance Controller | ⬜ Pending | — | — |
| B1–B7 | — | AP Team Lead | ⬜ Pending | — | — |
| C1–C7 | — | AP Team Lead + IT | ⬜ Pending | — | — |
| All | — | Procurement Manager | ⬜ Pending | — | — |

---

## REVISION HISTORY

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1.0 | 2026-03 | Initial draft — all assumptions from data analysis and Celonis guides | [Your Name] |

---

*This assumptions log follows the Celonis Value Framing Guide — Step 4 (Assumptions) framework.*
*Business case-related assumptions are used in the formula calculating the opportunity value.*
*Metric-related assumptions are included in the KPI definitions document.*