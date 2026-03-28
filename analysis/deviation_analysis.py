import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Config ──────────────────────────────────────────────────────────────────
DATA_DIR   = "data"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

NAVY   = "#1E2761"
BLUE   = "#2196F3"
ORANGE = "#FF6B35"
RED    = "#D32F2F"
GREEN  = "#388E3C"
GRAY   = "#888888"
LIGHT  = "#F5F7FA"

# ── Activity Classification ──────────────────────────────────────────────────
HAPPY_PATH = [
    "Create Purchase Requisition Item",
    "Create Purchase Order Item",
    "Send Purchase Order",
    "Record Goods Receipt",
    "Record Invoice Receipt",
    "Clear Invoice",
]

DEVIATION_MAP = {
    "Change Price"               : ("Rework",     "High",   10),
    "Block Purchase Order Item"  : ("Block",       "High",   15),
    "Set Payment Block"          : ("Block",       "High",   15),
    "Remove Payment Block"       : ("Resolution",  "Medium",  5),
    "Change Currency"            : ("Rework",      "Medium",  8),
    "Delete Purchase Order Item" : ("Waste",       "Medium",  5),
    "Change Quantity"            : ("Rework",      "Medium",  8),
    "Cancel Goods Receipt"       : ("Rework",      "Medium", 10),
    "Refuse Purchase Order"      : ("Rejection",   "Low",    10),
    "Dun Order Confirmation"     : ("Follow-up",   "Low",     5),
    "Send Purchase Order Update" : ("Rework",      "Low",     5),
}
DEVIATION_ACTS = set(DEVIATION_MAP.keys())

# ── Load Data ────────────────────────────────────────────────────────────────
print("=" * 60)
print("  P2P DEVIATION ANALYSIS")
print("  AP Value Framing Business Case")
print("=" * 60)

cases = pd.read_csv(os.path.join(DATA_DIR, "P2P-Cases.csv"))
acts  = pd.read_csv(os.path.join(DATA_DIR, "P2P-Activities.csv"), sep=";")
acts["EVENTTIME"] = pd.to_datetime(acts["EVENTTIME"])

total_cases  = acts["_CASE_KEY"].nunique()
total_events = len(acts)

# ── 1. Case Classification ───────────────────────────────────────────────────
print("\n[1] CASE CLASSIFICATION (Happy Path vs Deviant)")
print("-" * 40)

dev_case_ids = set(acts[acts["ACTIVITY_EN"].isin(DEVIATION_ACTS)]["_CASE_KEY"])
acts["is_deviation"] = acts["ACTIVITY_EN"].isin(DEVIATION_ACTS)
case_flags = acts.groupby("_CASE_KEY")["is_deviation"].any().reset_index()
case_flags.columns = ["_CASE_KEY", "has_deviation"]
case_flags["classification"] = case_flags["has_deviation"].map({True: "Deviant", False: "Happy Path"})

happy_n  = (~case_flags["has_deviation"]).sum()
deviant_n = case_flags["has_deviation"].sum()

print(f"  Total cases        : {total_cases:,}")
print(f"  Happy Path cases   : {happy_n:,}  ({happy_n/total_cases*100:.1f}%)")
print(f"  Deviant cases      : {deviant_n:,}  ({deviant_n/total_cases*100:.1f}%)")

# Enrich with case attributes and cycle time
ct = acts.groupby("_CASE_KEY")["EVENTTIME"].agg(["min", "max"])
ct["cycle_days"] = (ct["max"] - ct["min"]).dt.days
ct = ct.reset_index()[["_CASE_KEY", "cycle_days"]]

case_enriched = cases.merge(case_flags, on="_CASE_KEY", how="left").merge(ct, on="_CASE_KEY", how="left")
case_enriched["deviation_event_count"] = case_enriched["_CASE_KEY"].map(
    acts[acts["is_deviation"]].groupby("_CASE_KEY").size()
).fillna(0).astype(int)

print(f"\n  Avg cycle time (Happy Path) : {case_enriched[~case_enriched['has_deviation']]['cycle_days'].mean():.1f} days")
print(f"  Avg cycle time (Deviant)    : {case_enriched[case_enriched['has_deviation']]['cycle_days'].mean():.1f} days")
print(f"  Cycle time delta            : {case_enriched[case_enriched['has_deviation']]['cycle_days'].mean() - case_enriched[~case_enriched['has_deviation']]['cycle_days'].mean():.1f} days longer for deviant cases")

output_cases = os.path.join(DATA_DIR, "case_classification.csv")
case_enriched.to_csv(output_cases, index=False)
print(f"\n  [SAVED] {output_cases}")

# ── 2. Deviation Event Summary ───────────────────────────────────────────────
print("\n[2] DEVIATION EVENT BREAKDOWN")
print("-" * 40)

