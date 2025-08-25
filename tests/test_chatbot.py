"""Minimal tests for the project.

These tests are intentionally lightweight and focus on import and small utility
behaviour so CI can run quickly. They mock external dependencies where needed.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path


def test_helpers_clean_and_chunk():
    from src.langchain_documentation_aichatbot.utils.helpers import clean_text, chunk_text

    dirty_text = "  This   is   a   test   text  \n\n  with   extra   spaces  "
    assert clean_text(dirty_text) == "This is a test text with extra spaces"

    short_text = "This is a short text."
    chunks = chunk_text(short_text, chunk_size=100)
    assert chunks == [short_text]


def test_config_basic_properties():
    from src.langchain_documentation_aichatbot.utils.config import Config

    with patch('src.langchain_documentation_aichatbot.utils.config.load_dotenv'):
        cfg = Config()
        assert hasattr(cfg, 'model_name')
        assert isinstance(cfg.vector_store_dir, Path)


def test_vector_store_init():
    from src.langchain_documentation_aichatbot.core.vector_store import VectorStore

    with patch('src.langchain_documentation_aichatbot.core.vector_store.config') as mock_config:
        mock_config.vector_store_dir = Path("./test_vector_store")
        mock_config.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        mock_config.openai_api_key = None

        vs = VectorStore()
        assert vs is not None

