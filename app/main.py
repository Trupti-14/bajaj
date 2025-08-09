from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from api_models import QueryResponse
from query_engine import process_query
from document_ingestion import ingest_document
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.isdir("frontend"):
    app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.post("/process", response_model=QueryResponse)
async def process(query: str = Form(...), document: UploadFile = File(...)):
    logger.info(f"Received query: {query} with file: {document.filename}")
    try:
        suffix = f".{document.filename.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await document.read())
            tmp_path = tmp.name
        clauses = ingest_document(tmp_path)
        result = process_query(query, clauses, document.filename)
        os.remove(tmp_path)
        return result
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An error occurred while processing your request."}
        )
    