"""
Bedrock Service - Manages Amazon Bedrock AI interactions
"""

import json
from typing import Dict, Any, List, Optional
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from models import Intent, LogEntry, AnalysisResult
from config import settings

logger = structlog.get_logger()


class BedrockService:
    """
    Manages interactions with Amazon Bedrock for:
    - Intent extraction from natural language
    - Log analysis and root cause identification
    - Fix suggestions generation
    """
    
    def __init__(self):
        # Placeholder for boto3 bedrock client
        # In production: self.client = boto3.client('bedrock-runtime', region_name=settings.aws_region)
        self.client = None
        self.model_id = settings.bedrock_model_id
        self.max_tokens = settings.bedrock_max_tokens
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(
            multiplier=settings.retry_base_delay,
            max=settings.retry_max_delay
        )
    )
    async def extract_intent(self, query: str, context: Dict[str, Any]) -> Intent:
        """
        Extract debugging intent from natural language query
        
        Returns structured intent with:
        - Intent type (log_search, error_analysis, timeline, root_cause)
        - Confidence score
        - Extracted entities (services, time ranges, etc.)
        - Filters
        """
        logger.info("extracting_intent", query_length=len(query))
        
        prompt = self._build_intent_extraction_prompt(query, context)
        
        # Placeholder for actual Bedrock API call
        # response = await self.client.invoke_model(...)
        
        # Mock response for demonstration
        intent_data = self._mock_intent_extraction(query)
        
        intent = Intent(**intent_data)
        
        logger.info(
            "intent_extracted",
            intent_type=intent.type,
            confidence=intent.confidence,
            services=intent.services
        )
        
        return intent
    
    def _build_intent_extraction_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build prompt for intent extraction"""
        
        context_str = ""
        if context and "messages" in context:
            recent_messages = context["messages"][-3:]  # Last 3 messages
            context_str = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in recent_messages
            ])
        
        prompt = f"""You are an AI assistant for debugging distributed systems. 
Extract the debugging intent from the user's query.

Previous conversation context:
{context_str if context_str else "No previous context"}

Current query: {query}

Extract and return a JSON object with:
- type: one of [log_search, error_analysis, timeline, root_cause, comparison]
- confidence: float between 0 and 1
- entities: dict with service names, time ranges, trace IDs, etc.
- services: list of service names mentioned
- filters: dict with severity, error codes, etc.
- requires_visualization: boolean
- time_range: dict with 'gte' and 'lte' timestamps if time mentioned

