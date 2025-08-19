"""Small scaffold to evaluate retrieval metrics for Module 1.

This is a small, runnable script that loads a simple `data/eval` file format (JSONL) where each
record contains a `query`, `relevant_ids` (list of document ids), and an optional `description`.
It computes precision@k and recall@k for a nearest-neighbor retrieval result provided by a
callable `retrieve_fn(query, k)` that you must implement/inject.

Usage (example):
  python scripts/eval_retrieval.py --eval-file data/eval/sample.jsonl --k 5

You can adapt `retrieve_fn` to call your VectorStore.get_nearest(query, k) method.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Callable, List

# Make project root importable so `src.*` imports work when running this script
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def retrieve_fn(query: str, k: int) -> List[str]:
    """Retrieval function wired to the project's VectorStore.

    Returns a list of document source ids (metadata['source']). If the vector store
    is not initialized or empty, returns an empty list.
    """
    try:
        from src.langchain_documentation_aichatbot.core.vector_store import VectorStore
    except Exception as e:
        print(f"Could not import VectorStore: {e}")
        return []

    vs = VectorStore()
    # Try to load an existing vector store; do not create documents here
    vs.load_vector_store()
    if not vs.vector_store:
        print("Vector store not initialized. Please create/load a vector store first.")
        return []

    docs = vs.similarity_search(query=query, k=k)
    # Each Document typically has metadata with a 'source' key used across the repo
    ids = [getattr(d, 'metadata', {}).get('source', None) or getattr(d, 'id', None) or str(i) for i, d in enumerate(docs)]
    return [str(x) for x in ids if x]


def precision_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if not retrieved:
        return 0.0
    retrieved_k = retrieved[:k]
    true_positives = sum(1 for r in retrieved_k if r in relevant)
    return true_positives / float(min(k, len(retrieved_k)))


def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if not relevant:
        return 0.0
    retrieved_k = retrieved[:k]
    true_positives = sum(1 for r in retrieved_k if r in relevant)
    return true_positives / float(len(relevant))


def evaluate(eval_file: Path, k: int, retriever: Callable[[str, int], List[str]]):
    with eval_file.open("r", encoding="utf8") as fh:
        lines = [json.loads(l) for l in fh if l.strip()]

    precisions = []
    recalls = []
    for rec in lines:
        q = rec.get("query")
        relevant = rec.get("relevant_ids", [])
        retrieved = retriever(q, k)
        precisions.append(precision_at_k(retrieved, relevant, k))
        recalls.append(recall_at_k(retrieved, relevant, k))

    mean_p = sum(precisions) / len(precisions) if precisions else 0.0
    mean_r = sum(recalls) / len(recalls) if recalls else 0.0
    print(f"Eval samples: {len(lines)}  k={k}  mean_precision@{k}={mean_p:.3f}  mean_recall@{k}={mean_r:.3f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--eval-file", required=True, help="Path to eval JSONL file")
    p.add_argument("--k", type=int, default=5, help="k for precision@k")
    args = p.parse_args()
    evaluate(Path(args.eval_file), args.k, retrieve_fn)
