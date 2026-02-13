# AI-Powered Debugging Platform  
### Intent-Driven Observability for Distributed Systems

## 🚀 Overview

Modern distributed systems generate massive volumes of logs across multiple services, making debugging slow, fragmented, and heavily dependent on manual queries and dashboards.

**This project solves that problem.**

We built an AI-powered observability platform that allows developers and IT teams to debug complex systems using natural language — just by asking questions.

Instead of switching between dashboards or writing complex queries, users can simply ask:

> “At what stage did TRX_A2DC fail?”  
> “How many DB thread pool errors occurred last week?”  

The system automatically analyzes logs, correlates events across services, generates dynamic dashboards, and identifies root causes.

This solution directly addresses the hackathon challenge of helping people work smarter and become more productive while building or understanding technology.

---

## 🧠 Problem Statement

Debugging distributed systems today involves:

- Jumping across multiple monitoring tools  
- Writing structured queries (KQL, SQL, etc.)  
- Manually correlating logs across services  
- Spending hours identifying root causes  

This slows down teams and delays incident resolution.

---

## 💡 Our Solution

An **AI-driven conversational debugging interface** that:

- Understands natural language queries
- Extracts debugging intent
- Searches and correlates logs automatically
- Generates dynamic dashboards on demand
- Provides root cause analysis and fix suggestions

The platform transforms observability from **metric-driven monitoring** to **intent-driven investigation**.

---

## ⭐ Key Features

### 🤖 AI Chat-Based Debugging Assistant
Interact with system logs through a conversational interface powered by AI.

### 🔍 Root Cause Analysis & Fix Suggestions
Automatically identifies failure points and suggests actionable remediation steps.

### 📊 Dynamic Log Visualization
Dashboards are generated automatically based on query context — no manual setup required.

### ⏱️ Time-Based Incident Tracking
Correlates errors with deployments, configuration changes, or traffic spikes.

### 🧾 Log Summarization
Large volumes of logs are condensed into concise explanations for faster understanding.

---

## 🧬 Unique Selling Proposition

- **Intent-Driven Observability** instead of metric-driven monitoring  
- **Zero Query Language Dependency**  
- **Self-Adapting Dashboards per Query**  
- **Service-Agnostic & Cloud-Native Architecture**  

---

## 🏗️ Architecture Overview

### Workflow

1. User submits a natural language query
2. AI extracts intent using Amazon Bedrock
3. Relevant logs are retrieved from OpenSearch
4. Amazon Q analyzes logs for insights
5. Dynamic dashboards are generated
6. Root cause and recommendations are returned

### Log Pipeline

Service Logs → Kinesis Firehose → Lambda Processing →  
Normalization → OpenSearch + DynamoDB → AI Analysis

---

## 🛠️ Technology Stack

**Frontend**
- React + TypeScript  
- AWS Amplify  

**Backend**
- Flask on AWS Lambda  
- API Gateway  

**AI & Intelligence**
- Amazon Bedrock  
- Amazon Q  

**Data & Logs**
- Amazon OpenSearch  
- DynamoDB  
- Kinesis Firehose  

**Authentication**
- AWS Cognito  

---

## 🎯 Use Cases

- Debugging distributed microservices  
- Incident investigation  
- Performance bottleneck analysis  
- Deployment issue correlation  
- Operational analytics  

---

## 💰 Estimated Implementation Cost

Approximate monthly infrastructure cost for a medium-scale deployment:

| Service | Estimated Monthly Cost |
|--------|------------------------|
Amazon Bedrock | $180  
OpenSearch | $120  
Lambda | $12  
Kinesis Firehose | $35  
DynamoDB | $15  
Amplify Hosting | $20  

**Total ≈ $382/month**

---

## 🌍 Impact

By removing the need for manual queries and fragmented dashboards, this platform:
- Integration with Amazon Q
- Reduces debugging time  
- Improsves productivity of engineering teams  
- Enables faster incident resolution  
- Makes observability accessible to non-experts  

---

## 🔮 Future Scope

- Predictive incident detection  
- Automated remediation workflows  
- Multi-region deployment  
- Integration with CI/CD pipelines  
- Proactive alerts based on anomaly detection  

---

## 👥 Team

**Team Name:** Beff Jezos  
**Team Leader:** Hiten Sirwani  
**Team Members** Soham Yedgaonkar, Arya Pathak, Atharva Deshpande, Hiten Sirwani

---

## 🏁 Conclusion

This project reimagines debugging as a conversation rather than a manual investigation process.

By combining AI reasoning, log analytics, and autonomous visualization, the platform enables teams to understand complex systems faster and with far less effort.

---

