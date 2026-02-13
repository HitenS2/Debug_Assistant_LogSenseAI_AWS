# Design Document: AI-Powered Debugging Platform

## Overview

The AI-Powered Debugging Platform is a web-based observability portal that simplifies debugging of distributed systems through conversational AI. It eliminates the need for query languages and manual dashboard configuration by providing a natural language interface powered by Amazon Bedrock and Amazon Q.

### Key Design Principles

1. Intent-driven behavior based on user queries  
2. Natural language interaction without query syntax  
3. Automatic dashboard generation  
4. Context-aware correlation across services  
5. Unified interface for chat, dashboards, and history  

### Technology Stack

- **Frontend:** React with TypeScript (AWS Amplify)  
- **Backend API:** Flask on AWS Lambda via API Gateway  
- **AI Services:** Amazon Bedrock 
- **Log Ingestion:** Amazon Kinesis Firehose  
- **Processing:** AWS Lambda  
- **Storage:** Amazon OpenSearch Service, DynamoDB  



---


## Architecture Diagram

## Architecture Diagram

```mermaid
graph TB
    User[👤 User<br/>Natural Language Queries] -->|Queries| Frontend[💻 Web Frontend<br/>React + TypeScript]
    
    Frontend -->|API Requests| Bedrock[🤖 Amazon Bedrock<br/>Intent Extraction & AI]
    Frontend -->|Query Results| Dashboard[📊 Dynamic Dashboards<br/>Auto-generated based on queries]
    
    Bedrock -->|Analyzed Intent| OpenSearch[🔍 Amazon OpenSearch<br/>Log Storage & Search]
    
    Services[🌐 Microservices<br/>Logs of all services] -->|Log Ingestion| Kinesis[📥 Amazon Kinesis Firehose]
    
    Kinesis -->|Stream| Lambda[⚡ AWS Lambda<br/>Normalization & Categorization]
    
    Lambda -->|Processed Logs| OpenSearch
    Lambda -->|Metadata| DynamoDB[💾 DynamoDB<br/>Static Details, Queries, Alerts]
    
    OpenSearch -->|Search Results| Bedrock
    DynamoDB -->|Context| Bedrock
    
    Bedrock -->|Insights & Alerts| Alerts[🔔 Actionable Alerts<br/>Mobile Notifications]
    Alerts -->|Notifications| User
    
    Dashboard -.->|Displays| User
    
    style User fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style Frontend fill:#50C878,stroke:#2E7D4E,stroke-width:2px,color:#fff
    style Bedrock fill:#FF6B6B,stroke:#C44545,stroke-width:2px,color:#fff
    style OpenSearch fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    style DynamoDB fill:#3498DB,stroke:#21618C,stroke-width:2px,color:#fff
    style Kinesis fill:#E67E22,stroke:#A04000,stroke-width:2px,color:#fff
    style Lambda fill:#F39C12,stroke:#B9770E,stroke-width:2px,color:#fff
    style Services fill:#1ABC9C,stroke:#117A65,stroke-width:2px,color:#fff
    style Dashboard fill:#E74C3C,stroke:#A93226,stroke-width:2px,color:#fff
    style Alerts fill:#E91E63,stroke:#AD1457,stroke-width:2px,color:#fff
```

### High-Level Architecture

User → Web Interface → API Gateway → Backend Lambda → AI Services → Log Stores  

Microservices → Kinesis Firehose → Processing Lambda → OpenSearch + DynamoDB  

### Component Architecture

The platform consists of five main subsystems:

1. Web Frontend  
2. API Layer  
3. AI Orchestration Layer  
4. Log Analysis Engine  
5. Dashboard Generation Engine  

---

## Data Flow

### Query Processing Flow

User Query → Frontend → API Gateway → Intent Extraction → Log Retrieval → AI Analysis → Dashboard Generation → Response Display  

### Log Ingestion Flow

Service Logs → Kinesis Firehose → Lambda Processing → Normalization → OpenSearch (logs) + DynamoDB (metadata)  

---

## Components and Interfaces

### 1. Web Frontend

#### Chatbot Interface

**Responsibilities**

- Conversational UI  
- Query submission  
- Display formatted AI responses  
- Maintain conversation context  

#### Dashboard Visualization

**Responsibilities**

- Render dynamically generated dashboards  
- Support multiple chart types  
- Interactive filtering and drill-down  

#### History and Navigation

**Responsibilities**

- Query history display  
- Saved dashboards  
- Navigation to past investigations  

---

### 2. Backend API Layer

#### Query Handler Service

**Responsibilities**

- Validate incoming queries  
- Extract intent using Amazon Bedrock  
- Manage conversation context  
- Route processing pipeline  

#### AI Orchestration Service

**Responsibilities**

- Coordinate Amazon Bedrock and Amazon Q  
- Construct prompts for debugging context  
- Handle service failures and fallbacks  

#### Log Query Service

**Responsibilities**

- Translate intent into OpenSearch queries  
- Execute optimized searches  
- Correlate logs across services  

---

### 3. Dashboard Generation Engine

**Responsibilities**

- Determine optimal visualization types  
- Generate dashboards dynamically  
- Cache generated dashboards  

Supported dashboard types include error analysis, performance metrics, comparisons, and timelines.

---

### 4. Log Processing Pipeline

**Responsibilities**

- Ingest logs from Kinesis Firehose  
- Normalize heterogeneous formats  
- Extract and enrich metadata  
- Store logs in OpenSearch and DynamoDB  

---

### 5. Incident Intelligence Service

**Responsibilities**

- Detect incident patterns  
- Construct incident timelines  
- Identify root causes  
- Track incident history  

---

## Summary

The platform delivers an intent-driven debugging experience by combining scalable log ingestion, AI-powered analysis, and autonomous visualization into a unified cloud-native system.








