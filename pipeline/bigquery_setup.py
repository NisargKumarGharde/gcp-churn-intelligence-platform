import os
from google.cloud import bigquery

# Initialize the BigQuery Client
# Note: Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
PROJECT_ID = "amplified-time-498910-q6"
client = bigquery.Client(project=PROJECT_ID)

DATASET_ID = f"{PROJECT_ID}.raw_events"

def create_dataset():
    """Creates a BigQuery dataset programmatically."""
    dataset = bigquery.Dataset(DATASET_ID)
    dataset.location = "US"
    
    try:
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {client.project}.{dataset.dataset_id}")
    except Exception as e:
        print(f"Dataset creation skipped/failed: {e}")

if __name__ == "__main__":
    print("Initializing GCP BigQuery Infrastructure...")
    create_dataset()
    print("Infrastructure ready for ELT pipeline.")