import base64
import json
import logging
from google.cloud import bigquery

# Initialize BigQuery Client
PROJECT_ID = "amplified-time-498910-q6"
client = bigquery.Client(project=PROJECT_ID)

def process_live_event(event, context):
    """
    Triggered from a message on a Cloud Pub/Sub topic.
    This function simulates the real-time consumption of streaming events,
    parsing the payload and interfacing with the BQML environment.
    """
    try:
        # 1. Decode the Pub/Sub message
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        payload = json.loads(pubsub_message)
        
        customer_id = payload.get('customerID', 'Unknown')
        monthly_charges = payload.get('MonthlyCharges', 0)
        
        logging.info(f"Received live event for Customer: {customer_id} | Monthly: ${monthly_charges}")
        
        # 2. In a live production environment, this payload would either be:
        #    A) Pushed to a Vertex AI Endpoint for sub-millisecond inference
        #    B) Streamed into a BigQuery table for continuous BQML batch scoring
        
        # Simulating the pipeline routing...
        logging.info(f"Event routed to predictive analytics stream successfully.")
        
    except Exception as e:
        logging.error(f"Failed to process streaming event: {e}")
        raise
