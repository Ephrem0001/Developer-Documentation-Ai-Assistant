"""Professional CLI for managing LLM providers and API keys."""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from .core.llm_factory import llm_factory
from .utils.config import config


def setup_provider(provider: str, api_key: str, api_url: Optional[str] = None) -> bool:
    """Set up a provider with API key.
    
    Args:
        provider: Provider name (openai, grok, etc.)
        api_key: API key for the provider
        api_url: Optional API URL (for custom endpoints)
        
    Returns:
        True if successful, False otherwise
    """
    env_file = Path(".env")
    
    # Read existing .env file
    env_content = ""
    if env_file.exists():
        with open(env_file, "r") as f:
            env_content = f.read()
    
    # Update or add API key
    key_var = f"{provider.upper()}_API_KEY"
    new_line = f"{key_var}={api_key}\n"
    
    # Check if key already exists
    lines = env_content.split("\n")
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith(f"{key_var}="):
            lines[i] = new_line.strip()
            updated = True
            break
    
    if not updated:
        lines.append(new_line.strip())
    
    # Add API URL if provided
    if api_url and provider == "grok":
        url_var = "GROK_API_URL"
        url_line = f"{url_var}={api_url}\n"
        
        url_updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{url_var}="):
                lines[i] = url_line.strip()
                url_updated = True
                break
        
        if not url_updated:
            lines.append(url_line.strip())
    
    # Write back to .env file
    try:
        with open(env_file, "w") as f:
            f.write("\n".join(lines))
        
        print(f"✅ Successfully configured {provider.upper()} API key")
        return True
    except Exception as e:
        print(f"❌ Error writing to .env file: {e}")
        return False


def list_providers() -> None:
    """List all available providers and their status."""
    print("🔧 LLM Provider Status")
    print("=" * 50)
    
    provider_info = llm_factory.get_provider_info()
    
    for provider, info in provider_info.items():
        status = "✅ Available" if info["available"] else "❌ Not Available"
        print(f"{provider.upper():<15} {status}")
        if not info["available"]:
            print(f"              Set {info['config_key']} in .env file")
        print()


def test_provider(provider: str) -> bool:
    """Test a provider by attempting to create an LLM.
    
    Args:
        provider: Provider name to test
        
    Returns:
        True if successful, False otherwise
    """
    print(f"🧪 Testing {provider.upper()} provider...")
    
    llm = llm_factory.create_llm(provider)
    if llm:
        print(f"✅ {provider.upper()} provider is working correctly!")
        return True
    else:
        print(f"❌ {provider.upper()} provider is not available or configured incorrectly")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Professional LLM Provider Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all providers
  python -m langchain_documentation_aichatbot.cli_provider list
  
  # Set up OpenAI
  python -m langchain_documentation_aichatbot.cli_provider setup openai YOUR_API_KEY
  
  # Set up Grok
  python -m langchain_documentation_aichatbot.cli_provider setup grok YOUR_API_KEY
  
  # Test a provider
  python -m langchain_documentation_aichatbot.cli_provider test openai
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all providers and their status")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Set up a provider with API key")
    setup_parser.add_argument("provider", choices=["openai", "grok"], help="Provider to set up")
    setup_parser.add_argument("api_key", help="API key for the provider")
    setup_parser.add_argument("--api-url", help="Custom API URL (for Grok)")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test a provider")
    test_parser.add_argument("provider", choices=["openai", "grok"], help="Provider to test")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "list":
        list_providers()
    
    elif args.command == "setup":
        success = setup_provider(args.provider, args.api_key, args.api_url)
        if success:
            print(f"\n💡 To use {args.provider.upper()}, set MODEL_PROVIDER={args.provider} in your .env file")
    
    elif args.command == "test":
        test_provider(args.provider)


if __name__ == "__main__":
    main()
