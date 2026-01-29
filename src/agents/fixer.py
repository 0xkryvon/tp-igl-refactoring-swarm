import os
from langchain_core.messages import HumanMessage
from src.llm import llm
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType
from src.prompts.fixer_prompt import generate_fixer_prompt
from src.tools import write_to_file

def fixer_agent(state: SwarmState):
    """
    Role: Code Correction (Writer).
    1. Reads the plan and errors.
    2. Generates fixed code.
    3. Writes it SECURELY to the sandbox.
    """
    print("\n--- FIXER AGENT ---")
    
    # 1. Prepare Data
    current_code = state["code"]
    plan = state.get("refactoring_plan", "No plan provided")
    errors = state.get("error_logs", "None")
    filename = os.path.basename(state.get("target_file", "script.py"))

    prompt = generate_fixer_prompt(current_code, plan, errors)
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        fixed_code = response.content.replace("```python", "").replace("```", "").strip()
    except Exception as e:
        return {"code": current_code, "error_logs": f"Fixer LLM Failed: {str(e)}"}

    if write_to_file(filename, fixed_code):
        print(f"    Securely saved changes to: {filename}")
    else:
        print(f"    SECURITY BLOCK: Could not save {filename}")

    log_experiment(
        agent_name="Fixer",
        model_used="gemini-2.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": prompt,
            "output_response": fixed_code, 
            "bugs_fixed": "See plan in logs"
        },
        status="SUCCESS"
    )

    # We return the new code so the state is updated for the Judge
    return {"code": fixed_code}