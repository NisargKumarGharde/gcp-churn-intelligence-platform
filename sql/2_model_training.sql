CREATE OR REPLACE MODEL `amplified-time-498910-q6.raw_events.churn_xgboost_model`
OPTIONS(
  model_type='BOOSTED_TREE_CLASSIFIER',
  input_label_cols=['target_churn'],
  data_split_method='AUTO_SPLIT', 
  max_iterations=50
) AS
SELECT
  * EXCEPT(customerID)
FROM
  `amplified-time-498910-q6.raw_events.churn_features`
WHERE target_churn IS NOT NULL;
