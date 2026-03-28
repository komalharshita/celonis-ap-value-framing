import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

DATA_DIR   = "data"
ASSETS_DIR = "assets"
CASES_FILE = os.path.join(DATA_DIR, "P2P-Cases.csv")
ACTS_FILE  = os.path.join(DATA_DIR, "P2P-Activities.csv")

NAVY  = "#1E2761"
BLUE  = "#2196F3"
ORANGE = "#FF6B35"
GRAY  = "#888888"
LIGHT = "#F5F7FA"

os.makedirs(ASSETS_DIR, exist_ok=True)

print("=" * 60)
print("  P2P DATA PROFILING REPORT")
print("  Celonis × AICTE BA Internship Portfolio Project")
print("=" * 60)

cases = pd.read_csv(CASES_FILE)
acts  = pd.read_csv(ACTS_FILE, sep=";")
acts["EVENTTIME"] = pd.to_datetime(acts["EVENTTIME"])

print("\n[1] DATASET OVERVIEW")
print("-" * 40)
print(f"  Cases file   : {CASES_FILE}")
print(f"  Activities   : {ACTS_FILE}")
print(f"  Total cases  : {len(cases):,}")
print(f"  Total events : {len(acts):,}")
print(f"  Date range   : {acts['EVENTTIME'].min().date()} → {acts['EVENTTIME'].max().date()}")

print("\n[2] P2P-CASES.CSV SCHEMA")
print("-" * 40)
for col in cases.columns:
    null_pct = cases[col].isna().mean() * 100
    unique   = cases[col].nunique()
    print(f"  {col:<25} dtype={str(cases[col].dtype):<12} nulls={null_pct:.1f}%  unique={unique}")

print("\n[3] P2P-ACTIVITIES.CSV SCHEMA")
print("-" * 40)
for col in acts.columns:
    null_pct = acts[col].isna().mean() * 100
    unique   = acts[col].nunique()
    print(f"  {col:<25} dtype={str(acts[col].dtype):<12} nulls={null_pct:.1f}%  unique={unique}")


print("\n[4] SPEND SUMMARY (P2P-Cases)")
print("-" * 40)
print(f"  Total procurement spend : €{cases['Net Order Price'].sum():>12,.2f}")
print(f"  Average order value     : €{cases['Net Order Price'].mean():>12,.2f}")
print(f"  Median order value      : €{cases['Net Order Price'].median():>12,.2f}")
print(f"  Max order value         : €{cases['Net Order Price'].max():>12,.2f}")
print(f"  Min order value         : €{cases['Net Order Price'].min():>12,.2f}")
print(f"  Unique vendors          : {cases['Vendor'].nunique()}")
print(f"  Currencies              : {cases['Currency'].dropna().unique().tolist()}")

print("\n  Top 5 Vendors by Spend:")
top_v = cases.groupby("Vendor")["Net Order Price"].sum().sort_values(ascending=False).head(5)
for vendor, spend in top_v.items():
    pct = spend / cases["Net Order Price"].sum() * 100
    print(f"    {vendor:<20} €{spend:>10,.2f}  ({pct:.1f}%)")

print("\n  Top 5 Material Groups by Spend:")
top_m = cases.groupby("Material Group Text")["Net Order Price"].sum().sort_values(ascending=False).head(5)
for mg, spend in top_m.items():
    pct = spend / cases["Net Order Price"].sum() * 100
    print(f"    {mg:<25} €{spend:>10,.2f}  ({pct:.1f}%)")

HAPPY_PATH = {
    "Create Purchase Requisition Item",
    "Create Purchase Order Item",
    "Send Purchase Order",
    "Record Goods Receipt",
    "Record Invoice Receipt",
    "Clear Invoice",
}
DEVIATION_ACTS = {
    "Change Price", "Block Purchase Order Item", "Set Payment Block",
    "Remove Payment Block", "Change Currency", "Delete Purchase Order Item",
    "Change Quantity", "Cancel Goods Receipt", "Refuse Purchase Order",
    "Dun Order Confirmation", "Send Purchase Order Update",
}

print("\n[5] ACTIVITY DISTRIBUTION")
print("-" * 40)
act_counts = acts["ACTIVITY_EN"].value_counts()
for act, cnt in act_counts.items():
    pct  = cnt / len(acts) * 100
    tag  = " ✓ HAPPY" if act in HAPPY_PATH else (" ⚠ DEVIATION" if act in DEVIATION_ACTS else "")
    print(f"  {act:<40} {cnt:>5}  ({pct:.1f}%){tag}")

