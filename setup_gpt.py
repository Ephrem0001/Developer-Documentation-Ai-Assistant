#!/usr/bin/env python3
"""Setup script to configure GPT API for the Developer Documentation AI Assistant."""

import os
import sys
from pathlib import Path

def setup_gpt_environment():
    """Set up environment variables for GPT API."""
    
    print("🤖 Developer Documentation AI Assistant - GPT Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=your_openai_api_key_here" in content:
                print("⚠️  Please update your OpenAI API key in the .env file")
                print("   Edit .env and replace 'your_openai_api_key_here' with your actual API key")
            else:
                print("✅ .env file appears to be configured")
    else:
        print("📝 Creating .env file...")
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
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env and add your OpenAI API key")
    
    # Set environment variables for current session
    os.environ["MODEL_PROVIDER"] = "openai"
    os.environ["MODEL_NAME"] = "gpt-3.5-turbo"
    
    print("\n📋 Next Steps:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Edit the .env file and replace 'your_openai_api_key_here' with your actual key")
    print("3. Restart the Streamlit application")
    print("\n🚀 To start the application:")
    print("   streamlit run src/langchain_documentation_aichatbot/apps/streamlit_app.py")

if __name__ == "__main__":
    setup_gpt_environment()
