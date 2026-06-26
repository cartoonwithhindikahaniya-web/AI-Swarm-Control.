import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, model: Optional[str] = None):
        self.name = name
        self.role = role

        # Provider configuration
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if self.provider == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.base_url = "https://api.deepseek.com"
            self.model = model or "deepseek-reasoner" # Default to R1
        else:
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = None # Default OpenAI
            self.model = model or "gpt-4o"

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @abstractmethod
    def run(self, task: str) -> str:
        """Execute the assigned task."""
        pass

    def _get_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Internal method to get LLM completion."""
        try:
            # DeepSeek reasoner doesn't support temperature
            params = {
                "model": self.model,
                "messages": messages,
            }
            if self.model != "deepseek-reasoner":
                params["temperature"] = temperature

            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM ({self.provider}): {str(e)}"

    def __repr__(self):
        return f"{self.name} ({self.role}) [{self.provider}]"
