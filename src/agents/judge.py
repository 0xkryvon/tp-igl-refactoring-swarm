import os
from langchain_core.messages import HumanMessage
from src.llm import llm
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType
from src.prompts.judge_prompt import generate_judge_prompt
from src.tools import run_pytest_tool, write_to_file

def judge_agent(state: SwarmState):
    """
    Role: QA Engineer (Judge).
    """
    print("\n--- JUDGE AGENT ---")
    
    # 1. Prepare Data
    code_to_test = state["code"]
    filename = os.path.basename(state.get("target_file", "script.py"))
    
    # 2. STEP 1: GENERATE TESTS (Uses LLM)
    print("   [Judge] Generating unit tests...")
    prompt = generate_judge_prompt(code_to_test, filename)
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        test_code_content = response.content.replace("```python", "").replace("```", "").strip()
    except Exception as e:
        return {"success": False, "error_logs": f"LLM Error: {str(e)}"}

    # 3. STEP 2: SECURE FILE WRITE (Uses Toolsmith)
    # We only pass the filename. tools.py handles the 'sandbox/' folder logic.
    
    # Write the script to be tested
    if not write_to_file(filename, code_to_test):
        return {"success": False, "error_logs": "Security Error: Could not write script file."}
        
    # Write the test file
    if not write_to_file("test_generated.py", test_code_content):
        return {"success": False, "error_logs": "Security Error: Could not write test file."}

    # 4. STEP 3: EXECUTE TESTS
    print("   [Judge] Running Pytest...")
    test_result = run_pytest_tool(".") 

    success = "SUCCESS" in test_result
    print(f"   Judge Verdict: {'PASS' if success else 'FAIL'}")

    # 5. Log Evidence
    log_experiment(
        agent_name="Judge",
        model_used="gemini-2.5-flash",
        action=ActionType.DEBUG,  
        details={
            "input_prompt": prompt,
            "output_response": test_result,
            "generated_tests": test_code_content
        },
        status="SUCCESS" if success else "FAILURE"
    )

    return {
        "success": success, 
        "error_logs": test_result if not success else "None"
    }