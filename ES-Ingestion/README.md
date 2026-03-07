# UPI Transaction Log Simulator

A high-performance asynchronous log simulator for realistic UPI (Unified Payments Interface) transaction flows, designed for testing and development of log analysis systems, monitoring dashboards, and observability platforms.

## 🎯 Overview

This project simulates realistic UPI transaction logs with:
- Multi-stage transaction lifecycle (Payer PSP → Remitter Bank → NPCI Switch → Beneficiary Bank → Payee PSP)
- Infrastructure and business logic failure scenarios
- Configurable failure rates and throughput
- Support for both local Elasticsearch and AWS OpenSearch
- Async/parallel processing for high-volume log generation

## 🏗️ Architecture

### Transaction Flow
```
PAYER_PSP → REMITTER_BANK → NPCI_SWITCH → BENEFICIARY_BANK → PAYEE_PSP
```

Each transaction includes:
- Unique transaction ID (`txn_id`)
- Distributed trace ID (`trace_id`)
- Service-specific latency metrics
- State transitions with timestamps
- Success/failure status with detailed error codes

### Failure Scenarios

**Infrastructure Failures:**
- `DB_CONNECTION_TIMEOUT`
- `DOWNSTREAM_500`
- `REDIS_CLUSTER_UNAVAILABLE`
- `NETWORK_TIMEOUT`

**Business Failures:**
- `INSUFFICIENT_FUNDS`
- `ACCOUNT_BLOCKED`
- `USER_NOT_FOUND`
- `LIMIT_EXCEEDED`

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose (for local Elasticsearch)
- AWS OpenSearch domain (optional, for cloud deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai4Bharat_Private
pip install -r requirements.txt
```

### 2. Choose Your Backend

#### Option A: Local Elasticsearch

```bash
# Start local Elasticsearch
docker-compose up -d

# Verify Elasticsearch is running
curl http://localhost:9200
```

Edit `log_simulator.py`:
```python
USE_AWS = False
```

#### Option B: AWS OpenSearch

Edit `log_simulator.py`:
```python
USE_AWS = True
OPENSEARCH_URL = "https://<your-opensearch-domain>.es.amazonaws.com"
OPENSEARCH_USERNAME = "admin"
OPENSEARCH_PASSWORD = "<your-password>"
```

### 3. Run the Simulator

```bash
python log_simulator.py
```

Expected output:
```
Starting realistic UPI log simulator...
2026-03-02 10:15:23,456 | INFO | payer-psp | txn=abc123... | state=PAYER_PSP | Transaction processed successfully
2026-03-02 10:15:23,567 | INFO | remitter-bank | txn=abc123... | state=REMITTER_BANK | Transaction processed successfully
...
```

## ⚙️ Configuration

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `LOGS_PER_SECOND` | 50 | Number of transactions/logs generated per second |
| `FAILURE_RATE` | 0.4 | Probability of transaction failure (0.0 - 1.0) |
| `USE_AWS` | True | Use AWS OpenSearch (True) or local ES (False) |

### Adjusting Load

```python
# Low load (testing)
LOGS_PER_SECOND = 10
FAILURE_RATE = 0.2

# High load (stress testing)
LOGS_PER_SECOND = 100
FAILURE_RATE = 0.5
```

## 🔍 Querying Logs

### Local Elasticsearch Queries

```bash
# Make scripts executable
chmod +x query.sh

# Run queries
./query.sh
```

**Example queries included:**
1. Search all ERROR logs
2. Search ERROR logs from REMITTER_BANK
3. Search by specific transaction ID
4. Wildcard search for transaction patterns

### AWS OpenSearch Queries

```bash
# Update credentials in query_aws.sh first
chmod +x query_aws.sh

# Run queries
./query_aws.sh
```

### Sample Queries

**Find all failed transactions:**
```bash
curl -X GET "http://localhost:9200/upi-transaction-logs/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match": {
      "log": "ERROR"
    }
  }
}'
```

**Trace a specific transaction:**
```bash
curl -X GET "http://localhost:9200/upi-transaction-logs/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match_phrase": {
      "log": "txn=<transaction-id>"
    }
  }
}'
```

## 📊 Use Cases

1. **Testing Log Analytics Platforms**: Generate realistic UPI transaction data for testing log aggregation and analysis tools
2. **Developing Monitoring Dashboards**: Create visualizations for transaction success rates, latency, and failure patterns
3. **Training ML Models**: Generate labeled data for anomaly detection and fraud detection systems
4. **Load Testing**: Stress test Elasticsearch/OpenSearch clusters with high-volume log ingestion
5. **Observability Demos**: Demonstrate distributed tracing and transaction monitoring

## 🗂️ Project Structure

```
.
├── docker-compose.yml       # Local Elasticsearch setup
├── log_simulator.py         # Main simulator script
├── query.sh                 # Local Elasticsearch query examples
├── query_aws.sh            # AWS OpenSearch query examples
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📦 Dependencies

```
elasticsearch==8.11.1       # Elasticsearch Python client
aiohttp                     # Async HTTP client
asyncio                     # Async I/O library
python-dotenv              # Environment variable management
uuid                        # UUID generation
```

## 🛠️ Customization

### Adding New Failure Types

```python
custom_failures = [
    "MERCHANT_NOT_FOUND",
    "INVALID_VPA",
    "TRANSACTION_EXPIRED"
]

# Add to existing failure lists
business_failures.extend(custom_failures)
```

### Modifying Transaction Flow

```python
# Add new stages to the UPI flow
UPI_STATES = [
    ("payer-psp", "PAYER_PSP"),
    ("anti-fraud", "ANTI_FRAUD_CHECK"),  # New stage
    ("remitter-bank", "REMITTER_BANK"),
    # ... rest of the flow
]
```

## 🔒 Security Notes

⚠️ **Important:** The current code contains hardcoded credentials. Before deploying:

1. Move sensitive credentials to environment variables:
   ```bash
   export OPENSEARCH_USERNAME="admin"
   export OPENSEARCH_PASSWORD="your-secure-password"
   ```

2. Use `.env` file with `python-dotenv`:
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD")
   ```

3. Never commit credentials to version control

## 📈 Performance

- **Throughput**: Up to 100+ logs/second with async processing
- **Latency**: Simulated latencies between 10-300ms per stage
- **Concurrency**: Async/await pattern for parallel transaction processing

## 🐛 Troubleshooting

**Connection refused to Elasticsearch:**
```bash
# Check if container is running
docker ps

# Check logs
docker logs es-local
```

**AWS OpenSearch authentication errors:**
- Verify credentials are correct
- Check security group allows your IP
- Ensure fine-grained access control settings

**Memory issues:**
- Reduce `LOGS_PER_SECOND`
- Increase Docker memory allocation
- Adjust ES heap size: `ES_JAVA_OPTS=-Xms2g -Xmx2g`

## 📄 License

[Add your license information here]

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Contact

[Add your contact information here]
