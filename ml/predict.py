from __future__ import annotations

import joblib
import pandas as pd

from ml.config import DEFAULT_THRESHOLD, MODEL_FEATURES, MODEL_PATH


class ChurnPredictor:
    def __init__(self, model_path=MODEL_PATH, threshold: float = DEFAULT_THRESHOLD) -> None:
        self.model_path = model_path
        self.threshold = threshold
        self.model = joblib.load(self.model_path)

    def _prepare(self, data: dict | pd.DataFrame) -> pd.DataFrame:
        frame = pd.DataFrame([data]) if isinstance(data, dict) else data.copy()
        missing = [col for col in MODEL_FEATURES if col not in frame.columns]
        if missing:
            raise ValueError(f'Missing required features: {missing}')
        return frame[MODEL_FEATURES]

    def predict(self, data: dict | pd.DataFrame) -> pd.DataFrame:
        frame = self._prepare(data)
        prob = self.model.predict_proba(frame)[:, 1]
        pred = (prob > self.threshold).astype(int)
        confidence = (abs(prob - 0.5) * 2).clip(0, 1)

        return pd.DataFrame(
            {
                'churn_probability': prob,
                'churn_prediction': pred,
                'confidence': confidence,
            },
            index=frame.index,
        )


def predict_customer(customer_data: dict) -> dict:
    predictor = ChurnPredictor()
    row = predictor.predict(customer_data).iloc[0]
    return {
        'churn_probability': float(row['churn_probability']),
        'churn_prediction': int(row['churn_prediction']),
        'confidence': float(row['confidence']),
    }


if __name__ == '__main__':
    sample_customer = {
        'CreditScore': 600,
        'Geography': 'Germany',
        'Gender': 'Female',
        'Age': 45,
        'Tenure': 2,
        'Balance': 150000,
        'NumOfProducts': 1,
        'HasCrCard': 1,
        'IsActiveMember': 0,
        'EstimatedSalary': 80000,
    }
    print(predict_customer(sample_customer))