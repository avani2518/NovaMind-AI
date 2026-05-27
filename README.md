## Context-Aware FAQ API

Semantic FAQ generation and question-answering API using RAG.

### How it works
1. POST /ingest/pdf  → upload your docs
2. POST /ask        → ask any question
3. Get a grounded answer + source reference

### Stack
FastAPI · ChromaDB · sentence-transformers (SBERT) · LLaMA 3 via Groq