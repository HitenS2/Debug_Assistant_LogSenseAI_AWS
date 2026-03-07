# Requirements Document: Backend Orchestration Service

## Problem Statement

The AI-Powered Debugging Platform requires a backend orchestration layer that connects the web frontend with AWS services (Amazon Bedrock, Kinesis Firehose, Lambda, OpenSearch, DynamoDB) and external alert systems (Twilio). Currently, there is no unified service to:

- Process natural language debugging queries
- Orchestrate AI analysis workflows
- Retrieve and correlate logs from multiple sources
- Monitor warning thresholds and trigger alerts
- Generate dashboard-ready data

This backend service will act as the central nervous system, coordinating all interactions between components without redesigning the existing architecture.

## Goals

1. Build a FastAPI-based orchestration service that integrates with existing AWS infrastructure
2. Enable natural language query processing through Amazon Bedrock
3. Provide log retrieval and correlation from OpenSearch and DynamoDB
4. Implement intelligent alert monitoring with Twilio integration
5. Support external service integration (Uterva API)
6. Maintain conversation context across multiple queries
7. Generate structured data for dynamic dashboard creation

## Non-Goals

- Frontend implementation (handled separately)
- Redesigning the existing AWS architecture
- Direct log ingestion (handled by Kinesis + Lambda pipeline)
- Dashboard rendering (handled by frontend)
- User authentication (assumed to be handled by API Gateway/Cognito)

## Target Users

### Primary Users
- **DevOps Engineers**: Query logs, investigate incidents, receive alerts
- **SRE Teams**: Monitor system health, analyze root causes
- **Backend Engineers**: Debug distributed system issues
- **On-Call Engineers**: Receive and respond to critical alerts

### Secondary Users
- **System Administrators**: Configure alert thresholds
- **Platform Engineers**: Integrate external monitoring services

## User Personas

### Persona 1: DevOps Engineer (Priya)
- **Role**: Senior DevOps Engineer
- **Goals**: Quickly identify root causes of production incidents
- **Pain Points**: Switching between multiple tools, writing complex queries
- **Needs**: Natural language query interface, automated correlation, actionable insights

### Persona 2: On-Call SRE (Rahul)
- **Role**: Site Reliability Engineer (On-Call)
- **Goals**: Get alerted immediately when critical issues occur
- **Pain Points**: Alert fatigue, delayed notifications, unclear context
- **Needs**: Smart alerting with context, escalation workflows, multi-channel notifications

### Persona 3: Backend Engineer (Ananya)
- **Role**: Backend Software Engineer
- **Goals**: Debug microservice failures during development
- **Pain Points**: Correlating logs across services, understanding cascading failures
- **Needs**: Trace ID correlation, timeline visualization, suggested fixes

## Use Cases

### UC1: Natural Language Query Processing
**Actor**: DevOps Engineer  
**Precondition**: User is authenticated and has access to the platform  
**Flow**:
1. User submits query: "Show errors in payment-service in the last hour"
2. Backend forwards query to Amazon Bedrock for intent extraction
3. Bedrock returns structured intent (service: payment-service, time: 1h, severity: ERROR)
4. Backend translates intent to OpenSearch query
5. Backend retrieves logs and metadata
6. Backend sends logs to Bedrock for analysis
7. Backend returns formatted response with insights

**Postcondition**: User receives analyzed results with root cause suggestions

### UC2: Log Correlation Across Services
**Actor**: Backend Engineer  
**Precondition**: Logs exist in OpenSearch with trace IDs  
**Flow**:
1. User queries: "Trace transaction TRX_A2DC"
2. Backend extracts trace ID from query
3. Backend queries OpenSearch for all logs with matching trace_id
4. Backend retrieves metadata from DynamoDB
5. Backend constructs chronological timeline
6. Backend identifies failure points
7. Backend returns correlated logs with timeline

**Postcondition**: User sees complete transaction flow across all services

### UC3: Warning Threshold Alert
**Actor**: System (Automated)  
**Precondition**: Warning monitoring is enabled  
**Flow**:
1. Backend continuously monitors warning counts from log pipeline
2. Warning count exceeds threshold (e.g., >100 warnings in 5 minutes)
3. Backend triggers alert workflow
4. Backend calls Twilio API to send SMS/Voice/WhatsApp alert
5. Alert includes: service name, warning count, time window, severity
6. If warnings continue increasing, backend escalates to secondary contacts

**Postcondition**: On-call engineer receives timely alert with context

### UC4: Dashboard Data Generation
**Actor**: DevOps Engineer  
**Precondition**: Query has been processed  
**Flow**:
1. Backend receives query results from OpenSearch
2. Backend analyzes data characteristics (time-series, categorical, etc.)
3. Backend generates visualization-ready data structures
4. Backend returns data with suggested chart types
5. Frontend renders dashboard

