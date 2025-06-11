# COPY CONTENT FROM summary_flow.py ARTIFACT
# This file implements the Summary Flow for EduMUSE
from crewai import Agent, Crew, Task, Process
from typing import List, Dict, Any
from .flow_registry import EducationFlow, flow_registry

class SummaryFlow(EducationFlow):
    """Multi-level educational summary generation flow"""
    
    def __init__(self):
        # Concept Extraction Agent
        self.concept_extractor = Agent(
            role="Educational Concept Analyst",
            goal="Extract key concepts, learning objectives, and core ideas from academic sources",
            backstory="""You are an expert educator with deep experience in curriculum design 
            and pedagogical content analysis. You excel at identifying the most important 
            concepts in academic materials and understanding how they connect to form a 
            comprehensive knowledge structure. You can quickly identify learning objectives 
            and prerequisite knowledge required for understanding complex topics.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Summary Writer Agent
        self.summary_writer = Agent(
            role="Adaptive Educational Content Writer",
            goal="Create clear, engaging summaries tailored to different learning levels",
            backstory="""You are a skilled educational content creator who specializes in 
            making complex academic content accessible to learners at all levels. You have 
            extensive experience writing for diverse audiences, from beginners to advanced 
            students, and excel at explaining difficult concepts using appropriate analogies, 
            examples, and progressive complexity. You understand cognitive load theory and 
            apply it to create effective learning materials.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Learning Level Adapter Agent
        self.level_adapter = Agent(
            role="Educational Differentiation Specialist",
            goal="Adapt educational content to match learner's knowledge level and learning style",
            backstory="""You are an expert in differentiated instruction with deep understanding 
            of how students at different levels process information. You know how to scaffold 
            content, provide appropriate context, and adjust vocabulary and complexity to match 
            learner needs. You're skilled at creating multiple representations of the same 
            concept for different audiences while maintaining educational integrity.""",
            verbose=True,
            allow_delegation=False
        )
    
    @property
    def flow_type(self) -> str:
        return "content"
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process academic sources to generate multi-level educational summaries"""
        
        topic = context.get('topic', 'general academic topic')
        user_level = context.get('user_level', 'intermediate')
        learning_objectives = context.get('learning_objectives', [])
        summary_format = context.get('summary_format', 'structured')
        
        # Task 1: Extract key concepts and learning objectives
        concept_extraction_task = Task(
            description=f"""
            Analyze the provided academic sources about '{topic}' and extract:
            
            1. **Core Concepts**: Identify 5-10 key concepts that are essential for understanding the topic
            2. **Learning Objectives**: Determine what students should know/be able to do after studying this material
            3. **Concept Relationships**: Map how concepts connect and build upon each other
            4. **Prerequisite Knowledge**: Identify what learners need to know beforehand
            5. **Difficulty Indicators**: Note which concepts are typically challenging for learners
            
            Sources to analyze:
            {self._format_sources(sources)}
            
            Provide a structured analysis that will guide summary creation.
            """,
            agent=self.concept_extractor,
            expected_output="""A comprehensive concept analysis including:
            - List of core concepts with brief definitions
            - Clear learning objectives (knowledge, skills, applications)
            - Concept map showing relationships
            - Prerequisites and difficulty assessments"""
        )
        
        # Task 2: Create multi-level summaries
        summary_creation_task = Task(
            description=f"""
            Based on the concept analysis, create educational summaries for topic '{topic}':
            
            Create THREE versions targeting different levels:
            
            1. **Beginner Level**:
               - Use simple language and everyday examples
               - Focus on fundamental concepts only
               - Include helpful analogies and visual descriptions
               - Avoid technical jargon
               - Length: 300-400 words
            
            2. **Intermediate Level**:
               - Include more technical terminology with clear explanations
               - Cover main concepts and some applications
               - Provide real-world examples from the field
               - Show connections between concepts
               - Length: 500-700 words
            
            3. **Advanced Level**:
               - Use field-appropriate technical language
               - Include nuanced details and edge cases
               - Discuss current research and open questions
               - Connect to broader theoretical frameworks
               - Length: 800-1000 words
            
            Summary format requested: {summary_format}
            User's primary level: {user_level}
            """,
            agent=self.summary_writer,
            expected_output="""Three complete summaries (beginner, intermediate, advanced) 
            formatted according to the requested style, each clearly labeled and 
            containing appropriate content for its target level"""
        )
        
        # Task 3: Optimize for user's specific needs
        adaptation_task = Task(
            description=f"""
            Refine and optimize the summaries for the specific learner:
            
            User Level: {user_level}
            Learning Objectives: {learning_objectives if learning_objectives else 'General understanding'}
            
            Enhance the summaries by:
            1. **Highlighting** the most relevant summary level for the user
            2. **Adding transitions** between levels to show learning progression
            3. **Including study tips** specific to the user's level
            4. **Suggesting next steps** for continued learning
            5. **Creating a glossary** of important terms
            
            Also provide:
            - Key takeaways (5-7 bullet points)
            - Recommended study sequence
            - Self-check questions for understanding
            """,
            agent=self.level_adapter,
            expected_output="""Enhanced summaries with:
            - Optimized content for user's level
            - Learning progression guidance
            - Glossary and study aids
            - Personalized recommendations"""
        )
        
        # Create and run the crew
        summary_crew = Crew(
            agents=[self.concept_extractor, self.summary_writer, self.level_adapter],
            tasks=[concept_extraction_task, summary_creation_task, adaptation_task],
            process=Process.sequential,
            verbose=True
        )
        
        crew_output = summary_crew.kickoff()
        
        # ✅ FIXED: Match the expected frontend structure
        return {
            "flow_type": "summary",
            "retrieval_method": "educational_summarization",
            "sources_found": str(crew_output),  # ← Frontend expects this field!
            "topic": topic,
            "metadata": {
                "summary_levels": ["beginner", "intermediate", "advanced"],
                "user_level": user_level,
                "generation_method": "concept_extraction_to_adaptive_summary",
                "agents_used": ["concept_extractor", "summary_writer", "level_adapter"],
                "word_count": len(str(crew_output).split()),
                "estimated_reading_time": f"{len(str(crew_output).split()) // 200 + 1} minutes"
            },
            # Keep additional data for potential future use
            "summary_details": {
                "levels": ["beginner", "intermediate", "advanced"],
                "format": summary_format,
                "learning_objectives": learning_objectives
            }
        }
    
    def _format_sources(self, sources: List[Dict[str, Any]]) -> str:
        """Format sources for agent consumption"""
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"""
            Source {i}:
            Title: {source.get('title', 'Untitled')}
            Type: {source.get('source_type', 'Unknown')}
            Content: {source.get('abstract', source.get('content', 'No content available'))}
            """)
        return "\n".join(formatted)
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "Multi-Level Summary Generator",
            "description": "Creates educational summaries at multiple complexity levels with concept extraction",
            "category": "content",
            "capabilities": [
                "concept_extraction",
                "multi_level_summaries", 
                "adaptive_content",
                "learning_progression",
                "study_aids"
            ],
            "strengths": [
                "pedagogically_sound",
                "supports_differentiation",
                "comprehensive_coverage",
                "learner_focused"
            ],
            "limitations": [
                "processing_time",
                "requires_quality_sources"
            ],
            "input_requirements": {
                "sources": "List of academic sources with content",
                "context": {
                    "topic": "Subject matter to summarize",
                    "user_level": "beginner|intermediate|advanced",
                    "learning_objectives": "Optional specific goals",
                    "summary_format": "structured|narrative|bullet_points"
                }
            },
            "output_format": {
                "summaries": "Multi-level educational summaries",
                "study_aids": "Glossary, key points, study tips",
                "metadata": "Process and context information"
            }
        }

# Register the flow
flow_registry.register_flow("summary", SummaryFlow(), "content")