from fastapi import APIRouter
from pydantic import BaseModel
import json
from app.utils.embeddings import embed_documents, get_most_similar
from app.utils.vector_db import add_documents_to_db, query_similar_docs

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str


# Load sample travel documents once
with open("app/data/travel_docs.json", "r", encoding="utf-8") as f:
    travel_docs = json.load(f)

# Add documents to ChromaDB (only first time or restart)
add_documents_to_db(travel_docs)


@router.post("/")
def chat_endpoint(request: ChatRequest):
    user_question = request.question
    top_docs = query_similar_docs(user_question, n_results=3)
    context = "\n".join(top_docs)
    return {"context": context}
