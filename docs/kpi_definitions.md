# KPI Definitions
## AP Value Framing Business Case — KPI Formulas & Business Logic

> **Purpose**: This document defines every KPI used in the business case.
> Aligned with Celonis Validation Approach Step 3 (Metrics & Value Tracking).
> These definitions require sign-off from the business owner before the value is committed.

---

## KPI Categories

| Category | Purpose |
|----------|---------|
| **Process Health KPIs** | Measure overall P2P process quality |
| **Opportunity KPIs** | Track specific improvement opportunities |
| **Value Tracking KPIs** | Measure realized savings after intervention |

---

## SECTION 1: PROCESS HEALTH KPIs

---

### KPI-01: Total Case Count
| Field | Definition |
|-------|-----------|
| **Business Definition** | Total number of Purchase Order line items (cases) processed in the selected period |
| **Formula** | `COUNT(DISTINCT _CASE_KEY)` |
| **Data Source** | EKPO table (P2P-Cases.csv → _CASE_KEY) |
| **Filter** | Last 12 months by clearing date (or full dataset if no date filter applied) |
| **Current Value** | 812 cases |
| **Unit** | Count |
| **Sign-Off Status** | ⬜ Pending |

---

### KPI-02: Automation Rate
| Field | Definition |
|-------|-----------|
| **Business Definition** | Percentage of all P2P process activities executed automatically by the system (batch) without human intervention |
| **Formula** | `COUNT(events WHERE User Type = 'B') ÷ COUNT(all events)` |
| **Data Source** | _CEL_P2P_ACTIVITIES (P2P-Activities.csv → User Type) |
| **Current Value** | 47.5% (2,341 automated ÷ 4,927 total) |
| **Baseline** | 47.5% |
| **Target** | 70%+ |
| **Unit** | Percentage |
| **Sign-Off Status** | ⬜ Pending |
| **Notes** | User Type 'B' = BATCH_JOB (automated); User Type 'A' = human user |

---

### KPI-03: Deviation Case Rate
| Field | Definition |
|-------|-----------|
| **Business Definition** | Percentage of PO items (cases) that include at least one deviation activity (rework, block, waste) |
| **Formula** | `COUNT(DISTINCT _CASE_KEY WHERE at least one deviation activity exists) ÷ COUNT(DISTINCT _CASE_KEY)` |
| **Deviation Activities** | Change Price, Block PO Item, Set Payment Block, Remove Payment Block, Change Currency, Delete PO Item, Change Quantity, Cancel Goods Receipt, Refuse PO, Dun Order Confirmation, Send PO Update |
| **Data Source** | P2P-Activities.csv |
| **Current Value** | 33.9% (275 deviant ÷ 812 total) |
| **Target** | ≤ 15% |
| **Unit** | Percentage |
| **Sign-Off Status** | ⬜ Pending |

---

### KPI-04: Average Cycle Time
| Field | Definition |
|-------|-----------|
| **Business Definition** | Average number of calendar days from first activity to last activity per case (end-to-end PO processing time) |
| **Formula** | `AVG(MAX(EVENTTIME) - MIN(EVENTTIME)) per _CASE_KEY` |
| **Data Source** | P2P-Activities.csv → EVENTTIME |
| **Current Value** | 29.6 days |
| **Percentiles** | P25 = 26 days; P50 = 30 days; P75 = 34 days; P95 = 41 days |
| **Outliers** | Max = 190 days — 4 cases exceed 60 days (0.5% of all cases) |
| **Target** | ≤ 20 days |
| **Unit** | Days |
| **Sign-Off Status** | ⬜ Pending |

---

### KPI-05: Total Procurement Spend
| Field | Definition |
|-------|-----------|
| **Business Definition** | Sum of Net Order Price across all active PO line items in the selected period |
| **Formula** | `SUM(Net Order Price)` |
| **Data Source** | P2P-Cases.csv → Net Order Price |
| **Current Value** | €207,095.93 |
| **Currency Note** | Mixed currencies in raw data (EUR dominant; USD present); ensure consistent currency normalization |
| **Unit** | EUR (€) |
| **Sign-Off Status** | ⬜ Pending |

---

## SECTION 2: OPPORTUNITY KPIs

---

### KPI-06: Number of Payment Block Events (OPP_01)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Total number of manual payment block activities (both setting and PO-level blocking) in the selected period |
| **Formula** | `COUNT(events WHERE ACTIVITY_EN IN ('Set Payment Block', 'Block Purchase Order Item'))` |
| **Data Source** | P2P-Activities.csv |
| **Scope Decision** | Includes BOTH Set Payment Block (invoice level) AND Block Purchase Order Item (PO level) — confirm scope with AP lead |
| **Current Value** | 58 (20 Set Payment Block + 38 Block PO Item) |
| **Target** | ≤ 12 events (80% reduction) |
| **Unit** | Count |
| **Sign-Off Status** | ⬜ Pending |
| **Notes** | Remove Payment Block events (20) are excluded from count as they represent resolution, not the problem |

