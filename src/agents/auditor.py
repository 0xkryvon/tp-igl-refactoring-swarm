import os
from langchain_core.messages import HumanMessage
from src.llm import llm
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType
from src.prompts.auditor_prompt import generate_audit_prompt
from src.tools import run_pylint_tool, write_to_file

def auditor_agent(state: SwarmState):
    """
    Role: Static Analysis and Planning (Tool-Assisted).
    1. Writes code to sandbox.
    2. Runs Pylint tool.
    3. Sends code + Pylint report to LLM.
    """
    iteration = state.get("iterations", 0)
    print(f"\n--- AUDITOR AGENT (Cycle {iteration+1}) ---")
    
    code = state["code"]
    filename = os.path.basename(state.get("target_file", "script.py"))
    
    # 1. TOOL STEP: Write to sandbox so Pylint can read it
    if not write_to_file(filename, code):
        print("   ❌ Error: Could not write file for analysis.")
        return {"refactoring_plan": "Error writing file", "iterations": iteration + 1}

    # 2. TOOL STEP: Run Pylint
    print("   [Auditor] Running Pylint tool...")
    pylint_output = run_pylint_tool(filename)
    
    # 3. ANALYSIS STEP: Generate Prompt with Tool Data
    print("   [Auditor] Analyzing Pylint report with LLM...")
    prompt = generate_audit_prompt(code, pylint_output)
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        plan = response.content.strip()
    except Exception as e:
        plan = f"LLM Error: {str(e)}"

    # 4. LOGGING (Scientific Data)
    log_experiment(
        agent_name="Auditor",
        model_used="gemini-2.5-flash",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": prompt,
            "output_response": plan,
            "tool_output": pylint_output, # We log what the tool saw!
            "file_analyzed": filename
        },
        status="SUCCESS"
    )

    return {
        "refactoring_plan": plan,
        "iterations": iteration + 1
    }