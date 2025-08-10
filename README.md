# LangChain Documentation AI Chatbot

A sophisticated AI chatbot built with LangChain that leverages legitimate documentation sources to provide accurate and helpful responses.

## Features

- **Documentation-Based Responses**: Uses official documentation from trusted sources
- **Vector Database**: ChromaDB for efficient document retrieval
- **Multiple Interfaces**: Web UI (Streamlit/Gradio) and API endpoints
- **Modular Architecture**: Clean, maintainable code structure
- **Environment Configuration**: Secure API key management
- **Comprehensive Testing**: Unit and integration tests

## Legitimate Resources

This chatbot is trained on and references the following legitimate sources:

- **LangChain Documentation**: Official LangChain docs and tutorials
- **OpenAI Documentation**: API references and best practices
- **Python Documentation**: Core Python language documentation
- **Academic Papers**: Peer-reviewed research on NLP and AI
- **Technical Blogs**: Reputable tech blogs and tutorials

## Installation

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
