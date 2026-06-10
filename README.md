# Smart Customer Churn Intelligence Platform (GCP)

An end-to-end data warehousing and machine learning platform built completely within Google Cloud to predict customer flight risk and deliver actionable analytics to retention operations.

## 🔗 Live Interactive Assets
- **Production Dashboard:** [View Live Looker Studio Dashboard](https://datastudio.google.com/u/0/reporting/c06e5abd-8846-48aa-8c31-2b1c29d90237/page/Jgj0F)

## 🏗️ Architecture Overview
- **Data Warehouse Engine:** Google Cloud BigQuery (Serverless execution environment)
- **Feature Engineering Layer:** Optimized SQL Views utilizing defensive ELT patterns
- **Machine Learning Core:** BigQuery ML (BQML) distributed XGBoost Engine
- **Business Intelligence Reporting:** Interactive Executive Dashboard via Looker Studio

## 📁 Repository Structure
- `scripts/1_feature_engineering.sql`: Contains pipeline logic executing data cleansing, type casting, missing value handling, and dynamic tenure bucket generation.
- `scripts/2_model_training.sql`: Configures and invokes the `BOOSTED_TREE_CLASSIFIER` execution routine, holding back validation cohorts automatically via `AUTO_SPLIT`.
- `scripts/3_batch_predictions.sql`: Runs batch inference routines to append predictive probabilities alongside historical tenure scales.

## 🚀 Key Engineering Showcases
1. **Defensive Data Parsing:** Addressed empty string records (`' '`) natively within the source telemetry pipeline using SQL conditional strategies (`NULLIF(TRIM(TotalCharges), '')`) to ensure safe numerical evaluation.
2. **In-Place Distributed Machine Learning:** Completely bypassed massive local resource demands by delegating tree-based execution models directly to BigQuery's columnar storage layers.
3. **Actionable Operational Outputs:** Converted raw mathematical prediction probability distributions into high-risk cohort matrices to facilitate immediate real-world retention campaigns.
