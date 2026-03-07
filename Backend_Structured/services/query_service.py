"""
Query Service - Orchestrates end-to-end query processing
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import structlog

from models import QueryRequest, QueryResponse, Intent, QueryResults
from services.bedrock_service import BedrockService
from services.opensearch_service import OpenSearchService
from services.dynamodb_service import DynamoDBService
from services.dashboard_service import DashboardService
from services.uterva_service import UtervaService

logger = structlog.get_logger()


class QueryService:
    """
    Orchestrates query processing workflow:
    1. Retrieve conversation context
    2. Extract intent using Bedrock
    3. Query logs from OpenSearch
    4. Analyze logs with Bedrock
    5. Generate dashboard data
    6. Store conversation
    """
    
    def __init__(self):
        self.bedrock = BedrockService()
        self.opensearch = OpenSearchService()
        self.dynamodb = DynamoDBService()
        self.dashboard = DashboardService()
        self.uterva = UtervaService()
    
    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """
        Process a natural language debugging query
        """
        query_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        logger.info(
            "processing_query",
            query_id=query_id,
            user_id=request.user_id,
            query=request.query
        )
        
        try:
            # Step 1: Retrieve conversation context
            context = await self._get_conversation_context(request.conversation_id)
            
            # Step 2: Extract intent using Amazon Bedrock
            intent = await self.bedrock.extract_intent(request.query, context)
            
            logger.info(
                "intent_extracted",
                query_id=query_id,
                intent_type=intent.type,
                confidence=intent.confidence
            )
            
            # Step 3: Query logs from OpenSearch
            logs = await self.opensearch.query_logs(intent)
            
            logger.info(
                "logs_retrieved",
                query_id=query_id,
                log_count=len(logs)
            )
            
            # Step 4: Check if external metrics needed
            external_metrics = None
            if "bug" in request.query.lower() or "metrics" in request.query.lower():
                external_metrics = await self.uterva.fetch_bug_metrics(intent.services)
            
            # Step 5: Analyze logs with Bedrock
            analysis = await self.bedrock.analyze_logs(logs, intent, external_metrics)
            
            logger.info(
                "analysis_completed",
                query_id=query_id,
                root_cause=analysis.root_cause,
                confidence=analysis.confidence
            )
            
            # Step 6: Generate dashboard data
            dashboard_data = None
            if intent.requires_visualization:
                dashboard_data = await self.dashboard.generate_data(logs, intent)
            
            # Step 7: Store conversation
            conversation_id = request.conversation_id or str(uuid.uuid4())
            await self._store_conversation(
                conversation_id=conversation_id,
                user_id=request.user_id,
                query=request.query,
                intent=intent,
                analysis=analysis
            )
            
            # Calculate processing time
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            logger.info(
                "query_processing_completed",
                query_id=query_id,
                duration_ms=duration_ms
            )
            
            # Build response
            return QueryResponse(
                query_id=query_id,
                conversation_id=conversation_id,
                intent=intent,
                results={
                    "logs": [log.dict() for log in logs],
                    "analysis": analysis.dict() if analysis else None,
                    "dashboard_data": dashboard_data.dict() if dashboard_data else None,
                    "external_metrics": external_metrics
                },
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(
                "query_processing_failed",
                query_id=query_id,
                error=str(e)
            )
            raise
    
    async def _get_conversation_context(self, conversation_id: Optional[str]) -> Dict[str, Any]:
        """Retrieve conversation context from DynamoDB"""
        if not conversation_id:
            return {}
        
        try:
            context = await self.dynamodb.get_conversation(conversation_id)
            return context
        except Exception as e:
            logger.warning(
                "failed_to_retrieve_context",
                conversation_id=conversation_id,
                error=str(e)
            )
            return {}
    
    async def _store_conversation(
        self,
        conversation_id: str,
        user_id: str,
        query: str,
        intent: Intent,
        analysis: Any
    ):
        """Store conversation in DynamoDB"""
        try:
            await self.dynamodb.store_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                query=query,
                intent=intent.dict(),
                analysis=analysis.dict() if analysis else None
            )
        except Exception as e:
            logger.error(
                "failed_to_store_conversation",
                conversation_id=conversation_id,
                error=str(e)
            )
            # Don't fail the request if storage fails
    
    async def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Retrieve full conversation history"""
        return await self.dynamodb.get_conversation(conversation_id)
