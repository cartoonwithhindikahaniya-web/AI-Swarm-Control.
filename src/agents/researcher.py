from typing import List, Dict, Any
from src.agents.base import BaseAgent
from src.tools.research_tools import web_search

class ResearchAgent(BaseAgent):
    def __init__(self, name: str = "Researcher", model: str = "gpt-4o"):
        super().__init__(name, "Research Specialist", model)

    def run(self, task: str) -> str:
        print(f"[{self.name}] Starting research on: {task}")

        # 1. Perform search
        search_results = web_search(task)

        # 2. Synthesize results
        context = "\n".join([f"- {r.get('title')}: {r.get('snippet')} ({r.get('link')})" for r in search_results if "error" not in r])

        system_prompt = f"""You are a {self.role}. Your goal is to conduct deep research on the given topic.
Use the provided search results to create a comprehensive summary.
Focus on accuracy, key findings, and credible sources."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}\n\nSearch Results:\n{context}"}
        ]

        summary = self._get_completion(messages)
        return summary
