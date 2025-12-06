# app/utils/vector_db.py
import chromadb
from app.utils.embeddings import embed_documents

# Initialize Chroma client (new API)
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection(name="travel_docs")


def add_documents_to_db(documents: list):
    texts = [doc["content"] for doc in documents]
    ids = [doc["id"] for doc in documents]
    embeddings = embed_documents(texts).cpu().detach().numpy()
    collection.add(
        documents=texts,
        metadatas=[{"id": doc_id} for doc_id in ids],
        ids=ids,
        embeddings=embeddings
    )
    print(f"Added {len(documents)} docs to ChromaDB")


def query_similar_docs(query: str, n_results: int = 3):
    query_embedding = embed_documents([query]).cpu().detach().numpy()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results["documents"][0]
