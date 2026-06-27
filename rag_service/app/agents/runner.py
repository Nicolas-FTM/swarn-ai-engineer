from rag_service.app.agents.graph import agent_graph
from shared.observability.langfuse_client import get_langfuse_handler
from shared.schemas.agent import AgentState
from langfuse.decorators import observe, langfuse_context
import logging

logger = logging.getLogger(__name__)

@observe(name="call_llm")
def call_llm(prompt: str, otel_trace_id: str | None = None) -> str:
    if otel_trace_id:
        langfuse_context.update_current_trace(metadata={"otel_trace_id": otel_trace_id})

    handler = get_langfuse_handler()

    logging.info(f"LA INFORMACION DEL PROMPT LLEGA '{prompt}'")

    state = AgentState(question=prompt, answer="")

    result = agent_graph.invoke(
        state,
        config={"callbacks": [handler]},
    )
    return result["answer"]