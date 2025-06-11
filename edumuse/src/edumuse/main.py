#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from typing import List, Dict, Any

# Ensure all flows are imported to register them with the flow_registry
from edumuse.crew import EduMUSE
from edumuse.flows.flow_registry import flow_registry
from edumuse.flows.web_search_flow import WebSearchFlow
from edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
from edumuse.flows.assessment_flow import AssessmentFlow
from edumuse.flows.summary_flow import SummaryFlow

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run EduMUSE with educational content generation"""
    
    topic = "the role of artificial intelligence in personalized education"
    # Corrected 'quiz' to 'assessment' to match the registered flow
    requested_flows = ["summary", "assessment"] 
    
    learning_context = {
        "user_level": "intermediate",
        "learning_objective": "understand practical applications",
        "time_available": "30 minutes",
        "num_questions": 5 
    }
    
    try:
        edumuse = EduMUSE()
        result = edumuse.process_educational_request(
            topic=topic,
            requested_flows=requested_flows,
            context=learning_context
        )
        
        print("雌 EduMUSE Educational Content Generated:")
        print(f"答 Topic: {result['topic']}")
        print(f"剥 Sources Found: {result['metadata']['source_count']}")
        print(f"笞｡ Flows Executed: {', '.join(result['metadata']['flows_executed'])}")
        
        _save_educational_content(result)
        
    except Exception as e:
        raise Exception(f"An error occurred while running EduMUSE: {e}")

def train():
    """Train the EduMUSE crew"""
    inputs = {
        "topic": "educational technology",
        "requested_flows": ["summary", "assessment"]
    }
    try:
        EduMUSE().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training EduMUSE: {e}")

def replay():
    """Replay the EduMUSE crew execution from a specific task"""
    try:
        EduMUSE().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying EduMUSE: {e}")

def test():
    """Test the EduMUSE crew execution"""
    inputs = {
        "topic": "AI LLMs",
        "requested_flows": ["summary"]
    }
    try:
        EduMUSE().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing EduMUSE: {e}")

def _save_educational_content(result: Dict[str, Any]):
    """Save educational content to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    import json
    with open(f"educational_content_{timestamp}.json", "w") as f:
        json.dump(result, f, indent=2)
    
    # Save individual flow outputs
    for flow_name, flow_result in result["educational_content"].items():
        filename = f"{flow_name}_output_{timestamp}.md"
        with open(filename, "w") as f:
            f.write(f"# {flow_name.title()} Output\n\n")
            f.write(f"**Topic**: {result['topic']}\n\n")
            # Get the main content from the 'sources_found' key for cleaner output
            content = flow_result.get('sources_found', str(flow_result))
            f.write(content)

if __name__ == "__main__":
    run()
