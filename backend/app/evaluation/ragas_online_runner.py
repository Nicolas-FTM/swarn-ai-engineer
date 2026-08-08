"""
ragas_online_runner.py

On-demand Ragas evaluation over recent real production traces from Langfuse.

This module provides functions for:
- Fetching recent backend/chat_graph traces
- Scoring them with reference-free Ragas metrics (no ground_truth needed)
- Writing the scores back onto each original trace

Example:
    summary = run_online_evaluation(limit=20)
"""

# ============================================================================
# Packages
# ============================================================================
# Ragas
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

# Project Imports
from shared.observability.langfuse_client import get_langfuse_client
from shared.config.loader import load_agents
from shared.config.settings import settings

# LangChain Ollama
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Ragas LLM/Embeddings Wrappers
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# ============================================================================
# Constants
# ============================================================================
TRACE_NAME = "backend/chat_graph"

# Evaluator LLM/embeddings: ragas defaults to OpenAI unless explicitly
# overridden, so we wrap our local Ollama models for evaluation as well,
# keeping the entire pipeline (generation + evaluation) self-hosted.
agents_config = load_agents()
main_agent_config = agents_config.get("main_agent", {})
embedding_config = agents_config.get("llm_embedding", {})

evaluator_llm = None
evaluator_embeddings = None

if main_agent_config.get("provider", "") == "ollama":
    evaluator_llm = LangchainLLMWrapper(
        ChatOllama(
            model=main_agent_config.get("model", "llama3.1"),
            base_url=settings.ollama_base_url,
            temperature=0,
        )
    )     

if embedding_config.get("provider", "") == "ollama":
    embedding_model = LangchainEmbeddingsWrapper(
        OllamaEmbeddings(
            model=embedding_config.get("model", "mxbai-embed-large"),
            base_url=settings.ollama_base_url,
        )
    )


# ============================================================================
# Helpers
# ============================================================================
def fetch_recent_traces(limit: int) -> list[dict]:
    """Fetch recent chat_graph traces from Langfuse with their stored metadata.

    Args:
        limit: Maximum number of traces to fetch.

    Returns:
        A list of dicts with trace_id, question, context, and answer.
    """
    client = get_langfuse_client()
    response = client.fetch_traces(name=TRACE_NAME, limit=limit)

    entries = []
    for trace in response.data:
        metadata = trace.metadata or {}

        # Skip traces missing the fields we need (e.g. failed runs)
        if not all(k in metadata for k in ("ragas_question", "ragas_context", "ragas_answer")):
            continue

        entries.append({
            "trace_id": trace.id,
            "question": metadata["ragas_question"],
            "contexts": metadata["ragas_context"] or ["(no context retrieved)"],
            "answer": metadata["ragas_answer"],
        })

    return entries

# ============================================================================
# Services
# ============================================================================
def run_online_evaluation(limit: int = 20) -> dict:
    """Evaluate a sample of recent real traces using reference-free Ragas metrics.

    Uses only faithfulness and answer_relevancy, since production questions
    have no pre-written ground_truth available.

    Args:
        limit: Maximum number of recent traces to evaluate.

    Returns:
        A dict summarizing the evaluated trace count and average scores.
    """
    entries = fetch_recent_traces(limit)

    if not entries:
        return {"evaluated": 0, "message": "No eligible traces found"}

    dataset = Dataset.from_list([
        {"question": e["question"], "answer": e["answer"], "contexts": e["contexts"]}
        for e in entries
    ])

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )
    log_scores_to_langfuse(scores, entries)

    scores_df = scores.to_pandas()
    return {
        "evaluated": len(entries),
        "avg_faithfulness": float(scores_df["faithfulness"].mean()),
        "avg_answer_relevancy": float(scores_df["answer_relevancy"].mean()),
    }

# ============================================================================
# Helpers
# ============================================================================
def log_scores_to_langfuse(scores, entries: list[dict]) -> None:
    """Attach per-trace Ragas scores back onto their original Langfuse trace.

    Args:
        scores: Ragas evaluation result, indexable per row.
        entries: Original trace entries, same order as scores.
    """
    client = get_langfuse_client()
    scores_df = scores.to_pandas()

    for i, entry in enumerate(entries):
        row = scores_df.iloc[i]
        for metric_name in ["faithfulness", "answer_relevancy"]:
            client.score(
                trace_id=entry["trace_id"],
                name=f"ragas_online_{metric_name}",
                value=float(row[metric_name]),
            )