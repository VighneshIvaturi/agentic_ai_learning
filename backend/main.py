import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from app.llm_service import (
    analyze_prescription_image,
    analyze_prescription_text
)
from app.document_service import (
    convert_pdf_to_images,
    extract_text_from_docx,
    extract_images_from_docx
)
from fastapi.middleware.cors import CORSMiddleware

import logging
app = FastAPI(
    title="PrescriptionBot API",
    description="AI-powered prescription image and PDF analyzer",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/prescriptionbot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
UPLOAD_DIR = "uploads"
PDF_PAGES_DIR = "pdf_pages"
MAX_PDF_PAGES = 10
MAX_FILE_SIZE_MB = 20
DOCX_IMAGES_DIR = "docx_images"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_PAGES_DIR, exist_ok=True)
os.makedirs(DOCX_IMAGES_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "PrescriptionBot API is running"}
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PrescriptionBot API"
    }


@app.post("/analyze-prescription")
async def analyze_prescription(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    allowed_extensions = ["jpg", "jpeg", "png", "pdf", "docx"]
    file_extension = file.filename.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG, JPEG, PNG, PDF, or DOCX file."
        )

    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    
    content = await file.read()

    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400,detail=f"File size exceeds {MAX_FILE_SIZE_MB} MB limit.")

    with open(file_path, "wb") as buffer:
        buffer.write(content)
    logger.info(
    f"File uploaded: {file.filename} | Type: {file_extension}")

    if file_extension == "pdf":
        pdf_output_dir = os.path.join(
            PDF_PAGES_DIR,
            unique_filename.replace(".pdf", "")
        )

        try:
            image_paths = convert_pdf_to_images(file_path, pdf_output_dir)

            original_total_pages = len(image_paths)
            logger.info(f"PDF detected with {original_total_pages} pages")
            page_limit_applied = False

            if len(image_paths) > MAX_PDF_PAGES:
                image_paths = image_paths[:MAX_PDF_PAGES]
                page_limit_applied = True

            page_analyses = []

            for index, image_path in enumerate(image_paths, start=1):
                result = analyze_prescription_image(image_path)

                if "error" in result:
                    logger.error(f"PDF analysis failed: {file.filename} | Page: {index} | Error: {result['error']}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to analyze page {index}"
                    )

                page_analyses.append({
                    "page_number": index,
                    "analysis": result
                })
            logger.info(f"PDF analysis completed: {file.filename} | Pages analyzed: {len(page_analyses)}")

            return {
                "filename": file.filename,
                "file_type": "pdf",
                "total_pages_in_pdf": original_total_pages,
                "pages_analyzed": len(page_analyses),
                "page_limit_applied": page_limit_applied,
                "message": (
                    f"Only first {MAX_PDF_PAGES} pages were analyzed."
                    if page_limit_applied
                    else "All pages were analyzed."
                ),
                "analyses": page_analyses
            }

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

            if os.path.exists(pdf_output_dir):
                shutil.rmtree(pdf_output_dir)
    if file_extension == "docx":
        docx_output_dir = os.path.join(
        DOCX_IMAGES_DIR,
        unique_filename.replace(".docx", ""))

        try:
            logger.info(f"DOCX file detected: {file.filename}")

            extracted_text = extract_text_from_docx(file_path)
            image_paths = extract_images_from_docx(file_path, docx_output_dir)

            text_analysis = None
            image_analyses = []

            if extracted_text:
                text_analysis = analyze_prescription_text(extracted_text)

                if "error" in text_analysis:
                    logger.error(
                    f"DOCX text analysis failed: {file.filename} | Error: {text_analysis['error']}")
                    raise HTTPException(status_code=500,detail="Failed to analyze DOCX text")

            for index, image_path in enumerate(image_paths, start=1):
                result = analyze_prescription_image(image_path)

                if "error" in result:
                    logger.error(f"DOCX image analysis failed: {file.filename} | Image: {index} | Error: {result['error']}")
                    raise HTTPException(status_code=500,detail=f"Failed to analyze DOCX image {index}")

                image_analyses.append({"image_number": index,"analysis": result})

            logger.info(f"DOCX analysis completed: {file.filename} | Text found: {bool(extracted_text)} | Images analyzed: {len(image_analyses)}")

            return {
            "filename": file.filename,
            "file_type": "docx",
            "text_found": bool(extracted_text),
            "embedded_images_found": len(image_paths),
            "text_analysis": text_analysis,
            "image_analyses": image_analyses}

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

            if os.path.exists(docx_output_dir):
                shutil.rmtree(docx_output_dir)

    try:
        result = analyze_prescription_image(file_path)

        if "error" in result:
            logger.error(f"Image analysis failed: {file.filename} | Error: {result['error']}")
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        logger.info(f"Image analysis completed: {file.filename}")

        return {
            "filename": file.filename,
            "file_type": "image",
            "analysis": result
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)