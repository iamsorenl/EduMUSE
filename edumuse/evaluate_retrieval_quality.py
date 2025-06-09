#!/usr/bin/env python
"""Comprehensive evaluation of knowledge retrieval quality"""

import time
from typing import Dict, List, Any
from src.edumuse.flows.flow_registry import flow_registry

# 🔧 CRITICAL: Import flows to trigger registration
from src.edumuse.flows.web_search_flow import WebSearchFlow
from src.edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from src.edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow

class RetrievalQualityEvaluator:
    """Evaluate and compare knowledge retrieval methods quantitatively"""
    
    def __init__(self):
        self.evaluation_criteria = {
            "relevance": {"weight": 0.3, "max_score": 10},
            "credibility": {"weight": 0.25, "max_score": 10}, 
            "coverage": {"weight": 0.2, "max_score": 10},
            "recency": {"weight": 0.15, "max_score": 10},
            "accessibility": {"weight": 0.1, "max_score": 10}
        }
    
    def evaluate_retrieval_session(self, topic: str, flow_name: str) -> Dict[str, Any]:
        """Evaluate a single retrieval session with timing and quality metrics"""
        
        print(f"📊 Evaluating {flow_name} for topic: {topic}")
        
        # Time the retrieval
        start_time = time.time()
        
        # 🔧 FIXED: Call flows directly instead of through EduMUSE crew
        sources = [
            {
                "title": f"Academic Source about {topic}",
                "url": "https://example.edu/paper1",
                "credibility_score": 8.5,
                "source_type": "academic_paper"
            }
        ]
        
        context = {
            "topic": topic,
            "user_level": "graduate"
        }
        
        # Execute the actual working flow directly
        flow_result = flow_registry.execute_flow(flow_name, sources, context)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"   🔍 Flow result keys: {list(flow_result.keys())}")
        
        # Extract content using the same method that worked in tests
        content = self._extract_content_safely(flow_result)
        print(f"   📝 Content extracted: {len(content)} chars")
        
        # Evaluate quality dimensions with proper content
        quality_scores = self._evaluate_quality_dimensions(flow_result, topic, content)
        
        # Calculate weighted score
        total_score = sum(
            quality_scores[criterion] * self.evaluation_criteria[criterion]["weight"] 
            for criterion in quality_scores
        )
        
        return {
            "topic": topic,
            "flow_name": flow_name,
            "processing_time": processing_time,
            "quality_scores": quality_scores,
            "total_score": total_score,
            "sources_count": self._count_sources(flow_result, content),
            "content_length": len(content),
            "retrieval_method": flow_result.get("retrieval_method", "direct_flow_execution")
        }
    
    def _extract_content_safely(self, flow_result: Dict) -> str:
        """🔧 FIXED: Extract content using the exact same logic that worked in tests"""
        
        # First try 'sources_found' which is what our flows use
        if "sources_found" in flow_result:
            content = str(flow_result["sources_found"])
            if len(content) > 50:  # Substantial content
                return content
        
        # Fallback to other possible keys
        content_keys = ["content", "result", "output"]
        for key in content_keys:
            if key in flow_result:
                content = str(flow_result[key])
                if len(content) > 50:
                    return content
        
        # Last resort: full result
        return str(flow_result)
    
    def _evaluate_quality_dimensions(self, flow_result: Dict, topic: str, content: str) -> Dict[str, float]:
        """🔧 FIXED: Evaluate using the actual content"""
        
        print(f"   🔍 Evaluating content: {content[:100]}...")
        
        scores = {
            "relevance": self._score_relevance(content, topic),
            "credibility": self._score_credibility(flow_result, content),
            "coverage": self._score_coverage(content),
            "recency": self._score_recency(content),
            "accessibility": self._score_accessibility(flow_result)
        }
        
        print(f"   📊 Scores: {scores}")
        return scores
    
    def _score_relevance(self, content: str, topic: str) -> float:
        """Score relevance to topic"""
        if not content or len(content) < 50:
            return 0.0
            
        topic_keywords = topic.lower().split()
        content_lower = content.lower()
        
        # Count keyword matches
        matches = sum(1 for keyword in topic_keywords if keyword in content_lower)
        base_score = min(10.0, (matches / len(topic_keywords)) * 10)
        
        # Bonus for academic indicators
        academic_terms = ["paper", "research", "study", "analysis", "arxiv", "university", "journal"]
        academic_matches = sum(1 for term in academic_terms if term in content_lower)
        academic_bonus = min(3.0, academic_matches * 0.5)
        
        final_score = min(10.0, base_score + academic_bonus)
        print(f"     Relevance: {matches}/{len(topic_keywords)} keywords, {academic_matches} academic terms → {final_score:.1f}")
        
        return final_score
    
    def _score_credibility(self, flow_result: Dict, content: str) -> float:
        """Score source credibility"""
        retrieval_method = flow_result.get("retrieval_method", "")
        
        # Base score by method
        if "web_api_search" in retrieval_method:
            base_score = 8.5
        elif "training_data_synthesis" in retrieval_method:
            base_score = 7.5
        elif "web_search_plus_llm" in retrieval_method:
            base_score = 9.0
        else:
            base_score = 6.0  # Unknown but executed
        
        # Bonus for credible indicators
        if content:
            indicators = ["arxiv.org", ".edu", "university", "journal", "peer review", "doi:"]
            bonus = sum(0.2 for indicator in indicators if indicator in content.lower())
            base_score += min(1.0, bonus)
        
        return min(10.0, base_score)
    
    def _score_coverage(self, content: str) -> float:
        """Score content comprehensiveness"""
        length = len(content)
        
        if length > 3000:
            return 9.0
        elif length > 2000:
            return 8.0
        elif length > 1000:
            return 7.0
        elif length > 500:
            return 5.0
        elif length > 200:
            return 3.0
        elif length > 50:
            return 2.0
        else:
            return 1.0
    
    def _score_recency(self, content: str) -> float:
        """Score source recency"""
        if not content:
            return 0.0
            
        recent_years = ["2023", "2024", "2025"]
        recent_count = sum(content.count(year) for year in recent_years)
        
        older_years = ["2020", "2021", "2022"]
        older_count = sum(content.count(year) for year in older_years)
        
        score = (recent_count * 2.0) + (older_count * 1.0)
        return min(10.0, score)
    
    def _score_accessibility(self, flow_result: Dict) -> float:
        """Score source accessibility"""
        method = flow_result.get("retrieval_method", "")
        
        if "training_data" in method:
            return 10.0
        elif "web" in method:
            return 8.0
        else:
            return 7.0
    
    def _count_sources(self, flow_result: Dict, content: str) -> int:
        """Count sources found"""
        if not content:
            return 0
        
        # Count source indicators
        indicators = [
            content.count("http"),
            content.count("arxiv"),
            content.count("Title:"),
            content.count("Paper:"),
            content.count("Journal:"),
            len([line for line in content.split('\n') if any(term in line.lower() 
                for term in ['university', 'journal', 'conference'])])
        ]
        
        return max(indicators + [1])
    
    def compare_all_methods(self, test_topics: List[str]) -> Dict[str, Any]:
        """Comprehensive comparison across all retrieval methods"""
        
        flows = ["web_search", "llm_knowledge", "hybrid_retrieval"]
        results = []
        
        print(f"🔬 Testing {len(flows)} flows across {len(test_topics)} topics")
        print(f"📋 Available flows: {flow_registry.get_available_flows()}")
        
        for topic in test_topics:
            print(f"\n🎯 Testing topic: {topic}")
            for flow_name in flows:
                evaluation = self.evaluate_retrieval_session(topic, flow_name)
                results.append(evaluation)
        
        return self._analyze_comparative_results(results)
    
    def _analyze_comparative_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze comparative performance across methods"""
        
        # Group by flow type
        flow_performance = {}
        
        for result in results:
            flow_name = result["flow_name"]
            if flow_name not in flow_performance:
                flow_performance[flow_name] = []
            flow_performance[flow_name].append(result)
        
        # Calculate averages
        summary = {}
        for flow_name, flow_results in flow_performance.items():
            summary[flow_name] = {
                "avg_processing_time": sum(r["processing_time"] for r in flow_results) / len(flow_results),
                "avg_total_score": sum(r["total_score"] for r in flow_results) / len(flow_results),
                "avg_sources_count": sum(r["sources_count"] for r in flow_results) / len(flow_results),
                "avg_content_length": sum(r["content_length"] for r in flow_results) / len(flow_results),
                "quality_breakdown": {
                    criterion: sum(r["quality_scores"][criterion] for r in flow_results) / len(flow_results)
                    for criterion in self.evaluation_criteria.keys()
                }
            }
        
        return {
            "individual_results": results,
            "comparative_summary": summary,
            "methodology": {
                "evaluation_criteria": self.evaluation_criteria,
                "test_topics_count": len(set(r["topic"] for r in results)),
                "flows_tested": list(flow_performance.keys())
            }
        }

def run_comprehensive_evaluation():
    """Run comprehensive evaluation for academic reporting"""
    
    evaluator = RetrievalQualityEvaluator()
    
    test_topics = [
        "machine learning transformers",
        "quantum computing algorithms"
    ]
    
    print("🔬 Running DIRECT FLOW Comprehensive Evaluation")
    print("=" * 70)
    
    results = evaluator.compare_all_methods(test_topics)
    
    # Print detailed results
    print("\n📊 COMPARATIVE SUMMARY:")
    print("=" * 50)
    
    for flow_name, performance in results["comparative_summary"].items():
        print(f"\n🎯 {flow_name.upper()} PERFORMANCE:")
        print(f"   ⏱️  Avg Processing Time: {performance['avg_processing_time']:.2f}s")
        print(f"   🏆 Avg Quality Score: {performance['avg_total_score']:.2f}/10")
        print(f"   📚 Avg Sources Found: {performance['avg_sources_count']:.1f}")
        print(f"   📄 Avg Content Length: {performance['avg_content_length']:.0f} chars")
        
        print(f"   📊 Quality Breakdown:")
        for criterion, score in performance["quality_breakdown"].items():
            print(f"      {criterion.title()}: {score:.1f}/10")
    
    # Save results
    import json
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    with open(f"knowledge_retrieval_evaluation_WORKING_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: knowledge_retrieval_evaluation_WORKING_{timestamp}.json")
    
    return results

if __name__ == "__main__":
    run_comprehensive_evaluation()