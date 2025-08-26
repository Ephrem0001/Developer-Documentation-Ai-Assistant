"""Configuration management for the LangChain AI Chatbot."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import json

# Load .env early so environment variables are available before pydantic reads them
load_dotenv()

# Normalize DOCUMENTATION_SOURCES env var if provided as a comma-separated string
raw_docs = os.getenv("DOCUMENTATION_SOURCES")
if raw_docs and not raw_docs.strip().startswith("["):
    parts = [s.strip() for s in raw_docs.split(',') if s.strip()]
    os.environ["DOCUMENTATION_SOURCES"] = json.dumps(parts)


class Config(BaseSettings):
    """Configuration settings for the LangChain AI Chatbot."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    grok_api_key: Optional[str] = Field(None, env="GROK_API_KEY")
    grok_api_url: Optional[str] = Field("https://api.x.ai/v1", env="GROK_API_URL")
    langchain_api_key: Optional[str] = Field(None, env="LANGCHAIN_API_KEY")
    langchain_endpoint: Optional[str] = Field(
        "https://api.smith.langchain.com", env="LANGCHAIN_ENDPOINT"
    )
    langchain_project: Optional[str] = Field(None, env="LANGCHAIN_PROJECT")
    
    # Model Configuration
    model_provider: str = Field("openai", env="MODEL_PROVIDER")  # "openai", "grok", "anthropic"
    model_name: str = Field("gpt-3.5-turbo", env="MODEL_NAME")
    grok_model: str = Field("grok-beta", env="GROK_MODEL")
    temperature: float = Field(0.7, env="TEMPERATURE")
    max_tokens: int = Field(1000, env="MAX_TOKENS")
    
    # Vector Store Configuration
    vector_store_path: str = Field("./data/vector_store", env="VECTOR_STORE_PATH")
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    
    # Document Processing
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    # Local source loading
    extra_urls_file: str = Field("data/sources/urls.txt", env="EXTRA_URLS_FILE")
    sources_glob: list[str] = Field(default=["*.txt", "*.md", "*.pdf", "*.html", "*.htm"])
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(None, env="LOG_FILE")
    
    # Web Interface
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    
    # Documentation Sources
    documentation_sources: list[str] = Field(
        default=[
            # LangChain (stable entry points)
            "https://python.langchain.com/docs/",
            "https://python.langchain.com/docs/get_started/introduction",
            "https://python.langchain.com/docs/concepts/",
            "https://python.langchain.com/docs/tutorials/rag",
            "https://python.langchain.com/docs/how_to/",
            # LangGraph / LangSmith
            "https://langchain-ai.github.io/langgraph/",
            "https://python.langchain.com/docs/langgraph/",
            "https://docs.smith.langchain.com/",

            # OpenAI
            "https://platform.openai.com/docs/overview",
            "https://platform.openai.com/docs/api-reference/introduction",

            # Providers / Ecosystem
            "https://docs.x.ai/",
            "https://huggingface.co/docs",
            "https://www.sbert.net/",

            # Python & Core libs
            "https://docs.python.org/3/",
            "https://docs.pydantic.dev/latest/",
            "https://requests.readthedocs.io/en/latest/",
            "https://www.crummy.com/software/BeautifulSoup/bs4/doc/",

            # Vector stores / similarity
            "https://docs.trychroma.com/",
            "https://faiss.ai/",
            "https://github.com/facebookresearch/faiss/wiki",

            # Web frameworks used
            "https://docs.streamlit.io/",
            "https://fastapi.tiangolo.com/",
            "https://www.uvicorn.org/",
        ]
    )

    @field_validator('documentation_sources', mode='before')
    def _parse_documentation_sources(cls, v):
        """Allow DOCUMENTATION_SOURCES env var as comma-separated string or JSON list."""
        if isinstance(v, str):
            # try simple comma-split first
            parts = [s.strip() for s in v.split(',') if s.strip()]
            return parts
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        # Environment variables are loaded at module import time to allow
        # pydantic to read complex fields from env sources.
        super().__init__(**kwargs)

        # Ensure vector store directory exists
        Path(self.vector_store_path).mkdir(parents=True, exist_ok=True)
    
    @property
    def vector_store_dir(self) -> Path:
        """Get the vector store directory path."""
        return Path(self.vector_store_path)
    
    @property
    def data_dir(self) -> Path:
        """Get the data directory path."""
        return Path("data")
    
    @property
    def sources_dir(self) -> Path:
        """Get the sources directory path."""
        return self.data_dir / "sources"
    
    @property
    def processed_dir(self) -> Path:
        """Get the processed documents directory path."""
        return self.data_dir / "processed"


# Global configuration instance
config = Config()
