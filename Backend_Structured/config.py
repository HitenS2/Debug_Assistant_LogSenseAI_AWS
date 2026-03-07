"""
Configuration management using environment variables
"""

from pydantic_settings import BaseSettings
from typing import Dict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    
    # OpenSearch Configuration
    opensearch_endpoint: str = ""
    opensearch_username: str = ""
    opensearch_password: str = ""
    opensearch_index_pattern: str = "logs-*"
    
    # DynamoDB Tables
    dynamodb_conversation_table: str = "ConversationContext"
    dynamodb_metadata_table: str = "LogMetadata"
    dynamodb_alert_table: str = "AlertState"
    
    # Amazon Bedrock Configuration
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    bedrock_max_tokens: int = 2000
    
    # Twilio Configuration (Placeholder)
    twilio_account_sid: str = "TWILIO_ACCOUNT_SID_HERE"
    twilio_auth_token: str = "TWILIO_AUTH_TOKEN_HERE"
    twilio_phone_number: str = "+1234567890"
    oncall_phone_number: str = "+1234567890"
    oncall_whatsapp_number: str = "whatsapp:+1234567890"
    
    # Uterva API Configuration (Placeholder)
    uterva_api_key: str = "UTERVA_API_KEY_HERE"
    uterva_api_endpoint: str = "https://api.uterva.com"
    
    # Alert Thresholds
    alert_threshold_default: int = 100
    alert_window_seconds: int = 300  # 5 minutes
    alert_check_interval_seconds: int = 30
    
    # Alert Thresholds by Service
    alert_thresholds: Dict[str, int] = {
        "payment-service": 100,
        "auth-service": 50,
        "order-service": 75,
        "notification-service": 150
    }
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    
    # Query Configuration
    max_query_length: int = 1000
    max_logs_per_query: int = 1000
    default_time_range_hours: int = 1
    
    # Retry Configuration
    max_retries: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 10.0
    
    # Circuit Breaker Configuration
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: int = 60
    
    # Conversation TTL (90 days in seconds)
    conversation_ttl_seconds: int = 7776000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