---

### KPI-07: Average Manual Payment Block Removal per Invoice (OPP_01)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Average number of manual block events per invoice/PO item — indicates frequency of rework per case |
| **Formula** | `COUNT(block events) ÷ COUNT(DISTINCT _CASE_KEY with block events)` |
| **Current Value** | 58 events ÷ ~58 unique cases ≈ 1.0 blocks per affected case |
| **Note** | Header-level blocks are most common; item-level blocks may appear in some cases |
| **Unit** | Ratio |
| **Sign-Off Status** | ⬜ Pending |

---

### KPI-08: Number of Price Correction Events (OPP_02)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Total number of Change Price activities in the selected period — proxy for price mismatch frequency |
| **Formula** | `COUNT(events WHERE ACTIVITY_EN = 'Change Price')` |
| **Data Source** | P2P-Activities.csv |
| **Current Value** | 110 |
| **% of Total Events** | 2.2% of all 4,927 events |
| **% of Deviations** | 35.5% of all 310 deviation events |
| **Target** | ≤ 33 events (70% reduction) |
| **Unit** | Count |
| **Sign-Off Status** | ⬜ Pending |

---

### KPI-09: Price Correction Rate (OPP_02)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Percentage of PO items that required at least one price correction after PO issuance |
| **Formula** | `COUNT(DISTINCT _CASE_KEY WHERE Change Price event exists) ÷ COUNT(DISTINCT _CASE_KEY)` |
| **Data Source** | P2P-Activities.csv joined to P2P-Cases.csv |
| **Current Value** | ~13.5% of cases (110 events across ~110 unique cases) |
| **Target** | ≤ 4% |
| **Unit** | Percentage |
| **Sign-Off Status** | ⬜ Pending |

---

## SECTION 3: VALUE TRACKING KPIs (Post-Implementation)

These KPIs are used to measure realized savings after improvement initiatives are deployed.

---

### KPI-10: Value Realized — Labor Productivity (OPP_01)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Actual labor cost saved from reduced manual block removal activities after intervention |
| **Formula** | `(Baseline avg manual blocks per invoice [#] - Post-intervention avg [#]) × Total invoices after intervention [#] × Effort per block removal [min] × FTE cost per minute [$]` |
| **Baseline** | 58 block events / period |
| **Measurement Frequency** | Monthly |
| **Review Trigger** | If post-intervention block count increases >20% vs. prior month |
| **Unit** | USD ($) |
| **Sign-Off Status** | ⬜ Pending — required before Execute phase |

---

### KPI-11: Value Realized — Labor Productivity (OPP_02)
| Field | Definition |
|-------|-----------|
| **Business Definition** | Actual labor cost saved from reduced price correction activities after vendor master data sync |
| **Formula** | `(Baseline Change Price events [#] - Post-intervention Change Price events [#]) × Effort per correction [min] × FTE cost per minute [$]` |
| **Baseline** | 110 Change Price events / period |
| **Measurement Frequency** | Monthly |
| **Review Trigger** | If Change Price events drop by <20% within 60 days of vendor master data update |
| **Unit** | USD ($) |
| **Sign-Off Status** | ⬜ Pending |

---

## KPI SIGN-OFF TRACKER

| KPI ID | KPI Name | Business Owner | Tech Reviewer | Status | Sign-Off Date |
|--------|----------|---------------|---------------|--------|--------------|
| KPI-01 | Total Case Count | — | — | ⬜ Pending | — |
| KPI-02 | Automation Rate | — | — | ⬜ Pending | — |
| KPI-03 | Deviation Case Rate | — | — | ⬜ Pending | — |
| KPI-04 | Average Cycle Time | — | — | ⬜ Pending | — |
| KPI-05 | Total Procurement Spend | — | — | ⬜ Pending | — |
| KPI-06 | Payment Block Events | — | — | ⬜ Pending | — |
| KPI-07 | Avg Blocks per Invoice | — | — | ⬜ Pending | — |
| KPI-08 | Price Correction Events | — | — | ⬜ Pending | — |
| KPI-09 | Price Correction Rate | — | — | ⬜ Pending | — |
| KPI-10 | Value Realized OPP_01 | — | — | ⬜ Pending | — |
| KPI-11 | Value Realized OPP_02 | — | — | ⬜ Pending | — |

---

## FILTER DEFINITIONS

All KPIs should be calculated with these filters applied (align with business owner):

| Filter | Value | Type | Notes |
|--------|-------|------|-------|
| Time Period | Last 12 months by clearing date | Standalone | Ensures comparability across periods |
| Document Type | Vendor Invoice | Standalone | Exclude internal documents |
| Activity Scope | Payment Block Removal by manual user | Formula Embedded | Exclude automated removals from manual count |
| Currency | EUR (primary) | Standalone | Normalize to single currency for value calc |

---

*This document follows Celonis Value Framing Guide — Step 3 (Metrics & Value Tracking).*
*Filters follow Celonis Step 2 (Filters) classification: Standalone vs. Formula Embedded.*