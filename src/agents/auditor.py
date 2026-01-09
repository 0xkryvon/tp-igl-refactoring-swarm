from langchain_core.messages import HumanMessage
from src.llm import llm
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType
from src.prompts.auditor_prompt import generate_audit_prompt

def auditor_agent(state: SwarmState):
    """
    Role: Static Analysis and Planning.
    """
    iteration = state.get("iterations", 0)
    print(f"\n--- AUDITOR AGENT (Cycle {iteration+1}) ---")
    
    code = state["code"]
    
    prompt = generate_audit_prompt(code)
    
    response = llm.invoke([HumanMessage(content=prompt)])
    plan = response.content.strip()


    log_experiment(
        agent_name="Auditor",
        model_used="gemini-2.5-flash",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": prompt,
            "output_response": plan,
            "file_analyzed": "target_script.py"
        },
        status="SUCCESS"
    )

    return {
        "refactoring_plan": plan,
        "iterations": iteration + 1
    }