# 🚀 LogSense AI
### AI-Powered Observability & Debugging Platform for Distributed Systems

![Hackathon](https://img.shields.io/badge/Built%20for-Hackathon-orange)
![AI Powered](https://img.shields.io/badge/AI-Amazon%20Bedrock-purple)
![Status](https://img.shields.io/badge/Status-Prototype-success)

LogSense AI is an **AI-powered observability and debugging platform** designed to help developers investigate complex distributed systems using **natural language queries**.

Instead of manually searching logs or writing complex queries, developers can simply **ask questions about system behavior**, and the platform will automatically analyze logs, identify issues, and generate actionable insights.

> ⚡ Transform debugging from **manual investigation → conversational observability**

---

# 🌐 Live Project

🔗 **Project URL**

```
[http://100.48.76.239/]
```

---

# 🎥 Demo Videos

## 🧪 Product Prototype Demo

*(Add your product demo video here)*

[![Watch the Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)

---

## 🏗️ Architecture Explanation Video

*(Add your architecture explanation video here)*

[![Watch the Architecture Video](https://img.youtube.com/vi/AtXVfOwmeBE/maxresdefault.jpg)](https://youtu.be/AtXVfOwmeBE)

---

# 📸 Screenshots

## Dashboard Overview

![Dashboard Screenshot](./screenshots/dashboard.png)

---

## AI Debugging Chat Interface

![AI Chat Screenshot](./screenshots/chat-interface.png)

---

## Alert Monitoring System

![Alerts Screenshot](./screenshots/alerts-dashboard.png)

---

## Log Analysis Interface

![Logs Screenshot](./screenshots/log-analysis.png)

---

# 🏗️ System Architecture

![Architecture Diagram](./architecture/architecture-diagram.png)

---

# 🧠 Problem Statement

Modern distributed systems generate **massive volumes of logs across microservices**, making debugging slow and complicated.

Engineers often need to:

- Switch between multiple monitoring tools  
- Write complex queries (SQL, KQL, etc.)  
- Manually correlate logs across services  
- Spend hours identifying root causes  

This slows down incident response and affects system reliability.

---

# 💡 Our Solution

LogSense AI introduces **Intent-Driven Observability**.

Instead of dashboards and query languages, developers simply **ask questions**.

Example queries:

> “At what stage did transaction TRX_A2DC fail?”  
> “How many DB thread pool errors occurred last week?”

The system automatically:

1. Understands the query intent  
2. Searches and correlates relevant logs  
3. Identifies anomalies and failures  
4. Generates dashboards dynamically  
5. Suggests possible fixes  

---

# ⭐ Key Features

### 🤖 AI Chat-Based Debugging
Interact with system logs through a conversational interface.

### 🔍 Automated Root Cause Analysis
Detects failure points and provides possible remediation suggestions.

### 📊 Dynamic Dashboard Generation
Dashboards are automatically generated based on the context of the query.

### 🧾 Log Summarization
Large volumes of logs are condensed into clear explanations.

### ⏱️ Incident Timeline Tracking
Correlates system issues with deployments, configuration changes, or traffic spikes.

### 🚨 Intelligent Alert System
Monitor system health through customizable alert thresholds.

---

# 🧬 Unique Selling Proposition

LogSense AI introduces a new paradigm called:

## **Intent-Driven Observability**

Key differentiators:

- Natural language debugging
- No query language required
- AI-generated dashboards
- Cross-service log correlation
- Cloud-native architecture

---

# ⚙️ Architecture Overview

### System Workflow

**1️⃣ User Query**

Developers ask debugging questions through the web interface.

**2️⃣ Log Ingestion**

Logs from distributed services are streamed into:

Amazon Kinesis Firehose

**3️⃣ Log Processing**

AWS Lambda processes incoming logs by:

- Parsing log structures
- Normalizing log formats
- Enriching metadata
- Categorizing by service and severity

**4️⃣ Log Storage**

Processed logs are stored in:

- Amazon OpenSearch for fast search
- DynamoDB for metadata indexing

**5️⃣ AI Analysis**

Amazon Bedrock interprets user queries and retrieves relevant logs.

**6️⃣ Insight Generation**

The platform generates:

- Root cause analysis
- Incident timelines
- Dynamic dashboards
- Fix recommendations

---

### Log Pipeline

```
Service Logs
   ↓
Kinesis Firehose
   ↓
AWS Lambda Processing
   ↓
Log Normalization
   ↓
OpenSearch + DynamoDB
   ↓
AI Analysis (Amazon Bedrock)
   ↓
Dynamic Insights & Dashboards
```

---

# 🛠️ Tech Stack

## Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn-ui

## Backend
- FastAPI
- AWS Lambda
- API Gateway

## AI & Intelligence
- Amazon Bedrock

## Data & Observability
- Amazon OpenSearch
- DynamoDB
- Kinesis Firehose

## Authentication
- AWS Cognito

## Deployment
- AWS Amplify
## Mobile(Call/Mssgs) Alerts System
- Twilio 
---

# 📂 Project Setup

Clone the repository:

```bash
git clone <YOUR_GIT_URL>
```

Navigate to the project folder:

```bash
cd <PROJECT_NAME>
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

---

# 🎯 Use Cases

LogSense AI can be used for:

- Debugging distributed microservices
- Incident investigation
- Performance bottleneck detection
- Deployment issue tracking
- Operational analytics

---

# 💰 Estimated Infrastructure Cost

| Service | Estimated Monthly Cost |
|--------|-----------------------|
| Amazon Bedrock | $180 |
| OpenSearch | $120 |
| Lambda | $12 |
| Kinesis Firehose | $35 |
| DynamoDB | $15 |
| Amplify Hosting | $20 |

**Total Estimated Cost:** ~$382/month

---

# 🌍 Impact

LogSense AI helps organizations:

- Reduce debugging time
- Improve developer productivity
- Accelerate incident resolution
- Make observability accessible to non-experts

---

# 🔮 Future Scope

Planned improvements include:

- Planned integration with Amazon Q to deliver AI-assisted debugging directly within the AWS ecosystem.
- Predictive incident detection
- Automated remediation workflows
- AI anomaly detection
- CI/CD integration
- Multi-region scalability

---

# 👥 Team

**Team Name:** Beff Jezos

**Team Leader**  
Hiten Sirwani  

**Team Members**

- Soham Yedgaonkar  
- Arya Pathak  
- Atharva Deshpande  
- Hiten Sirwani  

---

# 🏁 Conclusion

LogSense AI transforms debugging from a **manual investigation process** into a **conversational AI-powered experience**.

By combining **AI reasoning, log analytics, and automated visualization**, the platform enables teams to understand complex systems faster and resolve incidents more efficiently.


