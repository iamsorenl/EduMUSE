import sys
import os

# Add the 'src' directory to Python's path to allow for clean imports
# This is the standard way to handle a 'src' layout
src_path = os.path.join(os.path.dirname(__file__), 'edumuse', 'src')
sys.path.insert(0, src_path)

# Now that the path is set, we can import everything cleanly
from edumuse.crew import EduMUSE
from edumuse.flows.web_search_flow import WebSearchFlow
from edumuse.flows.llm_knowledge_flow import LLMKnowledgeFlow
from edumuse.flows.hybrid_retrieval_flow import HybridRetrievalFlow
from edumuse.flows.assessment_flow import AssessmentFlow
from edumuse.flows.summary_flow import SummaryFlow
from edumuse.tools.pdf_generator import PDFGenerator

# --- Standard Flask Imports ---
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from datetime import datetime
import traceback

app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_document():
    # ... (this function remains the same)
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'message': 'PDF uploaded successfully',
            'filename': filename,
            'filepath': filepath,
            'file_type': 'pdf'
        }), 200
    return jsonify({'error': 'Invalid file type. Only PDF files are supported.'}), 400


@app.route('/files/<filename>')
@cross_origin()
def serve_file(filename):
    # ... (this function remains the same)
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404


@app.route('/files', methods=['GET'])
@cross_origin()
def list_files():
    # ... (this function remains the same)
    try:
        files = []
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.lower().endswith('.pdf'):
                    files.append({'filename': filename, 'url': f'/files/{filename}'})
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    # ... (this function remains the same)
    return jsonify({'status': 'healthy'}), 200


@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.json
        if not data or 'action' not in data:
            return jsonify({'error': 'Missing action'}), 400
        
        text = data.get('text', '')
        action = data['action']
        
        if not text or len(text.strip()) < 10:
            mock_texts = {
                'assess': "Machine Learning Fundamentals...",
                'summarize': "Climate Change and Environmental Impact...",
                'default': "Artificial Intelligence and Society..."
            }
            text = mock_texts.get(action, mock_texts['default'])
        
        flow_mapping = {
            'highlight': 'highlight',
            'search': 'web_search',
            'explain': 'llm_knowledge',
            'analyze': 'hybrid_retrieval',
            'summarize': 'summary',
            'assess': 'assessment'
        }
        
        flow = flow_mapping.get(action, 'summary')
        
        context = {
            "user_level": "intermediate",
            "learning_objective": "understand content",
            "time_available": "10 minutes"
        }
        
        # With imports handled at the top, this section becomes much cleaner
        edumuse = EduMUSE()
        result = edumuse.process_educational_request(
            topic=text[:100],
            requested_flows=[flow],
            context=context
        )

        # PDF generation logic remains the same
        pdf_files = None
        if action in ['assess', 'summarize']:
            try:
                pdf_generator = PDFGenerator(upload_folder=app.config['UPLOAD_FOLDER'])
                flow_data = result['educational_content'].get(flow, {})
                
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