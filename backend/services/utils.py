import os
import shutil
from werkzeug.utils import secure_filename
from config import DOCUMENTS_DIR

def create_claim_folder(claim_id):
    claim_folder = os.path.join(DOCUMENTS_DIR, str(claim_id))
    if os.path.exists(claim_folder):
        shutil.rmtree(claim_folder)
    os.makedirs(claim_folder, exist_ok=True)
    return claim_folder

def save_uploaded_files(files, claim_id):
    folder = create_claim_folder(claim_id)
    for upload in files:
        filename = secure_filename(upload.filename)
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(upload.file, f)
