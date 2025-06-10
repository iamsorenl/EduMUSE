
from crewai import Agent, Crew, Task, Process
from typing import List, Dict, Any, Optional
from .flow_registry import EducationFlow, flow_registry

class AssessmentFlow(EducationFlow):
    """Educational assessment and quiz generation flow"""
    
    def __init__(self):
        # Question Designer Agent
        self.question_designer = Agent(
            role="Educational Assessment Designer",
            goal="Create pedagogically sound questions that effectively test understanding",
            backstory="""You are an expert in educational assessment with decades of experience 
            designing tests, quizzes, and formative assessments. You understand Bloom's Taxonomy 
            and can create questions at different cognitive levels - from basic recall to 
            critical analysis and synthesis. You know how to craft clear, unambiguous questions 
            that accurately measure student understanding while avoiding common pitfalls like 
            unclear wording or cultural bias. You're skilled at creating various question types 
            that engage different learning styles.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Answer Validator Agent
        self.answer_validator = Agent(
            role="Assessment Quality Assurance Specialist",
            goal="Ensure assessment accuracy, fairness, and educational value",
            backstory="""You are a meticulous educational assessment expert who specializes 
            in validating test questions and answers. You have extensive experience in 
            psychometrics and understand how to evaluate questions for clarity, difficulty, 
            discrimination, and alignment with learning objectives. You ensure that correct 
            answers are accurate and that distractors (wrong answers) are plausible but 
            clearly incorrect. You also excel at writing clear explanations that help 
            students learn from their mistakes.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Difficulty Calibrator Agent
        self.difficulty_calibrator = Agent(
            role="Assessment Difficulty Specialist",
            goal="Calibrate question difficulty to match learner level and progression",
            backstory="""You are an expert in adaptive learning and assessment difficulty 
            calibration. You understand how cognitive load, prior knowledge, and question 
            complexity interact to create appropriate challenges for learners. You can 
            accurately gauge question difficulty and create balanced assessments that 
            neither frustrate nor bore students. You're skilled at creating question 
            progressions that guide learners from basic understanding to mastery.""",
            verbose=True,
            allow_delegation=False
        )
    
    @property
    def flow_type(self) -> str:
        return "assessment"
    
    def process(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process academic sources to generate educational assessments"""
        
        topic = context.get('topic', 'general academic topic')
        user_level = context.get('user_level', 'intermediate')
        assessment_type = context.get('assessment_type', 'mixed')
        num_questions = context.get('num_questions', 10)
        question_types = context.get('question_types', ['multiple_choice', 'short_answer', 'essay'])
        learning_objectives = context.get('learning_objectives', [])
        
        # Task 1: Design diverse questions
        question_design_task = Task(
            description=f"""
            Create {num_questions} assessment questions about '{topic}' based on the provided sources.
            
            Requirements:
            1. **Question Types to Include**:
               - Multiple Choice: {min(num_questions//2, 5)} questions with 4 options each
               - Short Answer: {min(num_questions//3, 3)} questions requiring 2-3 sentence responses
               - Essay/Long Answer: {min(num_questions//5, 2)} questions for deeper analysis
            
            2. **Cognitive Levels** (use Bloom's Taxonomy):
               - Remember/Understand: 30% of questions
               - Apply/Analyze: 50% of questions  
               - Evaluate/Create: 20% of questions
            
            3. **Question Design Principles**:
               - Clear, unambiguous wording
               - Test key concepts from the sources
               - Progressive difficulty
               - No trick questions
               - Culturally neutral language
            
            Sources to use:
            {self._format_sources(sources)}
            
            Format each question with:
            - Question text
            - Question type
            - Cognitive level
            - Concept being tested
            """,
            agent=self.question_designer,
            expected_output="""A complete set of assessment questions with:
            - Clear question text for each
            - Designated question type and cognitive level
            - Identified concepts being tested
            - Appropriate variety and progression"""
        )
        
        # Task 2: Create and validate answers
        answer_validation_task = Task(
            description=f"""
            Create correct answers and explanations for all questions, ensuring accuracy and educational value.
            
            For each question type:
            
            1. **Multiple Choice Questions**:
               - Mark the correct answer clearly
               - Ensure distractors are plausible but incorrect
               - Explain why each option is correct/incorrect
               - Include common misconceptions in distractors
            
            2. **Short Answer Questions**:
               - Provide model answer (2-3 sentences)
               - List key points that should be included
               - Create a simple rubric (0-3 points)
               - Note acceptable variations
            
            3. **Essay Questions**:
               - Create detailed rubric with criteria
               - Provide exemplar response outline
               - List required elements for full credit
               - Include point distribution
            
            Also add:
            - Learning explanations for each answer
            - References to source material
            - Tips for avoiding common errors
            """,
            agent=self.answer_validator,
            expected_output="""Complete answer key with:
            - Correct answers clearly marked
            - Detailed explanations for all answers
            - Rubrics for open-ended questions
            - Educational feedback for wrong answers"""
        )
        
        # Task 3: Calibrate difficulty and create final assessment
        calibration_task = Task(
            description=f"""
            Calibrate the assessment for {user_level} level learners and create the final formatted assessment.
            
            Tasks:
            1. **Difficulty Adjustment**:
               - Review all questions for appropriate difficulty
               - Adjust wording for target level
               - Ensure proper question progression
               - Balance challenge and accessibility
            
            2. **Assessment Organization**:
               - Order questions from easier to harder
               - Group by question type if appropriate
               - Create clear instructions for each section
               - Add time recommendations
            
            3. **Enhancement for Learning**:
               - Add pre-assessment preparation tips
               - Include self-check before submission
               - Create post-assessment reflection prompts
               - Suggest follow-up learning activities
            
            4. **Metadata and Scoring**:
               - Total points possible
               - Recommended time limit
               - Passing score suggestion
               - Alignment with learning objectives: {learning_objectives}
            
            Create both:
            - Student version (questions only)
            - Instructor version (with answers and rubrics)
            """,
            agent=self.difficulty_calibrator,
            expected_output="""Final calibrated assessment package with:
            - Student assessment version
            - Complete instructor answer key
            - Scoring guidelines and rubrics
            - Learning enhancement materials"""
        )
        
        # Create and run the crew
        assessment_crew = Crew(
            agents=[self.question_designer, self.answer_validator, self.difficulty_calibrator],
            tasks=[question_design_task, answer_validation_task, calibration_task],
            process=Process.sequential,
            verbose=True
        )
        
        crew_output = assessment_crew.kickoff()
        
        # Structure the output
        return {
            "flow_type": "assessment",
            "assessment_type": assessment_type,
            "content": {
                "raw_output": str(crew_output),
                "num_questions": num_questions,
                "question_types": question_types,
                "difficulty_level": user_level
            },
            "topic": topic,
            "sources_used": len(sources),
            "metadata": {
                "generation_method": "pedagogical_assessment_design",
                "agents_used": ["question_designer", "answer_validator", "difficulty_calibrator"],
                "learning_objectives": learning_objectives,
                "cognitive_levels": ["remember", "understand", "apply", "analyze", "evaluate", "create"],
                "assessment_features": [
                    "answer_key_included",
                    "rubrics_provided",
                    "explanations_included",
                    "difficulty_calibrated"
                ]
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
            Key Concepts: {source.get('key_concepts', 'Not specified')}
            """)
        return "\n".join(formatted)
    
    def get_flow_info(self) -> Dict[str, Any]:
        return {
            "name": "Educational Assessment Generator",
            "description": "Creates comprehensive assessments with multiple question types and difficulty levels",
            "category": "assessment",
            "capabilities": [
                "multiple_question_types",
                "cognitive_level_variation",
                "answer_key_generation",
                "rubric_creation",
                "difficulty_calibration"
            ],
            "strengths": [
                "pedagogically_sound_design",
                "comprehensive_explanations",
                "adaptive_difficulty",
                "learning_focused",
                "fair_assessment"
            ],
            "limitations": [
                "requires_quality_sources",
                "processing_intensive"
            ],
            "input_requirements": {
                "sources": "Academic content to assess",
                "context": {
                    "topic": "Subject matter",
                    "user_level": "Target difficulty level",
                    "num_questions": "Number of questions (default: 10)",
                    "question_types": "Types to include",
                    "assessment_type": "formative|summative|diagnostic",
                    "learning_objectives": "Specific objectives to assess"
                }
            },
            "output_format": {
                "student_version": "Questions without answers",
                "instructor_version": "Complete with answers and rubrics",
                "metadata": "Scoring guides and alignment info"
            }
        }

# Register the flow
flow_registry.register_flow("assessment", AssessmentFlow(), "assessment")