CREATE OR REPLACE VIEW `amplified-time-498910-q6.raw_events.churn_features` AS
SELECT
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure AS tenure_months,
    CASE 
        WHEN tenure <= 12 THEN 'New'
        WHEN tenure > 12 AND tenure <= 48 THEN 'Established'
        ELSE 'Loyal'
    END AS tenure_bucket,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    CAST(NULLIF(TRIM(TotalCharges), '') AS FLOAT64) AS TotalCharges,
    Churn AS target_churn
FROM
    `amplified-time-498910-q6.raw_events.customer_churn`;
