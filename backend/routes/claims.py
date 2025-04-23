# routes/claims.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from services.main_pipeline import run_full_pipeline
from services.utils import save_uploaded_files

router = APIRouter()

@router.post("/analyze")
async def analyze_claim(claim_id: str = Form(...), files: List[UploadFile] = File(...)):
    try:
        save_uploaded_files(files, claim_id)
        result = run_full_pipeline(claim_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
