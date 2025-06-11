from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime
import re

class PDFGenerator:
    """Utility class for generating assessment PDFs"""
    
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
    
    def _create_filename(self, base_name, suffix=''):
        """Create a unique filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}{suffix}.pdf"
    
    def _parse_assessment(self, assessment_data):
        """Parse assessment data into questions and answers"""
        raw_output = assessment_data.get('content', {}).get('raw_output', '')
        
        # Simple parsing logic - this would need to be adapted based on your actual output format
        questions = []
        answers = []
        
        # Split by question pattern (e.g., "1.", "2.", etc.)
        question_blocks = re.split(r'\n\s*\d+\.\s+', raw_output)
        
        # Skip the first split if it's empty (happens if the text starts with a question number)
        if question_blocks and not question_blocks[0].strip():
            question_blocks = question_blocks[1:]
        
        for i, block in enumerate(question_blocks):
            # Split each block into question and answer parts
            parts = block.split("ANSWER:", 1)
            
            if len(parts) == 2:
                question_text = parts[0].strip()
                answer_text = parts[1].strip()
                
                # For multiple choice, keep options with the question
                if "A)" in question_text and "B)" in question_text:
                    # Keep the question and options together
                    questions.append(f"{i+1}. {question_text}")
                    
                    # Extract explanation if present
                    if "EXPLANATION:" in answer_text:
                        answer_parts = answer_text.split("EXPLANATION:", 1)
                        answer = answer_parts[0].strip()
                        explanation = answer_parts[1].strip() if len(answer_parts) > 1 else ""
                        answers.append(f"{i+1}. Answer: {answer}\nExplanation: {explanation}")
                    else:
                        answers.append(f"{i+1}. Answer: {answer_text}")
                else:
                    # For short answer/essay questions
                    questions.append(f"{i+1}. {question_text}")
                    answers.append(f"{i+1}. {answer_text}")
            else:
                # If no answer found, just add the question
                questions.append(f"{i+1}. {block.strip()}")
                answers.append(f"{i+1}. [No answer provided]")
        
        return questions, answers
    
    def generate_assessment_pdfs(self, assessment_data):
        """Generate student assessment and answer key PDFs"""
        topic = assessment_data.get('topic', 'Assessment')
        assessment_type = assessment_data.get('assessment_type', 'formative')
        difficulty = assessment_data.get('content', {}).get('difficulty_level', 'intermediate')
        
        # Parse questions and answers
        questions, answers = self._parse_assessment(assessment_data)
        
        # Create filenames
        student_filename = self._create_filename(f"{topic}_assessment")
        answer_key_filename = self._create_filename(f"{topic}_answer_key")
        
        # Full paths
        student_path = os.path.join(self.upload_folder, student_filename)
        answer_key_path = os.path.join(self.upload_folder, answer_key_filename)
        
        # Generate student version (questions only)
        self._generate_student_pdf(student_path, topic, questions, assessment_type, difficulty)
        
        # Generate answer key version
        self._generate_answer_key_pdf(answer_key_path, topic, questions, answers, assessment_type, difficulty)
        
        return {
            "student_assessment": student_filename,
            "answer_key": answer_key_filename,
            "student_path": student_path,
            "answer_key_path": answer_key_path
        }
    
    def _generate_student_pdf(self, filename, topic, questions, assessment_type, difficulty):
        """Generate the student version of the assessment (questions only)"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Heading2'],
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            alignment=TA_LEFT,
            fontSize=10,
            spaceAfter=6
        )
        
        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Normal'],
            spaceAfter=10,
            spaceBefore=6
        )
        
        # Build the document
        elements = []
        
        # Title
        elements.append(Paragraph(f"Assessment: {topic}", title_style))
        elements.append(Spacer(1, 12))
        
        # Assessment info
        elements.append(Paragraph(f"Type: {assessment_type.capitalize()}", info_style))
        elements.append(Paragraph(f"Difficulty Level: {difficulty.capitalize()}", info_style))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style))
        elements.append(Spacer(1, 12))
        
        # Student info section
        elements.append(Paragraph("Student Information", subtitle_style))
        elements.append(Paragraph("Name: ________________________________", info_style))
        elements.append(Paragraph("Date: ________________________________", info_style))
        elements.append(Spacer(1, 24))
        
        # Instructions
        elements.append(Paragraph("Instructions:", subtitle_style))
        elements.append(Paragraph("Answer all questions to the best of your ability. Read each question carefully before responding.", styles['Normal']))
        elements.append(Spacer(1, 24))
        
        # Questions
        elements.append(Paragraph("Questions:", subtitle_style))
        for question in questions:
            elements.append(Paragraph(question, question_style))
            elements.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(elements)
    
    def _generate_answer_key_pdf(self, filename, topic, questions, answers, assessment_type, difficulty):
        """Generate the answer key version of the assessment"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles (same as student version)
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Heading2'],
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            alignment=TA_LEFT,
            fontSize=10,
            spaceAfter=6
        )
        
        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Normal'],
            spaceAfter=6,
            spaceBefore=6
        )
        
        answer_style = ParagraphStyle(
            'AnswerStyle',
            parent=styles['Normal'],
            leftIndent=20,
            textColor=colors.blue,
            spaceAfter=12
        )
        
        # Build the document
        elements = []
        
        # Title
        elements.append(Paragraph(f"Answer Key: {topic}", title_style))
        elements.append(Spacer(1, 12))
        
        # Assessment info
        elements.append(Paragraph(f"Type: {assessment_type.capitalize()}", info_style))
        elements.append(Paragraph(f"Difficulty Level: {difficulty.capitalize()}", info_style))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style))
        elements.append(Spacer(1, 24))
        
        # Questions and Answers
        elements.append(Paragraph("Questions and Answers:", subtitle_style))
        for i in range(len(questions)):
            elements.append(Paragraph(questions[i], question_style))
            elements.append(Paragraph(answers[i], answer_style))
            elements.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(elements)
