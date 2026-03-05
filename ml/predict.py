import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "banking_model.pkl")

model = joblib.load(MODEL_PATH)

THRESHOLD = 0.35

def predict_customer(customer_data):
    """
    customer_data: dict with feature values
    """

    # Convert to DataFrame
    import pandas as pd
    df = pd.DataFrame([customer_data])

    # Get probability
    prob = model.predict_proba(df)[0][1]

    churn = 1 if prob > THRESHOLD else 0

    return {
        "churn_probability": float(prob),
        "churn_prediction": int(churn),
    }

if __name__ == "__main__":
    sample_customer = {
        "CreditScore": 600,
        "Geography": "Germany",
        "Gender": "Female",
        "Age": 45,
        "Tenure": 2,
        "Balance": 150000,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 0,
        "EstimatedSalary": 80000
    }

    result = predict_customer(sample_customer)
    print(result)
