from src.state import SwarmState

def test_swarm_state_creation():
    state = SwarmState(
        target_dir="/tmp",
        target_file="file.py",
        code="print('hi')",
        refactoring_plan="plan",
        error_logs="",
        iterations=0,
        success=False
    )

    assert state["target_dir"] == "/tmp"
    assert state["target_file"] == "file.py"
    assert state["iterations"] == 0
    assert state["success"] is False
