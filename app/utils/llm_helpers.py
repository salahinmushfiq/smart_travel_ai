# apps/utils/llm_helpers.py
import ollama
from typing import List


def generate_answer(prompt: str, model_name: str = "llama3.1:8b") -> str:
    """
    Sends the final prompt to Ollama LLM and returns the response.

    Responsibility:
    - ONLY communicates with the LLM
    - Does NOT build prompt (single responsibility principle)
    """

    try:
        # Ollama expects messages in chat format
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        # Defensive handling for different Ollama response formats
        if hasattr(response, "message") and response.message:
            return response.message.content

        return "No answer returned by the model."

    except Exception as e:
        print(f"Ollama error: {e}")
        return "Sorry, AI failed to generate a response."


def build_prompt(question: str, history: list, context_docs: list, summary: str = ""):
    """
    Builds a SINGLE, token-efficient prompt for the LLM.

    - Injects old conversation summary (if available)
    - Injects recent conversation
    - Adds retrieved documents
    """
    prompt = "You are a helpful travel assistant.\n\n"

    # ---- Conversation summary ----
    if summary:
        prompt += f"Conversation summary:\n{summary}\n\n"

    # ---- Recent conversation ----
    if history:
        prompt += "Recent conversation:\n"
        for msg in history:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

    # ---- Retrieved Knowledge Context ----
    if context_docs:
        prompt += "\nRelevant Information:\n"
        for doc in context_docs:
            prompt += f"- {doc}\n"

    # ---- Current User Query ----
    prompt += f"\nUser: {question}\nAssistant:"

    return prompt
