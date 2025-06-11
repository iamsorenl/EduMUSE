import sys
import os
import PyPDF2
import traceback
from datetime import datetime

# Add the 'src' directory to Python's path to allow for clean imports
src_path = os.path.join(os.path.dirname(__file__), 'edumuse', 'src')
sys.path.insert(0, src_path)

# Import your EduMUSE components
from edumuse.crew import EduMUSE
from edumuse.tools.pdf_generator import PDFGenerator
from edumuse.flows.web_search_flow import WebSearchFlow
from edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
from edumuse.flows.assessment_flow import AssessmentFlow
from edumuse.flows.summary_flow import SummaryFlow

# --- Standard Flask Imports ---
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Define UPLOAD_FOLDER as an absolute path to prevent ambiguity
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def extract_text_from_pdf(filepath):
    """Opens a PDF file and returns its text content."""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return None
    return text

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'message': 'PDF uploaded successfully',
            'filename': filename,
        }), 200
    return jsonify({'error': 'Invalid file type.'}), 400

@app.route('/files/<filename>')
@cross_origin()
def serve_file(filename):
    """Serves a specific file from the uploads folder."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/files', methods=['GET'])
@cross_origin()
def list_files():
    """Lists all PDF files in the uploads folder."""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.lower().endswith('.pdf'):
                files.append({'filename': filename})
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    return jsonify({'status': 'healthy'}), 200


@app.route('/process', methods=['POST'])
@cross_origin()
def process_text():
    try:
        data = request.json
        action = data.get('action')
        filename = data.get('filename')
        input_text = data.get('text')
        
        text_for_flow = ""
        topic_for_crew = ""

        # This logic now correctly sets the topic and content for both workflows
        if filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({'error': f"File not found: {filename}"}), 404
            
            text_for_flow = extract_text_from_pdf(filepath)
            topic_for_crew = filename  # For whole file, topic is the filename
            
            if text_for_flow is None:
                return jsonify({'error': f"Could not extract text from {filename}"}), 500
        elif input_text:
            text_for_flow = input_text
            topic_for_crew = input_text  # For highlighted text, the topic IS the text
        else:
            return jsonify({'error': 'No input provided (missing "filename" or "text")'}), 400

        flow_mapping = {
            'highlight': 'highlight',
            'search': 'web_search',
            'explain': 'llm_knowledge',
            'analyze': 'hybrid_retrieval',
            'summarize': 'summary',
            'assess': 'assessment'
        }
        flow = flow_mapping.get(action)
        if not flow:
            return jsonify({'error': f"Invalid action: {action}"}), 400
        
        context = {
            "user_level": "intermediate",
            'document_content': text_for_flow
        }
        
        edumuse = EduMUSE()
        result = edumuse.process_educational_request(
            topic=topic_for_crew, # Use the correctly determined topic
            requested_flows=[flow],
            context=context
        )

        # PDF generation logic for summarize/assess actions
        if action in ['assess', 'summarize']:
            try:
                pdf_generator = PDFGenerator(upload_folder=app.config['UPLOAD_FOLDER'])
                flow_data = result['educational_content'].get(flow, {})
                
                # Use the original filename or a generic title for the PDF
                pdf_topic_title = filename if filename else f"{action.capitalize()} Result"
                flow_data['topic'] = f"{action.capitalize()} of {pdf_topic_title}"

                if action == 'assess':
                    pdf_files = pdf_generator.generate_assessment_pdfs(flow_data)
                elif action == 'summarize':
                    pdf_files = pdf_generator.generate_summary_pdf(flow_data)

                if pdf_files:
                    result['pdf_files'] = {**pdf_files, 'generated_at': datetime.now().isoformat()}
                    result['pdf_generated'] = True
            except Exception as e:
                result['pdf_error'] = str(e)
        
        return jsonify(result), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')