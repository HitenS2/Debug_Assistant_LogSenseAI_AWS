"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for natural language query"""
    query: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(..., pattern=r"^user-[a-zA-Z0-9]+$")
    conversation_id: Optional[str] = None


class FollowupRequest(BaseModel):
    """Request model for follow-up query"""
    query: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(..., pattern=r"^user-[a-zA-Z0-9]+$")
    conversation_id: str = Field(..., min_length=1)


class Intent(BaseModel):
    """Extracted intent from natural language query"""
    type: str  # log_search, error_analysis, timeline, root_cause
    confidence: float = Field(..., ge=0.0, le=1.0)
    entities: Dict[str, Any] = {}
    time_range: Optional[Dict[str, str]] = None
    services: List[str] = []
    filters: Dict[str, Any] = {}
    requires_visualization: bool = False
    visualization_hint: Optional[str] = None


class LogEntry(BaseModel):
    """Log entry model"""
    id: str
    timestamp: str
    service: str
    severity: str
    message: str
    trace_id: Optional[str] = None
    transaction_id: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Dict[str, Any] = {}


class AnalysisResult(BaseModel):
    """AI analysis result"""
    root_cause: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: List[str] = []
    suggestions: List[Dict[str, str]] = []
    similar_incidents: List[str] = []


class DashboardWidget(BaseModel):
    """Dashboard widget definition"""
    type: str  # timeseries, bar, pie, heatmap, table, metric
    title: str
    data: List[Dict[str, Any]]


class DashboardData(BaseModel):
    """Dashboard data structure"""
    widgets: List[DashboardWidget]


class QueryResults(BaseModel):
    """Query results container"""
    logs: List[LogEntry]
    analysis: Optional[AnalysisResult] = None
    dashboard_data: Optional[DashboardData] = None


class QueryResponse(BaseModel):
    """Response model for query endpoint"""
    query_id: str
    conversation_id: str
    intent: Intent
    results: Dict[str, Any]
    timestamp: str


class Message(BaseModel):
    """Conversation message"""
    role: str  # user or assistant
    content: str
    timestamp: str


class ConversationResponse(BaseModel):
    """Response model for conversation endpoint"""
    conversation_id: str
    user_id: str
    created_at: str
    messages: List[Message]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    services: Dict[str, str]
    timestamp: Optional[str] = None


class Alert(BaseModel):
    """Alert model"""
    alert_id: str
    service: str
    warning_count: int
    time_window: str
    severity: str
    suggested_action: str
    timestamp: str
