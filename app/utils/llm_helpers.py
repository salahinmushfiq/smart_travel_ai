import ollama
from typing import List


def generate_answer(context: str, question: str, model_name: str = "llama3.1:8b") -> str:
    """
    Generate an answer using Ollama local LLM.
    Ensures compatibility with multiple Ollama response formats.
    """
    prompt = f"""
You are a helpful travel assistant AI.
Answer the user's question using ONLY the following context.
Do not make up information.

CONTEXT:
{context}

USER QUESTION:
{question}

Answer:
"""

    try:
        response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])

        # Check Ollama response object
        if hasattr(response, "message") and response.message:
            return response.message.content
        elif hasattr(response, "result") and response.result:
            return response.result[0].get("content", "")

        return "No answer returned by the model."

    except Exception as e:
        return f"Error generating answer: {str(e)}"
