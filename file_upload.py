import sys
import os
import PyPDF2  # Import the new library
import traceback
from datetime import datetime

# Add the 'src' directory to Python's path
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

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# --- New Helper Function to Extract Text from PDF ---
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

# --- Existing Endpoints (largely unchanged) ---
@app.route('/upload', methods=['POST'])
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
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# --- Updated Process Endpoint ---
@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.json
        if not data or 'action' not in data:
            return jsonify({'error': 'Missing action'}), 400
        
        action = data.get('action')
        filename = data.get('filename')
        input_text = data.get('text')
        text_for_flow = ""

        # Determine the source of the text for the flow
        if filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return jsonify({'error': f"File not found: {filename}"}), 404
            text_for_flow = extract_text_from_pdf(filepath)
            if text_for_flow is None:
                return jsonify({'error': f"Could not extract text from {filename}"}), 500
        elif input_text:
            text_for_flow = input_text
        else:
            return jsonify({'error': 'No input provided (missing "filename" or "text")'}), 400

        flow_mapping = {
            'summarize': 'summary',
            'assess': 'assessment'
            # other flows can be added here
        }
        flow = flow_mapping.get(action)
        if not flow:
            return jsonify({'error': f"Invalid action: {action}"}), 400
        
        context = {"user_level": "intermediate"}
        
        # Add the full document content to the context to be processed
        context['document_content'] = text_for_flow
        
        edumuse = EduMUSE()
        # Use the filename as the topic for better tracking
        result = edumuse.process_educational_request(
            topic=(filename or "Uploaded Text"),
            requested_flows=[flow],
            context=context
        )
        # PDF generation logic
        pdf_files = None
        if action in ['assess', 'summarize']:
            try:
                pdf_generator = PDFGenerator(upload_folder=app.config['UPLOAD_FOLDER'])
                flow_data = result['educational_content'].get(flow, {})
                
                # Add original filename to the data for better PDF titles
                flow_data['topic'] = f"{action.capitalize()} of {filename or 'text'}"

                if action == 'assess':
                    pdf_files = pdf_generator.generate_assessment_pdfs(flow_data)
                elif action == 'summarize':
                    pdf_files = pdf_generator.generate_summary_pdf(flow_data)

                if pdf_files:
                    result['pdf_files'] = { **pdf_files, 'generated_at': datetime.now().isoformat() }
                    result['pdf_generated'] = True
                    
            except Exception as e:
                print(f"❌ PDF generation failed: {e}")
                traceback.print_exc()
                result['pdf_error'] = str(e)
        
        return jsonify(result), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')