from shared.schemas.chat import ChatRequest, ChatResponse
from shared.config import settings
from fastapi import APIRouter
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=ChatResponse) 
async def generate_chat_response(request: ChatRequest) -> ChatResponse:
    """
    Generate a chat response based on the provided request.

    Args:
        request (ChatRequest): The chat request containing the input message.

    Returns:
        ChatResponse: The generated chat response.
    """
    # Placeholder for the actual chat generation logic
    # In a real implementation, you would call your chat model or service here
    generated_response = f"Echo: {request.message}"

    logger.info(f"Received request: {request}")
    logger.info(f"Uoooh: {settings.rag_service_url}")

    return ChatResponse(
        session_id=request.session_id,
        message=generated_response,
        sources=["TESTING"]  # You can populate this with relevant sources if needed
    )