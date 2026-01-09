import argparse
import os
import glob  # Added this to find files
import time
from langgraph.graph import StateGraph, END

# --- 🛑 YOUR RATE LIMIT PATCH 🛑 ---
from langchain_google_genai import ChatGoogleGenerativeAI

original_invoke = ChatGoogleGenerativeAI.invoke

def slow_invoke(self, *args, **kwargs):
    print("⏳ Throttling: Waiting 5s to avoid Google Free Tier crash...")
    time.sleep(5) 
    return original_invoke(self, *args, **kwargs)

ChatGoogleGenerativeAI.invoke = slow_invoke


# Import Modules
from src.state import SwarmState
from src.agents.auditor import auditor_agent
from src.agents.fixer import fixer_agent
from src.agents.judge import judge_agent

# --- Logic Gates ---
def decision_gate(state: SwarmState):
    if state["iterations"] >= 10:
        print("--- MAX ITERATIONS REACHED ---")
        return END
        
    if state["success"]:
        return END
    else:
        return "fixer" 

# --- Graph Definition ---
workflow = StateGraph(SwarmState)

workflow.add_node("auditor", auditor_agent)
workflow.add_node("fixer", fixer_agent)
workflow.add_node("judge", judge_agent)

workflow.set_entry_point("auditor")
workflow.add_edge("auditor", "fixer")
workflow.add_edge("fixer", "judge")

workflow.add_conditional_edges(
    "judge",
    decision_gate,
    {END: END, "fixer": "fixer"}
)

app = workflow.compile()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", required=True, help="Target directory containing the buggy code")
    args = parser.parse_args()

    search_path = os.path.join(args.target_dir, "*.py")
    found_files = glob.glob(search_path)
    
    if not found_files:
        print(f"❌ ERROR: No .py file found in {args.target_dir}")
        exit(1)
        
    target_file = found_files[0]
    print(f"Found target file: {target_file}")

    with open(target_file, "r", encoding='utf-8') as f:
        original_code = f.read()

    print(f"STARTING REFACTORING SWARM on {target_file}")
    
    initial_state = {
        "code": original_code, 
        "refactoring_plan": "",
        "error_logs": "",
        "iterations": 0,
        "success": False
    }

    try:

        final_state = app.invoke(initial_state)
        
        print(f"\n WRITING FIXES TO {target_file}...")
        
        if final_state.get("code"):
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(final_state["code"])
            print("✅ File updated successfully.")
            
        print("\n✅ Mission Complete. Check 'logs/experiment_data.json'.")
        
    except Exception as e:
        print(f"\n❌ System Error: {e}")