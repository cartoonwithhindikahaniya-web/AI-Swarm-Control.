import os
import sys
from dotenv import load_dotenv
from src.swarm.controller import SwarmController

def main():
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key_env = "OPENAI_API_KEY" if provider == "openai" else "DEEPSEEK_API_KEY"

    if not os.getenv(api_key_env):
        print(f"Error: {api_key_env} not found in environment variables for provider {provider}.")
        sys.exit(1)

    print(f"=== Cyberscroti AGI Deep Research Swarm [{provider.upper()}] ===")

    if len(sys.argv) > 1:
        project_name = " ".join(sys.argv[1:])
    else:
        project_name = input("Enter the crypto project/topic to research: ")

    if not project_name:
        print("No project name provided. Exiting.")
        sys.exit(0)

    controller = SwarmController()
    final_report = controller.execute_workflow(project_name)

    print("\n--- FINAL RESEARCH REPORT ---")
    print(final_report)
    print("\n--- END OF REPORT ---")

    # Save to file
    filename = f"research_{project_name.lower().replace(' ', '_')}.md"
    with open(filename, "w") as f:
        f.write(final_report)
    print(f"\nReport saved to {filename}")

if __name__ == "__main__":
    main()
