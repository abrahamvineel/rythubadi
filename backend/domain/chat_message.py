from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass(frozen=True)
class ChatMessage:
    chat_session_id: UUID
    content: str
    attachment_url: Optional[str]
    system_generated: bool
    language: str = "EN"
