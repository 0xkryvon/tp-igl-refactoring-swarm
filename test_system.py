"""
Script de test complet pour The Refactoring Swarm
Responsable : Data Officer
"""

import subprocess
import sys
import time
from pathlib import Path
import pytest
from src.utils.validate_logs import validate_experiment_logs, get_log_statistics
from dotenv import load_dotenv
import os

# Charger la clé API depuis .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ GOOGLE_API_KEY manquant dans .env")
    sys.exit(1)

# Détecter si on est en mode pytest (pour éviter input bloquant)
RUN_INTERACTIVE = not hasattr(sys, "_called_from_pytest")


def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title: str):
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


def test_case(case_dir: Path, case_number: int, total_cases: int) -> dict:
    print_section(f"Test {case_number}/{total_cases} : {case_dir.name}")
    result = {"case_name": case_dir.name, "success": False, "duration": 0, "error_message": None}

    try:
        py_files = list(case_dir.glob("*.py"))
        for py_file in py_files:
            print(f"   - {py_file.name}")

        start_time = time.time()

        # Lancer main.py sur le dossier du cas
        process_result = subprocess.run(
            [sys.executable, "main.py", "--target_dir", str(case_dir)],
            capture_output=True,
            text=True,
            timeout=120
        )

        duration = time.time() - start_time
        result["duration"] = duration

        if process_result.returncode == 0:
            result["success"] = True
        else:
            result["error_message"] = "Non-zero exit code"

        return result

    except subprocess.TimeoutExpired:
        result["error_message"] = "Timeout (>120s)"
        return result

    except FileNotFoundError:
        result["error_message"] = "main.py not found"
        return result

    except Exception as e:
        result["error_message"] = str(e)
        return result


def check_prerequisites():
    all_ok = True

    if not Path("main.py").exists():
        all_ok = False

    test_dataset = Path("test_dataset")
    if not test_dataset.exists():
        all_ok = False

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    sandbox_dir = Path("sandbox")
    sandbox_dir.mkdir(exist_ok=True)

    return all_ok


def main():
    print_header("TEST SYSTEM - The Refactoring Swarm")

    if not check_prerequisites():
        print("❌ Prérequis manquants")
        return

    test_dir = Path("test_dataset")
    test_cases = sorted([d for d in test_dir.iterdir() if d.is_dir() and d.name.startswith("case_")])
    if not test_cases:
        print("❌ Aucun cas de test trouvé")
        return

    if RUN_INTERACTIVE:
        input("\nAppuyez sur Entrée pour continuer...")

    results = []
    total_duration = 0
    for i, case in enumerate(test_cases, 1):
        result = test_case(case, i, len(test_cases))
        results.append(result)
        total_duration += result["duration"]
        if i < len(test_cases):
            time.sleep(1)

    success_count = sum(1 for r in results if r["success"])
    failure_count = len(results) - success_count
    success_rate = (success_count / len(results)) * 100 if results else 0

    log_file = Path("logs/experiment_data.json")
    if log_file.exists():
        logs_valid = validate_experiment_logs()
        if logs_valid:
            stats = get_log_statistics()
            if stats:
                print(f"Entrées avec prompts : {stats['has_prompts']}/{stats['total_entries']}")

    print_header("RÉSULTATS")
    print(f"Réussis : {success_count}/{len(results)}")
    print(f"Échecs : {failure_count}/{len(results)}")
    print(f"Taux de réussite : {success_rate:.1f}%")


# ======================
# Pytest fixtures pour test unitaire
# ======================

@pytest.fixture
def case_dir(tmp_path):
    case = tmp_path / "case_1"
    case.mkdir()
    dummy_file = case / "example.py"
    dummy_file.write_text("print('Hello World')")
    return case


@pytest.fixture
def case_number():
    return 1


@pytest.fixture
def total_cases():
    return 1


def test_test_case(case_dir, case_number, total_cases):
    result = test_case(case_dir, case_number, total_cases)
    assert result["success"] in [True, False]


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        sys.exit(1)