**Postcondition**: User sees auto-generated dashboard

### UC5: External Service Integration
**Actor**: Backend Engineer  
**Precondition**: Uterva API credentials are configured  
**Flow**:
1. User queries for bug metrics
2. Backend calls Uterva API to fetch external metrics
3. Backend merges external data with AWS logs
4. Backend performs combined analysis
5. Backend returns unified insights

**Postcondition**: User sees comprehensive analysis from multiple sources

### UC6: Conversation Context Management
**Actor**: DevOps Engineer  
**Precondition**: User has an active conversation  
**Flow**:
1. User asks: "Show errors in payment-service"
2. Backend stores conversation context in DynamoDB
3. User asks follow-up: "What about auth-service?"
4. Backend retrieves context, understands implicit time range
5. Backend processes follow-up with context
6. Backend updates conversation history

**Postcondition**: User can have natural follow-up conversations

## Functional Requirements

### FR1: Query Handling API
- **FR1.1**: Accept POST requests to `/query` endpoint with natural language queries
- **FR1.2**: Support follow-up queries via `/query/followup` endpoint
- **FR1.3**: Retrieve conversation history via GET `/conversation/{id}`
- **FR1.4**: Validate query input (max length, sanitization)
- **FR1.5**: Return structured responses with query ID, results, and metadata

### FR2: Amazon Bedrock Integration
- **FR2.1**: Forward queries to Amazon Bedrock for intent extraction
- **FR2.2**: Parse Bedrock responses to extract:
  - Intent type (log_search, error_analysis, timeline, root_cause)
  - Entities (service names, time ranges, trace IDs)
  - Filters (severity, components)
  - Visualization hints
- **FR2.3**: Send retrieved logs to Bedrock for analysis
- **FR2.4**: Handle Bedrock API failures with retry logic
- **FR2.5**: Implement rate limiting for Bedrock calls

### FR3: OpenSearch Integration
- **FR3.1**: Translate AI-extracted intent into OpenSearch DSL queries
- **FR3.2**: Execute queries against OpenSearch cluster
- **FR3.3**: Support filters:
  - Time ranges (relative and absolute)
  - Service names
  - Severity levels (DEBUG, INFO, WARN, ERROR, FATAL)
  - Trace IDs
  - Transaction IDs
  - Error codes
- **FR3.4**: Implement pagination for large result sets
- **FR3.5**: Handle OpenSearch connection failures

### FR4: DynamoDB Integration
- **FR4.1**: Store conversation context with TTL
- **FR4.2**: Store alert state and history
- **FR4.3**: Store incident metadata
- **FR4.4**: Retrieve log metadata for correlation
- **FR4.5**: Query by trace_id and transaction_id using GSIs

### FR5: Log Correlation
- **FR5.1**: Correlate logs across services using trace IDs
- **FR5.2**: Correlate logs using transaction IDs
- **FR5.3**: Correlate logs using temporal proximity
- **FR5.4**: Construct chronological timelines
- **FR5.5**: Identify causal relationships between events

### FR6: AI Analysis Pipeline
- **FR6.1**: Format logs for Bedrock consumption
- **FR6.2**: Generate root cause analysis
- **FR6.3**: Generate error summaries
- **FR6.4**: Suggest fixes with confidence scores
- **FR6.5**: Identify similar historical incidents

### FR7: Dashboard Data Generation
- **FR7.1**: Analyze query results to determine data characteristics
- **FR7.2**: Generate time-series data for line charts
- **FR7.3**: Generate categorical distributions for bar/pie charts
- **FR7.4**: Generate correlation data for heatmaps
- **FR7.5**: Return data with suggested visualization types

### FR8: Warning Monitoring System
- **FR8.1**: Monitor warning/error counts in real-time
- **FR8.2**: Track warning rates over configurable time windows
- **FR8.3**: Compare current rates against baseline thresholds
- **FR8.4**: Detect anomalous spikes using statistical methods
- **FR8.5**: Maintain alert state to prevent duplicate alerts

### FR9: Twilio Alert Integration
- **FR9.1**: Send SMS alerts via Twilio API
- **FR9.2**: Send voice call alerts via Twilio API
- **FR9.3**: Send WhatsApp alerts via Twilio API
- **FR9.4**: Include in alerts:
  - Affected service name
  - Warning/error count
  - Time window
  - Severity level
  - Suggested action placeholder
- **FR9.5**: Implement escalation workflow for continued issues

### FR10: External Service Integration (Uterva)
- **FR10.1**: Connect to Uterva API for bug metrics
- **FR10.2**: Merge external metrics with AWS logs
- **FR10.3**: Perform combined analysis
- **FR10.4**: Handle Uterva API failures gracefully

