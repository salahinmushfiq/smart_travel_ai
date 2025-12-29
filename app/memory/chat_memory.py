# app/memory/chat_memory.py

from collections import defaultdict
from typing import List, Dict


class ChatMemory:
    def __init__(self, max_turns: int = 6):
        self.sessions: Dict[str, List[Dict]] = defaultdict(list)
        self.max_turns = max_turns

    def add_message(self, session_id: str, role: str, content: str):
        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

        # keep only last N turns (user+assistant)
        self.sessions[session_id] = self.sessions[session_id][-self.max_turns * 2:]

    def get_history(self, session_id: str) -> List[Dict]:
        return self.sessions.get(session_id, [])
