#!/usr/bin/env python
"""
Test and evaluate Summary and Assessment flows using the existing evaluation framework
"""

import time
from typing import Dict, List, Any
from src.edumuse.flows.flow_registry import flow_registry

# Import all flows
from src.edumuse.flows.web_search_flow import WebSearchFlow
from src.edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from src.edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
from src.edumuse.flows.summary_flow import SummaryFlow
from src.edumuse.flows.assessment_flow import AssessmentFlow

class NewFlowEvaluator:
    """Evaluate quality of Summary and Assessment flows"""
    
    def __init__(self):
        # Summary flow evaluation criteria
        self.summary_criteria = {
            "clarity": {"weight": 0.25, "max_score": 10},
            "completeness": {"weight": 0.20, "max_score": 10},
            "level_appropriateness": {"weight": 0.20, "max_score": 10},
            "pedagogical_value": {"weight": 0.20, "max_score": 10},
            "structure": {"weight": 0.15, "max_score": 10}
        }
        
        # Assessment flow evaluation criteria
        self.assessment_criteria = {
            "question_quality": {"weight": 0.30, "max_score": 10},
            "cognitive_variety": {"weight": 0.20, "max_score": 10},
            "answer_accuracy": {"weight": 0.20, "max_score": 10},
            "difficulty_calibration": {"weight": 0.15, "max_score": 10},
            "educational_value": {"weight": 0.15, "max_score": 10}
        }
    
    def evaluate_summary_flow(self, topic: str, user_level: str) -> Dict[str, Any]:
        """Evaluate summary flow performance"""
        
        print(f"\nEvaluating Summary Flow")
        print(f"   Topic: {topic}")
        print(f"   User Level: {user_level}")
        
        # Prepare test data
        sources = self._create_test_sources(topic)
        context = {
            "topic": topic,
            "user_level": user_level,
            "learning_objectives": [
                f"Understand fundamental concepts of {topic}",
                f"Apply {topic} principles to real scenarios",
                f"Analyze relationships within {topic}"
            ],
            "summary_format": "structured"
        }
        
        # Time the execution
        start_time = time.time()
        result = flow_registry.execute_flow("summary", sources, context)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Evaluate quality dimensions
        quality_scores = self._evaluate_summary_quality(result, topic, user_level)
        
        # Calculate weighted score
        total_score = sum(
            quality_scores[criterion] * self.summary_criteria[criterion]["weight"]
            for criterion in quality_scores
        )
        
        return {
            "flow_name": "summary",
            "topic": topic,
            "user_level": user_level,
            "processing_time": processing_time,
            "quality_scores": quality_scores,
            "total_score": total_score,
            "content_length": len(str(result.get("summaries", {}).get("raw_output", ""))),
            "features_delivered": self._check_summary_features(result)
        }
    
    def evaluate_assessment_flow(self, topic: str, user_level: str, num_questions: int = 10) -> Dict[str, Any]:
        """Evaluate assessment flow performance"""
        
        print(f"\nEvaluating Assessment Flow")
        print(f"   Topic: {topic}")
        print(f"   User Level: {user_level}")
        print(f"   Questions: {num_questions}")
        
        # Prepare test data
        sources = self._create_test_sources(topic)
        context = {
            "topic": topic,
            "user_level": user_level,
            "num_questions": num_questions,
            "assessment_type": "formative",
            "question_types": ["multiple_choice", "short_answer", "essay"],
            "learning_objectives": [
                f"Recall key facts about {topic}",
                f"Explain concepts related to {topic}",
                f"Apply {topic} knowledge to solve problems"
            ]
        }
        
        # Time the execution
        start_time = time.time()
        result = flow_registry.execute_flow("assessment", sources, context)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        # Evaluate quality dimensions
        quality_scores = self._evaluate_assessment_quality(result, topic, user_level)
        
        # Calculate weighted score
        total_score = sum(
            quality_scores[criterion] * self.assessment_criteria[criterion]["weight"]
            for criterion in quality_scores
        )
        
        return {
            "flow_name": "assessment",
            "topic": topic,
            "user_level": user_level,
            "processing_time": processing_time,
            "quality_scores": quality_scores,
            "total_score": total_score,
            "num_questions": num_questions,
            "features_delivered": self._check_assessment_features(result)
        }
    
    def _create_test_sources(self, topic: str) -> List[Dict[str, Any]]:
        """Create realistic test sources"""
        return [
            {
                "title": f"Introduction to {topic}",
                "source_type": "textbook",
                "content": f"Comprehensive overview of {topic} including fundamental principles, key concepts, and practical applications. This foundational text covers historical development, current state, and future directions.",
                "credibility_score": 9.0
            },
            {
                "title": f"Recent Advances in {topic}",
                "source_type": "academic_paper",
                "abstract": f"This paper reviews recent developments in {topic}, analyzing breakthrough discoveries and their implications for the field. We examine novel approaches and methodologies that have emerged in the last five years.",
                "credibility_score": 8.5
            },
            {
                "title": f"Practical Guide to {topic}",
                "source_type": "educational_resource",
                "content": f"Step-by-step guide for understanding and applying {topic} concepts. Includes examples, exercises, and real-world case studies to reinforce learning.",
                "credibility_score": 8.0
            }
        ]
    
    def _evaluate_summary_quality(self, result: Dict, topic: str, user_level: str) -> Dict[str, float]:
        """Evaluate summary quality dimensions"""
        
        content = str(result.get("summaries", {}).get("raw_output", ""))
        
        scores = {}
        
        # Clarity - Is the summary clear and well-written?
        clarity_indicators = ["clear", "example", "explain", "understand", "simple"]
        clarity_count = sum(1 for indicator in clarity_indicators if indicator in content.lower())
        scores["clarity"] = min(10.0, 2.0 + clarity_count * 1.6)
        
        # Completeness - Does it cover multiple levels?
        level_indicators = ["beginner", "intermediate", "advanced"]
        levels_found = sum(1 for level in level_indicators if level in content.lower())
        scores["completeness"] = min(10.0, levels_found * 3.3)
        
        # Level appropriateness - Is it tailored to the user level?
        if user_level.lower() in content.lower():
            scores["level_appropriateness"] = 8.0
        else:
            scores["level_appropriateness"] = 5.0
        
        # Pedagogical value - Does it include learning aids?
        pedagogy_indicators = ["objective", "concept", "takeaway", "glossary", "tip"]
        pedagogy_count = sum(1 for indicator in pedagogy_indicators if indicator in content.lower())
        scores["pedagogical_value"] = min(10.0, 2.0 + pedagogy_count * 1.6)
        
        # Structure - Is it well-organized?
        structure_indicators = ["===", "level", "summary", topic.lower()]
        structure_count = sum(1 for indicator in structure_indicators if indicator in content.lower())
        scores["structure"] = min(10.0, 2.0 + structure_count * 2.0)
        
        return scores
    
    def _evaluate_assessment_quality(self, result: Dict, topic: str, user_level: str) -> Dict[str, float]:
        """Evaluate assessment quality dimensions"""
        
        content = str(result.get("content", {}).get("raw_output", ""))
        
        scores = {}
        
        # Question quality - Are questions well-formed?
        quality_indicators = ["question", "?", "explain", "describe", "analyze"]
        quality_count = sum(1 for indicator in quality_indicators if indicator in content.lower())
        scores["question_quality"] = min(10.0, 2.0 + quality_count * 1.6)
        
        # Cognitive variety - Multiple cognitive levels?
        cognitive_indicators = ["remember", "understand", "apply", "analyze", "evaluate"]
        cognitive_count = sum(1 for indicator in cognitive_indicators if indicator in content.lower())
        scores["cognitive_variety"] = min(10.0, 2.0 + cognitive_count * 1.6)
        
        # Answer accuracy - Are answers provided?
        answer_indicators = ["answer", "correct", "explanation", "rubric"]
        answer_count = sum(1 for indicator in answer_indicators if indicator in content.lower())
        scores["answer_accuracy"] = min(10.0, 2.0 + answer_count * 2.0)
        
        # Difficulty calibration - Appropriate for level?
        if user_level.lower() in content.lower():
            scores["difficulty_calibration"] = 8.0
        else:
            scores["difficulty_calibration"] = 5.0
        
        # Educational value - Learning features included?
        edu_indicators = ["feedback", "learning", "tip", "explanation"]
        edu_count = sum(1 for indicator in edu_indicators if indicator in content.lower())
        scores["educational_value"] = min(10.0, 2.0 + edu_count * 2.0)
        
        return scores
    
    def _check_summary_features(self, result: Dict) -> List[str]:
        """Check which summary features were delivered"""
        features = []
        content = str(result)
        
        if "beginner" in content.lower() and "intermediate" in content.lower() and "advanced" in content.lower():
            features.append("multi_level_summaries")
        if "glossary" in content.lower() or "terms" in content.lower():
            features.append("glossary_included")
        if "takeaway" in content.lower() or "key point" in content.lower():
            features.append("key_takeaways")
        if "study" in content.lower() and "tip" in content.lower():
            features.append("study_tips")
        if "objective" in content.lower():
            features.append("learning_objectives")
            
        return features
    
    def _check_assessment_features(self, result: Dict) -> List[str]:
        """Check which assessment features were delivered"""
        features = []
        content = str(result)
        
        if "multiple choice" in content.lower():
            features.append("multiple_choice_questions")
        if "short answer" in content.lower():
            features.append("short_answer_questions")
        if "essay" in content.lower():
            features.append("essay_questions")
        if "rubric" in content.lower():
            features.append("scoring_rubrics")
        if "explanation" in content.lower():
            features.append("answer_explanations")
        if "feedback" in content.lower():
            features.append("learning_feedback")
            
        return features

