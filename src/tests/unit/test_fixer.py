from unittest.mock import Mock, patch
from src.state import SwarmState

@patch("src.agents.fixer.llm")
def test_fixer_updates_code(mock_llm):
    from src.agents.fixer import fixer_agent

    mock_llm.invoke.return_value = Mock(
        content="```python\nprint('fixed')\n```"
    )

    state = SwarmState(
        target_dir=".",
        target_file="test.py",
        code="print('broken')",
        refactoring_plan="Fix print",
        error_logs="",
        iterations=1,
        success=False
    )

    result = fixer_agent(state)

    assert "```" not in result["code"]
    assert "fixed" in result["code"]
