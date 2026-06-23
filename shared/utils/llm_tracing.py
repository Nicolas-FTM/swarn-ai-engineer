from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from shared.config import settings

langfuse_client = Langfuse(
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
    host=settings.langfuse_url,
)

def get_langfuse_handler(session_id: str | None = None):
    """
    Devuelve un CallbackHandler de Langfuse para usar en LangChain/LangGraph.
    """
    return CallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_url,
        session_id=session_id
    )