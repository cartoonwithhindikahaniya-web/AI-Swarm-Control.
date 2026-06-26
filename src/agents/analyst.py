from typing import List, Dict, Any, Optional
from src.agents.base import BaseAgent
from src.tools.crypto_tools import get_crypto_price, get_market_data

class CryptoAnalystAgent(BaseAgent):
    def __init__(self, name: str = "Analyst", model: Optional[str] = None):
        super().__init__(name, "Crypto Market Analyst", model)

    def run(self, task: str) -> str:
        print(f"[{self.name}] Analyzing crypto project/market: {task}")

        # 1. Attempt to extract symbol or project from task (simplified)
        # In a real scenario, we'd use LLM to extract the project name
        extraction_prompt = f"Extract the cryptocurrency symbol or name from this task: '{task}'. Return ONLY the symbol/name."
        project = self._get_completion([{"role": "user", "content": extraction_prompt}]).strip().lower()

        # 2. Fetch data
        price_data = get_crypto_price(project)
        market_data = get_market_data(project)

        # 3. Analyze
        system_prompt = f"""You are a {self.role}. Your goal is to analyze the market data of a crypto project.
Provide insights into its price, market cap, volume, and general standing in the market.
Keep it technical and data-driven."""

        context = f"Price Data: {price_data}\nMarket Data: {market_data}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}\n\nData Collected:\n{context}"}
        ]

        analysis = self._get_completion(messages)
        return analysis
