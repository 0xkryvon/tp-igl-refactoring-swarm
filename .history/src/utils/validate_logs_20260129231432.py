import json
from pathlib import Path
from typing import Dict, Any

LOG_FILE = Path("logs/experiment_data.json")

def validate_experiment_logs() -> bool:
    if not LOG_FILE.exists():
        print("Fichier logs introuvable")
        return False
    if LOG_FILE.stat().st_size == 0:
        print("Fichier logs vide")
        return False

    try:
        data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            print("Logs invalides ou vides")
            return False

        required_fields = {"agent_name", "model_used", "action", "details", "status", "timestamp"}
        required_details = {"input_prompt", "output_response"}

        errors, warnings = [], []

        for i, entry in enumerate(data, 1):
            for field in required_fields:
                if field not in entry:
                    errors.append(f"Entrée {i} : champ '{field}' manquant")

            details = entry.get("details")
            if isinstance(details, dict):
                for d in required_details:
                    if d not in details:
                        warnings.append(f"Entrée {i} : '{d}' manquant dans details")
            else:
                errors.append(f"Entrée {i} : details invalide")

        if errors:
            print("ERREURS :")
            for e in errors:
                print(" -", e)
            return False
        if warnings:
            print("AVERTISSEMENTS :")
            for w in warnings:
                print(" -", w)

        print(f"Total logs : {len(data)}")
        print(f"Succès : {sum(e['status'] == 'SUCCESS' for e in data)} | Échecs : {sum(e['status'] == 'FAILURE' for e in data)}")
        return True

    except json.JSONDecodeError:
        print("JSON invalide")
        return False


def get_log_statistics() -> Dict[str, Any] | None:
    if not LOG_FILE.exists():
        return None
    try:
        data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            return None
        return {
            "total_entries": len(data),
            "agents": list({e.get("agent_name") for e in data}),
            "actions": list({e.get("action") for e in data}),
            "success_count": sum(e.get("status") == "SUCCESS" for e in data),
            "failure_count": sum(e.get("status") == "FAILURE" for e in data),
        }
    except Exception:
        return None
    

    