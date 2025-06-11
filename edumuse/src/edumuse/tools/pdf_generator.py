from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os
import re

class PDFGenerator:
    """Generate PDF files for educational assessments"""
    
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)
    
    def generate_assessment_pdfs(self, assessment_data):
        """Generate both student assessment and answer key PDFs"""
        
        # Extract content
        content = assessment_data.get('sources_found', '')
        topic = assessment_data.get('topic', 'Educational Assessment')
        
        # Clean topic for filename
        safe_topic = re.sub(r'[^\w\s-]', '', topic)[:30]
        safe_topic = re.sub(r'[-\s]+', '_', safe_topic)
        
        # Generate filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        student_filename = f"{safe_topic}_assessment_{timestamp}.pdf"
        answer_key_filename = f"{safe_topic}_answer_key_{timestamp}.pdf"
        
        student_path = os.path.join(self.upload_folder, student_filename)
        answer_key_path = os.path.join(self.upload_folder, answer_key_filename)
        
        # Generate PDFs
        self._generate_student_pdf(student_path, content, topic)
        self._generate_answer_key_pdf(answer_key_path, content, topic)
        
        return {
            "student_assessment": student_filename,
            "answer_key": answer_key_filename,
            "student_path": student_path,
            "answer_key_path": answer_key_path
        }
    
    def _generate_student_pdf(self, filepath, content, topic):
        """Generate student assessment PDF"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=TA_CENTER)
        elements.append(Paragraph(f"Assessment: {topic}", title_style))
        elements.append(Spacer(1, 20))
        
        # Instructions
        elements.append(Paragraph("Instructions:", styles['Heading2']))
        elements.append(Paragraph("• Read each question carefully", styles['Normal']))
        elements.append(Paragraph("• Choose the best answer for multiple choice", styles['Normal']))
        elements.append(Paragraph("• Provide complete answers for short answer questions", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Questions (remove answers)
        questions = self._parse_content_for_student(content)
        for question in questions:
            elements.append(Paragraph(question, styles['Normal']))
            elements.append(Spacer(1, 15))
        
        doc.build(elements)
    
    def _generate_answer_key_pdf(self, filepath, content, topic):
        """Generate answer key PDF"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=TA_CENTER)
        elements.append(Paragraph(f"Answer Key: {topic}", title_style))
        elements.append(Spacer(1, 20))
        
        # Full content with answers
        elements.append(Paragraph(content.replace('\n', '<br/>'), styles['Normal']))
        
        doc.build(elements)
    
    def _parse_content_for_student(self, content):
        """Parse content to show only questions (no answers)"""
        lines = content.split('\n')
        questions = []
        current_question = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip answer lines
            if any(word in line.lower() for word in ['answer:', 'correct:', 'solution:']):
                continue
                
            # Question numbers or section headers
            if re.match(r'^\d+\.', line) or line.isupper():
                if current_question:
                    questions.append(current_question)
                current_question = f"<b>{line}</b><br/>"
            # Multiple choice options
            elif line.startswith(('A)', 'B)', 'C)', 'D)', 'a)', 'b)', 'c)', 'd)')):
                current_question += f"&nbsp;&nbsp;&nbsp;&nbsp;{line}<br/>"
            # Regular content
            else:
                current_question += f"{line}<br/>"
        
        if current_question:
            questions.append(current_question)
        
        return questions if questions else [content.replace('\n', '<br/>')]
