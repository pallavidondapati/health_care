import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.ml.knowledge_base import MEDICAL_KNOWLEDGE

print("Loading RAG embedding model...")
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("RAG model loaded!")

# Build FAISS index at startup
def build_index():
    texts = [doc["content"] for doc in MEDICAL_KNOWLEDGE]
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    
    print(f"FAISS index built with {len(texts)} documents")
    return index

index = build_index()

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve top_k relevant medical documents for a query"""
    query_embedding = embedding_model.encode([query], convert_to_numpy=True)
    
    distances, indices = index.search(query_embedding.astype(np.float32), top_k)
    
    retrieved = []
    for i, idx in enumerate(indices[0]):
        if idx < len(MEDICAL_KNOWLEDGE):
            doc = MEDICAL_KNOWLEDGE[idx]
            retrieved.append(f"[{doc['topic'].upper()}]: {doc['content']}")
    
    return "\n\n".join(retrieved)