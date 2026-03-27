# Data Dictionary — P2P Event Log Dataset

## Source
Celonis Guided Learning — Purchase-to-Pay Training Dataset (SAP-based simulation)

---

## File 1: P2P-Cases.csv

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| _CASE_KEY | String | Unique PO item identifier (maps to EKPO._CASE_KEY) | 1000010 |
| Material Group | String | SAP material group code | 00210 |
| Material Group Text | String | Human-readable material category | Input Devices |
| Material | String | SAP material number | DPC1011 |
| Material Text | String | Material description | Professional keyboard |
| Net Order Price | Float | PO item value in transaction currency | 20.50 |
| Currency | String | Transaction currency (EUR / USD / null) | EUR |
| Vendor | String | SAP vendor number (LFA1.LIFNR) | 0000001005 |

**Record Count**: 812
**Total Spend**: €207,095.93

---

## File 2: P2P-Activities.csv

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| _CASE_KEY | Integer | Links to P2P-Cases._CASE_KEY | 100000 |
| ACTIVITY_EN | String | Activity name in English | Record Invoice Receipt |
| EVENTTIME | Datetime | Timestamp of activity execution | 2016-10-13T10:00:01 |
| _SORTING | Integer | Sort order within case (for ordering events) | 0 |
| USER_NAME | String | SAP username or BATCH_JOB | BATCH_JOB |
| User Type | String | A = Manual (human), B = Automated (batch) | B |

**Record Count**: 4,927

---

## Activity Catalogue

### Happy Path Activities (Value-Adding)
| Activity | Expected Position | Notes |
|----------|------------------|-------|
| Create Purchase Requisition Item | 1 | Optional — not all POs start with PR |
| Create Purchase Order Item | 2 | Core activity |
| Send Purchase Order | 3 | PO issued to vendor |
| Record Goods Receipt | 4 | Goods received confirmation |
| Record Invoice Receipt | 5 | Invoice booked in system |
| Clear Invoice | 6 | Payment cleared |

### Deviation Activities (Non-Value-Adding / Rework)
| Activity | Category | Business Meaning |
|----------|----------|-----------------|
| Change Price | Rework | Price mismatch between PO and invoice |
| Block Purchase Order Item | Block | PO held — prevents goods receipt |
| Set Payment Block | Block | Invoice cannot be paid |
| Remove Payment Block | Resolution | Block manually removed |
| Change Quantity | Rework | Quantity mismatch correction |
| Change Currency | Rework | Currency correction |
| Delete Purchase Order Item | Waste | PO item cancelled |
| Cancel Goods Receipt | Rework | Goods receipt reversed |
| Refuse Purchase Order | Rejection | Vendor declined PO |
| Dun Order Confirmation | Follow-up | Chasing vendor for confirmation |
| Send Purchase Order Update | Rework | PO updated post-issue |

---

## Key Assumptions (for Value Calculations)

| Assumption | Value | Source |
|------------|-------|--------|
| FTE Annual Cost | $90,000 | Celonis lecture note example |
| Working days per year | 250 | Standard |
| Hours per working day | 8 | Standard |
| FTE cost per minute | $0.42 | $90K ÷ 250 ÷ 8 ÷ 60 |
| Effort per payment block removal | 15 minutes | Celonis Value Framing Guide benchmark |
| Effort per price correction | 10 minutes | Estimated (industry benchmark) |
| Payment block realization potential | 80% | Conservative estimate |
| Price deviation realization potential | 70% | Conservative estimate |

---

## SAP Table Mapping (Data Model)

```
LFA1 (Vendor Master)
  └── LIFNR, MANDT
      └── EKKO (Purchase Order Header)
            └── MANDT, EBELN, LIFNR
                └── EKPO (Purchase Order Items) ← CASE TABLE
                      └── MANDT, EBELN, _CASE_KEY
                          └── _CEL_P2P_ACTIVITIES (Activity Log)
                                └── _CASE_KEY
```
