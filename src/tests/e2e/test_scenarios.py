from src.state import SwarmState
from src.agents.judge import judge_agent

def test_end_to_end_valid_program():
    code = """
def add(a, b):
    return a + b
print(add(2, 3))
"""

    state = SwarmState(
        target_dir=".",
        target_file="add.py",
        code=code,
        refactoring_plan="",
        error_logs="",
        iterations=1,
        success=False
    )

    result = judge_agent(state)
    assert result["success"] is True