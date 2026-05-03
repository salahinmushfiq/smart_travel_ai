# app/utils/vector_db.py

from typing import List
from app.utils.logger import logger

DOCUMENTS = []


def add_documents_to_db(documents: List[dict]):
    global DOCUMENTS

    DOCUMENTS.extend(documents)

    logger.info(f"Loaded {len(documents)} docs")


def delete_by_source(source: str):
    global DOCUMENTS

    DOCUMENTS = [
        d for d in DOCUMENTS
        if d.get("metadata", {}).get("source") != source
    ]


def query_with_scores(query: str, n_results: int = 3):
    global DOCUMENTS

    query_lower = query.lower()

    scored = []

    for doc in DOCUMENTS:
        content = doc["content"]

        score = 0

        for word in query_lower.split():
            if word in content.lower():
                score += 1

        if score > 0:
            scored.append({
                "content": content,
                "score": score
            })

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored[:n_results]