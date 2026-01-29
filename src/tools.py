import os
import subprocess
import logging

# --- LOGGER SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Toolsmith")

# CONFIGURATION
# We ensure the sandbox directory exists immediately
SANDBOX_DIR = os.path.abspath("./sandbox")
if not os.path.exists(SANDBOX_DIR):
    os.makedirs(SANDBOX_DIR)

# --- SECURITY LAYER ---

def _get_safe_path(filename: str) -> str | None:
    """
    Security Enforcer: Resolves path and ensures it is inside the sandbox.
    Prevents directory traversal attacks (e.g. ../../)
    """
    # 1. Resolve absolute path
    if os.path.isabs(filename):
        # If absolute, check if it's inside sandbox
        abs_path = os.path.normpath(filename)
    else:
        # If relative, join with sandbox
        abs_path = os.path.abspath(os.path.join(SANDBOX_DIR, filename))
    
    # 2. Strict Check: Must start with SANDBOX_DIR
    if not abs_path.startswith(SANDBOX_DIR):
        logger.error(f"SECURITY ALERT: Agent attempted to access unsafe path: {abs_path}")
        return None
    
    return abs_path

# --- FILE OPERATIONS ---

def read_file(filename: str) -> str:
    """Reads a file securely from the sandbox."""
    safe_path = _get_safe_path(filename)
    if not safe_path or not os.path.exists(safe_path):
        return ""
    
    with open(safe_path, "r", encoding="utf-8") as f:
        return f.read()

def write_to_file(filename: str, content: str) -> bool:
    """
    Writes content to a file securely inside the sandbox.
    Returns True if successful, False if blocked by security.
    """
    safe_path = _get_safe_path(filename)
    
    if not safe_path:
        logger.error(f"Blocked write attempt to: {filename}")
        return False

    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Successfully wrote to {safe_path}")
        return True
    except Exception as e:
        logger.error(f"Write failed: {str(e)}")
        return False

# --- EXTERNAL TOOLS ---

def run_pylint_tool(filename: str) -> str:
    """Runs Pylint on a file inside the sandbox."""
    safe_path = _get_safe_path(filename)
    if not safe_path: return "Error: Invalid path."

    logger.info(f"Auditor is running Pylint on {safe_path}")
    
    try:
        # --disable=C,R ignores convention/refactoring noise, focuses on bugs
        result = subprocess.run(
            ["pylint", "--disable=C,R", safe_path],
            capture_output=True,
            text=True,
            timeout=30 
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Pylint execution timed out."
    except Exception as e:
        return f"Error running pylint: {str(e)}"

def run_pytest_tool(target_dir: str = ".") -> str:
    """
    Runs Pytest on the sandbox code.
    Input '.' means 'current sandbox directory'.
    """
    safe_path = _get_safe_path(target_dir)
    if not safe_path: return "Error: Invalid path."

    logger.info(f"Judge is running Pytest on {safe_path}")

    try:
        result = subprocess.run(
            ["pytest", safe_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return "SUCCESS: All tests passed."
        else:
            return f"FAILED:\n{result.stdout}\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: Pytest execution timed out."
    except Exception as e:
        return f"Error running pytest: {str(e)}"