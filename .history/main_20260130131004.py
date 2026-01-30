import argparse
import os
import glob
import time
from langgraph.graph import StateGraph, END

# --- 1. RATE LIMIT PATCH (Essential for Gemini Free Tier) ---
from langchain_google_genai import ChatGoogleGenerativeAI

original_invoke = ChatGoogleGenerativeAI.invoke

def slow_invoke(self, *args, **kwargs):
    print("⏳ Throttling: Waiting 5s to avoid Google Free Tier crash...")
    time.sleep(5) 
    return original_invoke(self, *args, **kwargs)

ChatGoogleGenerativeAI.invoke = slow_invoke

# --- 2. IMPORTS FROM SRC ---
try:
    from src.state import SwarmState
    from src.agents.auditor import auditor_agent
    from src.agents.fixer import fixer_agent
    from src.agents.judge import judge_agent
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Could not import agents. Reason: {e}")
    print("Ensure you have created 'src/state.py' and 'src/agents/*.py'")
    exit(1)

# --- 3. WRAPPER NODES ---

def auditor_wrapper(state: SwarmState):
    """Wraps the auditor agent."""
    print(f"\n🔍 [Auditor] Analyzing code...")
    return auditor_agent(state)

def fixer_wrapper(state: SwarmState):
    """
    Wraps the fixer agent AND saves the result to disk immediately.
    This ensures the Judge tests the NEW code, not the old file.
    """
    print(f"\n🔧 [Fixer] Applying patches (Iteration {state.get('iterations', 0) + 1})...")
    
    # Run the agent logic
    new_state = fixer_agent(state)
    
    # --- ENHANCEMENT: SAVE TO DISK NOW ---
    # We save immediately so Pytest sees the changes.
    target_file = state.get("target_file")
    new_code = new_state.get("code")
    
    if target_file and new_code:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"    💾 Saved changes to: {os.path.basename(target_file)}")
    else:
        print("    ⚠️ Warning: No code or target file found in state. Nothing saved.")
        
    return new_state

def judge_wrapper(state: SwarmState):
    """Wraps the judge agent."""
    print(f"\n⚖️ [Judge] Running tests...")
    return judge_agent(state)

# --- 4. LOGIC GATES ---

def decision_gate(state: SwarmState):
    # Safety Check
    if state["iterations"] >= 10:
        print("\n🛑 Max iterations reached. Stopping loop.")
        return END
        
    # Success Check
    if state["success"]:
        print("\n✅ Tests Passed! Stopping loop.")
        return END
    
    # Failure -> Loop back
    print(f"    ↺ Test failed. Looping back to Fixer.")
    return "fixer" 

# --- 5. GRAPH DEFINITION ---

workflow = StateGraph(SwarmState)

# Use the WRAPPERS instead of the raw agents
workflow.add_node("auditor", auditor_wrapper)
workflow.add_node("fixer", fixer_wrapper)
workflow.add_node("judge", judge_wrapper)

workflow.set_entry_point("auditor")
workflow.add_edge("auditor", "fixer")
workflow.add_edge("fixer", "judge")

workflow.add_conditional_edges(
    "judge",
    decision_gate,
    {END: END, "fixer": "fixer"}
)

app = workflow.compile()

# --- 6. MAIN EXECUTION ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_file", help="Single Python file to refactor")
    parser.add_argument("--target_dir", help="Directory containing Python files")
    args = parser.parse_args()

    if not args.target_file and not args.target_dir:
        print("❌ ERROR: Provide --target_file or --target_dir")
        exit(1)

    # -----------------------------------------------------
    # TARGET RESOLUTION (UNIQUE SOURCE OF TRUTH)
    # -----------------------------------------------------

    if args.target_file:
        if not os.path.isfile(args.target_file):
            print(f"❌ ERROR: File '{args.target_file}' not found.")
            exit(1)
        code_files = [args.target_file]

    else:  # target_dir
        if not os.path.isdir(args.target_dir):
            print(f"❌ ERROR: Directory '{args.target_dir}' not found.")
            exit(1)

        search_path = os.path.join(args.target_dir, "*.py")
        found_files = glob.glob(search_path)

        code_files = [
            f for f in found_files
            if not os.path.basename(f).startswith("test_")
        ]

        if not code_files:
            print(f"❌ ERROR: No suitable .py files found in {args.target_dir}")
            exit(1)

    # -----------------------------------------------------
    # EXECUTION LOOP (1 FILE = 1 SWARM)
    # -----------------------------------------------------

    for target_file in code_files:
        print(f"\n🎯 Target File: {target_file}")

        with open(target_file, "r", encoding="utf-8") as f:
            original_code = f.read()

        initial_state = {
            "target_dir": os.path.dirname(target_file),
            "target_file": target_file,
            "code": original_code,
            "refactoring_plan": "",
            "error_logs": "",
            "iterations": 0,
            "success": False
        }

        print("\n🚀 STARTING REFACTORING SWARM...")

        try:
            final_state = app.invoke(initial_state)

            if final_state.get("success"):
                print(f"🏆 SUCCESS: {os.path.basename(target_file)} fixed")
            else:
                print(f"💀 FAILED: {os.path.basename(target_file)}")

        except Exception as e:
            print(f"\n❌ SYSTEM CRASH on {target_file}: {e}")