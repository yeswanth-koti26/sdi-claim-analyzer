import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from config import OUTPUT_JSON_DIR, OUTPUT_EXCEL_DIR, OUTPUT_CHARTS_DIR

def build_final_output():
    data = []

    for fname in os.listdir(OUTPUT_JSON_DIR):
        with open(os.path.join(OUTPUT_JSON_DIR, fname), "r", encoding="utf-8") as f:
            claim = json.load(f)

        ai_total = claim.get("ai_approved_total", 0)
        human_total = claim.get("human_claimed_total", 0)
        payout = claim.get("final_payout", 0)

        # ✅ Accuracy: AI vs Human
        if human_total:
            accuracy = round((ai_total / human_total) * 100, 2)
        else:
            accuracy = 0.0

        # ✅ Summary
        if claim.get("assessment_confidence") == "Partial":
            summary = "Partially Evaluated due to missing docs. Payout based on available charges."
        elif claim["status"] == "Declined":
            summary = "Declined due to unpaid rent/SDI or missing information."
        else:
            summary = f"Approved. Final payout = ${payout} (policy-capped)."

        data.append({
            "Claim ID": claim["claim_id"],
            "Status": claim["status"],
            "Assessment Confidence": claim.get("assessment_confidence", "Unknown"),
            "Missing Documents": ", ".join(claim.get("missing_docs", [])),
            "First Month Paid": "Yes" if claim.get("first_month_rent_paid") else "No",
            "First Month SDI Paid": "Yes" if claim.get("first_month_sdi_paid") else "No",
            "Human Claimed": human_total,
            "AI Approved": ai_total,
            "Final Payout": payout,
            "AI vs Human Accuracy %": accuracy,
            "Summary of Decision": summary
        })

    # ✅ Save Excel file
    df = pd.DataFrame(data)
    os.makedirs(OUTPUT_EXCEL_DIR, exist_ok=True)
    df.to_excel(os.path.join(OUTPUT_EXCEL_DIR, "final_results.xlsx"), index=False)

    # ✅ Bar chart: Human Claimed vs AI Approved
    df = df.sort_values("Claim ID")
    x = range(len(df))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.bar([i - bar_width/2 for i in x], df["Human Claimed"], width=bar_width, label="Human Claimed", color="steelblue")
    ax.bar([i + bar_width/2 for i in x], df["AI Approved"], width=bar_width, label="AI Approved", color="orange")

    for i, acc in enumerate(df["AI vs Human Accuracy %"]):
        color = "green" if acc >= 70 else "red"
        ax.text(i, df["AI Approved"].iloc[i] + 150, f"{acc}%", ha="center", color=color, fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["Claim ID"], rotation=45)
    ax.set_ylabel("Amount ($)")
    ax.set_title("Human Claimed vs AI Approved + Accuracy (%)")
    ax.legend()
    plt.tight_layout()

    os.makedirs(OUTPUT_CHARTS_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_CHARTS_DIR, "batch_accuracy_chart.png"))
    plt.close()
