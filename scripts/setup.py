#!/usr/bin/env python3
"""Setup script for the LangChain Documentation AI Chatbot."""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories."""
    directories = [
        "data/sources",
        "data/processed",
        "data/vector_store",
        "logs",
        "models/pretrained",
        "models/trained"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print("❌ Python 3.12 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    
    # Install the project in editable mode
    if not run_command("pip install -e .", "Installing project dependencies"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -e .[dev]", "Installing development dependencies"):
        print("⚠️  Warning: Development dependencies installation failed")
    
    return True


def setup_environment():
    """Setup environment configuration."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file")
            print("⚠️  Please edit .env file with your API keys")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  No env.example file found, creating basic .env file...")
        basic_env = """# LangChain Documentation AI Chatbot Configuration

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

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
        try:
            with open(env_file, 'w') as f:
                f.write(basic_env)
            print("✅ Created basic .env file")
            print("⚠️  Please edit .env file with your API keys")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    
    return True


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    return run_command("python -m pytest tests/ -v", "Running test suite")


def setup_knowledge_base():
    """Setup the knowledge base."""
    print("📚 Setting up knowledge base...")
    
    try:
        # Import and setup chatbot
        sys.path.insert(0, str(Path("src")))
        from langchain_documentation_aichatbot.core.chatbot import LangChainChatbot

        chatbot = LangChainChatbot()
        success = chatbot.setup_knowledge_base()

        if success:
            print("✅ Knowledge base setup completed successfully!")
            return True
        else:
            print("❌ Knowledge base setup failed")
            return False

    except Exception as e:
        print(f"❌ Error setting up knowledge base: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Developer-Documentation-Ai-Assistant Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup environment
    print("\n⚙️  Setting up environment...")
    if not setup_environment():
        print("❌ Setup failed during environment setup")
        sys.exit(1)
    
    # Run tests
    print("\n🧪 Running tests...")
    if not run_tests():
        print("⚠️  Tests failed, but continuing with setup")
    
    # Setup knowledge base
    print("\n📚 Setting up knowledge base...")
    if not setup_knowledge_base():
        print("⚠️  Knowledge base setup failed, but you can run it manually later")
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your OpenAI API key")
    print("2. Run the chatbot using one of these methods:")
    print("   - CLI: python -m langchain_documentation_aichatbot.cli chat")
    print("   - Streamlit: streamlit run src/langchain_documentation_aichatbot/apps/streamlit_app.py")
    print("   - Gradio: python -m langchain_documentation_aichatbot.apps.gradio_app")
    print("   - API: uvicorn src.langchain_documentation_aichatbot.apps.api.main:app --reload")
    print("\n📖 For more information, see the README.md file")


if __name__ == "__main__":
    main()
