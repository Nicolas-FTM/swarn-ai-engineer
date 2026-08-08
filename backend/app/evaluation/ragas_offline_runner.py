"""
ragas_offline_runner.py

Offline Ragas evaluation against a golden dataset of role-tagged questions.
This module provides functions for:
- Running the chat graph against every golden dataset entry
- Computing Ragas metrics (faithfulness, answer relevancy, context precision/recall)
- Logging the resulting scores back to Langfuse, attached to each trace

Example:
    python -m app.evaluation.ragas_offline_runner
"""

# ============================================================================
# Packages
# ============================================================================
# System
import uuid

# Ragas
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from datasets import Dataset

# Project Imports
from backend.app.agents.runner import run_chat
from shared.observability.langfuse_client import get_langfuse_client
from shared.config.loader import load_golden_dataset, load_agents
from shared.config.settings import settings

# LangChain Ollama
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Ragas LLM/Embeddings Wrappers
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Ragas config
from ragas.run_config import RunConfig

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

faithfulness_custom = Faithfulness(llm=evaluator_llm)
answer_relevancy_custom = AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
context_precision_custom = ContextPrecision(llm=evaluator_llm)
context_recall_custom = ContextRecall(llm=evaluator_llm)

# ============================================================================
# Services
# ============================================================================
def run_offline_evaluation() -> dict:
    """Run the chat graph against the golden dataset and score it with Ragas.

    Returns:
        A dict summarizing average scores per metric.
    """
    golden_entries = load_golden_dataset()
    eval_rows = []
    trace_ids = []

    for entry in golden_entries:
        session_id = f"ragas-eval-{uuid.uuid4()}"
        result, trace_id = run_chat(role=entry["role"], query=entry["question"], session_id=session_id)

        eval_rows.append({
            "question": entry["question"],
            "answer": result["answer"],
            "contexts": result["context"] or ["(no context retrieved)"],
            "ground_truth": entry["ground_truth"],
        })
        trace_ids.append(trace_id)

    dataset = Dataset.from_list(eval_rows)

    scores = evaluate(
        dataset,
        metrics=[faithfulness_custom, answer_relevancy_custom, context_precision_custom, context_recall_custom],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        run_config=RunConfig(timeout=300, max_workers=1),  # 5 min per job, sequential to not saturate Ollama
    )

    log_scores_to_langfuse(scores, golden_entries, trace_ids)

    return scores

# ============================================================================
# Helpers
# ============================================================================
def log_scores_to_langfuse(scores, golden_entries: list[dict], trace_ids: list[str]) -> None:
    """Attach per-question Ragas scores to their exact Langfuse trace.

    Args:
        scores: Ragas evaluation result, indexable per row.
        golden_entries: Original golden dataset entries, same order as scores.
        trace_ids: Langfuse trace_id for each entry, same order as scores.
    """
    client = get_langfuse_client()
    scores_df = scores.to_pandas()

    for i, entry in enumerate(golden_entries):
        row = scores_df.iloc[i]
        trace_id = trace_ids[i]

        for metric_name in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
            client.score(
                trace_id=trace_id,
                name=f"ragas_{metric_name}",
                value=float(row[metric_name]),
                comment=f"role={entry['role']}",
            )

# ============================================================================
# Main Entry Point
# ============================================================================
def main() -> None:
    """Run the offline Ragas evaluation as a standalone script."""
    result = run_offline_evaluation()
    print(result)


if __name__ == "__main__":
    main()   