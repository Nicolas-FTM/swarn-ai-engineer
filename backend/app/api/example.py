# app/api/example.py
from fastapi import APIRouter, Depends, HTTPException, status
from shared.schemas.example import ExampleResponse, ExampleRequest
import logging

from shared.utils.llm_tracing import langfuse_client
from shared.config import settings
from app.agents.runner import call_llm

from opentelemetry import trace
from langfuse.decorators import observe

router = APIRouter()
logger = logging.getLogger(__name__)

# Simulación de una "base de datos"
fake_db = {
            1: {
                "id": 1,
                "name": "Ana",
                "email": "ana@mail.com"
                },
            2: {
                "id": 2,
                "name": "Juan",
                "email": "juan@mail2.com"
            },
            3: {
                "id": 3,
                "name": "María",
                "email": "maria@mail.com"
            }
        }

@router.post("/retrieve/{id}", response_model=ExampleResponse)
async def retrieve_user(id: int):
    """
    Retrieve an example.
    """
    example = fake_db.get(id)
    if not example:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
    
    return example

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

    examples = list(fake_db.values())

    if len(examples) == 0:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Examples List Empty",
        )
    
    response = call_llm(prompt="Hola Chatgpt", otel_trace_id=otel_trace_id) 
    logger.info(response, extra={"otel_trace_id": otel_trace_id})
    
    return fake_db[1]
