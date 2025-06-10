#!/usr/bin/env python
"""Basic test of assessment flow"""

import sys
sys.path.append('src')

from edumuse.crew import EduMUSE
from edumuse.flows.assessment_flow import AssessmentFlow

print("Testing Assessment Flow...")
print("=" * 50)

try:
    edumuse = EduMUSE()
    result = edumuse.process_educational_request(
        topic="data structures",
        requested_flows=["assessment"],
        context={
            "user_level": "intermediate",
            "num_questions": 5,
            "assessment_type": "formative",
            "question_types": ["multiple_choice", "short_answer"],
            "learning_objectives": [
                "Understand array vs linked list",
                "Analyze time complexity",
                "Choose appropriate data structures"
            ]
        }
    )
    
    print("Assessment generated successfully!")
    print(f"Topic: {result['topic']}")
    
    assessment_content = result['educational_content']['assessment']
    print(f"Assessment Type: {assessment_content.get('assessment_type', 'Unknown')}")
    print(f"Number of Questions: {assessment_content.get('content', {}).get('num_questions', 'Unknown')}")
    
    print("Assessment Preview (first 500 chars):")
    print("-" * 40)
    raw_output = assessment_content.get('content', {}).get('raw_output', 'No output')
    print(raw_output[:500] + "..." if len(raw_output) > 500 else raw_output)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
