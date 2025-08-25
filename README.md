
 # Developer-Documentation-Ai-Assistant — Grounded RAG to Reduce Hallucination and Improve Developer Productivity

TL;DR: A lightweight Retrieval-Augmented Generation (RAG) assistant that answers developer questions with citation-aware responses drawn from curated documentation to reduce hallucination and speed developer workflows.

A focused Retrieval-Augmented Generation (RAG) assistant that answers developer questions by retrieving authoritative passages from a curated documentation knowledge base and generating citation-aware responses to reduce hallucination and speed developer workflows.

Key goals:
- Provide accurate, citation-aware answers sourced from official docs.
- Keep the system simple for Module 1 while highlighting extension points (metrics, query processing, guardrails).

Tags: langchain, rag, retrieval-evaluation, citations, chromadb, faiss, sentence-transformers, developer-docs, reproducibility, safety, content-moderation

Target audience

- Developers and engineers who need quick, authoritative answers from official documentation.
- Tooling and platform teams evaluating RAG pipelines for internal documentation search.
- Researchers building retrieval evaluation or citation-aware assistants.

How to cite

If you use this work in a publication or demo, please cite the repository; see `CITATION.cff` for machine-readable citation metadata.

## Problem statement

Developers need fast, authoritative answers drawn from official documentation. Generic LLM answers risk hallucination and lack traceability. This project shows how to combine embeddings, a vector store, and retrieval pipelines to produce grounded responses with provenance.

## Preliminary research

Before building Module 1 we reviewed prior work, common tools, and data sources to ensure the project targets developer documentation retrieval with strong provenance.

- Goal: build a Retrieval-Augmented Generation (RAG) assistant that returns citation-aware answers sourced from authoritative developer docs and minimizes hallucination.
- Reviewed tools and references: LangChain docs, OpenAI model docs, FAISS and Chroma vector stores, sentence-transformers (SBERT) for dense embeddings, and common ingestion tooling (BeautifulSoup, requests).
- Data sources: curated documentation snapshots under `data/datasets/` (official docs, tutorials, and API references). Keep the corpus focused and labeled for domain clarity.
- Evaluation: use offline metrics (precision@k, recall@k, MRR), small labeled eval set under `data/eval`, and lightweight user-acceptance tests for citation quality.
- Best practice notes: keep a single, clear project title; separate human-facing project name from package/module names; document assumptions, limitations, and safety/guardrails; include tests for retrieval and end-to-end response formatting.

## Simplified Installation (Module 1)

This section focuses on the minimal steps to run the Module 1 demo. See the code and comments for production hardening notes.

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Developer-Documentation-Ai-Assistant
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Web Interface (Streamlit)
```bash
streamlit run src/langchain_documentation_aichatbot/apps/streamlit_app.py
```

### Web Interface (Gradio)
```bash
python -m langchain_documentation_aichatbot.apps.gradio_app
```

### API Server
```bash
uvicorn src.langchain_documentation_aichatbot.apps.api.main:app --reload
```

### Command Line Interface
```bash
python -m langchain_documentation_aichatbot.cli
```

## Project Structure

```
src/langchain_documentation_aichatbot/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── chatbot.py          # Main chatbot logic
│   ├── document_loader.py  # Document loading utilities
│   └── vector_store.py     # Vector database operations
├── data/
│   ├── __init__.py
│   ├── sources/            # Documentation sources
│   └── processed/          # Processed documents
├── models/
│   ├── __init__.py
│   └── embeddings.py       # Embedding models
├── utils/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   └── helpers.py          # Utility functions
├── apps/
│   ├── __init__.py
│   ├── streamlit_app.py    # Streamlit web app
│   ├── gradio_app.py       # Gradio web app
│   └── api/
│       ├── __init__.py
│       └── main.py         # FastAPI server
└── cli.py                  # Command line interface
```

## Configuration

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=your_project_name
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black src/
isort src/
```

4. Type checking:
```bash
mypy src/
```

## Reproducibility

To reproduce the environment and run the project consistently:

1. Create and activate a virtual environment (Windows PowerShell shown):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies in editable mode:
```powershell
python -m pip install --upgrade pip
pip install -e .
pip install -e ".[dev]"
```

3. Configure environment variables:
```powershell
Copy-Item env.example .env
# Edit .env and set your API keys, e.g. OPENAI_API_KEY
```

4. Run apps:
```powershell
# Streamlit
python -m streamlit run src\langchain_documentation_aichatbot\apps\streamlit_app.py

# Gradio
python -m langchain_documentation_aichatbot.apps.gradio_app

# API
python -m uvicorn src.langchain_documentation_aichatbot.apps.api.main:app --reload
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- LangChain team for the excellent framework
- OpenAI for providing the underlying AI models
- The open-source community for various tools and libraries

## Scope & Document Domain

This project is intentionally scoped to developer-facing technical documentation (LangChain, OpenAI, Python standard library, select libraries). Corpus files live under `data/datasets` and `data/processed` and are intended as an indexable knowledge base rather than a model training dataset.

If you extend the domain, add explicit domain labels and retrain/reevaluate retrieval settings.

## Maintenance, Versioning & Support

- Version: `0.1.0` (see `src/langchain_documentation_aichatbot/__init__.py` for package version).
- Releases: Tag commits with semantic versioning (vMAJOR.MINOR.PATCH).
- Support: For Module 1 please open issues on the repository. For production deployments add a dedicated support channel (Slack/Discord/email) and an on-call rotation.

## Safety, Guardrails & Content Moderation

To reduce harmful outputs and hallucinations:

- Use retrieval with strict citation: always include source links for any factual claim.
- Add a content moderation step on user inputs (block disallowed categories) and on model outputs (safety classifier).
- Limit model capabilities with prompt-level guardrails: refusal templates for disallowed requests, and explicit system messages to constrain behavior.
- Logging & monitoring: record queries, retrieved passages, and model responses for audit and improvement.

## Retrieval Evaluation & Metrics

For Module 1 provide basic evaluation and a path to extend:

- Offline metrics: precision@k, recall@k, and MRR over a labeled dev set.
- Online metrics: user satisfaction, response time, and rate of hallucination reports.
- Keep a small labeled testset under `data/eval` and evaluate retrieval changes before deployment.

## Query processing

Problem

Developer queries are often short, ambiguous, or use domain-specific terms. Without normalization and robust ranking, retrieval can return noisy passages and reduce citation quality.

Approach

The Module 1 pipeline takes a pragmatic, incremental approach: clean and normalize the input, optionally expand the query (for synonyms or API aliases), compute embeddings, and run a nearest-neighbor search against a vector store. For higher precision we plan a two-stage ranker: a fast ANN retrieval followed by an LLM-based re-ranker that scores passages for relevance and provenance.

Results (Module 1)

The current implementation provides a working baseline that returns candidate passages with citation metadata. It is suitable for demos and initial evaluation using offline metrics (precision@k, recall@k, MRR) on the small labeled dev set under `data/eval`.

Limitations & next steps

- Improve normalization: lowercase, punctuation stripping, stop-word handling, and domain synonym mapping.
- Add an LLM re-ranker to boost precision and reduce hallucination risk.
- Expose query-processing traces in the API for observability and debugging.
- Add unit tests and an end-to-end retrieval evaluation harness that computes precision@k and MRR automatically.

## Module 1 cleanup notes

To simplify for Module 1 I fixed a few packaging and import issues and standardized the package name to `langchain_documentation_aichatbot`. Keep public APIs stable; larger refactors can wait for Module 2.
