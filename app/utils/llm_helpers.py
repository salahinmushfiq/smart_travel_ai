# app/utils/llm_helpers.py
import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def generate_answer(prompt: str) -> str:

    if not GROQ_API_KEY:
        return "Error: Missing GROQ API key."

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a STRICT retrieval-based travel assistant.\n"
                    "Use ONLY provided context.\n"
                    "Do NOT guess missing information.\n"
                    "If missing, say: 'I don't have enough information from the database.'"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 350
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=HEADERS,
            json=payload,
            timeout=20
        )

        if response.status_code >= 400:
            return f"Error: API failure ({response.status_code})"

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("LLM error:", e)
        return "Error: AI service failure."


def build_prompt(
    question: str,
    history: List[Dict],
    context_docs: List[Any],
    summary: str = "",
    session_info: Dict = None,
    intent: str = "default"
) -> str:

    session_info = session_info or {}

    prompt = []

    # =========================
    # 🔥 SYSTEM RULES
    # =========================
    prompt.append(
        "You are a STRICT retrieval-based travel assistant.\n"
        "Use ONLY provided context.\n"
        "Do NOT guess missing information.\n"
        "If missing, say: 'I don't have enough information from the database.'\n"
    )
    # =========================
    # 🎯 INTENT CONTROL LAYER
    # =========================
    prompt.append(
        f"""Intent: {intent}

    FORMAT RULES:
    - If intent = itinerary → structured day-wise plan
    - If intent = list → bullet points only
    - If intent = explain → clear paragraph explanation
    - If intent = default → concise helpful answer
    """
    )
    prompt.append(
        "IMPORTANT:\n"
        "- If the user asks about previous conversation, use chat history.\n"
        "- Do NOT rely on external context for meta questions.\n"
        "- Questions like 'What did I just ask?' MUST be answered from history.\n\n"
    )

    # =========================
    # 🧠 SUMMARY
    # =========================
    if summary:
        prompt.append(f"Summary:\n{summary}\n")

    # =========================
    # 🧠 HISTORY
    # =========================
    if history:
        prompt.append("History:")
        for h in history:
            prompt.append(f"{h['role']}: {h['content']}")
        prompt.append("")

    # =========================
    # 📚 CONTEXT (RAG)
    # =========================
    if context_docs:
        prompt.append("Context:")
        for d in context_docs:
            prompt.append(f"- {d}")
        prompt.append("")

    # =========================
    # ❓ USER QUESTION
    # =========================
    prompt.append(f"User: {question}")
    prompt.append("Assistant:")

    return "\n".join(prompt)