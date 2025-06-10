#!/usr/bin/env python
"""Basic test of summary flow"""

import sys
sys.path.append('src')

from edumuse.crew import EduMUSE
from edumuse.flows.summary_flow import SummaryFlow

print("🎓 Testing Summary Flow...")
print("=" * 50)

try:
    edumuse = EduMUSE()
    result = edumuse.process_educational_request(
        topic="python programming basics",
        requested_flows=["summary"],
        context={
            "user_level": "beginner",
            "summary_format": "structured",
            "learning_objectives": [
                "Understand Python syntax",
                "Learn basic data types",
                "Write simple programs"
            ]
        }
    )
    
    print("Summary generated successfully!")
    print(f"Topic: {result['topic']}")
    
    summary_content = result['educational_content']['summary']
    print(f"Content Type: {summary_content.get('content_type', 'Unknown')}")
    print(f"Primary Level: {summary_content.get('summaries', {}).get('primary_level', 'Unknown')}")
    
    print("Content Preview (first 500 chars):")
    print("-" * 40)
    raw_output = summary_content.get('summaries', {}).get('raw_output', 'No output')
    print(raw_output)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
