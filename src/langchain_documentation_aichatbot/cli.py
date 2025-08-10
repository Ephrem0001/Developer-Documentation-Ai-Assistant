#!/usr/bin/env python3
"""Command-line interface for the LangChain AI Chatbot."""

import argparse
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_documentation_aichatbot.core.chatbot import LangChainChatbot
from langchain_documentation_aichatbot.utils.config import config
from langchain_documentation_aichatbot.utils.helpers import setup_logging


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="LangChain Documentation AI Chatbot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive chat mode
  python cli.py chat

  # Setup knowledge base
  python cli.py setup

  # Search documents
  python cli.py search "What is LangChain?"

  # Get system info
  python cli.py info

  # Reset chatbot
  python cli.py reset
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument(
        "--model", 
        default=config.model_name,
        help="Model to use for chat"
    )
    chat_parser.add_argument(
        "--temperature", 
        type=float, 
        default=config.temperature,
        help="Temperature for response generation"
    )
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup knowledge base")
    setup_parser.add_argument(
        "--force-rebuild", 
        action="store_true",
        help="Force rebuild the vector store"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "-k", 
        type=int, 
        default=4,
        help="Number of results to return"
    )
    
    # Info command
    subparsers.add_parser("info", help="Get system information")
    
    # Reset command
    subparsers.add_parser("reset", help="Reset chatbot")
    
    # Clear command
    subparsers.add_parser("clear", help="Clear chat memory")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logging
    logger = setup_logging(level=config.log_level, log_file=config.log_file)
    
    try:
        # Initialize chatbot
        logger.info("Initializing chatbot...")
        chatbot = LangChainChatbot()
        
        if args.command == "chat":
            run_chat_mode(chatbot, args)
        elif args.command == "setup":
            run_setup_mode(chatbot, args)
        elif args.command == "search":
            run_search_mode(chatbot, args)
        elif args.command == "info":
            run_info_mode(chatbot)
        elif args.command == "reset":
            run_reset_mode(chatbot)
        elif args.command == "clear":
            run_clear_mode(chatbot)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


def run_chat_mode(chatbot: LangChainChatbot, args):
    """Run interactive chat mode."""
    print("🤖 LangChain Documentation AI Chatbot")
    print("=" * 50)
    
    # Setup knowledge base if not already done
    if not chatbot.chain:
        print("📚 Setting up knowledge base...")
        success = chatbot.setup_knowledge_base()
        if not success:
            print("❌ Failed to setup knowledge base")
            return
    
    print("✅ Ready to chat! Type 'quit' or 'exit' to leave.")
    print("💡 Ask me anything about LangChain, OpenAI, or Python!")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Get response
            print("🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            
            if response["error"]:
                print(f"❌ Error: {response['error']}")
            else:
                print(response["response"])
                
                # Show sources if available
                if response["sources"]:
                    print("\n📚 Sources:")
                    for i, source in enumerate(response["sources"], 1):
                        title = source["metadata"].get("title", "Unknown")
                        source_url = source["metadata"].get("source", "Unknown")
                        print(f"  {i}. {title} ({source_url})")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def run_setup_mode(chatbot: LangChainChatbot, args):
    """Run setup mode."""
    print("📚 Setting up knowledge base...")
    
    success = chatbot.setup_knowledge_base(force_rebuild=args.force_rebuild)
    
    if success:
        print("✅ Knowledge base setup completed successfully!")
        
        # Show system info
        info = chatbot.get_system_info()
        print(f"\n📊 System Information:")
        print(f"  • Model: {info.get('model_name', 'Unknown')}")
        print(f"  • Temperature: {info.get('temperature', 'Unknown')}")
        print(f"  • Max Tokens: {info.get('max_tokens', 'Unknown')}")
        print(f"  • Embedding Model: {info.get('embedding_model', 'Unknown')}")
        
        vector_store = info.get('vector_store', {})
        if vector_store.get('status') == 'initialized':
            print(f"  • Vector Store Documents: {vector_store.get('document_count', 'Unknown')}")
    else:
        print("❌ Failed to setup knowledge base")


def run_search_mode(chatbot: LangChainChatbot, args):
    """Run search mode."""
    print(f"🔍 Searching for: {args.query}")
    
    if not chatbot.vector_store.vector_store:
        print("❌ Vector store not available. Please setup first.")
        return
    
    results = chatbot.search_documents(args.query, args.k)
    
    if not results:
        print("❌ No results found.")
        return
    
    print(f"✅ Found {len(results)} results:")
    print("-" * 50)
    
    for i, doc in enumerate(results, 1):
        print(f"\n📄 Result {i}:")
        print(f"  Title: {doc.metadata.get('title', 'Unknown')}")
        print(f"  Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"  Content: {doc.page_content[:200]}...")
        print("-" * 30)


def run_info_mode(chatbot: LangChainChatbot):
    """Run info mode."""
    print("📊 System Information:")
    print("=" * 50)
    
    info = chatbot.get_system_info()
    
    if "error" in info:
        print(f"❌ Error: {info['error']}")
        return
    
    print(f"🤖 Model: {info.get('model_name', 'Unknown')}")
    print(f"🌡️  Temperature: {info.get('temperature', 'Unknown')}")
    print(f"📝 Max Tokens: {info.get('max_tokens', 'Unknown')}")
    print(f"🔤 Embedding Model: {info.get('embedding_model', 'Unknown')}")
    print(f"💾 Memory Size: {info.get('memory_size', 'Unknown')}")
    print(f"🔗 Chain Initialized: {info.get('chain_initialized', 'Unknown')}")
    
    vector_store = info.get('vector_store', {})
    print(f"\n📚 Vector Store:")
    print(f"  Status: {vector_store.get('status', 'Unknown')}")
    if vector_store.get('status') == 'initialized':
        print(f"  Documents: {vector_store.get('document_count', 'Unknown')}")
        print(f"  Directory: {vector_store.get('persist_directory', 'Unknown')}")


def run_reset_mode(chatbot: LangChainChatbot):
    """Run reset mode."""
    print("🔄 Resetting chatbot...")
    chatbot.reset()
    print("✅ Chatbot reset successfully!")


def run_clear_mode(chatbot: LangChainChatbot):
    """Run clear mode."""
    print("🗑️  Clearing chat memory...")
    chatbot.clear_memory()
    print("✅ Chat memory cleared successfully!")


if __name__ == "__main__":
    main()
