"""
runner.py

Entry point for invoking the main chat orchestration graph.

This module provides functions for:
- Invoking the compiled chat graph with Langfuse/OTel observability

Example:
    result = run_chat(role="baker", query="how do I make bread?")
"""

# ============================================================================
# Packages
# ============================================================================
# Langfuse
from langfuse.decorators import observe, langfuse_context

# Project Imports
from backend.app.agents.graph import chat_graph
from shared.schemas.chat import ChatState
from shared.observability.langfuse_client import get_langfuse_handler
from shared.observability.telemetry import get_current_otel_trace_id

# ============================================================================
# Services
# ============================================================================
@observe(name="backend/chat_graph")
def run_chat(role: str, query: str, session_id: str) -> tuple[ChatState, str]:
    """Invoke the main chat orchestration graph for a given role and query.

    Args:
        role: Role of the requesting user, resolved upstream from JWT.
        query: Natural language question from the user.

    Returns:
        The final graph state, including the generated answer, route used,
        and sources.
    """
    otel_trace_id = get_current_otel_trace_id()
    if otel_trace_id:
        langfuse_context.update_current_trace(
            metadata={"otel_trace_id": otel_trace_id, 
                      "role": role,
                      "session_id": session_id}
        )

    handler = get_langfuse_handler()
    initial_state: ChatState = {
        "query": query,
        "role": role,
        "route": "",
        "context": [],
        "sources": [],
        "answer": "",
    }

    result = chat_graph.invoke(
        initial_state,
        config={"callbacks": [handler],
                "configurable": {"thread_id": session_id}
                },
    )

    # Store the data needed for later Ragas evaluation directly on the trace,
    # so the online evaluator doesn't need to parse nested graph spans.
    langfuse_context.update_current_trace(
        metadata={
            "ragas_question": query,
            "ragas_context": result["context"],
            "ragas_answer": result["answer"],
        }
    )

    langfuse_trace_id = langfuse_context.get_current_trace_id()

    return result, langfuse_trace_id