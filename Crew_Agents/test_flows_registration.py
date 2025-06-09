#!/usr/bin/env python
"""Test flow registration and basic functionality"""

from src.edumuse.flows.flow_registry import flow_registry

# 🔧 FIXED: Import your flows to trigger registration
from src.edumuse.flows.web_search_flow import WebSearchFlow
from src.edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow  
from src.edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow

def test_flow_registration():
    """Test that all knowledge retrieval flows are properly registered"""
    
    print("🔍 Testing Flow Registration")
    print("="*50)
    
    # Check available flows
    all_flows = flow_registry.get_available_flows()
    knowledge_flows = flow_registry.get_available_flows("knowledge_retrieval")
    
    print(f"📋 All Flows: {all_flows}")
    print(f"🧠 Knowledge Retrieval Flows: {knowledge_flows}")
    
    # Expected flows
    expected_flows = ["web_search", "llm_knowledge", "hybrid_retrieval"]
    
    for flow_name in expected_flows:
        if flow_name in knowledge_flows:
            print(f"✅ {flow_name} - Registered")
            
            # Test flow info
            try:
                if flow_name in flow_registry.flows:
                    flow_info = flow_registry.flows[flow_name].get_flow_info()
                    print(f"   📝 Description: {flow_info['description']}")
                    print(f"   💪 Strengths: {flow_info.get('strengths', [])}")
                else:
                    print(f"   ⚠️  Flow object not found in registry")
            except Exception as e:
                print(f"   ❌ Error getting flow info: {e}")
        else:
            print(f"❌ {flow_name} - NOT REGISTERED")
    
    return len(knowledge_flows) == 3

def test_mock_execution():
    """Test mock execution of flows"""
    
    print("\n🧪 Testing Mock Flow Execution")
    print("="*50)
    
    # Mock sources and context
    mock_sources = [
        {
            "title": "Test Academic Paper",
            "url": "https://arxiv.org/test",
            "credibility_score": 8.5
        }
    ]
    
    mock_context = {
        "topic": "machine learning transformers",
        "user_level": "graduate"
    }
    
    flows_to_test = ["web_search", "llm_knowledge", "hybrid_retrieval"]
    
    for flow_name in flows_to_test:
        print(f"\n📚 Testing {flow_name}...")
        
        try:
            result = flow_registry.execute_flow(flow_name, mock_sources, mock_context)
            
            print(f"✅ {flow_name} executed successfully")
            print(f"   🔍 Retrieval Method: {result.get('retrieval_method', 'unknown')}")
            print(f"   📊 Topic: {result.get('topic', 'unknown')}")
            print(f"   🎯 Flow Type: {result.get('flow_type', 'unknown')}")
            print(f"   📄 Content Length: {len(str(result.get('sources_found', '')))}")
            
        except Exception as e:
            print(f"❌ {flow_name} failed: {e}")

if __name__ == "__main__":
    print("🎓 EduMUSE Knowledge Retrieval Flow Testing")
    print("="*60)
    
    # Test registration
    registration_success = test_flow_registration()
    
    # Test mock execution
    test_mock_execution()
    
    if registration_success:
        print("\n🎯 Next Steps:")
        print("   1. Run: python test_knowledge_retrieval.py")
        print("   2. Compare retrieval quality across methods")
        print("   3. Analyze processing times and source credibility")
        print("   4. Document experimental findings")
        print("\n✨ Your knowledge retrieval system is ready for academic evaluation!")
    else:
        print("\n⚠️  Fix flow registration issues first")