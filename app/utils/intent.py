# app/utils/intent.py

def detect_intent(question: str) -> str:
    q = question.lower().strip()

    # 🟢 simple rule-based intent detection (keep lightweight)
    if any(word in q for word in ["plan", "itinerary", "trip plan"]):
        return "itinerary"

    if any(word in q for word in ["list", "top", "best", "recommend"]):
        return "list"

    if any(word in q for word in ["what is", "tell me about", "explain"]):
        return "explain"

    return "default"