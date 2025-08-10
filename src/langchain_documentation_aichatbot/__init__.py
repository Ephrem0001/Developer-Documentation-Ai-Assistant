"""LangChain Documentation AI Chatbot Package."""

__version__ = "0.1.0"
__author__ = "Ephrem0001"
__email__ = "ephrem8118@gmail.com"

from .core.chatbot import LangChainChatbot
from .utils.config import Config

__all__ = ["LangChainChatbot", "Config"]
