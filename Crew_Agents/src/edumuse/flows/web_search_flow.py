from crewai import Agent, Crew, Task
from crewai_tools import SerperDevTool
from typing import List, Dict, Any
from .flow_registry import EducationFlow, flow_registry

class WebSearchFlow(EducationFlow):
    """Web-enhanced academic source discovery using search APIs"""
    
    def __init__(self):
        self.search_agent = Agent(
            role="Web Search Academic Specialist",
            goal="Discover current academic sources using web search APIs",
            backstory="Expert at crafting academic search queries and filtering web results for educational credibility and relevance...",
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @property
    def flow_type(self) -> str:
        return "knowledge_retrieval"
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        topic = context.get('topic', 'academic research')
        
        search_task = Task(
            description=f"""
            Search the web for high-quality academic sources about: {topic}
            
            Use advanced search operators:
            - site:edu OR site:arxiv.org OR site:scholar.google.com
            - filetype:pdf for academic papers
            - "peer reviewed" OR "journal article" for credible sources
            
            Find 5-8 credible academic sources with:
            - Title and URL
            - Publication source/institution  
            - Brief description of relevance
            - Credibility assessment (1-10 scale)
            
            Focus on recent publications (2020+) and authoritative domains.
            """,
            agent=self.search_agent,
            expected_output="List of academic sources with URLs, credibility scores, and relevance descriptions"
        )
        
        crew = Crew(agents=[self.search_agent], tasks=[search_task])
        result = crew.kickoff()
        
        return {
            "flow_type": "web_search_retrieval",
            "retrieval_method": "web_api_search",
            "sources_found": str(result),
            "search_scope": "web_academic_databases",
            "topic": topic,
            "metadata": {
                "search_tools": ["SerperDevTool"],
                "target_domains": [".edu", "arxiv.org", "scholar.google.com"],
                "credibility_filter": "academic_institutions_only"
            }
        }
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "Web Search Academic Retrieval",
            "description": "Uses web search APIs to find current academic sources",
            "category": "knowledge_retrieval",
            "strengths": ["current_information", "broad_coverage", "real_time_results"],
            "limitations": ["requires_api_key", "dependent_on_search_quality"]
        }

# Register the flow
flow_registry.register_flow("web_search", WebSearchFlow(), "knowledge_retrieval")