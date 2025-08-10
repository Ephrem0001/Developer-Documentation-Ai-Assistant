#!/usr/bin/env python3
"""Demo script for the LangChain Documentation AI Chatbot."""

import sys
import time
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langchain_documentation_aichatbot.core.chatbot import LangChainChatbot


def print_header():
    """Print the demo header."""
    print("🤖 LangChain Documentation AI Chatbot Demo")
    print("=" * 60)
    print("This demo showcases the chatbot's capabilities using legitimate")
    print("documentation sources including LangChain, OpenAI, and Python docs.")
    print("=" * 60)
    print()


def print_system_info(chatbot):
    """Print system information."""
    print("📊 System Information:")
    print("-" * 30)
    
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
    
    print()


def demo_chat(chatbot):
    """Demo the chat functionality."""
    print("💬 Chat Demo")
    print("-" * 30)
    
    # Demo questions
    demo_questions = [
        "What is LangChain?",
        "How do I use OpenAI with LangChain?",
        "Explain Python decorators",
        "What are the best practices for prompt engineering?",
        "How do I create a custom LangChain chain?"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("🤖 Answer: ", end="", flush=True)
        
        try:
            response = chatbot.chat(question)
            
            if response["error"]:
                print(f"❌ Error: {response['error']}")
            else:
                print(response["response"])
                
                # Show sources
                if response["sources"]:
                    print(f"\n📚 Sources ({len(response['sources'])}):")
                    for j, source in enumerate(response["sources"], 1):
                        title = source["metadata"].get("title", "Unknown")
                        source_url = source["metadata"].get("source", "Unknown")
                        print(f"   {j}. {title} ({source_url})")
            
            # Add delay between questions
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)


def demo_search(chatbot):
    """Demo the search functionality."""
    print("\n🔍 Search Demo")
    print("-" * 30)
    
    search_queries = [
        "vector stores",
        "memory components",
        "agents and tools",
        "document loaders"
    ]
    
    for i, query in enumerate(search_queries, 1):
        print(f"\n{i}. Searching for: {query}")
        
        try:
            results = chatbot.search_documents(query, k=2)
            
            if not results:
                print("❌ No results found.")
            else:
                print(f"✅ Found {len(results)} results:")
                for j, doc in enumerate(results, 1):
                    print(f"\n   📄 Result {j}:")
                    print(f"      Title: {doc.metadata.get('title', 'Unknown')}")
                    print(f"      Source: {doc.metadata.get('source', 'Unknown')}")
                    print(f"      Content: {doc.page_content[:150]}...")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 30)


def demo_interactive(chatbot):
    """Demo interactive chat."""
    print("\n🎯 Interactive Chat Demo")
    print("-" * 30)
    print("You can now chat with the bot interactively!")
    print("Type 'quit' or 'exit' to end the demo.")
    print("Type 'sources' to see the documentation sources used.")
    print("-" * 30)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Ending demo...")
                break
            
            if user_input.lower() == "sources":
                print("\n📚 Documentation Sources:")
                from langchain_documentation_aichatbot.utils.config import config
                for i, source in enumerate(config.documentation_sources, 1):
                    print(f"   {i}. {source}")
                continue
            
            if not user_input:
                continue
            
            print("🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            
            if response["error"]:
                print(f"❌ Error: {response['error']}")
            else:
                print(response["response"])
                
                # Show sources
                if response["sources"]:
                    print(f"\n📚 Sources ({len(response['sources'])}):")
                    for i, source in enumerate(response["sources"], 1):
                        title = source["metadata"].get("title", "Unknown")
                        source_url = source["metadata"].get("source", "Unknown")
                        print(f"   {i}. {title} ({source_url})")
            
        except KeyboardInterrupt:
            print("\n👋 Ending demo...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main demo function."""
    print_header()
    
    try:
        # Initialize chatbot
        print("🔄 Initializing chatbot...")
        chatbot = LangChainChatbot()
        print("✅ Chatbot initialized successfully!")
        
        # Setup knowledge base
        print("\n📚 Setting up knowledge base...")
        success = chatbot.setup_knowledge_base()
        if not success:
            print("❌ Failed to setup knowledge base")
            print("Please ensure you have:")
            print("1. Set up your OpenAI API key in .env file")
            print("2. Internet connection to fetch documentation")
            return
        
        print("✅ Knowledge base setup completed!")
        
        # Show system info
        print_system_info(chatbot)
        
        # Run demos
        demo_chat(chatbot)
        demo_search(chatbot)
        demo_interactive(chatbot)
        
        print("\n🎉 Demo completed!")
        print("\n💡 You can continue using the chatbot with:")
        print("   - CLI: python src/langchain_documentation_aichatbot/cli.py chat")
        print("   - Streamlit: streamlit run src/langchain_documentation_aichatbot/apps/streamlit_app.py")
        print("   - Gradio: python src/langchain_documentation_aichatbot/apps/gradio_app.py")
        print("   - API: uvicorn src.langchain_documentation_aichatbot.apps.api.main:app --reload")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("\nTroubleshooting:")
        print("1. Check your OpenAI API key in .env file")
        print("2. Ensure you have internet connection")
        print("3. Check the logs for more details")


if __name__ == "__main__":
    main()
