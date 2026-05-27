from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Security
)

from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from pydantic import BaseModel
from dotenv import load_dotenv

from app.ingest import ingest_document, extract_text_from_pdf
from app.search import semantic_search
from app.generate import generate_answer
from app.dashboard import generate_dashboard

import os
import threading
import time
import webbrowser


# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()


# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------

app = FastAPI(
    title="NovaMind AI",
    version="1.0.0",
    description="AI Powered RAG Application"
)


# ---------------------------------------------------
# Auto Open Browser
# ---------------------------------------------------

browser_opened = False


@app.on_event("startup")
async def startup_event():

    global browser_opened

    if not browser_opened:

        browser_opened = True

        def open_browser():

            time.sleep(1.5)

            webbrowser.open_new(
                "http://127.0.0.1:8000/frontend/index.html"
            )

        threading.Thread(
            target=open_browser,
            daemon=True
        ).start()


# ---------------------------------------------------
# CORS Configuration
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Serve Frontend
# ---------------------------------------------------

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# ---------------------------------------------------
# API Key Authentication
# ---------------------------------------------------

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

VALID_KEYS = set(
    key.strip()
    for key in os.getenv(
        "VALID_API_KEYS",
        ""
    ).split(",")
    if key.strip()
)


def verify_api_key(
    api_key: str = Security(API_KEY_HEADER)
):

    if api_key not in VALID_KEYS:

        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )

    return api_key


# ---------------------------------------------------
# Request Models
# ---------------------------------------------------

class QueryRequest(BaseModel):

    question: str
    collection_name: str = "faq_kb"
    top_k: int = 3


class IngestTextRequest(BaseModel):

    text: str
    doc_name: str
    collection_name: str = "faq_kb"


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------

@app.get("/")
def home():

    return RedirectResponse(
        url="/frontend/index.html"
    )


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ---------------------------------------------------
# Ingest Text Endpoint
# ---------------------------------------------------

@app.post(
    "/ingest/text",
    dependencies=[Security(verify_api_key)]
)

def ingest_text(req: IngestTextRequest):

    try:

        result = ingest_document(
            req.text,
            req.doc_name,
            req.collection_name
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------
# Ingest PDF Endpoint
# ---------------------------------------------------

@app.post(
    "/ingest/pdf",
    dependencies=[Security(verify_api_key)]
)

async def ingest_pdf(
    file: UploadFile = File(...),
    collection_name: str = "faq_kb"
):

    try:

        if not file.filename.endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        contents = await file.read()

        text = extract_text_from_pdf(contents)

        result = ingest_document(
            text,
            file.filename,
            collection_name
        )

        return {
            "status": "success",
            "filename": file.filename,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ---------------------------------------------------
# Ask AI Endpoint
# ---------------------------------------------------

@app.post(
    "/ask",
    dependencies=[Security(verify_api_key)]
)

def ask_question(req: QueryRequest):

    try:

        chunks = semantic_search(
            req.question,
            req.collection_name,
            req.top_k
        )

        if not chunks:

            raise HTTPException(
                status_code=404,
                detail="No relevant content found"
            )

        answer = generate_answer(
            req.question,
            chunks
        )

        return {
            "status": "success",
            "question": req.question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/dashboard")
def dashboard():

    chunks = semantic_search(
        "summarize document",
        "faq_kb",
        8
    )

    data = generate_dashboard(
        chunks
    )

    return data


# ---------------------------------------------------
# Startup Message
# ---------------------------------------------------

print("\n")
print("======================================")
print("NovaMind AI Server Running")
print("Frontend:")
print("http://127.0.0.1:8000/frontend/index.html")
print("======================================")
print("\n")