"""
Minimal test backend without AI models
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/documents/upload', methods=['POST'])
def upload():
    """Mock upload without AI processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file'}), 400
        
        file = request.files['file']
        content = file.read().decode('utf-8')
        
        # Mock analysis
        clauses = content.split('\n\n')
        risk_dist = {'low': 1, 'medium': 2, 'high': 1, 'critical': 0}
        
        return jsonify({
            'success': True,
            'document': {
                'id': str(uuid.uuid4()),
                'filename': file.filename,
                'word_count': len(content.split())
            },
            'analysis': {
                'total_clauses': len(clauses),
                'risk_distribution': risk_dist,
                'processing_time': 0.1
            },
            'clauses': [
                {
                    'clause_text': clause[:100],
                    'clause_type': 'general',
                    'confidence_score': 0.95,
                    'risk_assessment': {
                        'risk_level': 'medium',
                        'risk_score': 0.6
                    }
                } for clause in clauses[:3]
            ],
            'processing_time': 0.1
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
