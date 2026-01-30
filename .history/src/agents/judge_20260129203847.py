import sys
import os
import subprocess
import tempfile
from src.state import SwarmState
from src.utils.logger import log_experiment, ActionType

def judge_agent(state: SwarmState):
    
    """
    Role: Execution and Verification.
    """
    print("--- JUDGE AGENT ---")
    
    code_to_test = state["code"]
    

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code_to_test)
        temp_file_path = temp_file.name

    try:

        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8'
        )
        os.remove(temp_file_path)


        if result.returncode != 0:
            error_msg = result.stderr.strip() or "Unknown Runtime Error"
            print(f"❌ JUDGE VERDICT: FAIL (Runtime Error)")
            
            log_experiment(
                agent_name="Judge",
                model_used="System_Compiler",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Execution",
                    "output_response": error_msg
                },
                status="FAILURE"
            )
            return {"success": False, "error_logs": error_msg}

        # 2. Empty Output Check
        if not result.stdout.strip():
            msg = "Code ran but produced NO OUTPUT."
            print(f"❌ JUDGE VERDICT: FAIL ({msg})")
            
            log_experiment(
                agent_name="Judge",
                model_used="System_Compiler",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Check stdout",
                    "output_response": msg
                },
                status="FAILURE"
            )
            return {"success": False, "error_logs": msg}

        print(f"✅ JUDGE VERDICT: PASS")
        print(f"   [Output]: {result.stdout.strip()}")
        
        log_experiment(
            agent_name="Judge",
            model_used="System_Compiler",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Final Verification",
                "output_response": "SUCCESS: All tests passed."
            },
            status="SUCCESS"
        )
        
        return {"success": True, "error_logs": "None"}

    except Exception as e:
        return {"success": False, "error_logs": str(e)}