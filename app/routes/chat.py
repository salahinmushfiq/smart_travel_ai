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

# 🆕 TOOLING
from app.tools.tool_router import detect_tool
from app.tools.registry import TOOLS

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
# MAIN CHAT ENDPOINT
# =====================================
@router.post("/")
def chat_endpoint(request: ChatRequest):

    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    session_id = request.session_id or str(uuid4())

    question = request.question.strip()

    # =====================================
    # INTENT + PREFERENCES
    # =====================================
    intent = detect_intent(question)

    prefs = extract_preferences(question)

    # =====================================
    # TOOL ROUTING
    # =====================================
    tool_decision = detect_tool(question)

    logger.info(
        f"[Tool Router] "
        f"mode={tool_decision['mode']} "
        f"tool={tool_decision['tool']}"
    )

    try:

        # =====================================
        # TOOL EXECUTION PATH
        # =====================================
        if tool_decision["mode"] == "tool":

            tool_name = tool_decision["tool"]

            tool_params = tool_decision["params"]

            tool_data = TOOLS.get(tool_name)

            if not tool_data:
                raise HTTPException(
                    status_code=500,
                    detail=f"Tool '{tool_name}' not registered."
                )

            tool_function = tool_data["function"]

            # 🧠 EXECUTE TOOL
            tool_result = tool_function(**tool_params)

            # 💾 MEMORY
            chat_memory.add_message(
                session_id,
                "user",
                question
            )

            chat_memory.add_message(
                session_id,
                "assistant",
                str(tool_result)
            )

            logger.info(
                f"[Tool Executed] "
                f"tool={tool_name}"
            )

            return {
                "status": "success",
                "session_id": session_id,
                "question": question,

                # frontend compatibility
                "answer": str(tool_result),

                "retrieved_docs": [],

                "history_length": len(
                    chat_memory.get_history(session_id)
                ),

                "intent": f"tool:{tool_name}",

                # 🆕 structured tool metadata
                "tool_used": tool_name,
                "tool_result": tool_result
            }

        # =====================================
        # RAG PATH
        # =====================================
        if is_meta_question(question):

            docs = []

            logger.info(
                f"Meta question detected "
                f"| session={session_id}"
            )

        else:

            docs = query_with_scores(
                question,
                n_results=request.top_k
            )

        if not docs:
            logger.warning(
                f"No context found "
                f"| session={session_id}"
            )

        # =====================================
        # MEMORY
        # =====================================
        history = chat_memory.get_history(session_id)

        summary = chat_memory.get_summary(session_id)

        session_info = chat_memory.get_session_info(session_id)

        context_texts = [
            d["content"]
            for d in docs
            if isinstance(d, dict)
        ]

        # =====================================
        # PROMPT BUILDING
        # =====================================
        prompt = build_prompt(
            question=question,
            history=history,
            context_docs=context_texts,
            summary=summary,
            session_info=session_info,
            intent=intent
        )

        # =====================================
        # LLM GENERATION
        # =====================================
        answer = generate_answer(prompt).strip()

        # =====================================
        # SAFETY FALLBACK
        # =====================================
        if not answer or len(answer.strip()) < 20:

            answer = (
                "I don't have enough information "
                "from the database."
            )

        # =====================================
        # MEMORY STORAGE
        # =====================================
        chat_memory.add_message(
            session_id,
            "user",
            question
        )

        chat_memory.add_message(
            session_id,
            "assistant",
            answer
        )

        if prefs:
            chat_memory.update_session_info(
                session_id,
                "interests",
                prefs
            )

        logger.info(
            f"Chat success "
            f"| session={session_id}"
        )

        return {
            "status": "success",
            "session_id": session_id,
            "question": question,
            "answer": answer,
            "retrieved_docs": docs,
            "history_length": len(
                chat_memory.get_history(session_id)
            ),
            "intent": intent
        }

    except Exception as e:

        logger.error(f"[Chat Error]: {e}")

        return {
            "status": "error",
            "session_id": session_id,
            "answer": "System error occurred."
        }