# Model Artifacts

The trained model artifacts (`churn_model.joblib`, `feature_columns.joblib`)
are not committed to this repository as they are binary files.

## Regenerating the model
Run `notebooks/01_eda_and_training.ipynb` in Google Colab end-to-end.
Artifacts will be saved locally and can be loaded by the Cloud Function.

## Production deployment note
In a production setup, these artifacts would be uploaded to Cloud Storage:
`gs://<bucket>/churn_model.joblib`
and loaded by the Cloud Function at cold-start via `google-cloud-storage`.
This project uses local artifact loading to remain within GCP free tier.
