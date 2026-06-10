"""
main.py — Cloud Function (Pub/Sub trigger)
Receives a customer event from Pub/Sub, loads the trained XGBoost model
from a local artifact, and writes the churn prediction to BigQuery.
"""

import json
import base64
import os
import joblib
import numpy as np
from datetime import datetime, timezone
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATASET_ID = os.environ.get("BQ_DATASET", "churn_dataset")

# Load model artifacts at cold-start (outside handler for reuse across invocations)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "churn_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "feature_columns.joblib")

model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)

bq_client = bigquery.Client(project=PROJECT_ID)

def predict_churn(event, context):
    # Decode Pub/Sub message
    raw = base64.b64decode(event["data"]).decode("utf-8")
    customer = json.loads(raw)

    customer_id = customer.get("customerid", "UNKNOWN")

    try:
        # Build feature vector in the same order as training
        feature_map = {
            "SeniorCitizen": int(customer.get("seniorcitizen", 0)),
            "Partner": 1 if customer.get("partner") == "Yes" else 0,
            "Dependents": 1 if customer.get("dependents") == "Yes" else 0,
            "tenure": int(customer.get("tenure", 0)),
            "PhoneService": 1 if customer.get("phoneservice") == "Yes" else 0,
            "MultipleLines": 1 if customer.get("multiplelines") == "Yes" else 0,
            "OnlineSecurity": 1 if customer.get("onlinesecurity") == "Yes" else 0,
            "OnlineBackup": 1 if customer.get("onlinebackup") == "Yes" else 0,
            "DeviceProtection": 1 if customer.get("deviceprotection") == "Yes" else 0,
            "TechSupport": 1 if customer.get("techsupport") == "Yes" else 0,
            "StreamingTV": 1 if customer.get("streamingtv") == "Yes" else 0,
            "StreamingMovies": 1 if customer.get("streamingmovies") == "Yes" else 0,
            "PaperlessBilling": 1 if customer.get("paperlessbilling") == "Yes" else 0,
            "MonthlyCharges": float(customer.get("monthlycharges", 0)),
            "TotalCharges": float(customer.get("totalcharges") or 0),
            "gender": 1 if customer.get("gender") == "Male" else 0,
            "InternetService": {"DSL": 0, "Fiber optic": 1, "No": 2}.get(
                customer.get("internetservice", "No"), 2),
            "Contract": {"Month-to-month": 0, "One year": 1, "Two year": 2}.get(
                customer.get("contract", "Month-to-month"), 0),
            "PaymentMethod": {
                "Bank transfer (automatic)": 0,
                "Credit card (automatic)": 1,
                "Electronic check": 2,
                "Mailed check": 3
            }.get(customer.get("paymentmethod", "Electronic check"), 2),
            "charge_per_tenure": float(customer.get("monthlycharges", 0)) / 
                                  (int(customer.get("tenure", 0)) + 1),
            "tenure_bucket": min(int(customer.get("tenure", 0)) // 12, 3),
        }

        # Align to training column order
        input_vector = np.array([[feature_map[col] for col in feature_columns]])

        churn_prob = float(model.predict_proba(input_vector)[0][1])

        risk_tier = "HIGH" if churn_prob >= 0.70 else "MEDIUM" if churn_prob >= 0.40 else "LOW"

        # Write prediction to BigQuery
        errors = bq_client.insert_rows_json(
            f"{PROJECT_ID}.{DATASET_ID}.predictions",
            [{
                "customerid": customer_id,
                "churn_probability": churn_prob,
                "risk_tier": risk_tier,
                "predicted_at": datetime.now(timezone.utc).isoformat(),
            }]
        )

        if errors:
            print(f"BigQuery insert error for {customer_id}: {errors}")
        else:
            print(f"{customer_id} → {churn_prob:.2%} ({risk_tier})")

    except Exception as e:
        print(f"Prediction failed for {customer_id}: {e}")
        raise
