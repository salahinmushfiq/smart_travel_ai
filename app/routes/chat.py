from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json

from app.utils.vector_db import add_documents_to_db, query_similar_docs
from app.utils.llm_helpers import generate_answer

router = APIRouter(prefix="/chat", tags=["chat"])

# Request body
class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


# Load sample travel documents once
with open("app/data/travel_docs.json", "r", encoding="utf-8") as f:
    travel_docs = json.load(f)

# Add docs to ChromaDB (first time or on restart)
add_documents_to_db(travel_docs)


@router.post("/", response_model=dict)
def chat_endpoint(request: ChatRequest):
    """
    Query LLM using top-k documents retrieved from ChromaDB.
    """
    user_question = request.question
    top_docs: List[str] = query_similar_docs(user_question, n_results=request.top_k)

    if not top_docs:
        return {
            "question": user_question,
            "retrieved_docs": [],
            "context": "",
            "answer": "No relevant documents found."
        }

    context = "\n".join(top_docs)
    answer = generate_answer(context, user_question)

    return {
        "question": user_question,
        "retrieved_docs": top_docs,
        "context": context,
        "answer": answer
    }
