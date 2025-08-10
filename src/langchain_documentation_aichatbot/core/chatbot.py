"""Main chatbot implementation for the LangChain AI Chatbot."""

import logging
from typing import Dict, List, Optional

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document

from ..utils.config import config
from ..utils.helpers import setup_logging
from .document_loader import DocumentLoader
from .vector_store import VectorStore
from .llm_factory import llm_factory


class LangChainChatbot:
    """Main chatbot class that handles conversations and document retrieval."""
    
    def __init__(self):
        self.logger = setup_logging(
            level=config.log_level,
            log_file=config.log_file
        )
        
        # Initialize components
        self.document_loader = DocumentLoader()
        self.vector_store = VectorStore()
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain = None
        
        self.logger.info("LangChain Chatbot initialized")
    
    def _initialize_llm(self):
        """Initialize the language model.
        
        Returns:
            LLM instance or None if no API key is available
        """
        # Try to create LLM using the factory
        llm = llm_factory.create_llm()
        
        if llm:
            self.logger.info(f"Successfully initialized LLM with provider: {config.model_provider}")
            return llm
        
        # Check available providers
        available_providers = llm_factory.get_available_providers()
        if available_providers:
            self.logger.warning(f"No API key for {config.model_provider}. Available providers: {available_providers}")
        else:
            self.logger.warning("No API keys found for any provider. Using mock responses for demo.")
        
        return None
    
    def setup_knowledge_base(self, force_rebuild: bool = False) -> bool:
        """Set up the knowledge base with documents.
        
        Args:
            force_rebuild: Whether to force rebuild the vector store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if vector store exists
            if not force_rebuild:
                existing_store = self.vector_store.load_vector_store()
                if existing_store:
                    self.logger.info("Using existing vector store")
                    self._setup_chain()
                    return True
            
            # Load documents
            self.logger.info("Loading documentation sources...")
            documents = self.document_loader.load_documentation_sources()
            
            if not documents:
                self.logger.warning("No documents loaded")
                return False
            
            # Split documents
            split_docs = self.document_loader.split_documents(documents)
            
            # Create vector store
            self.vector_store.create_vector_store(split_docs)
            
            # Setup conversation chain
            self._setup_chain()
            
            self.logger.info("Knowledge base setup completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up knowledge base: {e}")
            return False
    
    def _setup_chain(self):
        """Set up the conversational retrieval chain."""
        if not self.llm:
            self.logger.warning("LLM not available, chain will use mock responses")
            self.chain = None
            return
        
        try:
            self.logger.info("Setting up conversational retrieval chain...")
            
            # Create retriever
            retriever = self.vector_store.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # Create chain
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=self.memory,
                return_source_documents=True,
                verbose=True
            )
            
            self.logger.info("Conversational retrieval chain setup completed")
            
        except Exception as e:
            self.logger.error(f"Error setting up chain: {e}")
            self.chain = None
    
    def chat(self, message: str) -> Dict[str, any]:
        """Process a chat message and return a response.
        
        Args:
            message: User's message
            
        Returns:
            Dictionary containing response and metadata
        """
        if not self.chain:
            # Mock response for demo purposes
            mock_responses = {
                "What is LangChain?": "LangChain is a framework for developing applications powered by language models. It provides a standard interface for chains, lots of integrations with other tools, and end-to-end chains for common applications.",
                "How do I use OpenAI with LangChain?": "You can use OpenAI with LangChain by importing ChatOpenAI from langchain_openai and initializing it with your API key. Then you can use it in chains, agents, and other LangChain components.",
                "Explain Python decorators": "Python decorators are a way to modify or enhance functions or classes. They use the @ syntax and are a form of metaprogramming that allows you to wrap functions with additional functionality.",
                "What are the best practices for prompt engineering?": "Best practices for prompt engineering include being clear and specific, using few-shot examples, breaking down complex tasks, and testing your prompts thoroughly.",
                "How do I create a custom LangChain chain?": "To create a custom LangChain chain, you can inherit from the Chain class and implement the required methods like _call and _chain_type."
            }
            
            # Check if we have a mock response for this message
            for key, response in mock_responses.items():
                # Remove punctuation and make case-insensitive comparison
                clean_key = key.lower().replace('?', '').replace('!', '').strip()
                clean_message = message.lower().replace('?', '').replace('!', '').strip()
                if clean_key in clean_message or clean_message in clean_key:
                    return {
                        "response": response,
                        "sources": [{"content": "Mock response for demo purposes", "metadata": {"title": "Demo", "source": "demo"}}],
                        "error": None
                    }
            
            # Handle general greetings and simple interactions
            if message.lower().strip() in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']:
                return {
                    "response": "Hello! I'm your LangChain AI Chatbot. I can help you with questions about LangChain, Python programming, and AI development. Try asking me about LangChain, Python decorators, or prompt engineering!",
                    "sources": [{"content": "Demo greeting response", "metadata": {"title": "Demo", "source": "demo"}}],
                    "error": None
                }
            
            # Handle questions mentioning LangChain directly
            if 'langchain' in message.lower():
                return {
                    "response": (
                        "LangChain is a framework for building applications that use large language models (LLMs). "
                        "It's not a self‑driving car control stack. You could use LangChain for tasks around autonomous systems—"
                        "like documentation Q&A, code assistants, data retrieval, or workflow orchestration—but perception, planning, "
                        "and control for self‑driving rely on robotics/AV stacks (e.g., ROS, sensor fusion, planning)."
                    ),
                    "sources": [{"content": "Demo explanation about LangChain's purpose", "metadata": {"title": "Demo", "source": "demo"}}],
                    "error": None
                }

            # Handle general programming questions
            if any(keyword in message.lower() for keyword in ['python', 'programming', 'code', 'script']):
                return {
                    "response": "Python is a versatile programming language great for AI, web development, data science, and automation. I can help you with Python concepts, LangChain integration, and AI development. What specific Python topic would you like to explore?",
                    "sources": [{"content": "Python programming response", "metadata": {"title": "Demo", "source": "demo"}}],
                    "error": None
                }
            
            # Default helpful demo response (no error)
            return {
                "response": (
                    "I'm in demo mode using mock responses. Ask me about LangChain, Python, or AI development, "
                    "and I will provide helpful guidance. To enable live model answers, configure a provider/API key."
                ),
                "sources": [{"content": "Demo default response", "metadata": {"title": "Demo", "source": "demo"}}],
                "error": None
            }
        
        try:
            self.logger.info(f"Processing message: {message[:50]}...")
            
            # Get response from chain
            result = self.chain({"question": message})
            
            # Extract response and sources
            response = result.get("answer", "I'm sorry, I couldn't generate a response.")
            source_documents = result.get("source_documents", [])
            
            # Format sources
            sources = []
            for doc in source_documents:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            self.logger.info("Response generated successfully")
            
            return {
                "response": response,
                "sources": sources,
                "error": None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            
            # Check if it's a quota/rate limit error
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ['quota', 'rate limit', '429', 'insufficient_quota']):
                return {
                    "response": "I'm currently experiencing high demand. Here's a helpful response based on my knowledge: " + 
                               "I can help you with LangChain, Python programming, and AI development questions. " +
                               "For detailed responses, please try again later or check your API quota.",
                    "sources": [{"content": "Fallback response due to quota limits", "metadata": {"title": "System", "source": "fallback"}}],
                    "error": "Quota exceeded - using fallback response"
                }
            
            return {
                "response": "I'm sorry, I encountered an error while processing your message. Please try again.",
                "sources": [],
                "error": str(e)
            }
    
    def search_documents(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vector_store.vector_store:
            self.logger.error("Vector store not available")
            return []
        
        try:
            self.logger.info(f"Searching documents for: {query[:50]}...")
            results = self.vector_store.similarity_search(query, k=k)
            self.logger.info(f"Found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching documents: {e}")
            return []
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add new documents to the knowledge base.
        
        Args:
            documents: List of documents to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Adding {len(documents)} documents to knowledge base...")
            
            # Split documents
            split_docs = self.document_loader.split_documents(documents)
            
            # Add to vector store
            success = self.vector_store.add_documents(split_docs)
            
            if success:
                # Rebuild chain with new documents
                self._setup_chain()
                self.logger.info("Documents added successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error adding documents: {e}")
            return False
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the current chat history.
        
        Returns:
            List of chat messages
        """
        try:
            messages = self.memory.chat_memory.messages
            history = []
            
            for i in range(0, len(messages), 2):
                if i + 1 < len(messages):
                    history.append({
                        "user": messages[i].content,
                        "assistant": messages[i + 1].content
                    })
            
            return history
            
        except Exception as e:
            self.logger.error(f"Error getting chat history: {e}")
            return []
    
    def clear_memory(self):
        """Clear the conversation memory."""
        try:
            self.memory.clear()
            self.logger.info("Chat memory cleared")
        except Exception as e:
            self.logger.error(f"Error clearing memory: {e}")
    
    def get_system_info(self) -> Dict[str, any]:
        """Get information about the chatbot system.
        
        Returns:
            Dictionary with system information
        """
        try:
            vector_store_info = self.vector_store.get_vector_store_info()
            
            return {
                "model_name": config.model_name,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "embedding_model": config.embedding_model,
                "vector_store": vector_store_info,
                "memory_size": len(self.memory.chat_memory.messages),
                "chain_initialized": self.chain is not None
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
    
    def reset(self):
        """Reset the chatbot to initial state."""
        try:
            self.clear_memory()
            self.chain = None
            self.logger.info("Chatbot reset to initial state")
        except Exception as e:
            self.logger.error(f"Error resetting chatbot: {e}")
