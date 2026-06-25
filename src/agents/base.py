import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, model: str = "gpt-4o"):
        self.name = name
        self.role = role
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @abstractmethod
    def run(self, task: str) -> str:
        """Execute the assigned task."""
        pass

    def _get_completion(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Internal method to get LLM completion."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"

    def __repr__(self):
        return f"{self.name} ({self.role})"
