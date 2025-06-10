from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configure CORS to allow all origins and credentials
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_document():
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

# Remove @cross_origin() decorators since we're using global CORS
@app.route('/files/<filename>')
def serve_file(filename):
    """Serve uploaded PDF files"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404

@app.route('/files', methods=['GET'])
def list_files():
    """List all uploaded PDF files"""
    try:
        files = []
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                if filename.lower().endswith('.pdf'):
                    files.append({
                        'filename': filename,
                        'url': f'/files/{filename}'
                    })
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    if not data or 'text' not in data or 'action' not in data:
        return jsonify({'error': 'Missing text or action'}), 400
    
    text = data['text']
    action = data['action']
    
    # Map frontend actions to CrewAI flows
    flow_mapping = {
        'highlight': 'highlight',  # No AI processing, just highlighting
        'search': 'web_search',    # Web search flow
        'explain': 'llm_knowledge', # LLM knowledge flow
        'analyze': 'hybrid_retrieval' # Hybrid approach
    }
    
    # Get the corresponding flow
    flow = flow_mapping.get(action, 'summary')
    print(f"Mapped action '{action}' to flow '{flow}'")
    
    try:
        # Debug information
        import sys
        import os
        print(f"Current directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        
        # Add both the current directory and the edumuse directory to the path
        sys.path.append(os.path.abspath('.'))
        sys.path.append(os.path.abspath('./edumuse'))
        
        # Try to import EduMUSE
        try:
            print(f"Attempting to import EduMUSE for action: {action}, flow: {flow}")
            from edumuse.src.edumuse.crew import EduMUSE
            print("Successfully imported EduMUSE")
            use_real_implementation = True
        except ImportError as e:
            print(f"Import error: {e}")
            # Try alternative import paths
            try:
                from src.edumuse.crew import EduMUSE
                print("Successfully imported EduMUSE from alternative path")
                use_real_implementation = True
            except ImportError as e:
                print(f"Alternative import failed: {e}")
                print("Falling back to mock data")
                use_real_implementation = False
        
        # Create context from the text
        context = {
            "user_level": "intermediate",
            "learning_objective": "understand content",
            "time_available": "10 minutes"
        }
        
        # Process the request using EduMUSE if available, otherwise use mock data
        result = None
        
        if use_real_implementation:
            try:
                print("Using real EduMUSE implementation")
                edumuse = EduMUSE()
                
                # Convert frontend action to flow name
                requested_flows = [flow]
                
                # Process the request using EduMUSE
                print(f"Calling EduMUSE with flows: {requested_flows}")
                result = edumuse.process_educational_request(
                    topic=text[:100],  # Use selected text as topic
                    requested_flows=requested_flows,
                    context=context
                )
                
                print(f"Successfully processed with EduMUSE: {requested_flows}")
                print(f"Result: {result}")
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error using real implementation: {e}")
                print(f"Error type: {type(e)}")
                print(f"Error args: {e.args}")
                print("Falling back to mock data")
                use_real_implementation = False
        
        # If real implementation failed or is not available, use mock data
        if not use_real_implementation or result is None:
            print("Using mock data as fallback")
            
            # Mock result based on the action type
            mock_results = {
                'summarize': {
                    'flow_type': 'summary',
                    'retrieval_method': 'mock_data',
                    'sources_found': f"Summary of: {text[:100]}...\n\nThis is a mock summary generated for testing purposes. The actual summary would be generated by CrewAI.",
                    'topic': text[:50] + "...",
                    'metadata': {
                        'components': ['mock_component'],
                        'synthesis_approach': 'mock_synthesis',
                        'coverage': 'mock_coverage'
                    }
                },
                'quiz': {
                    'flow_type': 'quiz',
                    'retrieval_method': 'mock_data',
                    'sources_found': f"Quiz based on: {text[:100]}...\n\n1. What is the main topic of this text?\n2. What are the key concepts discussed?\n3. How would you apply these concepts in practice?",
                    'topic': text[:50] + "...",
                    'metadata': {
                        'components': ['mock_component'],
                        'synthesis_approach': 'mock_synthesis',
                        'coverage': 'mock_coverage'
                    }
                },
                'search': {
                    'flow_type': 'web_search_retrieval',
                    'retrieval_method': 'mock_data',
                    'sources_found': f"Search results for: {text[:100]}...\n\n1. Source 1: Example academic paper\n2. Source 2: Example textbook\n3. Source 3: Example website",
                    'topic': text[:50] + "...",
                    'metadata': {
                        'components': ['mock_component'],
                        'synthesis_approach': 'mock_synthesis',
                        'coverage': 'mock_coverage'
                    }
                },
                'explain': {
                    'flow_type': 'llm_knowledge_retrieval',
                    'retrieval_method': 'mock_data',
                    'sources_found': f"Explanation of: {text[:100]}...\n\nThis is a mock explanation generated for testing purposes. The actual explanation would be generated by CrewAI.",
                    'topic': text[:50] + "...",
                    'metadata': {
                        'components': ['mock_component'],
                        'synthesis_approach': 'mock_synthesis',
                        'coverage': 'mock_coverage'
                    }
                },
                'analyze': {
                    'flow_type': 'hybrid_knowledge_retrieval',
                    'retrieval_method': 'mock_data',
                    'sources_found': f"Analysis of: {text[:100]}...\n\nThis is a mock analysis generated for testing purposes. The actual analysis would be generated by CrewAI.",
                    'topic': text[:50] + "...",
                    'metadata': {
                        'components': ['mock_component'],
                        'synthesis_approach': 'mock_synthesis',
                        'coverage': 'mock_coverage'
                    }
                }
            }
        
            # Get the mock result for the requested action
            mock_result = mock_results.get(action, mock_results['summarize'])
            
            # Create a mock response that matches the structure of the CrewAI response
            result = {
                'topic': text[:50] + "...",
                'sources': [
                    {
                        'title': f"Mock Source about {text[:30]}...",
                        'url': "https://example.edu/mock",
                        'credibility_score': 8.5,
                        'source_type': "mock_source"
                    }
                ],
                'educational_content': {
                    flow: mock_result
                },
                'metadata': {
                    'flows_executed': [flow],
                    'source_count': 1,
                    'learning_context': context,
                    'execution_method': 'mock_execution'
                }
            }
        
        print(f"Processed request for action: {action}, flow: {flow}")
        print(f"Returning mock result for testing")
        
        return jsonify({
            'action': action,
            'text': text,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
