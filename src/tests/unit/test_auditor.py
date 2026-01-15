from unittest.mock import Mock, patch
from src.state import SwarmState

@patch("src.agents.auditor.llm")
def test_auditor_generates_plan(mock_llm):
    from src.agents.auditor import auditor_agent

    mock_llm.invoke.return_value = Mock(content="Detected bugs")

    state = SwarmState(
        target_dir=".",
        target_file="test.py",
        code="def f(): pass",
        refactoring_plan="",
        error_logs="",
        iterations=0,
        success=False
    )

    result = auditor_agent(state)

    assert result["refactoring_plan"] == "Detected bugs"
    assert result["iterations"] == 1
