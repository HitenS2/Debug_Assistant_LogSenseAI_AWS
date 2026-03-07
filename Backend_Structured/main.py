"""
FastAPI Backend Orchestration Service
AI-Powered Debugging Platform
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import structlog
from typing import Optional
import asyncio

from models import (
    QueryRequest, QueryResponse, FollowupRequest,
    ConversationResponse, HealthResponse
)
from services.query_service import QueryService
from services.alert_service import AlertService
from config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Security
security = HTTPBearer()

# Background task for alert monitoring
alert_monitor_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown"""
    global alert_monitor_task
    
    # Startup
    logger.info("starting_backend_orchestration_service")
    
    # Initialize services
    app.state.query_service = QueryService()
    app.state.alert_service = AlertService()
    
    # Start alert monitoring in background
    alert_monitor_task = asyncio.create_task(
        app.state.alert_service.monitor_warnings()
    )
    logger.info("alert_monitoring_started")
    
    yield
    
    # Shutdown
    logger.info("shutting_down_backend_orchestration_service")
    if alert_monitor_task:
        alert_monitor_task.cancel()
        try:
            await alert_monitor_task
        except asyncio.CancelledError:
            pass
    logger.info("alert_monitoring_stopped")


# Initialize FastAPI app
app = FastAPI(
    title="Backend Orchestration Service",
    description="AI-Powered Debugging Platform Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token (placeholder - integrate with Cognito)"""
    token = credentials.credentials
    # TODO: Implement JWT verification with AWS Cognito
    # For now, accept any token
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("health_check_requested")
    
    # Check service health
    services_status = {
        "bedrock": "up",  # TODO: Implement actual health checks
        "opensearch": "up",
        "dynamodb": "up",
        "twilio": "up"
    }
    
    overall_status = "healthy" if all(
        status == "up" for status in services_status.values()
    ) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        services=services_status
    )


@app.get("/metrics")
async def metrics():
    """Prometheus-format metrics endpoint"""
    # TODO: Implement metrics collection
    return {
        "queries_total": 0,
        "queries_success": 0,
        "queries_failed": 0,
        "alerts_sent": 0,
        "avg_response_time_ms": 0
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """
    Process a natural language debugging query
    
    Flow:
    1. Retrieve conversation context from DynamoDB
    2. Extract intent using Amazon Bedrock
    3. Query logs from OpenSearch
    4. Analyze logs with Bedrock
    5. Generate dashboard data
    6. Store conversation context
    """
    logger.info(
        "query_received",
        user_id=request.user_id,
        query_length=len(request.query),
        has_conversation=bool(request.conversation_id)
    )
    
    try:
        query_service: QueryService = app.state.query_service
        response = await query_service.process_query(request)
        
        logger.info(
            "query_completed",
            query_id=response.query_id,
            intent_type=response.intent.type,
            log_count=len(response.results.get("logs", []))
        )
        
        return response
        
    except Exception as e:
        logger.error(
            "query_failed",
            error=str(e),
            user_id=request.user_id
        )
        raise HTTPException(
            status_code=500,
            detail=f"Query processing failed: {str(e)}"
        )


@app.post("/query/followup", response_model=QueryResponse)
async def process_followup(
    request: FollowupRequest,
    token: str = Depends(verify_token)
):
    """
    Process a follow-up query with conversation context
    """
    logger.info(
        "followup_query_received",
        user_id=request.user_id,
        conversation_id=request.conversation_id
    )
    
    if not request.conversation_id:
        raise HTTPException(
            status_code=400,
            detail="conversation_id is required for follow-up queries"
        )
    
    try:
        query_service: QueryService = app.state.query_service
        
        # Convert followup to regular query request
        query_request = QueryRequest(
            query=request.query,
            user_id=request.user_id,
            conversation_id=request.conversation_id
        )
        
        response = await query_service.process_query(query_request)
        
        logger.info(
            "followup_query_completed",
            query_id=response.query_id,
            conversation_id=request.conversation_id
        )
        
        return response
        
    except Exception as e:
        logger.error(
            "followup_query_failed",
            error=str(e),
            conversation_id=request.conversation_id
        )
        raise HTTPException(
            status_code=500,
            detail=f"Follow-up query processing failed: {str(e)}"
        )


@app.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    token: str = Depends(verify_token)
):
    """
    Retrieve conversation history
    """
    logger.info(
        "conversation_retrieval_requested",
        conversation_id=conversation_id
    )
    
    try:
        query_service: QueryService = app.state.query_service
        conversation = await query_service.get_conversation(conversation_id)
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        
        logger.info(
            "conversation_retrieved",
            conversation_id=conversation_id,
            message_count=len(conversation.get("messages", []))
        )
        
        return ConversationResponse(**conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "conversation_retrieval_failed",
            error=str(e),
            conversation_id=conversation_id
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
