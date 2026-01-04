import json
from typing import List, Dict
from app.utils.redis_client import redis_client
from app.utils.llm_helpers import generate_answer


class ChatMemory:
    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns

    # ---------- Redis Keys ----------
    def _history_key(self, session_id: str) -> str:
        return f"chat:history:{session_id}"

    def _summary_key(self, session_id: str) -> str:
        return f"chat:summary:{session_id}"

    # ---------- Public API ----------
    def add_message(self, session_id: str, role: str, content: str):
        key = self._history_key(session_id)

        message = json.dumps({
            "role": role,
            "content": content
        })

        redis_client.rpush(key, message)

        # ⬅️ summarize FIRST
        self._update_summary(session_id)

        # ⬅️ then trim
        redis_client.ltrim(key, -self.max_turns * 2, -1)

    def get_history(self, session_id: str) -> List[Dict]:
        key = self._history_key(session_id)
        raw_messages = redis_client.lrange(key, 0, -1)

        return [json.loads(m) for m in raw_messages]

    def get_summary(self, session_id: str) -> str:
        return redis_client.get(self._summary_key(session_id)) or ""

    # ---------- Internal ----------
    def _update_summary(self, session_id: str):
        key = self._history_key(session_id)
        messages = redis_client.lrange(key, 0, -1)

        if len(messages) <= self.max_turns * 2:
            return

        old_messages = messages[:-self.max_turns * 2]

        text = "\n".join(
            f"{json.loads(m)['role'].capitalize()}: {json.loads(m)['content']}"
            for m in old_messages
        )

        prompt = (
            "Summarize the following conversation briefly.\n"
            "Keep important facts, preferences, and decisions.\n"
            "Do not invent information.\n\n"
            f"{text}"
        )

        try:
            summary = generate_answer(prompt)
            redis_client.set(self._summary_key(session_id), summary[:1500])
        except Exception as e:
            print(f"Redis memory summarization failed: {e}")
