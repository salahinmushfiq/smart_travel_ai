# app/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional

from app.utils.vector_db import query_similar_docs
from app.utils.llm_helpers import generate_answer, build_prompt
from app.memory.chat_memory import ChatMemory
from app.utils.logger import logger

chat_memory = ChatMemory()
router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: int = 3


def is_meta_question(question: str) -> bool:
    q = question.lower()

    triggers = [
        "what did i ask",
        "what did i just ask",
        "repeat my question",
        "what was my last question",
        "what did i say",
    ]

    return any(t in q for t in triggers)


@router.post("/")
def chat_endpoint(request: ChatRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    session_id = request.session_id or str(uuid4())
    question = request.question.strip()

    try:
        # 🔍 Retrieval
        # =========================
        # 🧠 INTENT ROUTING
        # =========================
        if is_meta_question(question):
            docs = []  # ❌ disable RAG for meta questions
            logger.info(f"Meta question detected | session={session_id}")
        else:
            docs = query_similar_docs(question, n_results=request.top_k)

        if not docs:
            logger.warning(f"No context found | session={session_id}")

        # 🧠 Memory
        history = chat_memory.get_history(session_id)
        summary = chat_memory.get_summary(session_id)
        session_info = chat_memory.get_session_info(session_id)

        # 🧩 Prompt
        prompt = build_prompt(
            question=question,
            history=history,
            context_docs=docs,
            summary=summary,
            session_info=session_info
        )

        # ⚡ LLM
        answer = generate_answer(prompt).strip()

        # 🛑 Safety
        if len(answer) < 10 or "error" in answer.lower():
            answer = "I don't have enough information from the database."

        # 💾 Memory
        chat_memory.add_message(session_id, "user", question)
        chat_memory.add_message(session_id, "assistant", answer)

        logger.info(f"Chat success | session={session_id}")

        return {
            "status": "success",
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "retrieved_docs": docs,
            "history_length": len(chat_memory.get_history(session_id))
        }

    except Exception as e:
        logger.error(f"[Chat Error]: {e}")

        return {
            "status": "error",
            "session_id": session_id,
            "answer": "System error occurred."
        }
