"""Document loading utilities for the LangChain AI Chatbot."""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..utils.config import config
from ..utils.helpers import (
    clean_text,
    create_safe_filename,
    fetch_webpage_content,
    save_document_content,
)


class DocumentLoader:
    """Handles loading and processing documents from various sources."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""],
        )
    
    def load_from_urls(self, urls: List[str]) -> List[Document]:
        """Load documents from a list of URLs.
        
        Args:
            urls: List of URLs to fetch documents from
            
        Returns:
            List of processed documents
        """
        documents = []
        
        for url in urls:
            try:
                self.logger.info(f"Loading document from: {url}")
                
                # Fetch content from URL
                content = fetch_webpage_content(url)
                if not content:
                    self.logger.warning(f"Failed to fetch content from {url}")
                    continue
                
                # Clean the content
                cleaned_content = clean_text(content)
                
                # Create document
                doc = Document(
                    page_content=cleaned_content,
                    metadata={
                        "source": url,
                        "type": "webpage",
                        "title": self._extract_title_from_url(url),
                    }
                )
                
                documents.append(doc)
                self.logger.info(f"Successfully loaded document from {url}")
                
            except Exception as e:
                self.logger.error(f"Error loading document from {url}: {e}")
                continue
        
        return documents
    
    def load_from_files(self, file_paths: List[Path]) -> List[Document]:
        """Load documents from local files.
        
        Args:
            file_paths: List of file paths to load
            
        Returns:
            List of processed documents
        """
        documents = []
        
        for file_path in file_paths:
            try:
                self.logger.info(f"Loading document from: {file_path}")
                
                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Clean the content
                cleaned_content = clean_text(content)
                
                # Create document
                doc = Document(
                    page_content=cleaned_content,
                    metadata={
                        "source": str(file_path),
                        "type": "file",
                        "title": file_path.stem,
                    }
                )
                
                documents.append(doc)
                self.logger.info(f"Successfully loaded document from {file_path}")
                
            except Exception as e:
                self.logger.error(f"Error loading document from {file_path}: {e}")
                continue
        
        return documents
    
    def load_documentation_sources(self) -> List[Document]:
        """Load documents from configured documentation sources.
        
        Returns:
            List of processed documents
        """
        self.logger.info("Loading documentation sources...")
        
        # Load from URLs
        documents = self.load_from_urls(config.documentation_sources)

        # Load extra URLs from file, if present
        try:
            urls_file = config.extra_urls_file
            from pathlib import Path as _P
            p = _P(urls_file)
            if p.exists():
                extra_urls = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")]
                if extra_urls:
                    self.logger.info(f"Loading extra URLs from {p} ({len(extra_urls)})...")
                    documents.extend(self.load_from_urls(extra_urls))
        except Exception as e:
            self.logger.warning(f"Failed to read extra URLs file: {e}")
        
        # Load from local files if they exist
        sources_dir = config.sources_dir
        if sources_dir.exists():
            patterns = getattr(config, "sources_glob", ["*.txt", "*.md"]) or ["*.txt", "*.md"]
            file_paths = []
            for pattern in patterns:
                file_paths.extend(list(sources_dir.rglob(pattern)))
            if file_paths:
                file_docs = self.load_from_files(file_paths)
                documents.extend(file_docs)
        
        self.logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of split documents
        """
        self.logger.info("Splitting documents into chunks...")
        
        split_docs = []
        for doc in documents:
            try:
                # Split the document
                splits = self.text_splitter.split_documents([doc])
                split_docs.extend(splits)
            except Exception as e:
                self.logger.error(f"Error splitting document {doc.metadata.get('source', 'unknown')}: {e}")
                continue
        
        self.logger.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")
        return split_docs
    
    def save_documents_to_files(self, documents: List[Document], output_dir: Path) -> List[Path]:
        """Save documents to files for later use.
        
        Args:
            documents: List of documents to save
            output_dir: Directory to save documents in
            
        Returns:
            List of saved file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_paths = []
        
        for i, doc in enumerate(documents):
            try:
                # Create filename
                source = doc.metadata.get("source", f"document_{i}")
                filename = create_safe_filename(source, ".txt")
                
                # Save document
                file_path = save_document_content(
                    doc.page_content, filename, output_dir
                )
                saved_paths.append(file_path)
                
            except Exception as e:
                self.logger.error(f"Error saving document {i}: {e}")
                continue
        
        self.logger.info(f"Saved {len(saved_paths)} documents to {output_dir}")
        return saved_paths
    
    def _extract_title_from_url(self, url: str) -> str:
        """Extract a title from URL.
        
        Args:
            url: URL to extract title from
            
        Returns:
            Extracted title
        """
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if path:
            # Convert path to title
            title = path.replace("/", " - ").replace("-", " ").title()
            return title
        
        # Use domain as title
        domain = parsed.netloc.replace("www.", "").replace(".", " ").title()
        return domain
