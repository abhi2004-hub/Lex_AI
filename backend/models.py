"""
Database Models for LexAI Platform
"""

from datetime import datetime
import uuid

# Import db from app to avoid duplicate instances
from app import db

class Document(db.Model):
    """Document model for storing uploaded legal documents"""
    __tablename__ = 'documents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(10), default='en')
    
    # Processing status
    status = db.Column(db.String(20), default='uploaded')  # uploaded, processing, completed, failed
    processing_started_at = db.Column(db.DateTime)
    processing_completed_at = db.Column(db.DateTime)
    
    # Document metadata
    page_count = db.Column(db.Integer)
    word_count = db.Column(db.Integer)
    clause_count = db.Column(db.Integer, default=0)
    
    # Relationships
    analysis_results = db.relationship('AnalysisResult', backref='document', lazy=True, cascade='all, delete-orphan')
    clauses = db.relationship('Clause', backref='document', lazy=True, cascade='all, delete-orphan')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert document to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'language': self.language,
            'status': self.status,
            'page_count': self.page_count,
            'word_count': self.word_count,
            'clause_count': self.clause_count,
            'processing_started_at': self.processing_started_at.isoformat() if self.processing_started_at else None,
            'processing_completed_at': self.processing_completed_at.isoformat() if self.processing_completed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Clause(db.Model):
    """Extracted legal clauses from documents"""
    __tablename__ = 'clauses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey('documents.id'), nullable=False)
    
    # Clause content
    clause_type = db.Column(db.String(100), nullable=False)  # confidentiality, termination, liability, etc.
    clause_text = db.Column(db.Text, nullable=False)
    section_reference = db.Column(db.String(100))  # Section 3.2, Article 7, etc.
    
    # Position in document
    start_page = db.Column(db.Integer)
    end_page = db.Column(db.Integer)
    start_char = db.Column(db.Integer)
    end_char = db.Column(db.Integer)
    
    # AI analysis results
    confidence_score = db.Column(db.Float, default=0.0)
    embedding = db.Column(db.Text)  # Store vector representation as JSON string
    
    # Relationships
    risk_assessment = db.relationship('RiskAssessment', backref='clause', uselist=False, cascade='all, delete-orphan')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert clause to dictionary"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'clause_type': self.clause_type,
            'clause_text': self.clause_text,
            'section_reference': self.section_reference,
            'start_page': self.start_page,
            'end_page': self.end_page,
            'confidence_score': self.confidence_score,
            'risk_assessment': self.risk_assessment.to_dict() if self.risk_assessment else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RiskAssessment(db.Model):
    """Risk assessment for individual clauses"""
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    clause_id = db.Column(db.String(36), db.ForeignKey('clauses.id'), nullable=False)
    
    # Risk classification
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    risk_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    confidence = db.Column(db.Float, default=0.0)
    
    # Risk factors
    risk_factors = db.Column(db.Text)  # JSON string of risk factors
    severity_indicators = db.Column(db.Text)  # JSON string of severity indicators
    
    # Recommendations
    recommendations = db.Column(db.Text)
    alternative_suggestions = db.Column(db.Text)
    
    # Model explanation
    shap_values = db.Column(db.Text)  # JSON string of SHAP values
    lime_explanation = db.Column(db.Text)  # JSON string of LIME explanation
    plain_language = db.Column(db.Text)  # JSON string of plain language explanation
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert risk assessment to dictionary"""
        return {
            'id': self.id,
            'clause_id': self.clause_id,
            'risk_level': self.risk_level,
            'risk_score': self.risk_score,
            'confidence': self.confidence,
            'risk_factors': self.risk_factors,
            'severity_indicators': self.severity_indicators,
            'recommendations': self.recommendations,
            'alternative_suggestions': self.alternative_suggestions,
            'shap_values': self.shap_values,
            'lime_explanation': self.lime_explanation,
            'plain_language': self.plain_language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AnalysisResult(db.Model):
    """Overall analysis results for documents"""
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey('documents.id'), nullable=False)
    
    # Analysis metadata
    analysis_type = db.Column(db.String(50), nullable=False)  # full, quick, comprehensive
    model_version = db.Column(db.String(50), nullable=False)
    processing_time = db.Column(db.Float)  # Processing time in seconds
    
    # Overall risk summary
    overall_risk_score = db.Column(db.Float)
    risk_distribution = db.Column(db.Text)  # JSON string of risk distribution
    verdict = db.Column(db.Text)  # Textual verdict based on document analysis
    
    # Key findings
    total_clauses = db.Column(db.Integer, default=0)
    high_risk_clauses = db.Column(db.Integer, default=0)
    medium_risk_clauses = db.Column(db.Integer, default=0)
    low_risk_clauses = db.Column(db.Integer, default=0)
    
    # Summary statistics
    confidence_distribution = db.Column(db.Text)  # JSON string
    clause_type_distribution = db.Column(db.Text)  # JSON string
    
    # Processing details
    processing_steps = db.Column(db.Text)  # JSON string of processing steps
    errors = db.Column(db.Text)  # JSON string of any errors encountered
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert analysis result to dictionary"""
        return {
            'id': self.id,
            'document_id': self.document_id,
            'analysis_type': self.analysis_type,
            'model_version': self.model_version,
            'processing_time': self.processing_time,
            'overall_risk_score': self.overall_risk_score,
            'risk_distribution': self.risk_distribution,
            'verdict': self.verdict,
            'total_clauses': self.total_clauses,
            'high_risk_clauses': self.high_risk_clauses,
            'medium_risk_clauses': self.medium_risk_clauses,
            'low_risk_clauses': self.low_risk_clauses,
            'confidence_distribution': self.confidence_distribution,
            'clause_type_distribution': self.clause_type_distribution,
            'processing_steps': self.processing_steps,
            'errors': self.errors,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255))
    
    # User preferences
    preferred_language = db.Column(db.String(10), default='en')
    analysis_preferences = db.Column(db.Text)  # JSON string of preferences
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Set password hash"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'organization': self.organization,
            'preferred_language': self.preferred_language,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
