#!/bin/bash

# AWS OpenSearch Query Scripts
# Load environment variables from .env file

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

OPENSEARCH_URL="${OPENSEARCH_URL}"
INDEX="${OPENSEARCH_INDEX:-logs-index}"
USERNAME="${OPENSEARCH_USERNAME}"
PASSWORD="${OPENSEARCH_PASSWORD}"

# Query 1: Search for ERROR logs
echo "=== Query 1: Search for ERROR logs ==="
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_search?pretty" \
-u "${USERNAME}:${PASSWORD}" \
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
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_search?pretty" \
-u "${USERNAME}:${PASSWORD}" \
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

# Query 3: Search by specific transaction ID (exact phrase)
echo "=== Query 3: Search by specific transaction ID ==="
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_search?pretty" \
-u "${USERNAME}:${PASSWORD}" \
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
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_search?pretty" \
-u "${USERNAME}:${PASSWORD}" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "wildcard": {
      "log.keyword": "*txn=3cb0ec6e*"
    }
  }
}'

echo -e "\n\n"

# Query 5: Get all documents (limit 10)
echo "=== Query 5: Get all documents (limit 10) ==="
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_search?pretty" \
-u "${USERNAME}:${PASSWORD}" \
-H "Content-Type: application/json" \
-d '{
  "size": 10,
  "query": {
    "match_all": {}
  }
}'

echo -e "\n\n"

# Query 6: Check index mapping
echo "=== Query 6: Check index mapping ==="
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_mapping?pretty" \
-u "${USERNAME}:${PASSWORD}"

echo -e "\n\n"

# Query 7: Count total documents
echo "=== Query 7: Count total documents ==="
curl -X GET "${OPENSEARCH_URL}/${INDEX}/_count?pretty" \
-u "${USERNAME}:${PASSWORD}"
