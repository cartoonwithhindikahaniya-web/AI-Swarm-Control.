from typing import List, Dict, Any
from src.agents.base import BaseAgent
from src.agents.researcher import ResearchAgent
from src.agents.analyst import CryptoAnalystAgent

class SwarmController:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.researcher = ResearchAgent(model=model)
        self.analyst = CryptoAnalystAgent(model=model)
        self.manager = ResearchAgent(name="Manager", model=model) # Using research agent as a proxy for manager for now

    def execute_workflow(self, project_name: str) -> str:
        print(f"[Swarm] Initiating deep research workflow for: {project_name}")

        # 1. Research
        research_report = self.researcher.run(f"Latest news and development of {project_name}")

        # 2. Market Analysis
        market_report = self.analyst.run(f"Market data analysis for {project_name}")

        # 3. Final Synthesis
        print("[Swarm] Synthesizing final report...")
        synthesis_prompt = f"""You are the lead AGI controller of the Cyberscroti swarm.
Synthesize the following reports into a final comprehensive Deep Research document for {project_name}.

RESEARCH REPORT:
{research_report}

MARKET ANALYSIS REPORT:
{market_report}

Ensure the final document is structured, insightful, and provides a clear conclusion on the project's current state."""

        final_report = self.manager._get_completion([{"role": "user", "content": synthesis_prompt}])
        return final_report