### FR11: Configuration Management
- **FR11.1**: Load AWS credentials from environment variables
- **FR11.2**: Load Twilio credentials from environment variables
- **FR11.3**: Load Uterva API credentials from environment variables
- **FR11.4**: Support configurable alert thresholds
- **FR11.5**: Support configurable escalation contacts

## Non-Functional Requirements

### NFR1: Performance
- **NFR1.1**: Query response time < 3 seconds for simple queries
- **NFR1.2**: Query response time < 10 seconds for complex queries
- **NFR1.3**: Alert latency < 30 seconds from threshold breach
- **NFR1.4**: Support 100 concurrent API requests
- **NFR1.5**: OpenSearch query execution < 2 seconds

### NFR2: Scalability
- **NFR2.1**: Handle 1000 queries per minute
- **NFR2.2**: Process 10,000 log entries per query
- **NFR2.3**: Support horizontal scaling via multiple instances
- **NFR2.4**: Stateless design for easy scaling

### NFR3: Reliability
- **NFR3.1**: 99.9% uptime for API endpoints
- **NFR3.2**: Graceful degradation when AI services unavailable
- **NFR3.3**: Retry logic for transient failures (3 retries with exponential backoff)
- **NFR3.4**: Circuit breaker pattern for external services
- **NFR3.5**: Alert delivery success rate > 99%

### NFR4: Security
- **NFR4.1**: API authentication via JWT tokens
- **NFR4.2**: Rate limiting: 100 requests/minute per user
- **NFR4.3**: Input validation and sanitization
- **NFR4.4**: Secure credential storage (AWS Secrets Manager)
- **NFR4.5**: HTTPS-only communication
- **NFR4.6**: Audit logging for all API calls

### NFR5: Maintainability
- **NFR5.1**: Modular service architecture
- **NFR5.2**: Comprehensive logging (structured JSON logs)
- **NFR5.3**: Health check endpoints
- **NFR5.4**: Metrics export (Prometheus format)
- **NFR5.5**: Clear error messages with request IDs

### NFR6: Observability
- **NFR6.1**: Log all API requests with timing
- **NFR6.2**: Track Bedrock API usage and costs
- **NFR6.3**: Monitor OpenSearch query performance
- **NFR6.4**: Track alert delivery success/failure
- **NFR6.5**: Export metrics to CloudWatch

## Success Metrics

### User Experience Metrics
- **Query Success Rate**: >95% of queries return valid results
- **Average Query Response Time**: <5 seconds
- **User Satisfaction**: >4.0/5.0 rating
- **Follow-up Query Success**: >90% of follow-ups maintain context

### System Performance Metrics
- **API Uptime**: >99.9%
- **Alert Delivery Rate**: >99%
- **Alert Latency**: <30 seconds
- **False Positive Rate**: <5% of alerts

### Business Metrics
- **Mean Time to Detection (MTTD)**: <2 minutes
- **Mean Time to Resolution (MTTR)**: Reduced by 40%
- **Manual Query Reduction**: 70% fewer manual log queries
- **On-Call Response Time**: <5 minutes

## Constraints

### Technical Constraints
- Must use FastAPI framework (Python)
- Must integrate with existing AWS architecture (no redesign)
- Must use async/await for I/O operations
- Must support deployment on AWS Lambda or ECS

### Business Constraints
- MVP delivery within 2-3 weeks
- Must work with existing log pipeline (Kinesis + Lambda)
- Must not require changes to frontend API contract

### Operational Constraints
- Must use existing AWS account and credentials
- Must comply with data retention policies (30 days)
- Must support deployment in us-east-1 region

## Assumptions

1. AWS services (Bedrock, OpenSearch, DynamoDB, Kinesis) are already provisioned
2. Log ingestion pipeline (Kinesis + Lambda) is operational
3. Logs follow a normalized schema in OpenSearch
4. Frontend handles user authentication and passes JWT tokens
5. Twilio account is provisioned with sufficient credits
6. Uterva API is accessible and documented
7. Network connectivity between backend and AWS services is reliable
8. DynamoDB tables have appropriate GSIs for trace_id and transaction_id queries

## Dependencies

### External Services
- Amazon Bedrock (AI analysis)
- Amazon OpenSearch Service (log storage)
- Amazon DynamoDB (metadata storage)
- Amazon Kinesis Firehose (log ingestion)
- AWS Lambda (log processing)
- Twilio API (alerts)
- Uterva API (external metrics)

### Libraries/Frameworks
- FastAPI (web framework)
- boto3 (AWS SDK)
- httpx (async HTTP client)
- pydantic (data validation)
- twilio (Twilio SDK)

## Out of Scope

- Frontend implementation
- Log ingestion pipeline implementation
- Dashboard rendering
- User authentication/authorization
- AWS infrastructure provisioning
- Mobile app development
- Real-time WebSocket streaming (future enhancement)
- Machine learning model training
- Custom visualization libraries
