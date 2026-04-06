from domain.human_loop.confirmable_action import ConfirmableAction
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from typing import Optional

@dataclass(frozen=True)
class HumanConfirmation:
    confirmation_id: UUID
    action: ConfirmableAction
    producer_id: UUID
    summary: str      
    consequences: str 
    expires_at: datetime 
    confirmed_at: Optional[datetime] = None
    biometric_required: bool = False

    def is_confirmed(self) -> bool:
        return self.confirmed_at is not None
    
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at
    