import json
import os
import re
from config import OUTPUT_JSON_DIR, POLICY

def extract_rent_from_any_text(doc_texts):
    possible_rents = []
    for text in doc_texts:
        lines = text.splitlines()
        for line in lines:
            if "rent" in line.lower() and "$" in line:
                try:
                    dollars = re.findall(r"\$?(\d{3,6}\.?\d*)", line)
                    for d in dollars:
                        val = float(d)
                        if 500 <= val <= 5000:
                            possible_rents.append(val)
                except:
                    continue
    return max(possible_rents) if possible_rents else 0

def check_first_month_rent_sdi(doc_texts):
    rent_paid = False
    sdi_paid = False
    rent_evidence = ""
    sdi_evidence = ""

    for text in doc_texts:
        if not rent_paid and ("first month" in text.lower() or "prorated rent" in text.lower()):
            rent_paid = True
            rent_evidence = text[:300]
        if not sdi_paid and ("sdi premium" in text.lower() or "$92" in text or "acct 2003" in text):
            sdi_paid = True
            sdi_evidence = text[:300]

    return rent_paid, rent_evidence, sdi_paid, sdi_evidence

def format_and_save_claim(claim_id, doc_results, charges, missing_docs, claim_row):
    approved = []
    excluded = []
    human_claimed_total = 0
    ai_approved_total = 0

    # Load text docs for rent/sdi evidence
    extracted_path = os.path.join("extracted", claim_id)
    doc_texts = []
    if os.path.exists(extracted_path):
        for file in os.listdir(extracted_path):
            if file.endswith(".txt"):
                with open(os.path.join(extracted_path, file), "r", encoding="utf-8") as f:
                    doc_texts.append(f.read())

    monthly_rent = extract_rent_from_any_text(doc_texts)
    rent_paid, rent_evidence, sdi_paid, sdi_evidence = check_first_month_rent_sdi(doc_texts)

    for item in charges:
        try:
            amt = float(item.get("amount", 0))
            human_claimed_total += amt
            if item.get("policy_covered", False):
                if item.get("category", "") == "landscaping":
                    amt = min(amt, POLICY["landscaping_limit"])
                ai_approved_total += amt
                approved.append({**item, "approved_reason": "policy-covered"})
            else:
                excluded.append({**item, "excluded_reason": "not in SDI coverage"})
        except:
            excluded.append(item)

    # Step 3: Pull spreadsheet values
    spreadsheet_claim_amount = float(claim_row.get("Amount of Claim", 0))
    spreadsheet_expected_benefit = float(claim_row.get("Benefit", 0))
    spreadsheet_approved_amount = float(claim_row.get("Approved Benefit Amount", 0))

    # Step 4: Use spreadsheet value for max benefit (fallback to rent)
    rent_based_cap = ((monthly_rent + 499) // 500) * 500 if monthly_rent else 0
    max_benefit = spreadsheet_approved_amount if spreadsheet_approved_amount else rent_based_cap
    final_payout = min(ai_approved_total, max_benefit)

    # Step 5: Decide status and assessment confidence
    has_all_required = not missing_docs and rent_paid and sdi_paid
    status = "Approved" if final_payout > 0 else "Declined"
    assessment_confidence = "Full" if has_all_required else "Partial"

    result = {
        "claim_id": claim_id,
        "status": status,
        "assessment_confidence": assessment_confidence,
        "missing_docs": missing_docs,
        "monthly_rent": monthly_rent,
        "first_month_rent_paid": rent_paid,
        "first_month_rent_evidence": rent_evidence,
        "first_month_sdi_paid": sdi_paid,
        "first_month_sdi_evidence": sdi_evidence,
        "spreadsheet_claim_amount": spreadsheet_claim_amount,
        "spreadsheet_expected_benefit": spreadsheet_expected_benefit,
        "spreadsheet_approved_amount": spreadsheet_approved_amount,
        "approved_charges": approved,
        "excluded_charges": excluded,
        "human_claimed_total": human_claimed_total,
        "ai_approved_total": ai_approved_total,
        "final_payout": final_payout
    }

    os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_JSON_DIR, f"{claim_id}.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
