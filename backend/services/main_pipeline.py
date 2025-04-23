import pandas as pd
import json
import os
from services.document_parser import parse_documents_for_claim
from services.analyzer import analyze_claim
from services.claim_formatter import format_and_save_claim
from config import BASE_DIR  # ✅ Import base directory

def run_full_pipeline(claim_id: str):
    print(f"🚀 Triggered full pipeline for claim {claim_id}")

    # ✅ Use absolute path to avoid file not found errors
    spreadsheet_path = os.path.join(BASE_DIR, "Security Deposit Claims (1).xlsx")
    if not os.path.exists(spreadsheet_path):
        print("❌ Spreadsheet not found.")
        return {"error": "Spreadsheet not found."}

    claim_data = pd.read_excel(spreadsheet_path)
    claim_data = claim_data.set_index("Tracking Number")

    if int(claim_id) not in claim_data.index:
        print(f"❌ Claim ID {claim_id} not found in spreadsheet.")
        return {"error": f"Claim ID {claim_id} not found in spreadsheet."}

    claim_row = claim_data.loc[int(claim_id)]

    # ⬇️ Log pipeline progress
    print("📄 Parsing uploaded documents...")
    parse_documents_for_claim(claim_id)

    print("📊 Analyzing parsed documents...")
    doc_results, charges, missing_docs = analyze_claim(claim_id)

    print("📁 Formatting results and saving to outputs...")
    format_and_save_claim(claim_id, doc_results, charges, missing_docs, claim_row)

    # ✅ Load result from output JSON
    json_path = os.path.join(BASE_DIR, "outputs", "json", f"{claim_id}.json")
    if not os.path.exists(json_path):
        print("❌ Output JSON not found.")
        return {"error": "Output not generated."}

    print(f"✅ Analysis complete for claim {claim_id}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
