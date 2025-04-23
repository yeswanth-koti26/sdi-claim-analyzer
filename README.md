
```markdown
# SDI Claim Analyzer

This is a full-stack AI-powered application designed to automate the evaluation of Security Deposit Insurance (SDI) claims. It extracts content from uploaded documents, applies SDI policy rules, evaluates charges, and generates a comprehensive Excel summary with payout decisions.

## What This Project Does

- Extracts text from PDFs, DOCX, and image files using OCR.
- Classifies documents using GPT-4 into categories like tenant ledger, lease agreement, etc.
- Uses GPT-4 to extract financial charges and determine if they are covered by SDI policy.
- Calculates both human-claimed and AI-approved amounts.
- Determines the final payout amount based on policy rules.
- Generates outputs in JSON, Excel, and bar chart formats.
- Displays claim analysis through a frontend React UI.

## Tech Stack

- **Frontend**: React.js
- **Backend**: FastAPI (Python)
- **AI/LLM**: OpenAI GPT-4
- **OCR**: Tesseract, PyMuPDF, pdf2image
- **Output Formats**: JSON, Excel, PNG charts
- **Libraries**: pandas, openpyxl, python-docx, matplotlib

## Folder Structure

```
sdi_claim_analyzer/
│
├── backend/
│   ├── main.py                # FastAPI app entrypoint
│   ├── config.py              # Directories and SDI policy rules
│   ├── routes/claims.py       # API route
│   └── services/              # Core logic (parser, analyzer, formatter)
│
├── frontend/                  # React drag-drop file upload + result viewer
├── documents/                 # Uploaded raw files (by claim ID)
├── extracted/                 # Extracted text from documents
├── outputs/
│   ├── json/                  # Final claim JSONs
│   ├── excel/                 # Final Excel report
│   └── charts/                # Accuracy comparison bar graphs
```

## Workflow

1. User uploads documents and enters Claim ID via frontend.
2. FastAPI backend saves the files and extracts text using OCR if needed.
3. GPT-4 classifies document types and extracts charges with SDI policy tagging.
4. Charges are approved or rejected based on SDI coverage logic.
5. Final output is saved in:
   - JSON (for UI)
   - Excel (for managers)
   - Charts (for visual AI-vs-human comparison)
6. React frontend displays Claim ID, AI Approved, Human Claimed, Final Payout, and Accuracy.

## Sample Output Fields

- Claim ID: 216  
- Status: Approved  
- Monthly Rent: $1650  
- Human Claimed: $7826.78  
- AI Approved: $5760.49  
- Final Payout: $3000  
- Accuracy: 76.2%  
- Missing Documents: tenant ledger, lease agreement  

## Key Highlights

- Real-world insurance use case with document automation
- Fully integrated GPT + OCR pipeline
- Clean, production-style React + FastAPI architecture
- Generates JSON, Excel, and visual analytics
- No database required – works entirely with file uploads and analysis


```

