"""Gradio web application for the LangChain AI Chatbot."""

import gradio as gr
from typing import List, Tuple

from ..core.chatbot import LangChainChatbot


def create_gradio_app():
    """Create and launch the Gradio application."""
    
    # Initialize chatbot
    chatbot = LangChainChatbot()
    
    def setup_knowledge_base(force_rebuild: bool) -> str:
        """Setup the knowledge base."""
        try:
            success = chatbot.setup_knowledge_base(force_rebuild=force_rebuild)
            if success:
                return "✅ Knowledge base setup completed successfully!"
            else:
                return "❌ Failed to setup knowledge base"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def chat_with_bot(message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """Chat with the bot."""
        if not chatbot.chain:
            return "⚠️ Please setup the knowledge base first.", history
        
        try:
            # Get response from chatbot
            response = chatbot.chat(message)
            
            if response["error"]:
                return f"❌ Error: {response['error']}", history
            
            # Format response with sources
            formatted_response = response["response"]
            if response["sources"]:
                formatted_response += "\n\n📚 **Sources:**\n"
                for i, source in enumerate(response["sources"], 1):
                    title = source["metadata"].get("title", "Unknown")
                    source_url = source["metadata"].get("source", "Unknown")
                    formatted_response += f"{i}. {title} ({source_url})\n"
            
            return formatted_response, history + [[message, formatted_response]]
            
        except Exception as e:
            return f"❌ Error: {str(e)}", history
    
    def get_system_info() -> str:
        """Get system information."""
        try:
            info = chatbot.get_system_info()
            if "error" in info:
                return f"❌ Error: {info['error']}"
            
            info_text = "📊 **System Information:**\n"
            info_text += f"• Model: {info.get('model_name', 'Unknown')}\n"
            info_text += f"• Temperature: {info.get('temperature', 'Unknown')}\n"
            info_text += f"• Max Tokens: {info.get('max_tokens', 'Unknown')}\n"
            info_text += f"• Embedding Model: {info.get('embedding_model', 'Unknown')}\n"
            info_text += f"• Memory Size: {info.get('memory_size', 'Unknown')}\n"
            info_text += f"• Chain Initialized: {info.get('chain_initialized', 'Unknown')}\n"
            
            vector_store = info.get('vector_store', {})
            if vector_store.get('status') == 'initialized':
                info_text += f"• Vector Store Documents: {vector_store.get('document_count', 'Unknown')}\n"
            
            return info_text
            
        except Exception as e:
            return f"❌ Error getting system info: {str(e)}"
    
    def clear_chat() -> Tuple[str, List[List[str]]]:
        """Clear the chat history."""
        try:
            chatbot.clear_memory()
            return "🗑️ Chat history cleared!", []
        except Exception as e:
            return f"❌ Error clearing chat: {str(e)}", []
    
    def reset_chatbot() -> str:
        """Reset the chatbot."""
        try:
            chatbot.reset()
            return "🔄 Chatbot reset successfully!"
        except Exception as e:
            return f"❌ Error resetting chatbot: {str(e)}"
    
    # Create Gradio interface
    with gr.Blocks(
        title="LangChain Documentation AI Chatbot",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        """
    ) as demo:
        gr.Markdown(
            """
            # 🤖 LangChain Documentation AI Chatbot
            
            This chatbot uses legitimate documentation sources including LangChain docs, OpenAI docs, and Python documentation to provide accurate and helpful responses.
            
            ## Features
            - 📚 Documentation-based responses
            - 🔍 Source attribution
            - 💾 Conversation memory
            - ⚙️ Configurable settings
            
            ## Getting Started
            1. Click "Setup Knowledge Base" to initialize the system
            2. Start chatting with the bot
            3. View sources for each response
            """
        )
        
        with gr.Row():
            with gr.Column(scale=3):
                # Chat interface
                chatbot_interface = gr.ChatInterface(
                    fn=chat_with_bot,
                    title="💬 Chat Interface",
                    description="Ask me anything about LangChain, OpenAI, or Python...",
                    examples=[
                        ["What is LangChain?"],
                        ["How do I use OpenAI with LangChain?"],
                        ["Explain Python decorators"],
                        ["What are the best practices for prompt engineering?"],
                        ["How do I create a custom LangChain chain?"]
                    ]
                )
            
            with gr.Column(scale=1):
                # Control panel
                gr.Markdown("### ⚙️ Control Panel")
                
                # Knowledge base setup
                gr.Markdown("#### 📚 Knowledge Base")
                setup_btn = gr.Button("Setup Knowledge Base", variant="primary")
                rebuild_btn = gr.Button("Force Rebuild", variant="secondary")
                setup_output = gr.Textbox(label="Setup Status", interactive=False)
                
                setup_btn.click(
                    fn=lambda: setup_knowledge_base(False),
                    outputs=setup_output
                )
                rebuild_btn.click(
                    fn=lambda: setup_knowledge_base(True),
                    outputs=setup_output
                )
                
                # System information
                gr.Markdown("#### 📊 System Information")
                info_btn = gr.Button("Get System Info")
                info_output = gr.Textbox(label="System Info", interactive=False, lines=10)
                
                info_btn.click(fn=get_system_info, outputs=info_output)
                
                # Actions
                gr.Markdown("#### 🔧 Actions")
                clear_btn = gr.Button("Clear Chat History", variant="secondary")
                reset_btn = gr.Button("Reset Chatbot", variant="secondary")
                
                clear_btn.click(
                    fn=clear_chat,
                    outputs=[gr.Textbox(label="Status"), chatbot_interface.chatbot]
                )
                reset_btn.click(fn=reset_chatbot, outputs=gr.Textbox(label="Status"))
        
        # Footer
        gr.Markdown(
            """
            ---
            **Powered by:** LangChain, OpenAI, and legitimate documentation sources
            
            **Built with ❤️ for accurate and helpful AI assistance**
            """
        )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_app()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
