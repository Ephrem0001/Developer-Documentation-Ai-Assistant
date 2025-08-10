"""Vector store operations for the LangChain AI Chatbot."""

import logging
from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from ..utils.config import config


class VectorStore:
    """Handles vector store operations for document retrieval."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vector_store_path = config.vector_store_dir
        self.embedding_model = config.embedding_model
        self.vector_store: Optional[Chroma] = None
        self.embeddings = self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize the embedding model.
        
        Returns:
            Embedding model instance
        """
        try:
            # Try OpenAI embeddings first if API key is available
            if config.openai_api_key:
                self.logger.info("Initializing OpenAI embeddings...")
                return OpenAIEmbeddings(
                    openai_api_key=config.openai_api_key,
                    model="text-embedding-ada-002"
                )
        except Exception as e:
            self.logger.warning(f"Failed to initialize OpenAI embeddings: {e}")
        
        # Fallback to HuggingFace embeddings
        self.logger.info(f"Initializing HuggingFace embeddings: {self.embedding_model}")
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create a new vector store from documents.
        
        Args:
            documents: List of documents to add to vector store
            
        Returns:
            Chroma vector store instance
        """
        self.logger.info(f"Creating vector store with {len(documents)} documents...")
        
        try:
            # Create vector store
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(self.vector_store_path)
            )
            
            # Persist the vector store
            vector_store.persist()
            
            self.vector_store = vector_store
            self.logger.info("Vector store created and persisted successfully")
            
            return vector_store
            
        except Exception as e:
            self.logger.error(f"Error creating vector store: {e}")
            raise
    
    def load_vector_store(self) -> Optional[Chroma]:
        """Load existing vector store from disk.
        
        Returns:
            Chroma vector store instance or None if not found
        """
        try:
            if not self.vector_store_path.exists():
                self.logger.info("No existing vector store found")
                return None
            
            self.logger.info("Loading existing vector store...")
            vector_store = Chroma(
                persist_directory=str(self.vector_store_path),
                embedding_function=self.embeddings
            )
            
            self.vector_store = vector_store
            self.logger.info("Vector store loaded successfully")
            
            return vector_store
            
        except Exception as e:
            self.logger.error(f"Error loading vector store: {e}")
            return None
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to existing vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            True if successful, False otherwise
        """
        if not self.vector_store:
            self.logger.error("No vector store available")
            return False
        
        try:
            self.logger.info(f"Adding {len(documents)} documents to vector store...")
            
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            # Persist changes
            self.vector_store.persist()
            
            self.logger.info("Documents added successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding documents: {e}")
            return False
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[Document]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional filter for metadata
            
        Returns:
            List of similar documents
        """
        if not self.vector_store:
            self.logger.error("No vector store available")
            return []
        
        try:
            self.logger.info(f"Searching for documents similar to: {query[:50]}...")
            
            # Perform similarity search
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter_dict
            )
            
            self.logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            self.logger.error(f"Error performing similarity search: {e}")
            return []
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[tuple[Document, float]]:
        """Search for similar documents with similarity scores.
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional filter for metadata
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vector_store:
            self.logger.error("No vector store available")
            return []
        
        try:
            self.logger.info(f"Searching for documents similar to: {query[:50]}...")
            
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
            
            self.logger.info(f"Found {len(results)} similar documents")
            return results
            
        except Exception as e:
            self.logger.error(f"Error performing similarity search: {e}")
            return []
    
    def get_vector_store_info(self) -> dict:
        """Get information about the vector store.
        
        Returns:
            Dictionary with vector store information
        """
        if not self.vector_store:
            return {"status": "not_initialized"}
        
        try:
            # Get collection info
            collection = self.vector_store._collection
            count = collection.count()
            
            return {
                "status": "initialized",
                "document_count": count,
                "embedding_model": self.embedding_model,
                "persist_directory": str(self.vector_store_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting vector store info: {e}")
            return {"status": "error", "error": str(e)}
    
    def delete_vector_store(self) -> bool:
        """Delete the vector store from disk.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            import shutil
            
            if self.vector_store_path.exists():
                shutil.rmtree(self.vector_store_path)
                self.logger.info("Vector store deleted successfully")
            
            self.vector_store = None
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting vector store: {e}")
            return False
