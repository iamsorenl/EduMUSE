from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from orchestrator.models import OrchestratorState

class OrchestratorState(BaseModel):
    """
    State model for the orchestrator flow. Carries data between steps.
    """
    user_input: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    parsed_query: Optional[Dict[str, Any]] = None
    retrieval_results: Optional[List[Any]] = None
    execution_plan: Optional[List[Any]] = None
    execution_outputs: Optional[List[Any]] = None
    final_response: Optional[str] = None
