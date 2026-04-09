"""
Application runner for LexAI Backend
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app, db
from models import User, Document, Clause, RiskAssessment, AnalysisResult

# Determine configuration
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """Make database models available in shell context"""
    return {
        'db': db,
        'User': User,
        'Document': Document,
        'Clause': Clause,
        'RiskAssessment': RiskAssessment,
        'AnalysisResult': AnalysisResult
    }

if __name__ == '__main__':
    app.run(use_reloader=False)
