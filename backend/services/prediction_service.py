from __future__ import annotations

import pandas as pd

from backend.services.model_service import get_model_service
from backend.services.retention_service import build_retention_suggestions
from backend.utils.formatting import format_probability
from backend.utils.risk import classify_risk


def predict_single_customer(payload: dict) -> dict:
    model_service = get_model_service()
    probability, confidence = model_service.predict_single(payload)

    churn_probability = format_probability(probability)
    risk_level = classify_risk(churn_probability)
    suggestions = build_retention_suggestions(payload, risk_level)

    return {
        'churn_probability': churn_probability,
        'confidence': format_probability(confidence),
        'risk_level': risk_level,
        'retention_suggestions': suggestions,
    }


def apply_batch_predictions(frame: pd.DataFrame) -> pd.DataFrame:
    model_service = get_model_service()
    probabilities, _ = model_service.predict_batch(frame)

    output = frame.copy()
    output['churn_probability'] = probabilities.map(format_probability)
    output['risk_level'] = output['churn_probability'].map(classify_risk)
    output['retention_suggestions'] = output.apply(
        lambda row: ' | '.join(build_retention_suggestions(row.to_dict(), row['risk_level'])), axis=1
    )

    return output