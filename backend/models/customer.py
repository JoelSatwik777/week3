from dataclasses import dataclass


@dataclass
class PredictionOutcome:
    churn_probability: float
    confidence: float
    risk_level: str