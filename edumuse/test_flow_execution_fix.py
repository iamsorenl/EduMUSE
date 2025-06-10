#!/usr/bin/env python
"""Test direct flow execution without CrewAI interference"""

from src.edumuse.flows.flow_registry import flow_registry

# 🔧 FIXED: Import all flows to trigger registration
from src.edumuse.flows.web_search_flow import WebSearchFlow
from src.edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from src.edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow

def test_direct_flow_execution():
    """Test flows execute directly and return substantial content"""
    
    print("🧪 Testing Direct Flow Execution")
    print("=" * 50)
    
    # Check what flows are registered
    print(f"📋 Registered flows: {flow_registry.get_available_flows()}")
    print(f"🧠 Knowledge flows: {flow_registry.get_available_flows('knowledge_retrieval')}")
    
    # Mock sources
    sources = [
        {
            "title": "Test Academic Paper on Machine Learning",
            "url": "https://arxiv.org/test",
            "credibility_score": 8.5
        }
    ]
    
    context = {
        "topic": "machine learning transformers",
        "user_level": "graduate"
    }
    
    flows_to_test = ["web_search", "llm_knowledge", "hybrid_retrieval"]
    
    for flow_name in flows_to_test:
        print(f"\n📚 Testing {flow_name} flow directly...")
        
        try:
            result = flow_registry.execute_flow(flow_name, sources, context)
            
            print(f"✅ {flow_name} executed successfully")
            print(f"   🔍 Flow Type: {result.get('flow_type', 'unknown')}")
            print(f"   📝 Retrieval Method: {result.get('retrieval_method', 'unknown')}")
            print(f"   📊 Content Length: {len(str(result.get('sources_found', '')))}")
            print(f"   📖 Content Sample: {str(result.get('sources_found', ''))[:100]}...")
            
            if len(str(result.get('sources_found', ''))) > 200:
                print(f"   ✅ Substantial content generated")
            else:
                print(f"   ⚠️  Limited content")
                print(f"   🔍 Full result: {result}")
                
        except Exception as e:
            print(f"❌ {flow_name} failed: {e}")
            import traceback
            traceback.print_exc()

def test_flow_info():
    """Test getting flow information"""
    
    print(f"\n📊 Testing Flow Information")
    print("=" * 50)
    
    flows = ["web_search", "llm_knowledge", "hybrid_retrieval"]
    
    for flow_name in flows:
        if flow_name in flow_registry.flows:
            try:
                info = flow_registry.flows[flow_name].get_flow_info()
                print(f"\n🔬 {flow_name.upper()} Info:")
                print(f"   📝 Name: {info.get('name', 'Unknown')}")
                print(f"   📖 Description: {info.get('description', 'No description')}")
                print(f"   💪 Strengths: {info.get('strengths', [])}")
                print(f"   ⚠️  Limitations: {info.get('limitations', [])}")
            except Exception as e:
                print(f"❌ Error getting {flow_name} info: {e}")
        else:
            print(f"❌ {flow_name} not found in registry")

if __name__ == "__main__":
    test_direct_flow_execution()
    test_flow_info()