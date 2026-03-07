# Backend Orchestration Service

FastAPI-based backend orchestration layer for the AI-Powered Debugging Platform.

## Overview

This service acts as the central coordination layer between:
- Web frontend (chat queries)
- AWS AI services (Amazon Bedrock)
- Log pipeline (Kinesis + Lambda + OpenSearch)
- Metadata storage (DynamoDB)
- Alert system (Twilio integration)

## Architecture

```
User → FastAPI Backend → Amazon Bedrock (AI)
                      → OpenSearch (Logs)
                      → DynamoDB (Context)
                      → Twilio (Alerts)
                      → Uterva API (External Metrics)
```

## Features

- ✅ Natural language query processing
- ✅ AI-powered intent extraction
- ✅ Log retrieval and correlation
- ✅ Root cause analysis
- ✅ Dashboard data generation
- ✅ Warning threshold monitoring
- ✅ Multi-channel alerts (SMS, Voice, WhatsApp)
- ✅ External service integration
- ✅ Conversation context management

## Project Structure

```
backend-orchestration/
├── main.py                 # FastAPI application entry point
├── models.py               # Pydantic data models
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── services/
│   ├── query_service.py        # Query orchestration
│   ├── bedrock_service.py      # Amazon Bedrock integration
│   ├── opensearch_service.py   # OpenSearch log retrieval
│   ├── dynamodb_service.py     # DynamoDB context storage
│   ├── alert_service.py        # Alert monitoring
│   ├── twilio_service.py       # Twilio alert delivery
│   ├── dashboard_service.py    # Dashboard data generation
│   └── uterva_service.py       # External API integration
└── README.md
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with configuration:
```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# OpenSearch
OPENSEARCH_ENDPOINT=https://your-opensearch-endpoint
OPENSEARCH_USERNAME=admin
OPENSEARCH_PASSWORD=your_password

# DynamoDB Tables
DYNAMODB_CONVERSATION_TABLE=ConversationContext
DYNAMODB_METADATA_TABLE=LogMetadata
DYNAMODB_ALERT_TABLE=AlertState

# Twilio (Replace with actual credentials)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
ONCALL_PHONE_NUMBER=+1234567890

# Uterva API (Replace with actual credentials)
UTERVA_API_KEY=your_api_key
UTERVA_API_ENDPOINT=https://api.uterva.com
```

## Running the Service

### Development Mode
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Query Endpoints

#### POST /query
Submit a natural language debugging query.

**Request:**
```json
{
  "query": "Show errors in payment-service in the last hour",
  "user_id": "user-123",
  "conversation_id": "conv-456"
}
```

**Response:**
```json
{
  "query_id": "query-789",
  "conversation_id": "conv-456",
  "intent": {...},
  "results": {
    "logs": [...],
    "analysis": {...},
    "dashboard_data": {...}
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### POST /query/followup
Submit a follow-up query with conversation context.

#### GET /conversation/{conversation_id}
Retrieve conversation history.

### Health Endpoints

#### GET /health
Health check endpoint.

#### GET /metrics
Prometheus-format metrics.

## Configuration

All configuration is managed through environment variables. See `config.py` for available settings.

### Alert Thresholds

Configure per-service alert thresholds in `config.py`:
```python
alert_thresholds: Dict[str, int] = {
    "payment-service": 100,
    "auth-service": 50,
    "order-service": 75,
}
```

## Alert Monitoring

The service automatically monitors warning/error counts and triggers alerts when thresholds are exceeded.

**Alert Workflow:**
1. Monitor warning counts every 30 seconds
2. Compare against configured thresholds
3. Send SMS alert when threshold exceeded
4. Send WhatsApp for critical alerts
5. Make voice call if not acknowledged within 1 minute
6. Escalate to secondary contacts if warnings continue increasing

## Development

### Running Tests
```bash
pytest tests/ -v --cov=.
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

## Deployment

### AWS Lambda
Use AWS Lambda Web Adapter for deployment:
```bash
# Build Docker image
docker build -t backend-orchestration .

# Deploy to Lambda
# (Use AWS SAM or Serverless Framework)
```

### ECS Fargate
```bash
# Build and push Docker image
docker build -t backend-orchestration .
docker tag backend-orchestration:latest <ecr-repo>:latest
docker push <ecr-repo>:latest

# Deploy to ECS
# (Use AWS CLI or CloudFormation)
```

## Placeholder Integrations

The following integrations use placeholder implementations:

- **Amazon Bedrock**: Mock intent extraction and analysis
- **OpenSearch**: Mock log queries
- **DynamoDB**: Mock context storage
- **Twilio**: Mock alert delivery
- **Uterva API**: Mock bug metrics

To enable real integrations:
1. Uncomment boto3/twilio client initialization in service files
2. Add actual API credentials to `.env`
3. Test with real AWS services

## Monitoring

The service exports structured logs in JSON format:
```json
{
  "event": "query_received",
  "user_id": "user-123",
  "query_length": 45,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

Metrics are available at `/metrics` endpoint in Prometheus format.

## Security

- JWT token authentication (integrate with AWS Cognito)
- Rate limiting: 100 requests/minute per user
- Input validation with Pydantic
- Secure credential storage (use AWS Secrets Manager)

## License

MIT License

## Support

For issues or questions, contact the development team.
