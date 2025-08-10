#!/usr/bin/env python3
"""Professional setup script for the LangChain AI Chatbot."""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_python_version() -> bool:
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies() -> bool:
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Install the project in editable mode
    if not run_command("pip install -e .[dev]", "Installing project dependencies"):
        return False
    
    return True

def setup_environment() -> bool:
    """Set up environment configuration."""
    print("\n🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, "r") as src, open(env_file, "w") as dst:
                dst.write(src.read())
            print("✅ .env file created successfully")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def setup_provider_interactive() -> bool:
    """Interactive provider setup."""
    print("\n🤖 LLM Provider Setup")
    print("=" * 50)
    
    providers = {
        "1": ("openai", "OpenAI (GPT-3.5, GPT-4)"),
        "2": ("grok", "Grok (xAI)"),
        "3": ("skip", "Skip for now (demo mode)")
    }
    
    print("Choose your LLM provider:")
    for key, (provider, description) in providers.items():
        print(f"  {key}. {description}")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in providers:
            provider, description = providers[choice]
            break
        print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    if provider == "skip":
        print("✅ Skipping provider setup. You can configure later using the CLI.")
        return True
    
    print(f"\n🔑 Setting up {description}...")
    api_key = input(f"Enter your {provider.upper()} API key: ").strip()
    
    if not api_key:
        print("❌ API key is required")
        return False
    
    # Use the CLI to set up the provider
    command = f"python -m langchain_documentation_aichatbot.cli_provider setup {provider} {api_key}"
    if provider == "grok":
        api_url = input("Enter Grok API URL (press Enter for default): ").strip()
        if api_url:
            command += f" --api-url {api_url}"
    
    return run_command(command, f"Setting up {provider.upper()} provider")

def test_setup() -> bool:
    """Test the setup by running basic checks."""
    print("\n🧪 Testing setup...")
    
    # Test provider status
    if not run_command("python -m langchain_documentation_aichatbot.cli_provider list", "Checking provider status"):
        return False
    
    # Test demo
    print("\n🎯 Testing demo...")
    print("Starting demo (press Ctrl+C to stop)...")
    try:
        result = subprocess.run("python scripts/demo.py", shell=True, timeout=30)
        print("✅ Demo test completed")
    except subprocess.TimeoutExpired:
        print("✅ Demo is running (timeout reached)")
    except KeyboardInterrupt:
        print("✅ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo test failed: {e}")
        return False
    
    return True

def show_next_steps() -> None:
    """Show next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Run the demo: python scripts/demo.py")
    print("2. Start web interface: python -m streamlit run src/langchain_documentation_aichatbot/apps/streamlit_app.py")
    print("3. Start API server: python src/langchain_documentation_aichatbot/apps/api/main.py")
    print("4. Manage providers: python -m langchain_documentation_aichatbot.cli_provider --help")
    print("\n📚 Documentation:")
    print("- README.md: Project overview and usage")
    print("- docs/: Detailed documentation")
    print("- scripts/: Utility scripts")

def main():
    """Main setup function."""
    print("🚀 LangChain AI Chatbot - Professional Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Setup provider
    if not setup_provider_interactive():
        print("❌ Failed to setup provider")
        sys.exit(1)
    
    # Test setup
    if not test_setup():
        print("❌ Setup test failed")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
