import random
import uuid
import logging
import time
import threading
import os
from datetime import datetime
from opensearchpy import OpenSearch
from queue import Queue
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================
# CONFIG
# =============================

USE_AWS = os.getenv("USE_AWS", "True").lower() == "true"

# Local Elasticsearch config
LOCAL_ES = os.getenv("LOCAL_ES", "http://localhost:9200")
LOCAL_INDEX = os.getenv("LOCAL_INDEX", "upi-transaction-logs")

# AWS OpenSearch config
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL", "")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "logs-index")
OPENSEARCH_USERNAME = os.getenv("OPENSEARCH_USERNAME", "")
OPENSEARCH_PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "")

# Select config based on USE_AWS flag
ES_URL = OPENSEARCH_URL if USE_AWS else LOCAL_ES
INDEX_NAME = OPENSEARCH_INDEX if USE_AWS else LOCAL_INDEX

LOGS_PER_SECOND = int(os.getenv("LOGS_PER_SECOND", "50"))
FAILURE_RATE = float(os.getenv("FAILURE_RATE", "0.4"))

# =============================
# ES CLIENT
# =============================

es = None
log_queue = Queue()

def get_es_client():
    global es
    if es is None:
        if USE_AWS:
            # AWS OpenSearch with authentication
            es = OpenSearch(
                ES_URL,
                http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
                use_ssl=True,
                verify_certs=True,
                ssl_show_warn=False
            )
        else:
            # Local Elasticsearch without authentication
            es = OpenSearch(ES_URL)
    return es

# =============================
# CUSTOM ASYNC LOG HANDLER
# =============================

class ElasticsearchHandler(logging.Handler):
    def emit(self, record):
        try:
            log_line = self.format(record)
            # Add log to queue for processing
            try:
                log_queue.put({
                    "timestamp": datetime.utcnow().isoformat(),
                    "log": log_line,
                    "record": record.__dict__
                })
            except Exception as e:
                print(f"Failed to queue log: {e}")
        except Exception as e:
            print(f"Error in emit: {e}")

def log_worker():
    """Background worker to send logs to OpenSearch"""
    client = get_es_client()
    
    # Test connection and create index if needed
    try:
        # Check if we can connect
        info = client.info()
        print(f"✓ Connected to OpenSearch: {info['version']['number']}")
        
        # Check if index exists, create if not
        if not client.indices.exists(index=INDEX_NAME):
            client.indices.create(
                index=INDEX_NAME,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "log": {"type": "text"}
                        }
                    }
                }
            )
            print(f"✓ Created index: {INDEX_NAME}")
        else:
            print(f"✓ Index exists: {INDEX_NAME}")
    except Exception as e:
        print(f"✗ OpenSearch connection/setup error: {e}")
        print(f"  URL: {ES_URL}")
        print(f"  Index: {INDEX_NAME}")
        return
    
    # Process logs from queue
    while True:
        try:
            log_doc = log_queue.get()
            
            try:
                response = client.index(
                    index=INDEX_NAME,
                    body=log_doc
                )
                # Uncomment for debugging:
                # print(f"✓ Indexed log: {response['_id']}")
            except Exception as e:
                print(f"✗ Failed to index log: {e}")
                
        except Exception as e:
            print(f"✗ Log worker error: {e}")
            time.sleep(1)

# =============================
# LOGGER SETUP
# =============================

logger = logging.getLogger("upi-system")
logger.setLevel(logging.INFO)

log_format = "%(asctime)s | %(levelname)s | %(service)s | txn=%(txn_id)s | state=%(state)s | %(message)s"

formatter = logging.Formatter(log_format)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Elasticsearch handler
es_handler = ElasticsearchHandler()
es_handler.setFormatter(formatter)
logger.addHandler(es_handler)

# =============================
# SIMULATED USERS
# =============================

users = {}
locks = {}

def create_user():
    user_id = str(uuid.uuid4())
    users[user_id] = random.randint(1000, 10000)
    locks[user_id] = threading.Lock()
    return user_id

def random_user():
    if not users:
        return None
    return random.choice(list(users.keys()))

# =============================
# FAILURE REASONS
# =============================

