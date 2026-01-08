import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment,ActionType

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    experiment_details = {
        "input_prompt": "Test Startup",
        "output_response": "Test startup.",
        "extra_metadata": "target_dir was ~/Documents/refactoring-swarm-template/src"
    }
    log_experiment("System", "STARTUP", ActionType.ANALYSIS, experiment_details, "INFO")
    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()