def run_comprehensive_flow_evaluation():
    """Run comprehensive evaluation of new flows"""
    
    evaluator = NewFlowEvaluator()
    
    test_configs = [
        {"topic": "machine learning fundamentals", "levels": ["beginner", "intermediate", "advanced"]},
        {"topic": "quantum computing basics", "levels": ["beginner", "intermediate"]},
        {"topic": "data structures and algorithms", "levels": ["intermediate", "advanced"]}
    ]
    
    all_results = {
        "summary_evaluations": [],
        "assessment_evaluations": []
    }
    
    print("Comprehensive Flow Quality Evaluation")
    print("=" * 70)
    
    # Evaluate Summary Flow
    print("\nSUMMARY FLOW EVALUATION")
    print("-" * 50)
    
    for config in test_configs:
        for level in config["levels"]:
            result = evaluator.evaluate_summary_flow(config["topic"], level)
            all_results["summary_evaluations"].append(result)
            
            print(f"\nCompleted: {config['topic']} - {level}")
            print(f"   Total Score: {result['total_score']:.2f}/10")
            print(f"   Processing Time: {result['processing_time']:.2f}s")
            print(f"   Features: {', '.join(result['features_delivered'])}")
    
    # Evaluate Assessment Flow
    print("\n\nASSESSMENT FLOW EVALUATION")
    print("-" * 50)
    
    for config in test_configs:
        for level in config["levels"]:
            result = evaluator.evaluate_assessment_flow(config["topic"], level, num_questions=8)
            all_results["assessment_evaluations"].append(result)
            
            print(f"\nCompleted: {config['topic']} - {level}")
            print(f"   Total Score: {result['total_score']:.2f}/10")
            print(f"   Processing Time: {result['processing_time']:.2f}s")
            print(f"   Features: {', '.join(result['features_delivered'])}")
    
    # Summary Statistics
    print("\n\nEVALUATION SUMMARY")
    print("=" * 70)
    
    # Summary Flow Stats
    summary_scores = [r["total_score"] for r in all_results["summary_evaluations"]]
    summary_times = [r["processing_time"] for r in all_results["summary_evaluations"]]
    
    print("\nSummary Flow Performance:")
    print(f"   Average Quality Score: {sum(summary_scores)/len(summary_scores):.2f}/10")
    print(f"   Average Processing Time: {sum(summary_times)/len(summary_times):.2f}s")
    print(f"   Tests Run: {len(summary_scores)}")
    
    # Assessment Flow Stats
    assessment_scores = [r["total_score"] for r in all_results["assessment_evaluations"]]
    assessment_times = [r["processing_time"] for r in all_results["assessment_evaluations"]]
    
    print("\nAssessment Flow Performance:")
    print(f"   Average Quality Score: {sum(assessment_scores)/len(assessment_scores):.2f}/10")
    print(f"   Average Processing Time: {sum(assessment_times)/len(assessment_times):.2f}s")
    print(f"   Tests Run: {len(assessment_scores)}")
    
    # Save results
    import json
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"new_flows_evaluation_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nDetailed results saved to: {filename}")
    
    return all_results

if __name__ == "__main__":
    run_comprehensive_flow_evaluation()