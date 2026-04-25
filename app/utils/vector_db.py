# app/utils/vector_db.py
import chromadb
from app.utils.embeddings import embed_documents
from typing import List
from app.utils.logger import logger

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="travel_docs")


# =========================
# ADD DOCUMENTS
# =========================
def add_documents_to_db(documents: List[dict]):
    try:
        existing = collection.get()
        existing_ids = set(existing.get("ids", []))

        new_docs = [doc for doc in documents if doc["id"] not in existing_ids]

        if not new_docs:
            logger.info("No new documents to add.")
            return

        texts = [doc["content"] for doc in new_docs]
        ids = [doc["id"] for doc in new_docs]

        embeddings = embed_documents(texts).cpu().detach().numpy()

        metadatas = []
        for doc in new_docs:
            meta = doc.get("metadata", {})
            meta["source"] = meta.get("source", "unknown")
            metadatas.append(meta)

        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

        logger.info(f"Added {len(new_docs)} docs to ChromaDB")

    except Exception as e:
        logger.error(f"[VectorDB Add Error]: {e}")


# =========================
# DELETE BY SOURCE
# =========================
def delete_by_source(source: str):
    try:
        results = collection.get()
        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])

        delete_ids = [
            ids[i] for i, meta in enumerate(metadatas)
            if meta and meta.get("source") == source
        ]

        if delete_ids:
            collection.delete(ids=delete_ids)
            logger.info(f"Deleted {len(delete_ids)} docs (source={source})")

    except Exception as e:
        logger.error(f"[VectorDB Delete Error]: {e}")


# =========================
# QUALITY FILTER
# =========================
def filter_low_quality_docs(docs: List[str]) -> List[str]:
    filtered = []

    for doc in docs:
        if not doc:
            continue

        text = doc.lower().strip()

        if len(text) < 80:
            continue

        if any(x in text for x in ["lorem", "null", "undefined", "error"]):
            continue

        filtered.append(doc)

    return filtered


# =========================
# MAIN QUERY (USED BY CHAT)
# =========================
# def query_similar_docs(query: str, n_results: int = 3) -> List[str]:
#     try:
#         query_embedding = embed_documents([query]).cpu().detach().numpy()
#
#         results = collection.query(
#             query_embeddings=query_embedding,
#             n_results=n_results,
#             include=["distances", "documents"]
#         )
#
#         docs = results.get("documents", [[]])[0]
#         distances = results.get("distances", [[]])[0]
#
#         return filter_low_quality_docs(docs)
#
#     except Exception as e:
#         logger.error(f"[VectorDB Query Error]: {e}")
#         return []


# =========================
# OPTIONAL SCORED VERSION
# =========================
def query_with_scores(query: str, n_results: int = 3):
    try:
        query_embedding = embed_documents([query]).cpu().detach().numpy()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["distances", "documents"]
        )

        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        return [
            {
                "content": doc,
                "score": round(1 - dist, 4)  # similarity score
            }
            for doc, dist in zip(docs, distances)
        ]

    except Exception as e:
        logger.error(f"[VectorDB Score Query Error]: {e}")
        return []