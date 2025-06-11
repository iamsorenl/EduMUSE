from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os
import re

class PDFGenerator:
    """Generate PDF files for educational assessments and summaries"""
    
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def generate_summary_pdf(self, summary_data):
        """Generate a PDF for an educational summary"""
        content = summary_data.get('sources_found', '')
        topic = summary_data.get('topic', 'Educational Summary')
        
        safe_topic = re.sub(r'[^\w\s-]', '', topic)[:30]
        safe_topic = re.sub(r'[-\s]+', '_', safe_topic)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{safe_topic}_summary_{timestamp}.pdf"
        filepath = os.path.join(self.upload_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=TA_CENTER)
        elements.append(Paragraph(f"Summary: {topic}", title_style))
        elements.append(Spacer(1, 20))
        
        # Replace newlines with <br/> for ReportLab Paragraphs
        formatted_content = content.replace('\n', '<br/>')
        elements.append(Paragraph(formatted_content, styles['Normal']))
        
        doc.build(elements)
        
        return {
            "summary_pdf": filename,
            "summary_path": filepath
        }

    def generate_assessment_pdfs(self, assessment_data):
        """Generate both student assessment and answer key PDFs"""
        content = assessment_data.get('sources_found', '')
        topic = assessment_data.get('topic', 'Educational Assessment')
        
        safe_topic = re.sub(r'[^\w\s-]', '', topic)[:30]
        safe_topic = re.sub(r'[-\s]+', '_', safe_topic)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        student_filename = f"{safe_topic}_assessment_{timestamp}.pdf"
        answer_key_filename = f"{safe_topic}_answer_key_{timestamp}.pdf"
        
        student_path = os.path.join(self.upload_folder, student_filename)
        answer_key_path = os.path.join(self.upload_folder, answer_key_filename)
        
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
        
        title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=TA_CENTER)
        elements.append(Paragraph(f"Assessment: {topic}", title_style))
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("Instructions:", styles['Heading2']))
        elements.append(Paragraph("• Read each question carefully", styles['Normal']))
        elements.append(Paragraph("• Choose the best answer for multiple choice", styles['Normal']))
        elements.append(Paragraph("• Provide complete answers for short answer questions", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        questions = self._parse_content_for_student(content)
        for question in questions:
            elements.append(Paragraph(question, styles['Normal']))
            elements.append(Spacer(1, 15))
        
        doc.build(elements)
    
    def _generate_answer_key_pdf(self, filepath, content, topic):
        """Generate answer key PDF with full content"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        title_style = ParagraphStyle('Title', parent=styles['Title'], alignment=TA_CENTER)
        elements.append(Paragraph(f"Answer Key: {topic}", title_style))
        elements.append(Spacer(1, 20))
        
        # Full content with answers, formatted for PDF
        elements.append(Paragraph(content.replace('\n', '<br/>'), styles['Normal']))
        
        doc.build(elements)
    
    def _parse_content_for_student(self, content):
        """Parse content to show only questions and hide answers"""
        lines = content.split('\n')
        questions = []
        current_question = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that appear to be answers or explanations
            if any(word in line.lower() for word in ['answer:', 'correct:', 'solution:', 'explanation:', 'rubric:']):
                continue
                
            # Treat lines starting with numbers or all-caps as question headers
            if re.match(r'^\d+\.', line) or line.isupper():
                if current_question:
                    questions.append(current_question)
                current_question = f"<b>{line}</b><br/>"
            # Format multiple choice options
            elif line.startswith(('A)', 'B)', 'C)', 'D)', 'a)', 'b)', 'c)', 'd)')):
                current_question += f"&nbsp;&nbsp;&nbsp;&nbsp;{line}<br/>"
            # Append all other lines to the current question
            else:
                current_question += f"{line}<br/>"
        
        if current_question:
            questions.append(current_question)
        
        # If no questions were parsed, return the whole content as a fallback
        return questions if questions else [content.replace('\n', '<br/>')]