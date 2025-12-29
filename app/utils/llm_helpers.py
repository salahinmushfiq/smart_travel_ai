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


def build_prompt(question: str, history: list, context_docs: list):
    """
    Builds a SINGLE, consistent prompt for the LLM.

    Why this function exists:
    - Centralizes prompt logic (important for maintainability)
    - Ensures conversation history is preserved
    - Prevents prompt duplication across routes
    """

    # System-level instruction to control LLM behavior
    prompt = "You are a helpful travel assistant.\n\n"

    # ---- Conversation Memory Injection ----
    # Past user/assistant messages are injected here
    # This is what enables multi-turn conversation continuity
    if history:
        prompt += "Conversation so far:\n"
        for msg in history:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

    # ---- Retrieved Knowledge Context ----
    # Documents retrieved from vector DB are added here
    # This grounds the LLM response in factual data (RAG)
    if context_docs:
        prompt += "\nRelevant Information:\n"
        for doc in context_docs:
            prompt += f"- {doc}\n"

    # ---- Current User Query ----
    prompt += f"\nUser: {question}\nAssistant:"

    return prompt
