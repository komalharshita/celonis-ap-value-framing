# Value Framing Methodology
## Celonis 6-Step Framework — Applied to AP Payment Blocks & Price Deviations

---

## Framework Overview

The **Celonis Value Delivery Framework** moves through three macro-phases:
```
Identify → Frame & Commit → Realize & Track
```

This project covers the **Frame & Commit** phase in full, applying the 6-step process below.

---

## Step 1: Qualify Value Opportunities

**Objective**: Filter opportunities worth investigating from the full list of potential improvements.

Three qualification criteria:

### 1A — Strategic Fit
Opportunities must align with organizational goals. For AP, the primary goals are:
- Reduce P&L leakage (Spend pillar)
- Improve productivity (Productivity pillar)
- Optimize working capital (Working Capital pillar)

**Assessment for this project:**
| Opportunity | Spend | Productivity | Working Capital | Qualified? |
|-------------|-------|--------------|-----------------|------------|
| Payment & PO Blocks | ✅ | ✅ | ✅ | ✅ Yes |
| Price Deviations | ✅ | ✅ | — | ✅ Yes |

### 1B — Business Impact
Both opportunities have high labor productivity impact (manual correction effort) and financial performance impact (delayed payments, missed discounts).

### 1C — Feasibility
- **Technical**: SAP connector available; data model validated (EKPO case table confirmed)
- **Operational**: Block removal and price correction are standard AP team activities — solution can be operationalized
- **Schedule**: Both opportunities addressable in 1–2 sprint cycles

---

## Step 2: Quantify Value Opportunities

**Formula:**
```
Expected Monetary Value = Affected Cases × Realization Potential × Value per Case
```

Where:
```
Value per Case (labor) = Effort (minutes) × FTE Cost per Minute
FTE Cost per Minute = Annual FTE Cost ÷ 250 days ÷ 8 hours ÷ 60 minutes
                    = $90,000 ÷ 120,000 = $0.42 per minute
```

### Opportunity 1: Payment & PO Blocks
```
Affected Events:        58 (20 Set Payment Block + 38 Block PO Item)
Realization Potential:  80%
Effort per resolution:  15 minutes
FTE Cost/min:           $0.42

EMV = 58 × 0.80 × (15 × $0.42)
    = 58 × 0.80 × $6.30
    = $292.08 (sample dataset)
```

*Enterprise scale note: At 279k cases (Celonis platform), equivalent rate produces ~$1.5M–$2.2M p.a.*

### Opportunity 2: Price Deviation Corrections
```
Affected Events:        110 (Change Price activities)
Realization Potential:  70%
Effort per correction:  10 minutes
FTE Cost/min:           $0.42

EMV = 110 × 0.70 × (10 × $0.42)
    = 110 × 0.70 × $4.20
    = $323.40 (sample dataset)
```

---

## Step 3: Investigate Root Causes

Root causes are grouped into three categories:

### Process-Based Root Causes
- Missing goods receipt confirmation triggers payment block automatically
- Price entered on PO does not match vendor invoice → Change Price required
- PO created without purchase requisition (maverick buying) → higher error rate

### Time-Based Root Causes
- Payment blocks cluster around month-end / quarter-end periods
- Fiscal year budget pressure drives rushed PO creation → more errors

### Attribute-Based Root Causes
- **Vendor 0000001001**: Highest Change Price frequency (34 events)
- **Vendor R1000**: Second highest (21 events) — price list not updated in SAP
- **Material Group "Elevators"**: Highest spend concentration (€100K, 48.3% of total)

---

## Step 4: Validate Value Opportunities

### Business Logic Validation
| KPI | Business Definition | Celonis Implementation |
|-----|--------------------|-----------------------|
| # Payment Block Events | Count of Set Payment Block activities | ACTIVITY_EN = 'Set Payment Block' |
| # Price Corrections | Count of Change Price activities | ACTIVITY_EN = 'Change Price' |
| Avg Cycle Time | Days from first to last event per case | MAX(EVENTTIME) - MIN(EVENTTIME) |
| Automation Rate | % of events executed by batch user | User Type = 'B' ÷ Total events |
| Deviation Rate | % of cases with at least one deviation event | Cases with deviation ÷ Total cases |

### KPI Sign-Off Checklist
- [ ] Business owner confirms payment block definition includes both Set Payment Block and Block PO Item
- [ ] FTE cost assumption ($90K/year) validated with HR
- [ ] Effort estimates (15 min, 10 min) reviewed by AP team lead
- [ ] Realization potentials (80%, 70%) agreed with process owner
- [ ] Date filter (last 12 months by clearing date) applied consistently

---

## Step 5: Prioritize Opportunities

**Impact-Effort Matrix Placement:**

```
         HIGH IMPACT
              │
    ┌─────────┼─────────────────┐
    │  Big    │   GOLD NUGGETS  │
    │  Bets   │                 │
    │         │  [Price Dev.]   │
    │         │  [Pay. Blocks]  │
    ├─────────┼─────────────────┤
    │ Long-   │  Low-Hanging    │
    │ Term    │  Fruit          │
    │         │                 │
    └─────────┼─────────────────┘
         SLOW │                FAST
              TIME TO VALUE
```

Both opportunities land in the **Gold Nuggets** quadrant:
- High business impact (productivity + financial performance)
- Fast to implement (existing SAP connector + standard automation patterns)

**Recommendation**: Address **Price Deviations** first (higher event count = larger sample; vendor-level root cause more actionable), then **Payment & PO Blocks** (lower frequency but directly impacts cash flow).

---

## Step 6: Commit Value Opportunities

**Sign-off requirements:**
1. Operational SME sign-off on KPI definitions and assumptions
2. AP team lead confirms effort estimates are realistic
3. Management sponsor approves the business case values
4. Implementation timeline and ownership agreed

**Committed Values (sample dataset):**
| Opportunity | Framed Value | Committed |
|------------|-------------|-----------|
| Payment & PO Blocks | $292 p.a. | Pending |
| Price Deviations | $323 p.a. | Pending |
| **Total** | **$615 p.a.** | **Pending** |

*Enterprise extrapolation (279k cases): $615K–$2M+ p.a.*

---

## References
- Celonis Value Delivery Framework Course Notes (2026)
- Celonis Value Framing Guides — Accounts Payable Module
- Celonis Business Case Per Individual Opportunity Template
- Celonis Business Case Overview Template
