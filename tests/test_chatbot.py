"""Tests for the LangChain AI Chatbot."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from src.langchain_documentation_aichatbot.core.chatbot import LangChainChatbot
from src.langchain_documentation_aichatbot.utils.config import config


class TestLangChainChatbot:
    """Test cases for the LangChainChatbot class."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
    with patch('src.langchain_documentation_aichatbot.core.chatbot.config') as mock_config:
            mock_config.openai_api_key = "test-api-key"
            mock_config.model_name = "gpt-3.5-turbo"
            mock_config.temperature = 0.7
            mock_config.max_tokens = 1000
            mock_config.log_level = "INFO"
            mock_config.log_file = None
            """Tests for the LangChain AI Chatbot."""

            import pytest
            from unittest.mock import Mock, patch
            from pathlib import Path

            from src.langchain_documentation_aichatbot.core.chatbot import LangChainChatbot
            from src.langchain_documentation_aichatbot.utils.config import config


            class TestLangChainChatbot:
                """Test cases for the LangChainChatbot class."""

                @pytest.fixture
                def mock_config(self):
                    """Mock configuration for testing."""
                    with patch('src.langchain_documentation_aichatbot.core.chatbot.config') as mock_config:
                        mock_config.openai_api_key = "test-api-key"
                        mock_config.model_name = "gpt-3.5-turbo"
                        mock_config.temperature = 0.7
                        mock_config.max_tokens = 1000
                        mock_config.log_level = "INFO"
                        mock_config.log_file = None
                        yield mock_config

                @pytest.fixture
                def chatbot(self, mock_config):
                    """Create a chatbot instance for testing."""
                    with patch('src.langchain_documentation_aichatbot.core.chatbot.ChatOpenAI'):
                        with patch('src.langchain_documentation_aichatbot.core.chatbot.ConversationBufferMemory'):
                            chatbot = LangChainChatbot()
                            yield chatbot

                def test_chatbot_initialization(self, chatbot):
                    """Test chatbot initialization."""
                    assert chatbot is not None
                    assert hasattr(chatbot, 'document_loader')
                    assert hasattr(chatbot, 'vector_store')
                    assert hasattr(chatbot, 'memory')

                def test_chatbot_without_chain(self, chatbot):
                    """Test chatbot response when chain is not initialized."""
                    response = chatbot.chat("Hello")
                    assert "not initialized" in response["response"].lower()
                    assert response["error"] == "Chain not initialized"

                def test_get_system_info(self, chatbot):
                    """Test getting system information."""
                    info = chatbot.get_system_info()
                    assert isinstance(info, dict)
                    assert "model_name" in info
                    assert "temperature" in info
                    assert "max_tokens" in info

                def test_clear_memory(self, chatbot):
                    """Test clearing memory."""
                    # Mock the memory clear method
                    chatbot.memory.clear = Mock()
                    chatbot.clear_memory()
                    chatbot.memory.clear.assert_called_once()

                def test_reset_chatbot(self, chatbot):
                    """Test resetting the chatbot."""
                    # Mock the memory clear method
                    chatbot.memory.clear = Mock()
                    chatbot.reset()
                    assert chatbot.chain is None
                    chatbot.memory.clear.assert_called_once()


            class TestDocumentLoader:
                """Test cases for the DocumentLoader class."""

                def test_clean_text(self):
                    """Test text cleaning functionality."""
                    from src.langchain_documentation_aichatbot.utils.helpers import clean_text

                    # Test basic cleaning
                    dirty_text = "  This   is   a   test   text  \n\n  with   extra   spaces  "
                    cleaned = clean_text(dirty_text)
                    assert cleaned == "This is a test text with extra spaces"

                    # Test special character removal
                    special_text = "This has @#$%^&*() special chars!"
                    cleaned = clean_text(special_text)
                    assert "@#$%^&*()" not in cleaned

                def test_chunk_text(self):
                    """Test text chunking functionality."""
                    from src.langchain_documentation_aichatbot.utils.helpers import chunk_text

                    # Test short text
                    short_text = "This is a short text."
                    chunks = chunk_text(short_text, chunk_size=100)
                    assert len(chunks) == 1
                    assert chunks[0] == short_text

                    # Test long text
                    long_text = "This is a longer text. " * 50
                    chunks = chunk_text(long_text, chunk_size=100, overlap=20)
                    assert len(chunks) > 1
                    assert all(len(chunk) <= 100 for chunk in chunks)


            class TestVectorStore:
                """Test cases for the VectorStore class."""

                def test_vector_store_initialization(self):
                    """Test vector store initialization."""
                    from src.langchain_documentation_aichatbot.core.vector_store import VectorStore

                    with patch('src.langchain_documentation_aichatbot.core.vector_store.config') as mock_config:
                        mock_config.vector_store_dir = Path("./test_vector_store")
                        mock_config.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
                        mock_config.openai_api_key = None

                        vector_store = VectorStore()
                        assert vector_store is not None
                        assert hasattr(vector_store, 'embeddings')

                def test_get_vector_store_info(self):
                    """Test getting vector store information."""
                    from src.langchain_documentation_aichatbot.core.vector_store import VectorStore

                    with patch('src.langchain_documentation_aichatbot.core.vector_store.config') as mock_config:
                        mock_config.vector_store_dir = Path("./test_vector_store")
                        mock_config.embedding_model = "test-model"
                        mock_config.openai_api_key = None

                        vector_store = VectorStore()
                        info = vector_store.get_vector_store_info()
                        assert info["status"] == "not_initialized"


            class TestConfig:
                """Test cases for the configuration."""

                def test_config_initialization(self):
                    """Test configuration initialization."""
                    from src.langchain_documentation_aichatbot.utils.config import Config

                    with patch('src.langchain_documentation_aichatbot.utils.config.load_dotenv'):
                        config = Config()
                        assert config is not None
                        assert hasattr(config, 'model_name')
                        assert hasattr(config, 'temperature')
                        assert hasattr(config, 'max_tokens')

                def test_config_properties(self):
                    """Test configuration properties."""
                    from src.langchain_documentation_aichatbot.utils.config import Config

                    with patch('src.langchain_documentation_aichatbot.utils.config.load_dotenv'):
                        config = Config()

                        # Test directory properties
                        assert isinstance(config.vector_store_dir, Path)
                        assert isinstance(config.data_dir, Path)
                        assert isinstance(config.sources_dir, Path)
                        assert isinstance(config.processed_dir, Path)


            if __name__ == "__main__":
                pytest.main([__file__])
