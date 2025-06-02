from crewai import Agent, Crew, Task
from crewai_tools import SerperDevTool
from typing import List, Dict, Any
from .flow_registry import EducationFlow, flow_registry

class HybridRetrievalFlow(EducationFlow):
    """Combines web search + LLM knowledge for comprehensive retrieval"""
    
    def __init__(self):
        self.hybrid_agent = Agent(
            role="Hybrid Knowledge Integration Specialist",
            goal="Combine web search results with LLM knowledge to create comprehensive academic source collection",
            backstory="Expert at synthesizing real-time web information with foundational academic knowledge to provide both current and authoritative educational resources...",
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @property
    def flow_type(self) -> str:
        return "knowledge_retrieval"
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = context.get('topic', 'academic research')
        
        hybrid_task = Task(
            description=f"""
            Create a comprehensive academic source collection about: {topic}
            
            Use BOTH approaches:
            
            1. WEB SEARCH COMPONENT:
               - Search for recent papers and current developments
               - Focus on 2023-2025 publications
               - Target academic databases and .edu sites
               
            2. LLM KNOWLEDGE COMPONENT:  
               - Identify foundational/seminal works from training data
               - Include highly-cited classic papers
               - Add authoritative textbooks and review articles
               
            3. SYNTHESIS:
               - Combine both sources into a coherent collection
               - Remove duplicates and rank by relevance + credibility
               - Provide 8-10 sources total with clear categorization
               
            For each source, specify:
            - Title, authors, publication venue
            - Source type (recent/foundational)
            - Retrieval method (web/knowledge)
            - Relevance and credibility scores
            """,
            agent=self.hybrid_agent,
            expected_output="Integrated academic source collection with clear methodology notes and source categorization"
        )
        
        crew = Crew(agents=[self.hybrid_agent], tasks=[hybrid_task])
        result = crew.kickoff()
        
        return {
            "flow_type": "hybrid_knowledge_retrieval",
            "retrieval_method": "web_search_plus_llm_synthesis",
            "sources_found": str(result),
            "search_scope": "web_plus_training_data",
            "topic": topic,
            "metadata": {
                "components": ["web_search", "llm_knowledge"],
                "synthesis_approach": "relevance_credibility_ranking",
                "coverage": "current_plus_foundational"
            }
        }
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "Hybrid Knowledge Retrieval",
            "description": "Combines web search with LLM knowledge for comprehensive coverage",
            "category": "knowledge_retrieval",
            "strengths": ["comprehensive_coverage", "current_plus_foundational", "high_relevance"],
            "limitations": ["slower_processing", "requires_api_access"]
        }

# Register the flow
flow_registry.register_flow("hybrid_retrieval", HybridRetrievalFlow(), "knowledge_retrieval")