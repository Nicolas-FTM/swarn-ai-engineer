# Router
from fastapi import APIRouter, HTTPException, status

# Responses Model
from shared.schemas.example import ExampleResponse

# Langfuse Client for LLM calls
from shared.utils.llm_tracing import langfuse_client
from langfuse.decorators import observe

# Environment Variables
from shared.config.settings import settings

# Call LLM 
from rag_service.app.agents.runner import call_llm

# Traces
from opentelemetry import trace

# Logger
import logging
logger = logging.getLogger(__name__)

# Definition of the router
router = APIRouter(
    prefix="/api",
    tags=["auxiliar"]
)

@router.post("/auxiliar_fun")
async def auxiliar_fun():
    """
    Use internal function.
    """
    span = trace.get_current_span()
    otel_trace_id = format(span.get_span_context().trace_id, "032x")

    # logger.info("Fetching users...", extra={"otel_trace_id": otel_trace_id})
    # users = list_users()
    # logger.info(users, extra={"otel_trace_id": otel_trace_id})

    # return users
    
@router.get("/retrieve", response_model=ExampleResponse)
@observe(name="example/retrieve_all")
async def retrieve_all():
    """
    Retrieve all examples.
    """
    span = trace.get_current_span()
    otel_trace_id = format(span.get_span_context().trace_id, "032x")

    # Link the Langfuse trace with the Tempo trace_id
    langfuse_client.trace(
        name="example/retrieve_all",
        metadata={"otel_trace_id": otel_trace_id},
    )
    
    response = call_llm(prompt="Hola Chatgpt", otel_trace_id=otel_trace_id) 
    logger.info(response, extra={"otel_trace_id": otel_trace_id})

