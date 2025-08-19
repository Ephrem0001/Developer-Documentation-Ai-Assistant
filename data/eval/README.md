Eval data format
================

Place labeled retrieval evaluation examples in this folder. Each line in the JSONL file should be a JSON object with at least the following fields:

- `query`: the user query string
- `relevant_ids`: a list of document ids that are relevant to the query (these should match your vector store document ids)
- `description` (optional): human-readable note about the example

Example JSONL line:

{"query": "How do I initialize a Chroma vector store?", "relevant_ids": ["docs/chroma_init.md"], "description": "Chroma setup doc"}

Use `scripts/eval_retrieval.py` to run basic precision@k / recall@k metrics against your retriever.
