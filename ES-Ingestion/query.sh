#!/bin/bash

# Local Elasticsearch Query Scripts
# Load environment variables from .env file

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

LOCAL_URL="${LOCAL_ES:-http://localhost:9200}"
INDEX="${LOCAL_INDEX:-upi-transaction-logs}"

# Query 1: Search for ERROR logs
echo "=== Query 1: Search for ERROR logs ==="
curl -X GET "${LOCAL_URL}/${INDEX}/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match": {
      "log": "ERROR"
    }
  }
}'

echo -e "\n\n"

# Query 2: Search for ERROR logs from REMITTER_BANK
echo "=== Query 2: Search for ERROR logs from REMITTER_BANK ==="
curl -X GET "${LOCAL_URL}/${INDEX}/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "bool": {
      "must": [
        { "match": { "log": "ERROR" }},
        { "match": { "log": "REMITTER_BANK" }}
      ]
    }
  }
}'

echo -e "\n\n"

# Query 3: Search by specific transaction ID
echo "=== Query 3: Search by specific transaction ID ==="
curl -X GET "${LOCAL_URL}/${INDEX}/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match_phrase": {
      "log": "txn=3cb0ec6e-dcc7-4c5e-9427-2f68546751e4"
    }
  }
}'

echo -e "\n\n"

# Query 4: Wildcard search for transaction ID
echo "=== Query 4: Wildcard search for transaction ID ==="
curl -X GET "${LOCAL_URL}/${INDEX}/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "wildcard": {
      "log.keyword": "*txn=3cb0ec6e*"
    }
  }
}'

echo -e "\n\n"

# Query 5: Count total documents
echo "=== Query 5: Count total documents ==="
curl -X GET "${LOCAL_URL}/${INDEX}/_count?pretty"