"""
EduMUSE Flow Registry and Flow Implementations
"""

# Import flow registry first
from .flow_registry import flow_registry, EducationFlow

# Import all flow implementations to ensure they register themselves
from .web_search_flow import WebSearchFlow
from .llm_knowledge_flow import LLMKnowledgeFlow
from .hybrid_retrieval_flow import HybridRetrievalFlow
