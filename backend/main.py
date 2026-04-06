from fastapi import FastAPI, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
import os
import hashlib
import io
import docx
import PyPDF2

# Import individual modules (Framework Pipelines)
from modules.text_processing import process_text
from modules.statistical_computation import compute_statistics
from modules.output_generator import generate_text_report, generate_word_report

app = FastAPI(title="Sentence Profiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage for reports cache mapped by text hash
report_cache = {}

@app.post("/api/profile")
async def profile_text(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Main API Pipeline Entry Point.
    """
    content = ""
    if file:
        file_bytes = await file.read()
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            content = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif filename.endswith(".docx") or filename.endswith(".doc"):
            try:
                doc = docx.Document(io.BytesIO(file_bytes))
                content = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            except Exception as e:
                return {"status": "error", "message": f"Could not read Word document: {str(e)}"}
        else:
            content = file_bytes.decode("utf-8", errors="replace")
    elif text:
        content = text
        
    if not content.strip():
        return {"status": "error", "message": "No text provided for analysis."}

    try:
        # Step 2: Processing Pipeline
        text_data = process_text(content)
        
        # Steps 3 to 7: Statistical & Linguistic Computations
        stats = compute_statistics(text_data)
        
        # Cache results for Step 5 (Output Generation download links)
        cache_id = hashlib.md5(content.encode()).hexdigest()
        report_cache[cache_id] = stats
        
        return {
            "status": "success",
            "message": "Analysis completed successfully.",
            "stats": stats,
            "cache_id": cache_id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/download/txt/{cache_id}")
def download_txt(cache_id: str):
    if cache_id in report_cache:
        report = generate_text_report(report_cache[cache_id])
        return PlainTextResponse(
            report, 
            headers={"Content-Disposition": "attachment; filename=profiler_report.txt"}
        )
    return {"error": "Report not found or expired from cache."}

@app.get("/api/download/docx/{cache_id}")
def download_docx(cache_id: str):
    if cache_id in report_cache:
        stream = generate_word_report(report_cache[cache_id])
        return StreamingResponse(
            stream, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=profiler_report.docx"}
        )
    return {"error": "Report not found or expired from cache."}

# Mount frontend files properly
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    print(f"Warning: Frontend not found at {frontend_dir}")
