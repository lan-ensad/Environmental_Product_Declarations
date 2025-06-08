import os
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path
from tqdm import tqdm

pdf_dir = Path("docs")
output_dir = Path("ocr_output")
output_dir.mkdir(exist_ok=True)

def ocr_pdf(pdf_path, output_txt_path):
    images = convert_from_path(pdf_path, dpi=300)
    text = ""
    print(f"OCRing {pdf_path.name} ({len(images)} pages)")
    for img in tqdm(images, desc=f"OCR {pdf_path.stem}", unit="page"):
        text += pytesseract.image_to_string(img, lang='fra')
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(text)

for pdf_file in pdf_dir.glob("*.pdf"):
    output_txt = output_dir / f"{pdf_file.stem}.txt"
    
    if output_txt.exists():
        print(f"Already exist : {pdf_file.name} -> ignore")
        continue

    ocr_pdf(pdf_file, output_txt)
    print(f"OCR done : {output_txt.name}")
