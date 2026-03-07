"""
Dashboard Service - Generates visualization-ready data
"""

from typing import List, Dict, Any
from collections import Counter
from datetime import datetime, timedelta
import structlog

from models import Intent, LogEntry, DashboardData, DashboardWidget

logger = structlog.get_logger()


class DashboardService:
    """
    Generates dashboard data from query results
    
    Analyzes logs and creates visualization-ready data structures:
    - Time series charts
    - Distribution charts
    - Tables
    - Metrics
    """
    
    async def generate_data(self, logs: List[LogEntry], intent: Intent) -> DashboardData:
        """
        Generate dashboard data based on intent type
        """
        logger.info(
            "generating_dashboard_data",
            intent_type=intent.type,
            log_count=len(logs)
        )
        
        if intent.type == "error_analysis":
            return await self._generate_error_dashboard(logs)
        elif intent.type == "timeline":
            return await self._generate_timeline_dashboard(logs)
        else:
            return await self._generate_generic_dashboard(logs)
    
    async def _generate_error_dashboard(self, logs: List[LogEntry]) -> DashboardData:
        """
        Generate error analysis dashboard
        
        Widgets:
        1. Error count over time (time series)
        2. Errors by service (bar chart)
        3. Top error messages (table)
        4. Error severity distribution (pie chart)
        """
        logger.info("generating_error_dashboard")
        
        widgets = []
        
        # Widget 1: Error count over time
        time_series_data = self._aggregate_by_time(logs, interval_minutes=5)
        widgets.append(DashboardWidget(
            type="timeseries",
            title="Error Count Over Time",
            data=time_series_data
        ))
        
        # Widget 2: Errors by service
        service_dist = self._aggregate_by_field(logs, field="service")
        widgets.append(DashboardWidget(
            type="bar",
            title="Errors by Service",
            data=service_dist
        ))
        
        # Widget 3: Top error messages
        top_errors = self._get_top_errors(logs, limit=10)
        widgets.append(DashboardWidget(
            type="table",
            title="Top Error Messages",
            data=top_errors
        ))
        
        # Widget 4: Severity distribution
        severity_dist = self._aggregate_by_field(logs, field="severity")
        widgets.append(DashboardWidget(
            type="pie",
            title="Error Severity Distribution",
            data=severity_dist
        ))
        
        return DashboardData(widgets=widgets)
    
    async def _generate_timeline_dashboard(self, logs: List[LogEntry]) -> DashboardData:
        """
        Generate timeline dashboard for trace analysis
        """
        logger.info("generating_timeline_dashboard")
        
        widgets = []
        
        # Widget 1: Event timeline
        timeline_data = self._create_timeline(logs)
        widgets.append(DashboardWidget(
            type="timeline",
            title="Event Timeline",
            data=timeline_data
        ))
        
        # Widget 2: Service call sequence
        sequence_data = self._create_service_sequence(logs)
        widgets.append(DashboardWidget(
            type="table",
            title="Service Call Sequence",
            data=sequence_data
        ))
        
        return DashboardData(widgets=widgets)
    
    async def _generate_generic_dashboard(self, logs: List[LogEntry]) -> DashboardData:
        """
        Generate generic dashboard for log search
        """
        logger.info("generating_generic_dashboard")
        
        widgets = []
        
        # Widget 1: Log count over time
        time_series_data = self._aggregate_by_time(logs, interval_minutes=10)
        widgets.append(DashboardWidget(
            type="timeseries",
            title="Log Count Over Time",
            data=time_series_data
        ))
        
        # Widget 2: Logs by severity
        severity_dist = self._aggregate_by_field(logs, field="severity")
        widgets.append(DashboardWidget(
            type="bar",
            title="Logs by Severity",
            data=severity_dist
        ))
        
        return DashboardData(widgets=widgets)
    
    def _aggregate_by_time(self, logs: List[LogEntry], interval_minutes: int = 5) -> List[Dict[str, Any]]:
        """
        Aggregate logs into time buckets
        """
        time_buckets: Dict[str, int] = {}
        
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log.timestamp.replace('Z', '+00:00'))
                # Round to interval
                bucket_time = timestamp.replace(
                    minute=(timestamp.minute // interval_minutes) * interval_minutes,
                    second=0,
                    microsecond=0
                )
                bucket_key = bucket_time.isoformat()
                time_buckets[bucket_key] = time_buckets.get(bucket_key, 0) + 1
            except Exception as e:
                logger.warning("failed_to_parse_timestamp", error=str(e))
                continue
        
        # Convert to list of dicts
        data = [
            {"timestamp": timestamp, "count": count}
            for timestamp, count in sorted(time_buckets.items())
        ]
        
        return data
    
    def _aggregate_by_field(self, logs: List[LogEntry], field: str) -> List[Dict[str, Any]]:
        """
        Aggregate logs by a specific field
        """
        counter = Counter()
        
        for log in logs:
            value = getattr(log, field, "unknown")
            counter[value] += 1
        
        # Convert to list of dicts
        data = [
            {"name": name, "value": count}
            for name, count in counter.most_common()
        ]
        
        return data
    
    def _get_top_errors(self, logs: List[LogEntry], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top error messages
        """
        error_logs = [log for log in logs if log.severity == "ERROR"]
        
        message_counter = Counter()
        for log in error_logs:
            # Truncate long messages
            message = log.message[:100]
            message_counter[message] += 1
        
        # Convert to table data
        data = [
            {
                "message": message,
                "count": count,
                "percentage": f"{(count / len(error_logs) * 100):.1f}%"
            }
            for message, count in message_counter.most_common(limit)
        ]
        
        return data
    
    def _create_timeline(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """
        Create timeline visualization data
        """
        timeline_data = []
        
        for log in sorted(logs, key=lambda x: x.timestamp):
            timeline_data.append({
                "timestamp": log.timestamp,
                "service": log.service,
                "severity": log.severity,
                "message": log.message[:100],
                "trace_id": log.trace_id
            })
        
        return timeline_data
    
    def _create_service_sequence(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """
        Create service call sequence data
        """
        sequence_data = []
        
        for i, log in enumerate(sorted(logs, key=lambda x: x.timestamp)):
            sequence_data.append({
                "step": i + 1,
                "timestamp": log.timestamp,
                "service": log.service,
                "severity": log.severity,
                "trace_id": log.trace_id
            })
        
        return sequence_data
