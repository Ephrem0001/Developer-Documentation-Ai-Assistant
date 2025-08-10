"""LLM Factory for managing different language model providers."""

import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel

from ..utils.config import config


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def create_llm(self) -> Optional[BaseLanguageModel]:
        """Create and return an LLM instance."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available (has API key)."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def is_available(self) -> bool:
        return bool(config.openai_api_key)
    
    def create_llm(self) -> Optional[BaseLanguageModel]:
        if not self.is_available():
            return None
        
        try:
            model = config.model_name or "gpt-4o-mini"
            return ChatOpenAI(
                api_key=config.openai_api_key,
                model=model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
        except Exception as e:
            logging.error(f"Error creating OpenAI LLM: {e}")
            return None


class GrokProvider(LLMProvider):
    """Grok LLM provider."""
    
    def is_available(self) -> bool:
        return bool(config.grok_api_key)
    
    def create_llm(self) -> Optional[BaseLanguageModel]:
        if not self.is_available():
            return None
        
        try:
            model = config.grok_model or "grok-beta"
            # Grok uses OpenAI-compatible API
            return ChatOpenAI(
                api_key=config.grok_api_key,
                model=model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                base_url=config.grok_api_url,
            )
        except Exception as e:
            logging.error(f"Error creating Grok LLM: {e}")
            return None


class DemoProvider(LLMProvider):
    """Demo provider that disables live LLM calls.

    When selected, no real LLM is created so the chatbot will operate
    exclusively using its built-in mock responses. This is useful for demos
    and development without incurring API usage or requiring keys.
    """

    def is_available(self) -> bool:
        # Always available because it requires no credentials
        return True

    def create_llm(self) -> Optional[BaseLanguageModel]:
        # Returning None tells the chatbot to use mock responses
        return None

class LLMFactory:
    """Factory for creating LLM instances based on configuration."""
    
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {
            "openai": OpenAIProvider(),
            "grok": GrokProvider(),
            "demo": DemoProvider(),
        }
        self.logger = logging.getLogger(__name__)
    
    def get_available_providers(self) -> list[str]:
        """Get list of available providers."""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def create_llm(self, provider: Optional[str] = None) -> Optional[BaseLanguageModel]:
        """Create an LLM instance.
        
        Args:
            provider: Provider name. If None, uses config.model_provider
            
        Returns:
            LLM instance or None if not available
        """
        if provider is None:
            provider = config.model_provider
        
        if provider not in self.providers:
            self.logger.error(f"Unknown provider: {provider}")
            return None
        
        provider_instance = self.providers[provider]
        
        if not provider_instance.is_available():
            self.logger.warning(f"Provider {provider} is not available (no API key)")
            return None
        
        llm = provider_instance.create_llm()
        if llm:
            self.logger.info(f"Successfully created LLM with provider: {provider}")
        else:
            self.logger.error(f"Failed to create LLM with provider: {provider}")
        
        return llm
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about all providers."""
        info = {}
        for name, provider in self.providers.items():
            info[name] = {
                "available": provider.is_available(),
                "config_key": f"{name.upper()}_API_KEY"
            }
        return info


# Global factory instance
llm_factory = LLMFactory()
