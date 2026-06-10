CREATE OR REPLACE TABLE `amplified-time-498910-q6.raw_events.churn_predictions` AS
SELECT
  customerID,
  predicted_target_churn AS churn_prediction,
  predicted_target_churn_probs[OFFSET(0)].prob AS churn_probability,
  tenure_months,
  MonthlyCharges
FROM
  ML.PREDICT(MODEL `amplified-time-498910-q6.raw_events.churn_xgboost_model`,
    (SELECT * FROM `amplified-time-498910-q6.raw_events.churn_features`)
  )
ORDER BY
  churn_probability DESC;
