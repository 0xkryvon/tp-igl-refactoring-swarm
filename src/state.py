from typing import TypedDict

class SwarmState(TypedDict):
    code: str      
    refactoring_plan: str   
    error_logs: str       
    iterations: int        
    success: bool          