dev_events = acts[acts["ACTIVITY_EN"].isin(DEVIATION_ACTS)].copy()
dev_summary = dev_events["ACTIVITY_EN"].value_counts().reset_index()
dev_summary.columns = ["Activity", "Event_Count"]
dev_summary["Category"]       = dev_summary["Activity"].map(lambda x: DEVIATION_MAP.get(x, ("Other","Low",0))[0])
dev_summary["Impact"]         = dev_summary["Activity"].map(lambda x: DEVIATION_MAP.get(x, ("Other","Low",0))[1])
dev_summary["Effort_Min"]     = dev_summary["Activity"].map(lambda x: DEVIATION_MAP.get(x, ("Other","Low",0))[2])
dev_summary["Pct_of_Dev"]     = dev_summary["Event_Count"] / dev_summary["Event_Count"].sum()
dev_summary["Cumulative_Pct"] = dev_summary["Pct_of_Dev"].cumsum()
dev_summary["FTE_Cost_Min"]   = 90000 / (250 * 8 * 60)
dev_summary["Value_at_Stake"] = dev_summary["Event_Count"] * dev_summary["Effort_Min"] * dev_summary["FTE_Cost_Min"]

total_dev = dev_summary["Event_Count"].sum()
print(f"  Total deviation events : {total_dev}")
print(f"  Deviation rate         : {total_dev/total_events*100:.1f}% of all events\n")

for _, row in dev_summary.iterrows():
    print(f"  {row['Activity']:<40} {row['Event_Count']:>4} events  "
          f"({row['Pct_of_Dev']*100:.1f}%)  [{row['Category']:<12}] Impact={row['Impact']}")

output_acts = os.path.join(DATA_DIR, "activity_summary.csv")
dev_summary.to_csv(output_acts, index=False)
print(f"\n  [SAVED] {output_acts}")

# ── 3. User Type per Deviation ───────────────────────────────────────────────
print("\n[3] AUTOMATION PROFILE")
print("-" * 40)
ut = acts["User Type"].value_counts()
for utype, cnt in ut.items():
    label = "Automated (Batch)" if utype == "B" else "Manual (Human)"
    print(f"  {label:<25}: {cnt:>5} events ({cnt/total_events*100:.1f}%)")

print(f"\n  Manual deviation events : {dev_events[dev_events['User Type']=='A'].shape[0]}")
print(f"  Auto  deviation events  : {dev_events[dev_events['User Type']=='B'].shape[0]}")

# ── 4. Vendor-Level Root Cause ───────────────────────────────────────────────
print("\n[4] VENDOR ROOT CAUSE ANALYSIS")
print("-" * 40)

vendor_acts = dev_events.merge(cases[["_CASE_KEY", "Vendor", "Net Order Price"]], on="_CASE_KEY", how="left")
vendor_dev  = vendor_acts.groupby("Vendor").agg(
    Dev_Events=("ACTIVITY_EN", "count"),
    Affected_Cases=("_CASE_KEY", "nunique"),
).reset_index()
vendor_spend = cases.groupby("Vendor")["Net Order Price"].sum().reset_index()
vendor_full  = vendor_spend.merge(vendor_dev, on="Vendor", how="left").fillna(0)
vendor_full["Dev_Events"]      = vendor_full["Dev_Events"].astype(int)
vendor_full["Affected_Cases"]  = vendor_full["Affected_Cases"].astype(int)
vendor_full["Spend_Pct"]       = vendor_full["Net Order Price"] / vendor_full["Net Order Price"].sum()
vendor_full["Risk"] = vendor_full["Dev_Events"].apply(
    lambda x: "HIGH" if x >= 30 else ("MEDIUM" if x >= 10 else "LOW")
)
vendor_full = vendor_full.sort_values("Dev_Events", ascending=False)

print(f"  {'Vendor':<20} {'Spend (€)':>12} {'Spend %':>8} {'Dev Events':>10} {'Risk':>8}")
print(f"  {'-'*64}")
for _, r in vendor_full.head(10).iterrows():
    print(f"  {r['Vendor']:<20} €{r['Net Order Price']:>10,.0f} {r['Spend_Pct']*100:>7.1f}% "
          f"{r['Dev_Events']:>10} {r['Risk']:>8}")

print(f"\n  Change Price by vendor (top 5):")
cp = vendor_acts[vendor_acts["ACTIVITY_EN"] == "Change Price"].groupby("Vendor").size().sort_values(ascending=False).head(5)
for vendor, cnt in cp.items():
    print(f"    {vendor:<20} {cnt} Change Price events")

# ── 5. Chart: Deviation Pareto ───────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(LIGHT)
ax1.set_facecolor(LIGHT)

