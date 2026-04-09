"""
LexAI - Legal Document Intelligence Platform
Backend API Server
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from logging.handlers import RotatingFileHandler

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory pattern"""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions BEFORE creating app context
    db.init_app(app)
    CORS(app)
    
    # Enable SQLite WAL mode to permanently fix 'database is locked' errors
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    import sqlite3

    @event.listens_for(Engine, "connect")
    def set_sqlite_wal_mode(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.close()

    
    # Setup logging
    setup_logging(app)
    
    # Create upload directory
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Create database tables within app context
    with app.app_context():
        db.create_all()
        
    # Initialize expensive NLP models once at startup
    app.logger.info("Initializing document and AI processors... This may take a moment.")
    from document_processor import DocumentProcessor
    from ai_models import LegalAIProcessor
    app.config['DOC_PROCESSOR'] = DocumentProcessor()
    app.config['AI_PROCESSOR'] = LegalAIProcessor()
    app.logger.info("Processors initialized.")
    
    return app

def setup_logging(app):
    """Setup application logging"""
    
    if not app.debug and not app.testing:
        # File logging
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.info('LexAI Backend startup')

def register_blueprints(app):
    """Register application blueprints"""
    
    from api_routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(413)
    def too_large(e):
        """Handle file too large error"""
        return {'error': 'File too large. Maximum size is 50MB'}, 413

    @app.errorhandler(404)
    def not_found(e):
        """Handle not found error"""
        return {'error': 'Endpoint not found'}, 404

    @app.errorhandler(500)
    def internal_error(e):
        """Handle internal server error"""
        app.logger.error(f"Internal server error: {str(e)}")
        return {'error': 'Internal server error'}, 500

def register_cli_commands(app):
    """Register CLI commands"""
    
    @app.cli.command()
    def init_db():
        """Initialize the database"""
        db.create_all()
        print("Database initialized.")
    
    @app.cli.command()
    def reset_db():
        """Reset the database"""
        db.drop_all()
        db.create_all()
        print("Database reset.")
    
    @app.cli.command()
    def seed_db():
        """Seed the database with sample data"""
        from models import User
        
        # Create sample user
        user = User(
            email='demo@lexai.com',
            full_name='Demo User',
            organization='LexAI Demo'
        )
        user.set_password('demo123')
        
        db.session.add(user)
        db.session.commit()
        
        print("Database seeded with sample data.")
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        from datetime import datetime
        
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }

if __name__ == '__main__':
    # Determine configuration
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create and run app
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
