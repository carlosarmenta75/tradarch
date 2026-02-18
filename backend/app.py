from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
import os
import tempfile

app = Flask(__name__)
CORS(app)

md = MarkItDown()

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        result = md.convert(tmp.name)
        os.unlink(tmp.name)
    
    return jsonify({'markdown': result.text_content})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
