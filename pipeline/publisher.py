import json
import time
import pandas as pd
from google.cloud import pubsub_v1

PROJECT_ID = "amplified-time-498910-q6"
TOPIC_ID = "churn-events-stream"

def simulate_streaming_events(csv_path: str):
    """Reads a CSV and publishes rows as JSON to Pub/Sub to simulate a live stream."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    
    print(f"Starting stream to {topic_path}...")
    
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Iterate and publish
    for index, row in df.iterrows():
        # Convert row to dictionary, handle NaN values
        event_data = row.dropna().to_dict()
        
        # Convert to JSON bytes
        data_str = json.dumps(event_data)
        data_bytes = data_str.encode("utf-8")
        
        # Publish to GCP
        try:
            future = publisher.publish(topic_path, data_bytes)
            print(f"Published event for Customer: {event_data.get('customerID')} | Message ID: {future.result()}")
        except Exception as e:
            print(f"Failed to publish {event_data.get('customerID')}: {e}")
        
        # Sleep to simulate real-time traffic
        time.sleep(0.5)

if __name__ == "__main__":
    # Ensure you have downloaded the Kaggle CSV to your local pipeline directory
    CSV_FILE_PATH = "WA_Fn-UseC_-Telco-Customer-Churn.csv" 
    simulate_streaming_events(CSV_FILE_PATH)