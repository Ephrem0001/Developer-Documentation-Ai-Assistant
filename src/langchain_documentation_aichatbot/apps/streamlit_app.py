"""Streamlit web application for the LangChain AI Chatbot."""

import streamlit as st
from typing import Dict, List

from langchain_documentation_aichatbot.core.chatbot import LangChainChatbot
from langchain_documentation_aichatbot.utils.config import config


def create_streamlit_app():
    """Create and run the Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="LangChain Documentation AI Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .source-info {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background-color: #f5f5f5;
        border-radius: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">Developer Documentation Ai-Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model settings
        st.subheader("Model Settings")
        model_name = st.selectbox(
            "Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens", 100, 2000, 1000, 100)
        
        # Vector store settings
        st.subheader("Vector Store Settings")
        k_results = st.slider("Number of Results", 1, 10, 4, 1)
        
        # System info
        st.subheader("System Information")
        if 'chatbot' in st.session_state:
            system_info = st.session_state.chatbot.get_system_info()
            st.json(system_info)
        
        # Actions
        st.subheader("Actions")
        if st.button("🔄 Reset Chat"):
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.reset()
                st.session_state.messages = []
                st.success("Chat reset successfully!")
        
        if st.button("🗑️ Clear Memory"):
            if 'chatbot' in st.session_state:
                st.session_state.chatbot.clear_memory()
                st.success("Memory cleared successfully!")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner("Initializing chatbot..."):
            try:
                st.session_state.chatbot = LangChainChatbot()
                st.success("Chatbot initialized successfully!")
            except Exception as e:
                st.error(f"Error initializing chatbot: {e}")
                return
    
    # Auto-setup knowledge base on first run
    if 'kb_attempted' not in st.session_state:
        with st.spinner("Setting up knowledge base..."):
            try:
                kb_success = st.session_state.chatbot.setup_knowledge_base()
                st.session_state.kb_attempted = True
                if kb_success and st.session_state.chatbot.chain is not None:
                    st.success("Knowledge base setup completed!")
                    st.rerun()
            except Exception as e:
                st.warning(f"Knowledge base auto-setup skipped: {e}")
                st.session_state.kb_attempted = True

    # Initialize messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Knowledge base setup UI (only blocks when an LLM is available but chain not built)
    if not st.session_state.chatbot.chain:
        if st.session_state.chatbot.llm is None:
            # Demo mode: allow chatting with mock responses, don't block UI
            st.info("Demo mode active: Using mock responses. You can chat below. Knowledge base has been indexed for search.")
        else:
            st.warning("⚠️ Knowledge base not initialized. Please set it up first.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📚 Setup Knowledge Base"):
                    with st.spinner("Setting up knowledge base..."):
                        success = st.session_state.chatbot.setup_knowledge_base()
                        if success:
                            st.success("Knowledge base setup completed!")
                            st.rerun()
                        else:
                            st.error("Failed to setup knowledge base")
            
            with col2:
                if st.button("🔄 Force Rebuild"):
                    with st.spinner("Rebuilding knowledge base..."):
                        success = st.session_state.chatbot.setup_knowledge_base(force_rebuild=True)
                        if success:
                            st.success("Knowledge base rebuilt successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to rebuild knowledge base")
            st.info("The chatbot uses legitimate documentation sources including LangChain docs, OpenAI docs, and Python documentation.")
            return
    
    # Chat interface
    st.subheader("💬 Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.markdown(f"**Source {i+1}:**")
                        st.markdown(f"**Title:** {source['metadata'].get('title', 'Unknown')}")
                        st.markdown(f"**Source:** {source['metadata'].get('source', 'Unknown')}")
                        st.markdown(f"**Content:** {source['content']}")
                        st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about LangChain, OpenAI, or Python..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chatbot.chat(prompt)
                    
                    if response["error"]:
                        st.error(f"Error: {response['error']}")
                    else:
                        st.markdown(response["response"])
                        
                        # Display sources
                        if response["sources"]:
                            with st.expander("📚 Sources"):
                                for i, source in enumerate(response["sources"]):
                                    st.markdown(f"**Source {i+1}:**")
                                    st.markdown(f"**Title:** {source['metadata'].get('title', 'Unknown')}")
                                    st.markdown(f"**Source:** {source['metadata'].get('source', 'Unknown')}")
                                    st.markdown(f"**Content:** {source['content']}")
                                    st.divider()
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["response"],
                        "sources": response["sources"]
                    })
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>Powered by LangChain, OpenAI, and legitimate documentation sources</p>
        <p>Built with ❤️ for accurate and helpful AI assistance</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    create_streamlit_app()
