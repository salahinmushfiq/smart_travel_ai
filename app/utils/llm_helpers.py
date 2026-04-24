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


# =========================
# 🔥 STRICT LLM CALL LAYER
# =========================
def generate_answer(prompt: str) -> str:
    """
    Sends prompt to Groq LLM and returns safe response.
    """

    if not GROQ_API_KEY:
        return "Error: Missing GROQ API key."

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a STRICT retrieval-based travel assistant.\n"
                    "RULES:\n"
                    "- Use ONLY provided context.\n"
                    "- NEVER guess missing information.\n"
                    "- NEVER infer hotel prices from tour prices.\n"
                    "- If information is missing, say: "
                    "'I don't have enough information from the database.'\n"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,  # 🔥 lower temp = less hallucination
        "max_tokens": 350
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers=HEADERS,
            json=payload,
            timeout=20
        )

        # =========================
        # STATUS HANDLING FIRST
        # =========================
        if response.status_code == 401:
            return "Error: Invalid Groq API key."

        if response.status_code == 403:
            return "Error: Access denied (Groq)."

        if response.status_code == 404:
            return f"Error: Model '{GROQ_MODEL}' not found."

        if response.status_code == 429:
            return "Error: Rate limit exceeded."

        if response.status_code >= 500:
            return "Error: Groq server issue."

        data = response.json()

        # =========================
        # SAFE PARSING
        # =========================
        choices = data.get("choices", [])
        if not choices:
            return f"Error: No response from model. Raw: {data}"

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            return "Error: Empty model response."

        return content.strip()

    except requests.exceptions.Timeout:
        return "Error: Request timed out."

    except Exception as e:
        print("Groq fatal error:", e)
        return "Error: AI service failure."


# ==================================
# 🧠 IMPROVED PROMPT BUILDER (RAG)
# ==================================
def build_prompt(
    question: str,
    history: List[Dict],
    context_docs: List[Any],
    summary: str = "",
    session_info: Dict = None
) -> str:

    session_info = session_info or {}

    prompt_parts = []

    # =========================
    # 🔥 STRICT RULE BLOCK
    # =========================
    prompt_parts.append(
        "You are a STRICT retrieval-based AI travel assistant.\n\n"
        "IMPORTANT RULES:\n"
        "1. Use ONLY the provided context.\n"
        "2. Do NOT guess or hallucinate missing facts.\n"
        "3. Do NOT convert tour prices into hotel prices.\n"
        "4. If answer is missing, say:\n"
        "   'I don't have enough information from the database.'\n"
        "5. Be concise and factual.\n\n"
    )

    # =========================
    # MEMORY SUMMARY
    # =========================
    if summary:
        prompt_parts.append(f"Conversation Summary:\n{summary}\n")

    # =========================
    # SESSION INFO
    # =========================
    if session_info:
        prompt_parts.append("Session Context:")
        for k, v in session_info.items():
            prompt_parts.append(f"- {k}: {v}")
        prompt_parts.append("")

    # =========================
    # CHAT HISTORY
    # =========================
    if history:
        prompt_parts.append("Recent Conversation:")
        for msg in history:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")
        prompt_parts.append("")

    # =========================
    # RETRIEVED CONTEXT (RAG)
    # =========================
    if context_docs:
        prompt_parts.append("Relevant Context:")

        for doc in context_docs:
            # structured support (future-proof)
            if isinstance(doc, dict):
                doc_type = doc.get("type", "info")
                title = doc.get("title", "")
                content = doc.get("content", "")
                prompt_parts.append(f"[{doc_type}] {title}: {content}")
            else:
                prompt_parts.append(f"- {doc}")

        prompt_parts.append("")

    # =========================
    # USER QUESTION
    # =========================
    prompt_parts.append(f"User: {question}")
    prompt_parts.append("Assistant:")

    return "\n".join(prompt_parts)