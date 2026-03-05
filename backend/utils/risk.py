from backend.config.constants import LOW_RISK_MAX, MEDIUM_RISK_MAX


def classify_risk(probability: float) -> str:
    if probability <= LOW_RISK_MAX:
        return 'Low'
    if probability <= MEDIUM_RISK_MAX:
        return 'Medium'
    return 'High'