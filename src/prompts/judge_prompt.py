JUDGE_SYSTEM_PROMPT = """
You are a QA Automation Engineer specialized in Pytest. 
Generate a HIGHLY CONCISE and EFFICIENT test suite.

### STRICT CONSTRAINTS:
1. **Focus:** Test ONLY the main logic and 2-3 critical edge cases. Do NOT test trivial getters/setters.
2. **Style:** - NO comments (unless absolutely necessary for complex logic).
   - NO docstrings for test functions.
   - Use parameterized tests (`@pytest.mark.parametrize`) to combine similar test cases into one function.
3. **Format:** Output raw Python code only.

### OUTPUT TEMPLATE:
import pytest
from {filename_no_ext} import *

# Tests start here
...

### INPUT CODE:
{code_to_test}
"""

def generate_judge_prompt(code_content: str, filename: str) -> str:
    """
    Prepares the prompt for the test generator.
    """
    # Remove extension if present (e.g. "script.py" -> "script")
    name_only = filename.replace(".py", "")
    
    return JUDGE_SYSTEM_PROMPT.format(
        code_to_test=code_content,
        filename_no_ext=name_only
    )