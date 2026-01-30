from langchain_core.messages import HumanMessage
from src.llm import llm
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType

def fixer_agent(state: SwarmState):
    time.sleep(5)
    """
    Role: Code Correction.
    """
    print("---FIXER AGENT---")
    
    current_code = state["code"]
    plan = state.get("refactoring_plan", "No plan provided")
    errors = state.get("error_logs", "None")
    
    prompt = f"""
    You are the Code Fixer.
    
    GOAL: Apply the Refactoring Plan and fix any Runtime Errors reported by the Judge.
    
    REFACTORING PLAN:
    {plan}
    
    PREVIOUS RUNTIME ERRORS:
    {errors}
    
    CURRENT CODE:
    {current_code}
    
    OUTPUT:
    Return ONLY the full corrected Python code. No Markdown blocks.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    fixed_code = response.content.replace("```python", "").replace("```", "").strip()

    log_experiment(
        agent_name="Fixer",
        model_used="gemini-2.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": prompt,
            "output_response": response.content,
            "bugs_fixed": "See plan in logs"
        },
        status="SUCCESS"
    )

    return {"code": fixed_code}