print("\n[6] USER TYPE (AUTOMATION PROFILE)")
print("-" * 40)
ut = acts["User Type"].value_counts()
total = len(acts)
for utype, cnt in ut.items():
    label = "Automated (Batch)" if utype == "B" else "Manual (Human)"
    print(f"  Type {utype} — {label:<22} {cnt:>5} events  ({cnt/total*100:.1f}%)")

print("\n[7] CYCLE TIME ANALYSIS (per case)")
print("-" * 40)
ct = acts.groupby("_CASE_KEY")["EVENTTIME"].agg(["min", "max"])
ct["days"] = (ct["max"] - ct["min"]).dt.days
print(f"  Average cycle time  : {ct['days'].mean():.1f} days")
print(f"  Median cycle time   : {ct['days'].median():.1f} days")
print(f"  P25 cycle time      : {ct['days'].quantile(0.25):.1f} days")
print(f"  P75 cycle time      : {ct['days'].quantile(0.75):.1f} days")
print(f"  P95 cycle time      : {ct['days'].quantile(0.95):.1f} days")
print(f"  Max cycle time      : {ct['days'].max()} days  ← investigate these outliers")
print(f"  Cases ≤ 30 days     : {(ct['days'] <= 30).sum()} ({(ct['days'] <= 30).mean()*100:.1f}%)")
print(f"  Cases > 60 days     : {(ct['days'] > 60).sum()} ({(ct['days'] > 60).mean()*100:.1f}%)")

act_df = act_counts.reset_index()
act_df.columns = ["Activity", "Count"]

def get_color(act):
    if act in HAPPY_PATH:
        return NAVY
    if act in DEVIATION_ACTS:
        return ORANGE
    return GRAY

act_df["color"] = act_df["Activity"].apply(get_color)
act_df = act_df.sort_values("Count")

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(LIGHT)
ax.set_facecolor(LIGHT)

bars = ax.barh(act_df["Activity"], act_df["Count"], color=act_df["color"], height=0.7, edgecolor="white", linewidth=0.5)
for bar, cnt in zip(bars, act_df["Count"]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
            str(cnt), va="center", ha="left", fontsize=10, color="#333333", fontweight="bold")

ax.set_xlabel("Number of Events", fontsize=12, color="#333333")
ax.set_title("P2P Activity Distribution\nAll 4,927 Events — Purchase-to-Pay Dataset",
             fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", labelsize=10)
ax.set_xlim(0, act_df["Count"].max() * 1.15)
ax.grid(axis="x", linestyle="--", alpha=0.4, color=GRAY)

legend_patches = [
    mpatches.Patch(color=NAVY,   label="Happy Path (Value-Adding)"),
    mpatches.Patch(color=ORANGE, label="Deviation (Rework / Block)"),
    mpatches.Patch(color=GRAY,   label="Other"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=10, framealpha=0.8)

plt.tight_layout()
chart1_path = os.path.join(ASSETS_DIR, "activity_distribution.png")
plt.savefig(chart1_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[CHART SAVED] {chart1_path}")

top8 = cases.groupby("Material Group Text")["Net Order Price"].sum().sort_values(ascending=False).head(8)

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(LIGHT)
ax.set_facecolor(LIGHT)

colors = [NAVY if i == 0 else BLUE if i < 3 else "#CADCFC" for i in range(len(top8))]
bars = ax.bar(range(len(top8)), top8.values, color=colors, width=0.65, edgecolor="white", linewidth=0.8)

for i, (bar, val) in enumerate(zip(bars, top8.values)):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 800,
            f"€{val:,.0f}", ha="center", va="bottom", fontsize=9, color="#333333", fontweight="bold")

ax.set_xticks(range(len(top8)))
ax.set_xticklabels(top8.index, rotation=30, ha="right", fontsize=10)
ax.set_ylabel("Total Net Order Value (€)", fontsize=11, color="#333333")
ax.set_title("Procurement Spend by Material Group\nTop 8 Categories — P2P Dataset",
             fontsize=14, fontweight="bold", color=NAVY, pad=15)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4, color=GRAY)

plt.tight_layout()
chart2_path = os.path.join(ASSETS_DIR, "spend_by_material.png")
plt.savefig(chart2_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"[CHART SAVED] {chart2_path}")

print("\n" + "=" * 60)
print("  PROFILING COMPLETE")
print("=" * 60)