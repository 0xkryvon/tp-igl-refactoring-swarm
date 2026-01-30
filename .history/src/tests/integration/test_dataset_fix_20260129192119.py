import pytest
from pathlib import Path
from src.agents.fixer import fixer_agent
from src.agents.judge import judge_agent
from src.state import SwarmState

DATASET_DIR = Path(__file__).parents[2] / "test_dataset"

@pytest.mark.integration
@pytest.mark.parametrize("file_name", [
    "case_1.py",
    "case_2.py",
    "case_3.py",
    "case_4.py",
    "case_5.py",
])
def test_dataset_files(file_name):
    file_path = DATASET_DIR / file_name
    code = file_path.read_text()

    state = SwarmState(
        target_dir=str(DATASET_DIR),
        target_file=str(file_path),
        code=code,
        refactoring_plan="",
        error_logs="",
        iterations=0,
        success=False
    )

    state = fixer_agent(state)
    state = judge_agent(state)

    assert state["success"] is True