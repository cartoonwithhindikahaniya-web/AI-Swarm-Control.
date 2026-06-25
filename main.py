import os
import sys
from dotenv import load_dotenv
from src.swarm.controller import SwarmController

def main():
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)

    print("=== Cyberscroti AGI Deep Research Swarm ===")

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
