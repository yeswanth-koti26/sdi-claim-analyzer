import os

# 🔍 Resolve BASE_DIR to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 Directory Paths
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
EXTRACTED_DIR = os.path.join(BASE_DIR, "extracted")
OUTPUT_JSON_DIR = os.path.join(BASE_DIR, "outputs", "json")
OUTPUT_EXCEL_DIR = os.path.join(BASE_DIR, "outputs", "excel")
OUTPUT_CHARTS_DIR = os.path.join(BASE_DIR, "outputs", "charts")

# 📜 SDI Policy Rules
POLICY = {
    "landscaping_limit": 500,
    "approved_categories": [
        "unpaid rent",
        "lease break fee",
        "utilities",
        "cleaning",
        "rekey",
        "landscaping"
    ]
}

# 📑 Required Document Types
REQUIRED_DOC_TYPES = [
    "tenant_ledger",
    "lease_addendum",
    "lease_agreement",
    "notification_to_tenant"
]
