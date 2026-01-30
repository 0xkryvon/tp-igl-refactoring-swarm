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
    parser.add_argument("--target_dir", help="Directory containing the buggy code")
parser.add_argument("--target_file", help="Single Python file to refactor")

    args = parser.parse_args()

    # 1. Validation
    if not os.path.isdir(args.target_dir):
        print(f"❌ ERROR: Directory '{args.target_dir}' not found.")
        exit(1)

    # 2. File Discovery (Enhanced)
    search_path = os.path.join(args.target_dir, "*.py")
    found_files = glob.glob(search_path)
    
    # Filter out test files so we don't try to refactor the tests themselves!
    code_files = [f for f in found_files if "test_" not in os.path.basename(f)]

    if not code_files:
        print(f"❌ ERROR: No suitable .py files found in {args.target_dir}")
        exit(1)
        
    target_file = code_files[0] # Pick the first non-test file
    print(f"🎯 Target File: {target_file}")

    # 3. Read Original Code
    with open(target_file, "r", encoding='utf-8') as f:
        original_code = f.read()

    # 4. Initialize State
    # We added 'target_file' to state so the Fixer knows where to save.
    initial_state = {
        "target_dir": args.target_dir,
        "target_file": target_file,
        "code": original_code, 
        "refactoring_plan": "",
        "error_logs": "",
        "iterations": 0,
        "success": False
    }

    print(f"\n🚀 STARTING REFACTORING SWARM...")
    
    try:
        final_state = app.invoke(initial_state)
        
        print("\n------------------------------------------------")
        if final_state["success"]:
            print("🏆 MISSION SUCCESS: The code has been fixed and tested.")
        else:
            print("💀 MISSION FAILED: Could not fix the code within the limit.")
            
        print("📝 Check 'logs/experiment_data.json' for scientific data.")
        print("------------------------------------------------")
        
    except Exception as e:
        print(f"\n❌ SYSTEM CRASH: {e}")