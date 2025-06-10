#!/usr/bin/env python
"""Verify new flows are properly installed"""

import sys
sys.path.append('src')

from edumuse.flows.flow_registry import flow_registry

# Import all flows to trigger registration
try:
    from edumuse.flows.web_search_flow import WebSearchFlow
    from edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
    from edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
    from edumuse.flows.summary_flow import SummaryFlow
    from edumuse.flows.assessment_flow import AssessmentFlow
    print("All flow imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

print("Checking Flow Registration...")
print("-" * 50)

all_flows = flow_registry.get_available_flows()
print(f"Total Registered Flows: {len(all_flows)}")
print(f"All Flows: {all_flows}")

# Check specific categories
content_flows = flow_registry.get_available_flows("content")
assessment_flows = flow_registry.get_available_flows("assessment")

print(f"Content Flows: {content_flows}")
print(f"Assessment Flows: {assessment_flows}")

# Verify our new flows are registered
if "summary" in all_flows and "assessment" in all_flows:
    print("Both new flows are successfully registered!")
else:
    print("New flows are not properly registered")
    if "summary" not in all_flows:
        print("   - Summary flow missing")
    if "assessment" not in all_flows:
        print("   - Assessment flow missing")
