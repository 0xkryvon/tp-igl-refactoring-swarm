from typing import TypedDict

class SwarmState(TypedDict):
    target_dir: str
    target_file: str
    code: str      
    refactoring_plan: str   
    error_logs: str       
    iterations: int        
    success: bool          