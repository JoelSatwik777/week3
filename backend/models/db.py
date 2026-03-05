from dataclasses import dataclass


@dataclass
class CustomerPredictionRecord:
    customer_id: str
    churn_probability: float
    risk_level: str


# Placeholder for future ORM model integration.