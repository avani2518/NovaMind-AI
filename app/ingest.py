# app/ingest.py

from sentence_transformers import SentenceTransformer
import chromadb
import uuid
import PyPDF2          # ← add this
import io              # ← add this

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vector_store")

# ── PDF text extractor ──────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    return " ".join(page.extract_text() for page in reader.pages if page.extract_text())

# ── Chunking ────────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# ── Ingestion ───────────────────────────────────────────────
def ingest_document(text: str, doc_name: str, collection_name: str = "faq_kb"):
    collection = client.get_or_create_collection(collection_name)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": doc_name, "chunk_index": i} for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
    return {"chunks_stored": len(chunks)}