## RAG for Developer Documentation — LangChain Documentation AI Chatbot

A LangChain-based Retrieval-Augmented Generation (RAG) system that answers developer questions by retrieving and synthesizing information from a curated knowledge base of official documentation and trusted resources. This repository demonstrates a production-oriented architecture for building documentation assistants, with notes on safety, maintenance, scope, and evaluation suitable for Module 1.

Key goals:
- Provide accurate, citation-aware answers sourced from official docs.
- Keep the system simple for Module 1 while highlighting extension points (metrics, query processing, guardrails).

Tags: langchain, rag, documentation, retrieval, developer-experience, vector-database, chromadb

## Problem statement

Developers need fast, authoritative answers drawn from official documentation. Generic LLM answers risk hallucination and lack traceability. This project shows how to combine embeddings, a vector store, and retrieval pipelines to produce grounded responses with provenance.

## Simplified Installation (Module 1)

This section focuses on the minimal steps to run the Module 1 demo. See the code and comments for production hardening notes.

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Langchain-Documentation-AIChatBot
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

## Query Processing & TODOs

Query processing is currently a lightweight pipeline: cleaning, optional query expansion, embed, and nearest-neighbor search. Recommended improvements:

- Implement normalized query preprocessing (lowercase, remove stop-words, synonyms mapping).
- Add a ranking stage that re-scores retrieved passages using the LLM for relevance before prompting.
- Track and expose the query processing stage in the API for observability.

## Module 1 cleanup notes

To simplify for Module 1 I fixed a few packaging and import issues and standardized the package name to `langchain_documentation_aichatbot`. Keep public APIs stable; larger refactors can wait for Module 2.
