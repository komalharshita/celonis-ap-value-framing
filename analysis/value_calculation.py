import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os

DATA_DIR   = "data"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

NAVY   = "#1E2761"
BLUE   = "#2196F3"
ORANGE = "#FF6B35"
GREEN  = "#388E3C"
LIGHT  = "#F5F7FA"
GRAY   = "#888888"


FTE_ANNUAL_COST   = 90_000   # USD — Annual FTE cost
WORKING_DAYS      = 250      # Days per year
HOURS_PER_DAY     = 8        # Working hours per day
ENTERPRISE_CASES  = 279_000  # Cases in enterprise deployment (from Celonis screenshots)
SAMPLE_CASES      = 812      # Cases in this dataset

# Derived — do not change
FTE_COST_PER_MIN = FTE_ANNUAL_COST / (WORKING_DAYS * HOURS_PER_DAY * 60)

opportunities = [
    {
        "id"                    : "OPP_01",
        "name"                  : "Payment & PO Block Resolution",
        "pillar"                : "Productivity",
        "affected_events"       : 58,       # Set Payment Block (20) + Block PO Item (38)
        "effort_min"            : 15,       # minutes per block resolution
        "realization_pct"       : 0.80,     # 80% — conservative for automation
        "time_to_value"         : "Short",  # 1–2 sprints
        "source_activity"       : "Set Payment Block + Block Purchase Order Item",
        "assumption_source"     : "Celonis Value Framing Guide benchmark",
        "recommended_solution"  : "Parked & Blocked Invoices Starter Kit App + Action Flows",
        "root_cause_type"       : "Process-based + Attribute-based",
    },
    {
        "id"                    : "OPP_02",
        "name"                  : "Price Deviation Rework Elimination",
        "pillar"                : "Productivity",
        "affected_events"       : 110,      # Change Price activities
        "effort_min"            : 10,       # minutes per price correction
        "realization_pct"       : 0.70,     # 70% — master data fix + process change
        "time_to_value"         : "Short",
        "source_activity"       : "Change Price",
        "assumption_source"     : "Industry benchmark; validated with AP team estimate",
        "recommended_solution"  : "Vendor master data sync + 3-way match automation",
        "root_cause_type"       : "Attribute-based (vendor-specific)",
    },
]

# calculation engine 

def calculate_emv(opp, fte_cost_per_min):
    """EMV = Affected Events × Realization Potential × (Effort × FTE Cost/min)"""
    value_per_event = opp["effort_min"] * fte_cost_per_min
    emv = opp["affected_events"] * opp["realization_pct"] * value_per_event
    return round(emv, 2)

def enterprise_scale(sample_value, sample_cases, enterprise_cases):
    """Linear extrapolation to enterprise case volume."""
    return sample_value * (enterprise_cases / sample_cases)

print("=" * 70)
print("  ACCOUNTS PAYABLE VALUE FRAMING — BUSINESS CASE REPORT")
print("  Celonis 6-Step Methodology | P2P Event Log Dataset")
print("=" * 70)

print(f"\n  ASSUMPTIONS")
print(f"  {'─'*40}")
print(f"  Annual FTE Cost         : ${FTE_ANNUAL_COST:>10,}")
print(f"  Working Days / Year     : {WORKING_DAYS:>10}")
print(f"  Hours / Day             : {HOURS_PER_DAY:>10}")
print(f"  FTE Cost / Minute       : ${FTE_COST_PER_MIN:>10.4f}")
print(f"  Dataset Cases           : {SAMPLE_CASES:>10,}")
print(f"  Enterprise Cases        : {ENTERPRISE_CASES:>10,}")
print(f"  Scale Factor            : {ENTERPRISE_CASES/SAMPLE_CASES:>10.1f}x")

total_sample     = 0
total_enterprise = 0
results = []

