"""
LangGraph agent graph definition.
"""
from langgraph.graph import StateGraph, START, END


def create_rag_graph():
    """
    Create LangGraph state graph for RAG agent.
    """
    # TODO: Define agent graph with retrieve, generate, and evaluate nodes
    graph = StateGraph(dict)

    # TODO: Add nodes and edges

    return graph.compile()
