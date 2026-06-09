"""
Wraps the Neuro-SAN HTTP streaming API into a simple async function.
"""
import asyncio
import json
import httpx
from typing import Optional


NEURO_SAN_BASE_URL = "http://localhost:8080"


async def chat_with_faq_agent(
    user_message: str,
    chat_context: Optional[dict] = None
) -> dict:
    """
    Sends a message to the Neuro-SAN faq_agent and collects the streamed response.
    
    Returns:
        { "answer": str, "chat_context": dict }
    """
    payload = {
        "user_message": {
            "text": user_message
        }
    }

    # Include conversation context for multi-turn support
    if chat_context:
        payload["user_message"]["chat_context"] = chat_context

    url = f"{NEURO_SAN_BASE_URL}/api/v1/faq_agent/streaming_chat"
    answer_text = ""
    returned_context = {}

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    msg = data.get("response", {})
                    # Collect final AI answer
                    if msg.get("type") == "AGENT_FRAMEWORK":
                        answer_text = msg.get("text", "")
                        returned_context = msg.get("chat_context", {})
                except json.JSONDecodeError:
                    continue

    return {
        "answer": answer_text,
        "chat_context": returned_context
    }