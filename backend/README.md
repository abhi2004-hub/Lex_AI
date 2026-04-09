# LexAI Backend - Legal Document Intelligence Platform

## Overview

This is the backend API server for the LexAI Legal Document Intelligence Platform. It provides AI-powered analysis of legal documents using transformer models like LegalBERT and CaseLaw-BERT.

## Features

- **Document Processing**: Support for PDF, DOCX, and TXT files
- **AI Analysis**: Clause extraction, risk assessment, and sentiment analysis
- **Explainable AI**: SHAP and LIME explanations for model decisions
- **Semantic Search**: Find similar clauses using embeddings
- **RESTful API**: Comprehensive API for frontend integration
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support

## Architecture

```
backend/
├── app.py                 # Application factory and main entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── ai_models.py           # AI model integration
├── document_processor.py  # Document parsing and preprocessing
├── api_routes.py          # REST API endpoints
├── requirements.txt       # Python dependencies
├── run.py                 # Application runner
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create directories**
   ```bash
   mkdir -p uploads logs models_cache
   ```

4. **Initialize database**
   ```bash
   flask init-db
   ```

5. **Run the server**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///legal_ai.db

# File Upload
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=52428800  # 50MB

# AI Models
MODEL_CACHE_DIR=models_cache
MAX_MODEL_MEMORY=4GB
```

### Configuration Files

- `config.py`: Contains different configuration classes for development, testing, and production
- `.env`: Environment-specific variables (create this file)

## API Endpoints

### Document Management

- `POST /api/documents/upload` - Upload and analyze a document
- `GET /api/documents` - List all documents
- `GET /api/documents/{id}` - Get document details
- `GET /api/documents/{id}/clauses` - Get document clauses

### Analysis

- `POST /api/analyze/text` - Analyze raw text
- `GET /api/clauses/{id}/risk` - Get clause risk assessment
- `POST /api/search/similar` - Find similar clauses

### System

- `GET /health` - Health check
- `GET /api/models/info` - Model information

## AI Models

### Supported Models

1. **LegalBERT**: Legal text understanding and clause classification
2. **Risk Assessment Model**: Risk level classification
3. **CaseLaw Model**: Legal precedent analysis

### Model Capabilities

- Clause extraction and classification
- Risk assessment (low, medium, high, critical)
- Sentiment analysis
- Text embeddings for semantic search
- Explainable AI with SHAP and LIME

## Database Schema

### Core Models

- **Document**: Uploaded legal documents
- **Clause**: Extracted legal clauses
- **RiskAssessment**: Risk analysis for clauses
- **AnalysisResult**: Overall document analysis
- **User**: User authentication and management

## Usage Examples

### Upload Document

```bash
curl -X POST \
  http://localhost:5000/api/documents/upload \
  -F "file=@contract.pdf" \
  -F "analysis_type=detailed" \
  -F "language=en"
```

### Analyze Text

```bash
curl -X POST \
  http://localhost:5000/api/analyze/text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The parties agree to maintain confidentiality...",
    "analysis_type": "both"
  }'
```

### Get Document Analysis

```bash
curl http://localhost:5000/api/documents/{document_id}
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

### Database Management

```bash
flask init-db      # Initialize database
flask reset-db     # Reset database
flask seed-db      # Seed with sample data
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app('production')"]
```

### Environment Setup

1. Set `FLASK_ENV=production`
2. Use PostgreSQL instead of SQLite
3. Configure proper logging
4. Set up reverse proxy (nginx)
5. Configure SSL/TLS

## Security Considerations

- File upload validation
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Rate limiting (implement as needed)
- Input validation and sanitization
- Secure file storage

## Performance

- Model caching in `models_cache/`
- Database connection pooling
- Async processing for large documents
- Request timeout configuration
- Memory management for AI models

## Logging

Logs are stored in `logs/legal_ai.log` with rotation:
- Max file size: 10MB
- Backup count: 10
- Log levels: DEBUG, INFO, WARNING, ERROR

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Check internet connection for first-time downloads
   - Verify `MODEL_CACHE_DIR` permissions
   - Ensure sufficient memory (4GB+ recommended)

2. **Database Errors**
   - Run `flask init-db` to create tables
   - Check database file permissions
   - Verify DATABASE_URL configuration

3. **File Upload Issues**
   - Check file size limits (50MB default)
   - Verify supported formats (PDF, DOCX, TXT)
   - Ensure UPLOAD_FOLDER exists and is writable

### Debug Mode

Enable debug mode for detailed error messages:
```bash
export FLASK_ENV=development
python run.py
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add tests for new features
3. Update documentation
4. Use semantic versioning
5. Create feature branches

## License

This project is part of the LexAI Legal Document Intelligence Platform - B.Tech CSE Final Year Project.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation
- Examine the logs in `logs/legal_ai.log`
