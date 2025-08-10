"""FastAPI server for the LangChain AI Chatbot."""

from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ...core.chatbot import LangChainChatbot
from ...utils.config import config


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, any]]
    error: Optional[str] = None


class SystemInfoResponse(BaseModel):
    model_name: str
    temperature: float
    max_tokens: int
    embedding_model: str
    vector_store: Dict[str, any]
    memory_size: int
    chain_initialized: bool


class SetupRequest(BaseModel):
    force_rebuild: bool = False


class SetupResponse(BaseModel):
    success: bool
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="LangChain Documentation AI Chatbot API",
    description="API for the LangChain AI Chatbot with legitimate documentation sources",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot: Optional[LangChainChatbot] = None


def get_chatbot() -> LangChainChatbot:
    """Get or create the chatbot instance."""
    global chatbot
    if chatbot is None:
        chatbot = LangChainChatbot()
    return chatbot


@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup."""
    global chatbot
    try:
        chatbot = LangChainChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LangChain Documentation AI Chatbot API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        bot = get_chatbot()
        return {
            "status": "healthy",
            "chatbot_initialized": bot is not None,
            "chain_initialized": bot.chain is not None if bot else False
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/setup", response_model=SetupResponse)
async def setup_knowledge_base(request: SetupRequest):
    """Setup the knowledge base."""
    try:
        bot = get_chatbot()
        success = bot.setup_knowledge_base(force_rebuild=request.force_rebuild)
        
        if success:
            return SetupResponse(
                success=True,
                message="Knowledge base setup completed successfully!"
            )
        else:
            return SetupResponse(
                success=False,
                message="Failed to setup knowledge base"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the bot."""
    try:
        bot = get_chatbot()
        
        if not bot.chain:
            raise HTTPException(
                status_code=400,
                detail="Knowledge base not initialized. Please setup first."
            )
        
        # Get response from chatbot
        result = bot.chat(request.message)
        
        if result["error"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            error=result["error"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def search_documents(query: str, k: int = 4):
    """Search for relevant documents."""
    try:
        bot = get_chatbot()
        
        if not bot.vector_store.vector_store:
            raise HTTPException(
                status_code=400,
                detail="Vector store not available"
            )
        
        results = bot.search_documents(query, k)
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/system-info", response_model=SystemInfoResponse)
async def get_system_info():
    """Get system information."""
    try:
        bot = get_chatbot()
        info = bot.get_system_info()
        
        if "error" in info:
            raise HTTPException(status_code=500, detail=info["error"])
        
        return SystemInfoResponse(**info)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat-history")
async def get_chat_history():
    """Get the current chat history."""
    try:
        bot = get_chatbot()
        history = bot.get_chat_history()
        return {"history": history}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear-memory")
async def clear_memory():
    """Clear the conversation memory."""
    try:
        bot = get_chatbot()
        bot.clear_memory()
        return {"message": "Memory cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_chatbot():
    """Reset the chatbot."""
    try:
        bot = get_chatbot()
        bot.reset()
        return {"message": "Chatbot reset successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/docs")
async def get_documentation_sources():
    """Get the list of documentation sources."""
    return {
        "sources": config.documentation_sources,
        "description": "Legitimate documentation sources used by the chatbot"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=True,
        log_level="info"
    )
