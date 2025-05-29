from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    # Image formats
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp',
    # Video formats
    'mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv', 'webm'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    if extension in {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}:
        return 'image'
    elif extension in {'mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv', 'webm'}:
        return 'video'
    return 'unknown'

@app.route('/upload-media', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        file_type = get_file_type(filename)
        
        return jsonify({
            'message': f'{file_type.capitalize()} uploaded successfully',
            'filename': filename,
            'filepath': filepath,
            'file_type': file_type
        }), 200
    
    return jsonify({'error': 'Invalid file type. Supported: images and videos (including MP4)'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)