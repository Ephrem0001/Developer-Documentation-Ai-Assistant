#!/usr/bin/env python3
"""Update .env file with the provided OpenAI API key."""

import os

def update_env_file():
    """Update .env file with the OpenAI API key."""
    
    env_content = """# Developer Documentation AI Assistant Configuration

# LLM Provider Configuration
MODEL_PROVIDER=openai

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LangChain Configuration (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=developer-documentation-ai-assistant

# Model Configuration
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000

# Vector Store Configuration
VECTOR_STORE_PATH=./data/vector_store
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/chatbot.log

# Web Interface
HOST=0.0.0.0
PORT=8000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file updated with OpenAI API key")
    print("🚀 Ready to start the application with GPT support!")

if __name__ == "__main__":
    update_env_file()
