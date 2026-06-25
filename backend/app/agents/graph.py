"""
LangGraph agent graph definition.
"""
from langgraph.graph import StateGraph, START, END
from shared.schemas.agent import AgentState
from backend.app.services.rag_service import RAGService
from langchain_ollama import ChatOllama
from typing import TypedDict

import logging

logger = logging.getLogger(__name__)

llm = ChatOllama(model="llama3.1", temperature=0.3)

async def retrieve_and_generate_node(state: AgentState) -> AgentState:
    """Nodo que llama al rag_service."""
    # result = await RAGService.call_rag_service(state["query"])
    # state["message"] = result.message
    # state["sources"] = result.sources
    return state

def call_model_node(state: AgentState) -> AgentState:
    logging.info(f"LA INFORMACION DEL PROMPT LLEGA '{state}'")

    response = llm.invoke(state["question"])
    return AgentState(question=state["question"], answer=response.content)

def build_graph():
    """
    Create LangGraph state graph for RAG agent.
    """
    graph = StateGraph(AgentState)

    graph.add_node("call_model", call_model_node)
    graph.add_edge(START, "call_model")
    graph.add_edge("call_model", END)

    return graph.compile()

# Compile the graph at module load time
agent_graph = build_graph()