infra_failures = [
    "DB_CONNECTION_TIMEOUT",
    "DOWNSTREAM_500",
    "REDIS_CLUSTER_UNAVAILABLE",
    "NETWORK_TIMEOUT"
]

business_failures = [
    "INSUFFICIENT_FUNDS",
    "ACCOUNT_BLOCKED",
    "USER_NOT_FOUND",
    "LIMIT_EXCEEDED"
]

# =============================
# UPI TRANSACTION FLOW
# =============================

UPI_STATES = [
    ("payer-psp", "PAYER_PSP"),
    ("remitter-bank", "REMITTER_BANK"),
    ("npci-switch", "NPCI_SWITCH"),
    ("beneficiary-bank", "BENEFICIARY_BANK"),
    ("payee-psp", "PAYEE_PSP"),
]

def simulate_transaction():
    txn_id = str(uuid.uuid4())
    trace_id = str(uuid.uuid4())
    sender = random_user()
    receiver = random_user()
    amount = random.randint(1, 5000)

    if not sender or not receiver or sender == receiver:
        return

    will_fail = random.random() < FAILURE_RATE
    fail_state_index = random.randint(0, 4) if will_fail else None

    for idx, (service, state) in enumerate(UPI_STATES):

        time.sleep(random.uniform(0.05, 0.15))

        # Simulate latency
        latency = random.randint(10, 300)

        # Inject failure at chosen state
        if will_fail and idx == fail_state_index:
            reason = random.choice(infra_failures + business_failures)

            logger.error(
                f"Transaction failed due to {reason}",
                extra={
                    "service": service,
                    "trace_id": trace_id,
                    "txn_id": txn_id,
                    "state": state,
                    "latency_ms": latency,
                },
            )
            return

        # Business logic at REMITTER_BANK
        if state == "REMITTER_BANK":
            with locks[sender]:
                if users[sender] < amount:
                    logger.warning(
                        "Transaction failed - insufficient funds",
                        extra={
                            "service": service,
                            "trace_id": trace_id,
                            "txn_id": txn_id,
                            "state": state,
                            "latency_ms": latency,
                        },
                    )
                    return
                users[sender] -= amount

        if state == "BENEFICIARY_BANK":
            with locks[receiver]:
                users[receiver] += amount

        logger.info(
            "Transaction processed successfully at this state",
            extra={
                "service": service,
                "trace_id": trace_id,
                "txn_id": txn_id,
                "state": state,
                "latency_ms": latency,
            },
        )

    logger.info(
        "Transaction completed SUCCESSFULLY",
        extra={
            "service": "upi-orchestrator",
            "trace_id": trace_id,
            "txn_id": txn_id,
            "state": "COMPLETED",
            "latency_ms": random.randint(200, 800),
        },
    )

# =============================
# ACCOUNT CREATION
# =============================

def simulate_account_creation():
    user_id = create_user()
    logger.info(
        f"Account created for user {user_id}",
        extra={
            "service": "user-service",
            "txn_id": None,
            "state": "ACCOUNT_CREATED",
            "trace_id": str(uuid.uuid4()),
            "latency_ms": random.randint(20, 80),
        },
    )

# =============================
# GENERATOR LOOP
# =============================

def generate_logs():
    # create some initial users
    for _ in range(20):
        create_user()

    while True:
        threads = []

        for _ in range(LOGS_PER_SECOND):
            action = random.choice(["txn", "create"])

            if action == "txn":
                thread = threading.Thread(target=simulate_transaction)
            else:
                thread = threading.Thread(target=simulate_account_creation)
            
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        
        time.sleep(1)

# =============================
# MAIN
# =============================

def main():
    print("Starting realistic UPI log simulator...")
    print(f"Target: {'AWS OpenSearch' if USE_AWS else 'Local Elasticsearch'}")
    print(f"URL: {ES_URL}")
    print(f"Index: {INDEX_NAME}")
    print("-" * 60)
    
    # Start the log worker in background thread
    worker_thread = threading.Thread(target=log_worker, daemon=True)
    worker_thread.start()
    
    try:
        generate_logs()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if es is not None:
            es.close()
            print("✓ Closed OpenSearch connection")

if __name__ == "__main__":
    main()