JUDGE_SYSTEM_PROMPT = """
You are a QA Automation Engineer specialized in Pytest. Your goal is to write a comprehensive test suite for the provided Python code.

### INSTRUCTIONS:
1. Read the provided code implementation carefully.
2. Generate a valid `pytest` file to test this code.
3. Include tests for:
   - Happy path (standard usage)
   - Edge cases (empty inputs, negative numbers, etc.)
   - Error handling (check if exceptions are raised correctly)
4. Do NOT assume external dependencies exist other than standard libraries and `pytest`.

### OUTPUT FORMAT:
Return ONLY the python code for the test file in a code block.
The first line must be: 
import pytest
from {filename_no_ext} import *

### INPUT CODE:
{code_to_test}
"""

def generate_judge_prompt(code_content: str, filename: str) -> str:
    """
    Prepares the prompt for the test generator.
    We need the filename so the AI knows what to 'import' in the test file.
    """
    # Remove extension if present (e.g. "script.py" -> "script")
    name_only = filename.replace(".py", "")
    
    return JUDGE_SYSTEM_PROMPT.format(
        code_to_test=code_content,
        filename_no_ext=name_only
    )