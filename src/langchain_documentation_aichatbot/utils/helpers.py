"""Helper utility functions for the LangChain AI Chatbot."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Log message format
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("langchain_chatbot")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def validate_api_key(api_key: str) -> bool:
    """Validate API key format and availability.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation - check if it's not empty and has reasonable length
    if len(api_key) < 10:
        return False
    
    # Check if it starts with expected prefixes
    valid_prefixes = ["sk-", "pk-", "rk-"]
    if not any(api_key.startswith(prefix) for prefix in valid_prefixes):
        return False
    
    return True


def fetch_webpage_content(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch content from a webpage.
    
    Args:
        url: The URL to fetch content from
        timeout: Request timeout in seconds
        
    Returns:
        Extracted text content or None if failed
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = " ".join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        logging.error(f"Failed to fetch content from {url}: {e}")
        return None


def save_document_content(content: str, filename: str, output_dir: Path) -> Path:
    """Save document content to a file.
    
    Args:
        content: The content to save
        filename: The filename to save as
        output_dir: The output directory
        
    Returns:
        Path to the saved file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path


def load_document_content(file_path: Path) -> Optional[str]:
    """Load document content from a file.
    
    Args:
        file_path: Path to the file to load
        
    Returns:
        File content or None if failed
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Failed to load content from {file_path}: {e}")
        return None


def clean_text(text: str) -> str:
    """Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    import re
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r"[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]", "", text)
    
    # Normalize line breaks
    text = text.replace("\n", " ").replace("\r", " ")
    
    return text.strip()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings
            for i in range(end, max(start + chunk_size // 2, end - 100), -1):
                if text[i] in ".!?":
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks


def get_file_extension(url: str) -> str:
    """Extract file extension from URL.
    
    Args:
        url: URL to extract extension from
        
    Returns:
        File extension (with dot) or empty string
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    path = parsed.path
    
    # Extract extension
    if "." in path:
        return "." + path.split(".")[-1]
    
    return ""


def create_safe_filename(url: str, extension: str = ".txt") -> str:
    """Create a safe filename from URL.
    
    Args:
        url: URL to create filename from
        extension: File extension to append
        
    Returns:
        Safe filename
    """
    import re
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_")
    path = parsed.path.replace("/", "_").replace("-", "_")
    
    # Remove special characters
    filename = re.sub(r"[^\w_]", "", domain + path)
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename + extension
