# Smart Customer Churn Intelligence Platform (GCP)

**Problem Statement:** A SaaS telecommunications provider was experiencing a ~26% annual customer churn rate with no early-warning detection system. 

**Solution:** This platform ingests customer usage events in real-time via Pub/Sub, engineers churn-predictive features defensively in BigQuery, and utilizes a BQML XGBoost classifier to score customers 30 days prior to predicted churn. This enables proactive, targeted retention campaigns via a live operational dashboard.

## 🔗 Live Interactive Assets
- **Production Dashboard:** [View Live Looker Studio Executive Dashboard](https://datastudio.google.com/u/0/reporting/c06e5abd-8846-48aa-8c31-2b1c29d90237/page/Jgj0F)

## 🏗️ Architecture Overview
`![Architecture Diagram](image_50b2db.png)`

- **Ingestion & Streaming:** Google Cloud Pub/Sub (simulated via Python publisher)
- **Data Warehouse Engine:** Google Cloud BigQuery 
- **Feature Engineering Layer:** Optimized SQL Views utilizing defensive ELT patterns
- **Machine Learning Core:** BigQuery ML (BQML) distributed XGBoost Engine
- **Business Intelligence:** Interactive Executive Dashboard via Looker Studio

## 📁 Repository Structure
```text
├── pipeline/
│   ├── publisher.py          # Streams live events to Pub/Sub
│   ├── bigquery_setup.py     # Programmatic IaC for BQ resources
│   └── requirements.txt      # Python dependencies
├── sql/
│   ├── 1_feature_engineering.sql # ELT, casting, missing value handling
│   ├── 2_model_training.sql      # BQML BOOSTED_TREE_CLASSIFIER logic
│   └── 3_batch_predictions.sql   # Batch inference routines
├── functions/
│   └── predict/              # (WIP) Real-time scoring trigger
└── README.md
