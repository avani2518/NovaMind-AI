from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vector_store")

def semantic_search(query: str, collection_name: str = "faq_kb", top_k: int = 3):
    collection = client.get_or_create_collection(collection_name)
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return [
        {
            "chunk": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "relevance_score": 1 - results["distances"][0][i]
        }
        for i in range(len(results["documents"][0]))
    ]