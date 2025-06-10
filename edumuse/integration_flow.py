#!/usr/bin/env python
"""
Integration examples showing how Summary and Assessment flows work with EduMUSE
"""

from src.edumuse.crew import EduMUSE
from src.edumuse.flows.flow_registry import flow_registry

# Import all flows to ensure registration
from src.edumuse.flows.web_search_flow import WebSearchFlow
from src.edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from src.edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
from src.edumuse.flows.summary_flow import SummaryFlow
from src.edumuse.flows.assessment_flow import AssessmentFlow

def example_1_summary_generation():
    """Example: Generate multi-level summaries from academic sources"""
    
    print("Example 1: Educational Summary Generation")
    print("=" * 60)
    
    # Initialize EduMUSE
    edumuse = EduMUSE()
    
    # Process a topic with summary flow
    result = edumuse.process_educational_request(
        topic="neural networks in deep learning",
        requested_flows=["summary"],
        context={
            "user_level": "intermediate",
            "learning_objectives": [
                "Understand basic neural network architecture",
                "Learn about backpropagation",
                "Apply knowledge to simple problems"
            ],
            "summary_format": "structured",
            "study_time": "45 minutes"
        }
    )
    
    # Display results
    summary_result = result["educational_content"]["summary"]
    print(f"\nSummary Generated for: {result['topic']}")
    print(f"Content Type: {summary_result['content_type']}")
    print(f"User Level: {summary_result['summaries']['primary_level']}")
    print(f"Format: {summary_result['summaries']['format']}")
    
    print("\nSummary Preview:")
    print(summary_result['summaries']['raw_output'][:500] + "...\n")
    
    return result

def example_2_assessment_creation():
    """Example: Create assessments from academic content"""
    
    print("Example 2: Assessment Generation")
    print("=" * 60)
    
    edumuse = EduMUSE()
    
    # Generate assessment
    result = edumuse.process_educational_request(
        topic="machine learning algorithms",
        requested_flows=["assessment"],
        context={
            "user_level": "intermediate",
            "assessment_type": "formative",
            "num_questions": 10,
            "question_types": ["multiple_choice", "short_answer", "essay"],
            "learning_objectives": [
                "Identify different ML algorithm types",
                "Explain supervised vs unsupervised learning",
                "Apply algorithms to problem scenarios"
            ]
        }
    )
    
    assessment_result = result["educational_content"]["assessment"]
    print(f"\nAssessment Created for: {result['topic']}")
    print(f"Number of Questions: {assessment_result['content']['num_questions']}")
    print(f"Question Types: {', '.join(assessment_result['content']['question_types'])}")
    print(f"Difficulty Level: {assessment_result['content']['difficulty_level']}")
    
    print("\n🔍 Assessment Features:")
    for feature in assessment_result['metadata']['assessment_features']:
        print(f"   ✓ {feature.replace('_', ' ').title()}")
    
    return result

def example_3_combined_workflow():
    """Example: Complete learning workflow - discovery → summary → assessment"""
    
    print("🎓 Example 3: Complete Educational Workflow")
    print("=" * 60)
    
    edumuse = EduMUSE()
    
    # Step 1: Discover sources
    print("\nStep 1: Discovering Academic Sources...")
    discovery_result = edumuse.process_educational_request(
        topic="quantum computing fundamentals",
        requested_flows=["web_search"],
        context={"user_level": "beginner"}
    )
    
    # Step 2: Generate summaries
    print("\nStep 2: Creating Educational Summaries...")
    summary_result = edumuse.process_educational_request(
        topic="quantum computing fundamentals",
        requested_flows=["summary"],
        context={
            "user_level": "beginner",
            "summary_format": "structured",
            "sources": discovery_result["sources"]  # Use discovered sources
        }
    )
    
    # Step 3: Create assessment
    print("\nStep 3: Generating Assessment Questions...")
    assessment_result = edumuse.process_educational_request(
        topic="quantum computing fundamentals",
        requested_flows=["assessment"],
        context={
            "user_level": "beginner",
            "num_questions": 5,
            "assessment_type": "diagnostic",
            "sources": discovery_result["sources"]
        }
    )
    
    print("\nComplete Educational Package Created!")
    print(f"Sources Found: {discovery_result['metadata']['source_count']}")
    print(f"Summary Levels: {', '.join(summary_result['educational_content']['summary']['summaries']['levels'])}")
    print(f"Assessment Questions: {assessment_result['educational_content']['assessment']['content']['num_questions']}")
    
    return {
        "discovery": discovery_result,
        "summary": summary_result,
        "assessment": assessment_result
    }

