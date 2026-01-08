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

    # 1. Expand user (handle ~)
    # 2. Convert to absolute path (resolve relative to CWD immediately)
    target_dir = os.path.abspath(os.path.expanduser(args.target_dir))

    # Debug print to see what Python is actually checking
    print(f"🔍 CHECKING PATH: {target_dir}")

    if not os.path.exists(target_dir):
        print(f"❌ Dossier {target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {target_dir}")

    experiment_details = {
        "input_prompt": "Startup",
        "output_response": f"Startup initialized for target_dir: {args.target_dir}",
        "extra_metadata": f"target_dir was {target_dir}"
    }

    log_experiment("System", "STARTUP", ActionType.ANALYSIS, experiment_details, "INFO")
    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()