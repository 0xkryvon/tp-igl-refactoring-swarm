from src.state import SwarmState
from src.agents.judge import judge_agent

def test_judge_success():
    state = SwarmState(
        target_dir=".",
        target_file="test.py",
        code="print('ok')",
        refactoring_plan="",
        error_logs="",
        iterations=1,
        success=False
    )

    result = judge_agent(state)

    assert result["success"] is True


def test_judge_runtime_error():
    state = SwarmState(
        target_dir=".",
        target_file="test.py",
        code="1/0",
        refactoring_plan="",
        error_logs="",
        iterations=1,
        success=False
    )

    result = judge_agent(state)

    assert result["success"] is False
    assert "ZeroDivisionError" in result["error_logs"]