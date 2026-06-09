from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.neuro_san_client import chat_with_faq_agent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    chat_context: Optional[dict] = None


class ChatResponse(BaseModel):
    answer: str
    session_id: Optional[str] = None
    chat_context: Optional[dict] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Accepts a user message and returns an answer from the Neuro-SAN FAQ agent.
    Passes chat_context back and forth to maintain multi-turn conversation state.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        result = await chat_with_faq_agent(
            user_message=request.message,
            chat_context=request.chat_context
        )
        return ChatResponse(
            answer=result["answer"],
            session_id=request.session_id,
            chat_context=result["chat_context"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Agent service error: {str(e)}"
        )