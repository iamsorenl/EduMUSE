from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from typing import List, Dict, Any
from .flows.flow_registry import flow_registry

@CrewBase
class EduMUSE():
    """EduMUSE: Modular Educational AI Assistant with Pluggable Flows"""

    def __init__(self):
        super().__init__()
        self.search_tool = SerperDevTool()

    @agent
    def academic_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['academic_searcher'],
            tools=[self.search_tool],
            verbose=True
        )

    @agent
    def flow_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['flow_coordinator'],
            verbose=True
        )

    @task
    def discovery_task(self) -> Task:
        return Task(
            config=self.tasks_config['discovery_task'],
        )

    @task
    def flow_orchestration_task(self) -> Task:
        return Task(
            config=self.tasks_config['flow_orchestration_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EduMUSE crew for educational content processing"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
            # Remove knowledge_sources for now
        )
    
    def process_educational_request(self, topic: str, requested_flows: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main entry point for educational content processing"""
        
        if context is None:
            context = {}
        
        # 1. Discover academic sources
        inputs = {
            "topic": topic, 
            "requested_flows": requested_flows
        }
        crew_result = self.crew().kickoff(inputs=inputs)
        
        # 2. Parse sources from crew result (mock for now)
        sources = [
            {
                "title": f"Academic Source about {topic}",
                "url": "https://example.edu/paper1",
                "credibility_score": 8.5,
                "source_type": "academic_paper"
            }
        ]
        
        # 3. Execute requested educational flows
        flow_results = {}
        for flow_name in requested_flows:
            flow_results[flow_name] = flow_registry.execute_flow(
                flow_name, 
                sources, 
                {"topic": topic, **context}
            )
        
        return {
            "topic": topic,
            "sources": sources,
            "educational_content": flow_results,
            "metadata": {
                "flows_executed": requested_flows,
                "source_count": len(sources),
                "learning_context": context
            }
        }
