import json
import pytest
from pathlib import Path
from src.utils.logger import log_experiment, ActionType, LOG_FILE

@pytest.fixture
def tmp_log_file(tmp_path):
    """Fixture pour utiliser un fichier de logs temporaire"""
    log_file = tmp_path / "experiment_data.json"
    return log_file

def test_log_written(tmp_log_file, monkeypatch):
    # Rediriger LOG_FILE vers tmp_path
    monkeypatch.setattr("src.utils.logger.LOG_FILE", tmp_log_file)

    details = {"input_prompt": "in", "output_response": "out"}

    log_experiment(
        agent_name="Test",
        model_used="pytest_model",
        action=ActionType.FIX,
        details=details,
        status="SUCCESS"
    )

    # Vérifier que le fichier a été créé
    assert tmp_log_file.exists()

    # Vérifier le contenu
    data = json.loads(tmp_log_file.read_text())
    entry = data[0]
    assert entry["agent"] == "Test" or entry["agent_name"] == "Test"
    assert entry["action"] == ActionType.FIX.value
    assert entry["details"]["input_prompt"] == "in"
    assert entry["details"]["output_response"] == "out"
    assert entry["status"] == "SUCCESS"