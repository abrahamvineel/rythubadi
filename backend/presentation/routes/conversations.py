from fastapi import APIRouter, Depends
from uuid import UUID, uuid4
from bootstrap import build_services
from domain.chat_session import ChatSession
from domain.chat_message import ChatMessage
from presentation.dependencies.auth import get_current_user_id
from presentation.schemas.create_conversation_request import CreateConversationRequest
from presentation.schemas.create_message_request import CreateMessageRequest

router = APIRouter()

@router.post("/conversations", status_code=201)
def create_conversation(request: CreateConversationRequest,
                        user_id: str = Depends(get_current_user_id)):
    repo = build_services().postgres_conversation_repo
    session = ChatSession(id=uuid4(), title=request.title, producer_id=user_id)
    repo.create(session)
    return {"id": str(session.id), "title": session.title}

@router.get("/conversations")
def get_conversations(user_id: str = Depends(get_current_user_id)):
    repo = build_services().postgres_conversation_repo
    sessions = repo.find_all_by_user(user_id)
    return [{"id": str(s.id), "title": s.title} for s in sessions]

@router.delete("/conversations/{session_id}", status_code=204)
def delete_conversation(session_id: UUID,
                        user_id: str = Depends(get_current_user_id)):
    repo = build_services().postgres_conversation_repo
    repo.delete(session_id, user_id)

@router.get("/conversations/{session_id}/messages")
def get_messages(session_id: UUID,
                 user_id: str = Depends(get_current_user_id)):
    repo = build_services().postgres_conversation_repo
    messages = repo.find_messages_by_session(session_id)
    return [{"content": m.content, "system_generated": m.system_generated,
             "attachment_url": m.attachment_url, "language": m.language} for m in messages]

@router.post("/conversations/{session_id}/messages", status_code=201)
def save_message(session_id: UUID,
                 request: CreateMessageRequest,
                 user_id: str = Depends(get_current_user_id)):
    repo = build_services().postgres_conversation_repo
    message = ChatMessage(chat_session_id=session_id, content=request.content,
                          attachment_url=request.attachment_url,
                          system_generated=request.system_generated,
                          language=request.language)
    repo.save_message(message)
    return {"chat_session_id": str(session_id), "content": request.content,
            "system_generated": request.system_generated}