colors = []
for act in dev_summary["Activity"]:
    cat = DEVIATION_MAP.get(act, ("Other","Low",0))[0]
    if cat == "Block":           colors.append(RED)
    elif cat in ("Rework","Waste"): colors.append(ORANGE)
    else:                        colors.append(GRAY)

bars = ax1.bar(dev_summary["Activity"], dev_summary["Event_Count"],
               color=colors, width=0.6, edgecolor="white", linewidth=0.8)
ax1.set_ylabel("Event Count", fontsize=11, color=NAVY)
ax1.set_xlabel("")
ax1.tick_params(axis="x", rotation=35, labelsize=9)
ax1.spines[["top", "right"]].set_visible(False)

for bar, cnt in zip(bars, dev_summary["Event_Count"]):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
             str(cnt), ha="center", va="bottom", fontsize=9, fontweight="bold", color="#333333")

ax2 = ax1.twinx()
ax2.plot(dev_summary["Activity"], dev_summary["Cumulative_Pct"] * 100,
         color=NAVY, marker="o", linewidth=2, markersize=6, label="Cumulative %")
ax2.axhline(80, color=NAVY, linestyle="--", alpha=0.5, linewidth=1)
ax2.text(len(dev_summary) - 1, 81, "80% line", fontsize=9, color=NAVY, ha="right")
ax2.set_ylabel("Cumulative % of Deviations", fontsize=11, color=NAVY)
ax2.set_ylim(0, 110)
ax2.spines[["top"]].set_visible(False)

patches = [
    mpatches.Patch(color=RED,    label="Block Events"),
    mpatches.Patch(color=ORANGE, label="Rework / Waste"),
    mpatches.Patch(color=GRAY,   label="Other"),
]
ax1.legend(handles=patches, loc="upper right", fontsize=9)
plt.title("Deviation Pareto Analysis\nP2P Event Log — Identifying Top Improvement Opportunities",
          fontsize=13, fontweight="bold", color=NAVY, pad=12)
plt.tight_layout()
p1 = os.path.join(ASSETS_DIR, "deviation_pareto.png")
plt.savefig(p1, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[CHART SAVED] {p1}")

# ── 6. Chart: Vendor Risk Matrix ─────────────────────────────────────────────
vp = vendor_full[vendor_full["Net Order Price"] > 0].copy()
risk_colors = {"HIGH": RED, "MEDIUM": ORANGE, "LOW": GREEN}

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(LIGHT)
ax.set_facecolor(LIGHT)

for _, r in vp.iterrows():
    size = max(r["Affected_Cases"] * 8, 80)
    ax.scatter(r["Net Order Price"], r["Dev_Events"],
               s=size, color=risk_colors[r["Risk"]], alpha=0.75, edgecolors="white", linewidth=1.5)
    if r["Dev_Events"] > 5 or r["Net Order Price"] > 5000:
        ax.annotate(r["Vendor"], (r["Net Order Price"], r["Dev_Events"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8, color="#333333")

ax.set_xlabel("Total Procurement Spend (€)", fontsize=11, color=NAVY)
ax.set_ylabel("Total Deviation Events", fontsize=11, color=NAVY)
ax.set_title("Vendor Risk Matrix\nSpend Concentration vs. Process Deviation Frequency",
             fontsize=13, fontweight="bold", color=NAVY, pad=12)
ax.spines[["top", "right"]].set_visible(False)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"€{x/1000:.0f}K"))
ax.grid(linestyle="--", alpha=0.3, color=GRAY)

med_spend = vp["Net Order Price"].median()
med_dev   = vp["Dev_Events"].median()
ax.axvline(med_spend, color=GRAY, linestyle=":", alpha=0.6)
ax.axhline(med_dev,   color=GRAY, linestyle=":", alpha=0.6)
ax.text(med_spend * 1.02, ax.get_ylim()[1] * 0.97, "Median Spend", fontsize=8, color=GRAY)

legend_patches = [
    mpatches.Patch(color=RED,    label="HIGH Risk (30+ deviation events)"),
    mpatches.Patch(color=ORANGE, label="MEDIUM Risk (10–29 events)"),
    mpatches.Patch(color=GREEN,  label="LOW Risk (<10 events)"),
]
ax.legend(handles=legend_patches, fontsize=9, loc="upper right")
plt.tight_layout()
p2 = os.path.join(ASSETS_DIR, "vendor_risk_matrix.png")
plt.savefig(p2, dpi=150, bbox_inches="tight")
plt.close()
print(f"[CHART SAVED] {p2}")

print("\n" + "=" * 60)
print("  DEVIATION ANALYSIS COMPLETE")
print(f"  Outputs saved to: {DATA_DIR}/ and {ASSETS_DIR}/")
print("=" * 60)