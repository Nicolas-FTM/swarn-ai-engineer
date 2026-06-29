"""
graph.py

Main chat orchestration LangGraph: intent routing, retrieval and generation.

This module provides functions for:
- Classifying user intent (vector vs sql)
- Retrieving context from rag_service accordingly
- Generating the final answer constrained to retrieved context

Example:
    graph = build_chat_graph()
    result = graph.invoke({"query": "...", "role": "baker", ...})
"""
# ============================================================================
# Packages
# ============================================================================
# LangChain Ollama
from langchain_ollama import ChatOllama

# LangGraph
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

# Shared Config Loader
from shared.config.loader import load_agents
from shared.config.settings import settings

# Project Imports
from shared.schemas.chat import ChatState
from backend.app.services.rag_service import retrieve_vector, retrieve_sql, RetrievalError

# ============================================================================
# Constants
# ============================================================================
agents_config = load_agents()

main_agent_config = agents_config.get("main_agent", None)
intent_router_prompt = agents_config.get("intent_router", None).get("prompt", None)
generation_prompt = agents_config.get("generation", None).get("prompt", None) 
vector_top_k = agents_config.get("retrieval", None).get("vector", None).get("top_k", None) 

llm = None

if main_agent_config.get("provider", None) == "ollama":
    llm = ChatOllama(
        model=main_agent_config["model"],
        base_url=settings.ollama_base_url,
        temperature=main_agent_config["temperature"],
    )         

checkpointer_cm = PostgresSaver.from_conn_string(settings.db_url)
checkpointer = checkpointer_cm.__enter__()

checkpointer.setup()

# ============================================================================
# Graph Nodes
# ============================================================================
def classify_intent_node(state: ChatState) -> ChatState:
    """Classify the user's question as 'vector' or 'sql'.

    Args:
        state: Current graph state.

    Returns:
        Updated state with the route field populated.
    """
    prompt = intent_router_prompt.format(question=state["query"])
    response = llm.invoke(prompt)
    route = response.content.strip().lower()

    # Default to vector retrieval if the LLM returns anything unexpected
    if route not in ("vector", "sql"):
        route = "vector"

    return {**state, "route": route}


def retrieve_vector_node(state: ChatState) -> ChatState:
    """Retrieve document chunks from rag_service for the resolved role.

    Args:
        state: Current graph state.

    Returns:
        Updated state with context and sources populated, or an error route
        if retrieval fails or is rejected by rag_service.
    """
    try:
        texts, sources = retrieve_vector(
            role=state["role"], query=state["query"], top_k=vector_top_k
        )
        return {**state, "context": texts, "sources": sources}
    except RetrievalError as e:
        return {**state, "context": [], "sources": [], "answer": f"Retrieval error: {e}"}


def retrieve_sql_node(state: ChatState) -> ChatState:
    """Retrieve tabular rows from rag_service for the resolved role.

    Args:
        state: Current graph state.

    Returns:
        Updated state with context (rows as text) and sources (generated SQL).
    """
    try:
        rows, generated_sql = retrieve_sql(role=state["role"], query=state["query"])
        context = [str(row) for row in rows]
        return {**state, "context": context, "sources": [generated_sql]}
    except RetrievalError as e:
        return {**state, "context": [], "sources": [], "answer": f"Retrieval error: {e}"}


def generate_answer_node(state: ChatState) -> ChatState:
    """Generate the final answer constrained to the retrieved context.

    Args:
        state: Current graph state.

    Returns:
        Updated state with the answer field populated.
    """
    # If an error already set the answer (e.g. retrieval failure), skip generation
    if state.get("answer"):
        return state

    context_text = "\n".join(state["context"]) if state["context"] else "(no context retrieved)"
    prompt = generation_prompt.format(context=context_text, question=state["query"])
    response = llm.invoke(prompt)

    return {**state, "answer": response.content.strip()}

# ============================================================================
# Routing
# ============================================================================
def route_after_classification(state: ChatState) -> str:
    """Route to the appropriate retrieval node based on classified intent.

    Args:
        state: Current graph state.

    Returns:
        The name of the next node to execute.
    """
    return "retrieve_sql" if state["route"] == "sql" else "retrieve_vector"

# ============================================================================
# Graph Definition
# ============================================================================
def build_chat_graph():
    """Build and compile the main chat orchestration LangGraph.

    Uses PostgresSaver as checkpointer so conversation state persists
    across backend restarts and survives multiple replicas.

    Returns:
        A compiled LangGraph ready to be invoked, with checkpointing enabled.
    """
    graph = StateGraph(ChatState)

    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("retrieve_vector", retrieve_vector_node)
    graph.add_node("retrieve_sql", retrieve_sql_node)
    graph.add_node("generate_answer", generate_answer_node)

    graph.add_edge(START, "classify_intent")
    graph.add_conditional_edges("classify_intent", route_after_classification)
    graph.add_edge("retrieve_vector", "generate_answer")
    graph.add_edge("retrieve_sql", "generate_answer")
    graph.add_edge("generate_answer", END)
    
    return graph.compile(checkpointer=checkpointer)

chat_graph = build_chat_graph()