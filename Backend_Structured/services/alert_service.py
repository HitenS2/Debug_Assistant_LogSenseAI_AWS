"""
Alert Service - Monitors thresholds and triggers alerts
"""

import asyncio
import time
import uuid
from datetime import datetime
from typing import Dict, List
import structlog

from models import Alert
from services.opensearch_service import OpenSearchService
from services.dynamodb_service import DynamoDBService
from services.twilio_service import TwilioService
from config import settings

logger = structlog.get_logger()


class AlertService:
    """
    Monitors warning/error thresholds and triggers alerts
    
    Workflow:
    1. Continuously monitor warning counts from OpenSearch
    2. Compare against configured thresholds
    3. Trigger alerts via Twilio when thresholds exceeded
    4. Implement escalation for continued issues
    5. Prevent duplicate alerts using DynamoDB state
    """
    
    def __init__(self):
        self.opensearch = OpenSearchService()
        self.dynamodb = DynamoDBService()
        self.twilio = TwilioService()
        self.monitored_services = list(settings.alert_thresholds.keys())
        self.check_interval = settings.alert_check_interval_seconds
        self.alert_window = settings.alert_window_seconds
    
    async def monitor_warnings(self):
        """
        Continuous monitoring loop for warning/error thresholds
        
        Runs in background and checks every 30 seconds
        """
        logger.info(
            "alert_monitoring_started",
            services=self.monitored_services,
            check_interval=self.check_interval
        )
        
        try:
            while True:
                await self._check_all_services()
                await asyncio.sleep(self.check_interval)
                
        except asyncio.CancelledError:
            logger.info("alert_monitoring_cancelled")
            raise
        except Exception as e:
            logger.error("alert_monitoring_error", error=str(e))
            # Continue monitoring even if one check fails
            await asyncio.sleep(self.check_interval)
    
    async def _check_all_services(self):
        """Check warning counts for all monitored services"""
        
        for service in self.monitored_services:
            try:
                await self._check_service(service)
            except Exception as e:
                logger.error(
                    "service_check_failed",
                    service=service,
                    error=str(e)
                )
    
    async def _check_service(self, service: str):
        """Check warning count for a specific service"""
        
        # Get warning count for the time window
        count = await self._get_warning_count(service)
        
        threshold = settings.alert_thresholds.get(
            service,
            settings.alert_threshold_default
        )
        
        logger.debug(
            "service_checked",
            service=service,
            count=count,
            threshold=threshold
        )
        
        if count > threshold:
            logger.warning(
                "threshold_exceeded",
                service=service,
                count=count,
                threshold=threshold
            )
            
            await self._handle_threshold_breach(service, count, threshold)
    
    async def _get_warning_count(self, service: str) -> int:
        """
        Get warning/error count for service in the alert window
        
        Queries OpenSearch for ERROR and WARN logs in the last N minutes
        """
        # Placeholder for actual OpenSearch aggregation query
        # query = {
        #     "query": {
        #         "bool": {
        #             "filter": [
        #                 {"term": {"service": service}},
        #                 {"terms": {"severity": ["ERROR", "WARN"]}},
        #                 {"range": {"timestamp": {"gte": f"now-{self.alert_window}s"}}}
        #             ]
        #         }
        #     },
        #     "size": 0
        # }
        # response = await self.opensearch.client.count(index="logs-*", body=query)
        # return response['count']
        
        # Mock count for demonstration
        import random
        return random.randint(50, 150)
    
    async def _handle_threshold_breach(self, service: str, count: int, threshold: int):
        """
        Handle threshold breach:
        1. Check if already alerted recently
        2. Send new alert or escalate
        3. Store alert state
        """
        # Check alert state
        alert_state = await self.dynamodb.get_alert_state(service)
        
        current_time = time.time()
        
        if alert_state:
            alerted_at = alert_state.get("alerted_at", 0)
            previous_count = alert_state.get("previous_count", 0)
            
            # If alerted in last 5 minutes
            if current_time - alerted_at < 300:
                # Check if count increased significantly (50% increase)
                if count > previous_count * 1.5:
                    logger.warning(
                        "escalating_alert",
                        service=service,
                        previous_count=previous_count,
                        current_count=count
                    )
                    await self._escalate_alert(service, count)
                else:
                    logger.info(
                        "alert_suppressed",
                        service=service,
                        reason="recently_alerted"
                    )
                return
        
        # Send new alert
        await self._trigger_alert(service, count, threshold)
    
    async def _trigger_alert(self, service: str, count: int, threshold: int):
        """
        Trigger new alert via Twilio
        """
        logger.info(
            "triggering_alert",
            service=service,
            count=count,
            threshold=threshold
        )
        
        # Determine severity
        if count > threshold * 2:
            severity = "CRITICAL"
        elif count > threshold * 1.5:
            severity = "HIGH"
        else:
            severity = "MEDIUM"
        
        # Create alert
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            service=service,
            warning_count=count,
            time_window=f"{self.alert_window // 60} minutes",
            severity=severity,
            suggested_action="Check service logs and recent deployments. Verify database connections and service health.",
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Send alert via Twilio
        await self.twilio.send_alert(alert)
        
        # Store alert state
        await self.dynamodb.store_alert_state(service, count)
        
        logger.info(
            "alert_triggered",
            alert_id=alert.alert_id,
            service=service,
            severity=severity
        )
    
    async def _escalate_alert(self, service: str, count: int):
        """
        Escalate alert to secondary contacts
        """
        logger.warning(
            "escalating_alert",
            service=service,
            count=count
        )
        
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            service=service,
            warning_count=count,
            time_window=f"{self.alert_window // 60} minutes",
            severity="CRITICAL",
            suggested_action="ESCALATED: Warnings continue to increase. Immediate action required.",
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Send escalated alert
        await self.twilio.send_escalated_alert(alert)
        
        # Update alert state
        await self.dynamodb.store_alert_state(service, count)
        
        logger.warning(
            "alert_escalated",
            alert_id=alert.alert_id,
            service=service
        )
