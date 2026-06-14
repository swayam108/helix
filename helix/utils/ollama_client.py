"""Ollama integration and model management"""

import asyncio
import aiohttp
import json
from typing import Optional, Dict, Any, List
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Unified client for Ollama API"""

    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 300):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.available_models: List[str] = []
        self.default_model = "qwen:32b"

    async def list_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [m["name"] for m in data.get("models", [])]
                        self.available_models = models
                        logger.info(f"Available models: {models}")
                        return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
        return []

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
    ) -> str:
        """Generate text using Ollama model"""
        model = model or self.default_model
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_p": top_p,
                    "stream": False,
                }
                if system:
                    payload["system"] = system
                
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        raise Exception(f"Ollama API error: {response.status}")
        except Exception as e:
            logger.error(f"Error generating with {model}: {e}")
            raise

    async def embeddings(
        self,
        text: str,
        model: str = "nomic-embed-text"
    ) -> List[float]:
        """Generate embeddings for semantic search"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": text,
                }
                async with session.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("embedding", [])
                    else:
                        raise Exception(f"Ollama API error: {response.status}")
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def health_check(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    def route_model(self, task_type: str) -> str:
        """
        Route to best model based on task type.
        Implements intelligent model selection strategy.
        """
        routing = {
            "general_reasoning": "qwen:32b",
            "code_generation": "deepseek-coder:33b",
            "complex_reasoning": "deepseek-r1:32b",
            "fast_response": "phi:latest",
            "research": "llama2:latest",
            "vision": "llava:latest",
        }
        return routing.get(task_type, self.default_model)
