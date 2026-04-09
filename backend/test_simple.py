"""
Simple test to isolate the issue
"""

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_upload():
    """Simple test endpoint"""
    try:
        print("Received POST request")
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        # Read file content
        content = file.read().decode('utf-8')
        print(f"Content length: {len(content)}")
        
        return jsonify({
            'success': True,
            'filename': file.filename,
            'content_length': len(content),
            'message': 'File processed successfully'
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
