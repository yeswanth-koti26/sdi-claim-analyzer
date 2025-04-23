import os
from config import EXTRACTED_DIR, REQUIRED_DOC_TYPES
from services.gpt_utils import classify_document_fulltext, extract_charges_fulltext


def analyze_claim(claim_id):
    folder = os.path.join(EXTRACTED_DIR, claim_id)
    doc_results = {}
    charges = []
    missing_required = set(REQUIRED_DOC_TYPES)

    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
            text = f.read()
        doc_type = classify_document_fulltext(text)
        print(f"[{claim_id}] {filename} → Classified as: {doc_type}")
        doc_results[filename] = doc_type

        if doc_type in REQUIRED_DOC_TYPES:
            missing_required.discard(doc_type)

        if doc_type in ["invoice", "move_out_statement", "tenant_ledger", "claim_evaluation_report"]:
            extracted = extract_charges_fulltext(text)
            if isinstance(extracted, list) and extracted:
                charges.extend(extracted)

    return doc_results, charges, list(missing_required)