def example_4_multi_flow_execution():
    """Example: Execute multiple flows simultaneously"""
    
    print("🎓 Example 4: Multi-Flow Execution")
    print("=" * 60)
    
    edumuse = EduMUSE()
    
    # Execute multiple flows at once
    result = edumuse.process_educational_request(
        topic="artificial intelligence ethics",
        requested_flows=["llm_knowledge", "summary", "assessment"],
        context={
            "user_level": "advanced",
            "learning_objectives": [
                "Analyze ethical frameworks in AI",
                "Evaluate bias in ML systems",
                "Propose ethical guidelines"
            ],
            "summary_format": "narrative",
            "num_questions": 8,
            "assessment_type": "summative"
        }
    )
    
    print(f"\nMulti-Flow Results for: {result['topic']}")
    print(f"Flows Executed: {', '.join(result['metadata']['flows_executed'])}")
    
    # Show results from each flow
    for flow_name, flow_result in result["educational_content"].items():
        print(f"\n{flow_name.upper()} Flow:")
        if "retrieval_method" in flow_result:
            print(f"   Method: {flow_result['retrieval_method']}")
        if "content_type" in flow_result:
            print(f"   Type: {flow_result['content_type']}")
        if "assessment_type" in flow_result:
            print(f"   Assessment: {flow_result['assessment_type']}")
    
    return result

def test_flow_integration():
    """Test that new flows are properly registered and working"""
    
    print("Testing Flow Integration")
    print("=" * 60)
    
    # Check registration
    all_flows = flow_registry.get_available_flows()
    content_flows = flow_registry.get_available_flows("content")
    assessment_flows = flow_registry.get_available_flows("assessment")
    
    print(f"Total Registered Flows: {len(all_flows)}")
    print(f"Content Flows: {content_flows}")
    print(f"Assessment Flows: {assessment_flows}")
    
    # Test direct flow execution
    test_sources = [{
        "title": "Introduction to Neural Networks",
        "content": "Neural networks are computing systems inspired by biological neural networks...",
        "source_type": "academic_paper"
    }]
    
    test_context = {
        "topic": "neural networks",
        "user_level": "beginner"
    }
    
    # Test summary flow
    print("\nTesting Summary Flow Direct Execution...")
    summary_result = flow_registry.execute_flow("summary", test_sources, test_context)
    print(f"Summary flow executed: {summary_result['flow_type']}")
    
    # Test assessment flow
    print("\nTesting Assessment Flow Direct Execution...")
    assessment_result = flow_registry.execute_flow("assessment", test_sources, test_context)
    print(f"Assessment flow executed: {assessment_result['flow_type']}")

if __name__ == "__main__":
    print("🎓 EduMUSE Integration Examples")
    print("=" * 70)
    print("Demonstrating Summary and Assessment Flow Integration\n")
    
    # Run examples
    example_1_summary_generation()
    print("\n" + "="*70 + "\n")
    
    example_2_assessment_creation()
    print("\n" + "="*70 + "\n")
    
    example_3_combined_workflow()
    print("\n" + "="*70 + "\n")
    
    example_4_multi_flow_execution()
    print("\n" + "="*70 + "\n")
    
    test_flow_integration()
    
    print("\nIntegration examples completed successfully!")