for opp in opportunities:
    emv_sample     = calculate_emv(opp, FTE_COST_PER_MIN)
    emv_enterprise = enterprise_scale(emv_sample, SAMPLE_CASES, ENTERPRISE_CASES)
    total_sample     += emv_sample
    total_enterprise += emv_enterprise
    opp["emv_sample"]     = emv_sample
    opp["emv_enterprise"] = emv_enterprise
    results.append(opp)

    print(f"\n  {'─'*60}")
    print(f"  OPPORTUNITY: {opp['id']} — {opp['name']}")
    print(f"  {'─'*60}")
    print(f"  Pillar              : {opp['pillar']}")
    print(f"  Root Cause Type     : {opp['root_cause_type']}")
    print(f"  Source Activity     : {opp['source_activity']}")
    print(f"  Affected Events     : {opp['affected_events']:,}")
    print(f"  Effort / Event      : {opp['effort_min']} minutes")
    print(f"  Realization Pct     : {opp['realization_pct']*100:.0f}%")
    print(f"  Time to Value       : {opp['time_to_value']}")
    print(f"  Solution            : {opp['recommended_solution']}")
    print(f"  Assumption Source   : {opp['assumption_source']}")
    print(f"")
    print(f"  Formula:")
    print(f"    EMV = {opp['affected_events']} events")
    print(f"        × {opp['realization_pct']*100:.0f}% realization")
    print(f"        × ({opp['effort_min']} min × ${FTE_COST_PER_MIN:.4f}/min)")
    print(f"        = ${emv_sample:,.2f}")
    print(f"")
    print(f"  ▸ Sample Dataset Value   : ${emv_sample:>10,.2f}  (812 cases)")
    print(f"  ▸ Enterprise Scale Value : ${emv_enterprise:>10,.0f}  ({ENTERPRISE_CASES:,} cases)")

print(f"\n  {'═'*60}")
print(f"  BUSINESS CASE TOTALS")
print(f"  {'─'*60}")
print(f"  Total Value (Sample Dataset)   : ${total_sample:>10,.2f}")
print(f"  Total Value (Enterprise Scale) : ${total_enterprise:>10,.0f}")
print(f"  {'═'*60}")

# kpi targets

print(f"\n  SUCCESS KPI TARGETS")
print(f"  {'─'*60}")
kpis = [
    ("Change Price Events",   "110/period", "≤ 33/period", "70% reduction"),
    ("Payment Block Events",  " 20/period", "≤  4/period", "80% reduction"),
    ("Block PO Item Events",  " 38/period", "≤  8/period", "80% reduction"),
    ("Automation Rate",       "47.5%",      "70%+",        "+22.5 pp"),
    ("Avg Cycle Time",        "29.6 days",  "≤ 20 days",   "−10 days"),
    ("Deviation Case Rate",   "33.9%",      "≤ 15%",       "−19 pp"),
]
print(f"  {'KPI':<28} {'Baseline':>12}  {'Target':>12}  {'Goal'}")
print(f"  {'-'*65}")
for kpi, baseline, target, goal in kpis:
    print(f"  {kpi:<28} {baseline:>12}  {target:>12}  {goal}")

# SENSITIVITY ANALYSIS

print(f"\n  SENSITIVITY ANALYSIS — OPP_01 (Payment & PO Blocks)")
print(f"  Varying Realization % vs. Effort (minutes)")
print(f"  {'─'*60}")

real_range   = [0.50, 0.60, 0.70, 0.80, 0.90]
effort_range = [10, 15, 20, 25]

header = f"  {'Effort':>8} |" + "".join(f" {int(r*100):>6}%" for r in real_range)
print(header)
print(f"  {'─'*55}")
for effort in effort_range:
    row_str = f"  {effort:>5} min |"
    for real in real_range:
        val = 58 * real * effort * FTE_COST_PER_MIN
        row_str += f" ${val:>6.0f}"
    print(row_str)

print(f"\n  SENSITIVITY ANALYSIS — OPP_02 (Price Deviations)")
print(f"  {'─'*60}")
header = f"  {'Effort':>8} |" + "".join(f" {int(r*100):>6}%" for r in real_range)
print(header)
print(f"  {'─'*55}")
for effort in effort_range:
    row_str = f"  {effort:>5} min |"
    for real in real_range:
        val = 110 * real * effort * FTE_COST_PER_MIN
        row_str += f" ${val:>6.0f}"
    print(row_str)

