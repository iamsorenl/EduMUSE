from crewai import Agent, Crew, Task
from typing import List, Dict, Any
from .flow_registry import EducationFlow, flow_registry

class LLMKnowledgeFlow(EducationFlow):
    """Knowledge retrieval using LLM's training data (baseline approach)"""
    
    def __init__(self):
        self.knowledge_agent = Agent(
            role="LLM Knowledge Specialist", 
            goal="Extract comprehensive academic knowledge from LLM training data",
            backstory="Expert at accessing and organizing the vast academic knowledge contained in large language model training data, with deep understanding of academic literature across disciplines...",
            tools=[],  # No external tools - pure LLM knowledge
            verbose=True
        )
    
    @property
    def flow_type(self) -> str:
        return "knowledge_retrieval"
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = context.get('topic', 'academic research')
        
        knowledge_task = Task(
            description=f"""
            Using your comprehensive training data knowledge, provide academic sources about: {topic}
            
            Generate a curated list of 5-8 academic sources including:
            - Key academic papers, textbooks, and authoritative sources
            - Publication details (authors, journals, approximate years)
            - Brief description of each source's contribution
            - Relevance to the topic (1-10 scale)
            
            Focus on:
            - Foundational papers and seminal works
            - Highly cited research in the field
            - Authoritative textbooks and review papers
            - Recent significant developments (within training data cutoff)
            
            Note: This is based on training data, not real-time web search.
            """,
            agent=self.knowledge_agent,
            expected_output="Curated list of academic sources with detailed descriptions and relevance scores"
        )
        
        crew = Crew(agents=[self.knowledge_agent], tasks=[knowledge_task])
        result = crew.kickoff()
        
        return {
            "flow_type": "llm_knowledge_retrieval",
            "retrieval_method": "training_data_synthesis",
            "sources_found": str(result),
            "search_scope": "llm_training_corpus",
            "topic": topic,
            "metadata": {
                "knowledge_source": "LLM_training_data",
                "cutoff_limitation": "training_data_cutoff",
                "strength": "comprehensive_foundational_knowledge"
            }
        }
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "LLM Knowledge Base Retrieval",
            "description": "Extracts academic knowledge from LLM training data",
            "category": "knowledge_retrieval", 
            "strengths": ["no_api_required", "comprehensive_coverage", "fast_response"],
            "limitations": ["training_cutoff", "no_real_time_updates", "potential_hallucination"]
        }

# Register the flow
flow_registry.register_flow("llm_knowledge", LLMKnowledgeFlow(), "knowledge_retrieval")