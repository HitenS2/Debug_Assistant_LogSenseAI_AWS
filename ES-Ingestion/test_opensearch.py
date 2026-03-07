#!/usr/bin/env python3
"""
Simple script to test OpenSearch connection and publish test documents
"""
import asyncio
import os
from datetime import datetime
from opensearchpy import AsyncOpenSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenSearch Configuration
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL", "")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", "")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "")
INDEX_NAME = os.getenv("OPENSEARCH_INDEX", "logs-index")


async def test_opensearch():
    """Test OpenSearch connection and publish sample documents"""
    
    print("=" * 60)
    print("OpenSearch Connection Test")
    print("=" * 60)
    print(f"URL: {OPENSEARCH_URL}")
    print(f"Index: {INDEX_NAME}")
    print()
    
    # Create client
    client = AsyncOpenSearch(
        OPENSEARCH_URL,
        http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=True,
        ssl_show_warn=False
    )
    
    try:
        # Step 1: Test connection
        print("Step 1: Testing connection...")
        info = await client.info()
        print(f"✓ Connected successfully!")
        print(f"  Cluster: {info['cluster_name']}")
        print(f"  Version: {info['version']['number']}")
        print()
        
        # Step 2: Check if index exists
        print("Step 2: Checking index...")
        index_exists = await client.indices.exists(index=INDEX_NAME)
        
        if index_exists:
            print(f"✓ Index '{INDEX_NAME}' already exists")
        else:
            print(f"  Index '{INDEX_NAME}' doesn't exist, creating...")
            await client.indices.create(
                index=INDEX_NAME,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "message": {"type": "text"},
                            "level": {"type": "keyword"},
                            "source": {"type": "keyword"}
                        }
                    }
                }
            )
            print(f"✓ Created index '{INDEX_NAME}'")
        print()
        
        # Step 3: Publish test documents
        print("Step 3: Publishing test documents...")
        
        test_docs = [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Test log entry #1",
                "level": "INFO",
                "source": "test_script"
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Test log entry #2",
                "level": "WARNING",
                "source": "test_script"
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Test log entry #3",
                "level": "ERROR",
                "source": "test_script"
            }
        ]
        
        for i, doc in enumerate(test_docs, 1):
            response = await client.index(
                index=INDEX_NAME,
                body=doc
            )
            print(f"✓ Published document #{i} - ID: {response['_id']}")
        
        print()
        
        # Step 4: Verify documents were indexed
        print("Step 4: Verifying documents...")
        await asyncio.sleep(1)  # Wait for indexing
        
        search_result = await client.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "match": {
                        "source": "test_script"
                    }
                },
                "size": 10,
                "sort": [{"timestamp": {"order": "desc"}}]
            }
        )
        
        hits = search_result['hits']['total']['value']
        print(f"✓ Found {hits} documents in index")
        print()
        
        if hits > 0:
            print("Recent documents:")
            for hit in search_result['hits']['hits'][:3]:
                doc = hit['_source']
                print(f"  - [{doc['level']}] {doc['message']}")
        
        print()
        print("=" * 60)
        print("✓ All tests passed! OpenSearch is working correctly.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"\nConnection failed. Please check:")
        print("  1. OpenSearch URL is correct")
        print("  2. Credentials are valid")
        print("  3. Network connectivity")
        print("  4. Security group allows your IP")
        
    finally:
        await client.close()
        print("\n✓ Connection closed")


if __name__ == "__main__":
    asyncio.run(test_opensearch())
