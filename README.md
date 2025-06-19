# GRC Compliance Monitoring API

A FastAPI-based backend for security investment optimization and compliance monitoring.

## Features

- **Compliance Monitoring**: Track and manage compliance checks across multiple frameworks
- **Security Analytics**: Real-time insights into security posture
- **Budget Optimization**: AI-powered recommendations for security investments
- **Multi-Framework Support**: SOC 2, HIPAA, GDPR, PCI-DSS, NIST, ISO 27001

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /api/test` - API connectivity test
- `GET /api/checks` - Compliance checks with filtering options
- `GET /docs` - Interactive API documentation (Swagger UI)

## Quick Start

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

### Production Deployment

The application is configured for deployment on Railway, Heroku, or similar platforms.

**Railway Deployment**:
- The app will automatically detect the FastAPI application
- Uses the command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Environment Variables

No environment variables are required for basic functionality. The application uses mock data for demonstration purposes.

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation and settings management
- **Python 3.11+**: Required Python version

## API Documentation

Once running, visit `/docs` for interactive API documentation powered by Swagger UI.

## CORS Configuration

The API is configured to accept requests from:
- `https://frontenduidashboard.netlify.app` (production frontend)
- `http://localhost:3000` (local development)
- All origins (`*`) for maximum compatibility

## Health Monitoring

Use the `/health` endpoint to monitor application status:

```json
{
  "status": "healthy",
  "timestamp": "2025-06-19T04:30:00.000Z",
  "version": "1.0.0"
}
```

