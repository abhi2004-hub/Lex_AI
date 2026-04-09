"""
Configuration settings for LexAI Backend
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///legal_ai.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # AI Model Settings
    MODEL_CACHE_DIR = os.environ.get('MODEL_CACHE_DIR') or 'models_cache'
    MAX_MODEL_MEMORY = os.environ.get('MAX_MODEL_MEMORY', '4GB')
    
    # Processing Settings
    MAX_CLAUSES_PER_DOCUMENT = 1000
    MAX_TEXT_LENGTH = 100000  # Maximum characters to process
    
    # API Settings
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Security Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/legal_ai.log'
    
    # Performance Settings
    REQUEST_TIMEOUT = 300  # 5 minutes
    MAX_CONCURRENT_PROCESSING = 5
    
    # External Services
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Use SQLite for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///legal_ai_dev.db'
    
    # Enable WAL mode to prevent 'database is locked' errors with concurrent connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30,
        },
        'pool_pre_ping': True,
    }
    
    # More verbose logging for development
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """Testing configuration"""
    
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED = False
    
    # Use smaller limits for testing
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    MAX_CLAUSES_PER_DOCUMENT = 50

class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Production database (PostgreSQL recommended)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/legal_ai'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # Logging
    LOG_LEVEL = 'WARNING'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