Return only valid JSON, no additional text."""
        
        return prompt
    
    def _mock_intent_extraction(self, query: str) -> Dict[str, Any]:
        """Mock intent extraction for demonstration"""
        
        query_lower = query.lower()
        
        # Determine intent type
        if "error" in query_lower or "fail" in query_lower:
            intent_type = "error_analysis"
        elif "timeline" in query_lower or "trace" in query_lower:
            intent_type = "timeline"
        elif "root cause" in query_lower or "why" in query_lower:
            intent_type = "root_cause"
        else:
            intent_type = "log_search"
        
        # Extract services
        services = []
        service_keywords = ["payment", "auth", "order", "notification"]
        for keyword in service_keywords:
            if keyword in query_lower:
                services.append(f"{keyword}-service")
        
        # Extract time range
        time_range = None
        if "last hour" in query_lower or "1 hour" in query_lower:
            time_range = {"gte": "now-1h", "lte": "now"}
        elif "last day" in query_lower or "24 hours" in query_lower:
            time_range = {"gte": "now-24h", "lte": "now"}
        
        # Extract severity
        filters = {}
        if "error" in query_lower:
            filters["severity"] = "ERROR"
        elif "warning" in query_lower:
            filters["severity"] = "WARN"
        
        return {
            "type": intent_type,
            "confidence": 0.85,
            "entities": {
                "query_text": query,
                "extracted_services": services,
                "time_mentioned": time_range is not None
            },
            "time_range": time_range,
            "services": services,
            "filters": filters,
            "requires_visualization": intent_type in ["error_analysis", "timeline"],
            "visualization_hint": "timeseries" if intent_type == "error_analysis" else None
        }
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(
            multiplier=settings.retry_base_delay,
            max=settings.retry_max_delay
        )
    )
    async def analyze_logs(
        self,
        logs: List[LogEntry],
        intent: Intent,
        external_metrics: Optional[Dict] = None
    ) -> AnalysisResult:
        """
        Analyze logs using Amazon Bedrock to generate:
        - Root cause analysis
        - Error summaries
        - Fix suggestions
        - Confidence scores
        """
        logger.info("analyzing_logs", log_count=len(logs))
        
        if not logs:
            return AnalysisResult(
                root_cause="No logs found matching the query criteria",
                confidence=1.0,
                evidence=[],
                suggestions=[],
                similar_incidents=[]
            )
        
        prompt = self._build_analysis_prompt(logs, intent, external_metrics)
        
        # Placeholder for actual Bedrock API call
        # response = await self.client.invoke_model(...)
        
        # Mock analysis for demonstration
        analysis_data = self._mock_log_analysis(logs, intent)
        
        analysis = AnalysisResult(**analysis_data)
        
        logger.info(
            "analysis_completed",
            root_cause=analysis.root_cause,
            confidence=analysis.confidence,
            suggestion_count=len(analysis.suggestions)
        )
        
        return analysis
    
    def _build_analysis_prompt(
        self,
        logs: List[LogEntry],
        intent: Intent,
        external_metrics: Optional[Dict]
    ) -> str:
        """Build prompt for log analysis"""
        
        # Format logs for AI consumption
        log_summary = []
        for log in logs[:50]:  # Limit to first 50 logs
            log_summary.append(
                f"[{log.timestamp}] {log.service} - {log.severity}: {log.message[:200]}"
            )
        
        logs_text = "\n".join(log_summary)
        
        external_context = ""
        if external_metrics:
            external_context = f"\nExternal metrics: {json.dumps(external_metrics, indent=2)}"
        
        prompt = f"""You are an expert in debugging distributed systems.
Analyze the following logs and provide root cause analysis.

Intent: {intent.type}
Services: {', '.join(intent.services)}
Time range: {intent.time_range}

Logs:
{logs_text}
{external_context}

Provide analysis in JSON format:
- root_cause: string describing the root cause
- confidence: float between 0 and 1
- evidence: list of log IDs supporting the analysis
- suggestions: list of dicts with 'title' and 'description' for fixes
- similar_incidents: list of similar incident IDs (if any)

Return only valid JSON."""
        
        return prompt
    
    def _mock_log_analysis(self, logs: List[LogEntry], intent: Intent) -> Dict[str, Any]:
        """Mock log analysis for demonstration"""
        
        # Count errors
        error_count = sum(1 for log in logs if log.severity == "ERROR")
        
        # Find common error patterns
        error_messages = [log.message for log in logs if log.severity == "ERROR"]
        
        # Generate mock root cause
        if error_count > 50:
            root_cause = "High volume of errors detected. Possible causes: database connection timeout, service overload, or recent deployment issue."
        elif "timeout" in " ".join(error_messages).lower():
            root_cause = "Database connection timeout detected across multiple services."
        elif "null" in " ".join(error_messages).lower():
            root_cause = "Null pointer exceptions detected, likely due to missing data validation."
        else:
            root_cause = "Multiple error patterns detected. Further investigation needed."
        
        # Generate suggestions
        suggestions = [
            {
                "title": "Check database connection pool",
                "description": "Verify database connection pool settings and increase max connections if needed."
            },
            {
                "title": "Review recent deployments",
                "description": "Check if errors started after a recent deployment and consider rollback."
            },
            {
                "title": "Scale service instances",
                "description": "Consider scaling up service instances to handle increased load."
            }
        ]
        
        # Get evidence (log IDs)
        evidence = [log.id for log in logs[:5] if log.severity == "ERROR"]
        
        return {
            "root_cause": root_cause,
            "confidence": 0.75,
            "evidence": evidence,
            "suggestions": suggestions,
            "similar_incidents": []
        }
