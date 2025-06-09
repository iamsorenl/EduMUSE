from typing import Dict, List, Any
from abc import ABC, abstractmethod

class EducationFlow(ABC):
    """Base class for all educational processing flows"""
    
    @abstractmethod
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process sources with educational context to produce learning content"""
        pass
    
    @abstractmethod
    def get_flow_info(self) -> Dict[str, Any]:
        """Return metadata about this flow's capabilities and requirements"""
        pass
    
    @property
    @abstractmethod
    def flow_type(self) -> str:
        """Return the type of educational flow (quiz, summary, study_plan, etc.)"""
        pass

class FlowRegistry:
    """Registry for managing educational processing flows"""
    
    def __init__(self):
        self.flows: Dict[str, EducationFlow] = {}
        self.flow_categories = {
            "knowledge_retrieval": [],    # Your specialty! Multiple approaches
            "assessment": [],             # Quiz flows (others can build)
            "content": [],               # Summary flows (others can build)  
            "planning": [],              # Study plan flows (others can build)
            "reference": [],             # Citation flows (others can build)
        }
    
    def register_flow(self, name: str, flow: EducationFlow, category: str = "content"):
        """Register a new educational flow"""
        self.flows[name] = flow
        
        if category in self.flow_categories:
            self.flow_categories[category].append(name)
    
    def get_available_flows(self, category: str = None) -> List[str]:
        """Get available flows, optionally filtered by category"""
        if category and category in self.flow_categories:
            return self.flow_categories[category]
        return list(self.flows.keys())
    
    def execute_flow(self, name: str, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific educational flow"""
        if name not in self.flows:
            # Return mock data for now instead of failing
            return {
                "type": name,
                "content": f"Mock {name} output - flow not implemented yet",
                "sources_used": len(sources),
                "context": context
            }
        
        return self.flows[name].process(sources, context)

# Global registry instance
flow_registry = FlowRegistry()