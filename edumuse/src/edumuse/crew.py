from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from typing import List, Dict, Any
from edumuse.flows.flow_registry import flow_registry

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
        )
    
    def process_educational_request(self, topic: str, requested_flows: List[str], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main entry point for educational content processing"""
        
        if context is None:
            context = {}

        # Get the real document content that was passed from file_upload.py
        document_content = context.get('document_content', '')

        # Create a proper source object with the real content from the PDF
        sources = [
            {
                "title": topic,
                "url": f"localfile://{topic.replace(' ', '_')}",
                "content": document_content, # Use the actual content here
                "source_type": "uploaded_document"
            }
        ]
        
        # This part remains the same, but now it uses the REAL sources
        flow_results = {}
        for flow_name in requested_flows:
            print(f"🔧 Directly executing flow: {flow_name}")
            
            try:
                flow_results[flow_name] = flow_registry.execute_flow(
                    flow_name, 
                    sources, 
                    {"topic": topic, **context}
                )
                print(f"✅ {flow_name} executed successfully")
                
            except Exception as e:
                print(f"❌ Error executing {flow_name}: {e}")
                flow_results[flow_name] = {
                    "type": f"{flow_name}_error",
                    "content": f"Error during {flow_name} execution: {str(e)}",
                }
        
        return {
            "topic": topic,
            "sources": sources,
            "educational_content": flow_results,
            "metadata": {
                "flows_executed": requested_flows,
                "source_count": len(sources),
                "learning_context": context,
                "execution_method": "direct_flow_execution"
            }
        }
