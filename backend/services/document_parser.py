import os
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from docx import Document
from PIL import Image, ImageFilter
from config import DOCUMENTS_DIR, EXTRACTED_DIR

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\kotiy\poppler-24.08.0\Library\bin"

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text if text.strip() else extract_text_via_ocr(path)

def extract_text_via_ocr(pdf_path):
    print(f"OCR (PDF/Image Scan): {os.path.basename(pdf_path)}")
    ocr_text = ""
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as tempdir:
        images = convert_from_path(pdf_path, dpi=300, output_folder=tempdir, poppler_path=POPPLER_PATH)
        for image in images:
            try:
                image = image.convert("L")
                image = image.point(lambda x: 0 if x < 180 else 255, '1')
                image = image.rotate(0, expand=True)
                custom_config = r'--psm 6 --oem 3'
                text = pytesseract.image_to_string(image, config=custom_config)
                ocr_text += text
            finally:
                image.close()
    return ocr_text

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else extract_text_via_ocr(path)
    except:
        return extract_text_via_ocr(path)

def extract_text_from_image(image_path):
    print(f"OCR (Image): {os.path.basename(image_path)}")
    image = Image.open(image_path).convert("L").filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def parse_documents_for_claim(claim_id):
    claim_folder = os.path.join(DOCUMENTS_DIR, claim_id)
    output_folder = os.path.join(EXTRACTED_DIR, claim_id)
    os.makedirs(output_folder, exist_ok=True)
    print(f"📄 Processing files for Claim ID: {claim_id}")
    for filename in os.listdir(claim_folder):
        print(f"📂 Reading: {filename}")
        input_path = os.path.join(claim_folder, filename)
        text = ""
        try:
            if filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(input_path)
            elif filename.lower().endswith(".docx"):
                text = extract_text_from_docx(input_path)
            elif filename.lower().endswith((".jpg", ".jpeg", ".png")):
                text = extract_text_from_image(input_path)
            else:
                continue
            with open(os.path.join(output_folder, filename + ".txt"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"❌ Error parsing {filename}: {e}")