# Chart 1: Value Summary Bar
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(LIGHT)
ax.set_facecolor(LIGHT)

names  = [f"OPP_01\n{opportunities[0]['name'][:22]}...",
          f"OPP_02\n{opportunities[1]['name'][:22]}...",
          "Total"]
sample_vals     = [opportunities[0]["emv_sample"], opportunities[1]["emv_sample"], total_sample]
enterprise_vals = [opportunities[0]["emv_enterprise"]/1000, opportunities[1]["emv_enterprise"]/1000, total_enterprise/1000]

x = np.arange(len(names))
w = 0.35
b1 = ax.bar(x - w/2, sample_vals, width=w, label="Sample Dataset ($)", color=NAVY, edgecolor="white")
ax2 = ax.twinx()
b2 = ax2.bar(x + w/2, enterprise_vals, width=w, label="Enterprise Scale ($K)", color=ORANGE, alpha=0.85, edgecolor="white")

for bar, val in zip(b1, sample_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f"${val:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold", color=NAVY)
for bar, val in zip(b2, enterprise_vals):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f"${val:.0f}K", ha="center", va="bottom", fontsize=9, fontweight="bold", color=ORANGE)

ax.set_ylabel("Sample Dataset Value ($)", fontsize=10, color=NAVY)
ax2.set_ylabel("Enterprise Scale Value ($K)", fontsize=10, color=ORANGE)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=9)
ax.set_title("AP Value Framing — Framed Business Case Values\nSample Dataset vs Enterprise Scale",
             fontsize=12, fontweight="bold", color=NAVY, pad=12)
ax.spines[["top"]].set_visible(False)
ax2.spines[["top"]].set_visible(False)
lines = [plt.Rectangle((0,0),1,1,fc=NAVY), plt.Rectangle((0,0),1,1,fc=ORANGE,alpha=0.85)]
ax.legend(lines, ["Sample Dataset ($)", "Enterprise Scale ($K)"], loc="upper left", fontsize=9)
plt.tight_layout()
p1 = os.path.join(ASSETS_DIR, "value_summary.png")
plt.savefig(p1, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[CHART SAVED] {p1}")

# Chart 2: Sensitivity Heatmap
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor(LIGHT)
fig.suptitle("Sensitivity Analysis — Expected Monetary Value ($)\nVarying Effort (rows) × Realization Potential (columns)",
             fontsize=12, fontweight="bold", color=NAVY)

for idx, (opp_events, opp_name, ax) in enumerate([
    (58,  "OPP_01: Payment & PO Blocks",    axes[0]),
    (110, "OPP_02: Price Deviation Rework",  axes[1]),
]):
    matrix = [[opp_events * r * e * FTE_COST_PER_MIN for r in real_range] for e in effort_range]
    matrix = np.array(matrix)
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#FFFFFF", "#CADCFC", NAVY])
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(real_range)))
    ax.set_xticklabels([f"{int(r*100)}%" for r in real_range], fontsize=10)
    ax.set_yticks(range(len(effort_range)))
    ax.set_yticklabels([f"{e} min" for e in effort_range], fontsize=10)
    ax.set_xlabel("Realization Potential", fontsize=10)
    ax.set_ylabel("Effort per Event", fontsize=10)
    ax.set_title(opp_name, fontsize=10, fontweight="bold", color=NAVY)
    for i in range(len(effort_range)):
        for j in range(len(real_range)):
            val = matrix[i, j]
            color = "white" if val > matrix.max() * 0.6 else "#333333"
            ax.text(j, i, f"${val:.0f}", ha="center", va="center", fontsize=9,
                    fontweight="bold", color=color)

plt.tight_layout()
p2 = os.path.join(ASSETS_DIR, "sensitivity_table.png")
plt.savefig(p2, dpi=150, bbox_inches="tight")
plt.close()
print(f"[CHART SAVED] {p2}")

print("\n" + "=" * 70)
print("  VALUE CALCULATION COMPLETE")
print("=" * 70)
