# app/routes/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
import json
from uuid import uuid4
from typing import Optional
from app.utils.vector_db import add_documents_to_db, query_similar_docs
from app.utils.llm_helpers import generate_answer, build_prompt
from app.memory.chat_memory import ChatMemory

# In-memory chat session manager
# (Later replaceable with Redis / DB)
chat_memory = ChatMemory()

router = APIRouter(prefix="/chat", tags=["chat"])


# Request body
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None  # Enables conversation continuation
    top_k: int = 3  # Number of relevant documents to retrieve


# ---- Load Knowledge Base Once ----
# Travel documents are loaded only at startup
with open("app/data/travel_docs.json", "r", encoding="utf-8") as f:
    travel_docs = json.load(f)

# Store documents in vector DB (Chroma)
add_documents_to_db(travel_docs)


@router.post("/")
def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint.

    Responsibilities:
    - Maintain session-based conversation memory
    - Retrieve relevant documents (RAG)
    - Build prompt
    - Call LLM
    - Store conversation history
    """

    # If frontend does not provide a session_id, create one
    session_id = request.session_id or str(uuid4())
    user_question = request.question

    # Fetch conversation history for this session
    history = chat_memory.get_history(session_id)

    try:
        # ---- Vector Search (Retrieval) ----
        top_docs = query_similar_docs(user_question, n_results=request.top_k)

        # Fetch conversation history
        history = chat_memory.get_history(session_id)

        # Fetch summary of older turns
        summary = chat_memory.get_summary(session_id)
        # ---- Prompt Construction ----
        prompt = build_prompt(
            question=user_question,
            history=history,
            context_docs=top_docs,
            summary=summary
        )

        # ---- LLM Call ----
        answer = generate_answer(prompt)

        # ---- Persist Conversation Memory ----
        chat_memory.add_message(session_id, "user", user_question)
        chat_memory.add_message(session_id, "assistant", answer)

        return {
            "status": "success",
            "session_id": session_id,
            "question": user_question,
            "answer": answer,
            "retrieved_docs": top_docs,
            "history_length": len(chat_memory.get_history(session_id))
        }

    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return {
            "status": "error",
            "session_id": session_id,
            "answer": "Sorry, something went wrong."
        }


@router.get("/history/{session_id}")
def get_history(session_id: str):
    """
    Returns the full conversation history for a given session_id
    """
    history = chat_memory.get_history(session_id)
    return {
        "status": "success",
        "session_id": session_id,
        "history": history
    }
