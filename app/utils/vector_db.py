import chromadb
from app.utils.embeddings import embed_documents
from typing import List

# Initialize Chroma persistent client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="travel_docs")


def add_documents_to_db(documents: List[dict]):
    """
    Add a list of dicts with keys 'id' and 'content' to Chroma.
    """
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


def query_similar_docs(query: str, n_results: int = 3) -> List[str]:
    """
    Return top-n similar documents from Chroma for a user query.
    """
    query_embedding = embed_documents([query]).cpu().detach().numpy()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)

    # Always return a list of strings
    docs: List[str] = results.get("documents", [[]])[0]
    return docs
