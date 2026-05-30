from fastapi import APIRouter, Depends
from presentation.dependencies.auth import get_current_user_id
from bootstrap import build_services
from uuid import UUID

router = APIRouter()


def _serialise(event) -> dict:
    return {
        "id":           str(event.id),
        "severity":     event.severity,
        "agent":        event.agent,
        "agent_emoji":  event.agent_emoji,
        "title":        event.title,
        "body":         event.body,
        "subject_type": event.subject_type,
        "subject_id":   event.subject_id,
        "subject_name": event.subject_name,
        "location_id":  str(event.location_id) if event.location_id else None,
        "reply_count":  event.reply_count,
        "created_at":   event.created_at.isoformat(),
    }


@router.get("/feed")
def get_feed(user_id: UUID = Depends(get_current_user_id)):
    events = build_services().feed_event_repo.find_by_producer(user_id)
    return [_serialise(e) for e in events]
