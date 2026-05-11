# app/routes/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional

from app.utils.llm_helpers import generate_answer, build_prompt
from app.memory.chat_memory import ChatMemory
from app.utils.logger import logger
from app.utils.intent import detect_intent
from app.utils.vector_db import query_with_scores
from app.utils.preferences import extract_preferences

from app.tools.tool_router import detect_tool
from app.tools.tool_executor import execute_tool


chat_memory = ChatMemory()

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: int = 3


# =====================================
# META QUESTION DETECTION
# =====================================
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


# =====================================
# MEMORY HELPER (NEW SMALL CLEANUP)
# =====================================
def save_turn(session_id: str, user_msg: str, assistant_msg: str):
    chat_memory.add_message(session_id, "user", user_msg)
    chat_memory.add_message(session_id, "assistant", assistant_msg)


# =====================================
# MAIN CHAT ENDPOINT
# =====================================
@router.post("/")
def chat_endpoint(request: ChatRequest):

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    session_id = request.session_id or str(uuid4())
    question = request.question.strip()

    intent = detect_intent(question)
    prefs = extract_preferences(question)

    tool_decision = detect_tool(question)

    logger.info(
        f"[Tool Router] mode={tool_decision['mode']} tool={tool_decision['tool']}"
    )

    try:

        # =====================================
        # TOOL PATH
        # =====================================
        if tool_decision["mode"] == "tool":

            tool_name = tool_decision["tool"]
            tool_params = tool_decision["params"]

            try:
                tool_result = execute_tool(
                    tool_name=tool_name,
                    params=tool_params
                )

            except ValueError as e:
                logger.error(f"[Tool Validation Error] {e}")
                return {
                    "status": "error",
                    "session_id": session_id,
                    "answer": str(e)
                }

            except Exception as e:
                logger.error(f"[Tool Execution Error] {e}")
                return {
                    "status": "error",
                    "session_id": session_id,
                    "answer": "Tool execution failed."
                }

            save_turn(
                session_id,
                question,
                tool_result["message"]
            )

            return {
                "status": "success",
                "session_id": session_id,
                "question": question,
                "answer": tool_result["message"],
                "retrieved_docs": [],
                "history_length": len(chat_memory.get_history(session_id)),
                "intent": f"tool:{tool_name}",
                "tool_used": tool_name,
                "tool_result": tool_result
            }

        # =====================================
        # RAG PATH
        # =====================================
        if is_meta_question(question):
            docs = []
            logger.info(f"Meta question detected | session={session_id}")
        else:
            docs = query_with_scores(question, n_results=request.top_k)

        context_texts = [
            d["content"]
            for d in docs
            if isinstance(d, dict)
        ]

        history = chat_memory.get_history(session_id)
        summary = chat_memory.get_summary(session_id)
        session_info = chat_memory.get_session_info(session_id)

        prompt = build_prompt(
            question=question,
            history=history,
            context_docs=context_texts,
            summary=summary,
            session_info=session_info,
            intent=intent
        )

        answer = generate_answer(prompt).strip()

        if not answer or len(answer) < 20:
            answer = "I don't have enough information from the database."

        save_turn(session_id, question, answer)

        if prefs:
            chat_memory.update_session_info(session_id, "interests", prefs)

        return {
            "status": "success",
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "retrieved_docs": docs,
            "history_length": len(chat_memory.get_history(session_id)),
            "intent": intent
        }

    except Exception as e:
        logger.error(f"[Chat Error]: {e}")
        return {
            "status": "error",
            "session_id": session_id,
            "answer": "System error occurred."
        }