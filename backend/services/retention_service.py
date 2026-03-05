def build_retention_suggestions(customer: dict, risk_level: str) -> list[str]:
    suggestions = []

    if customer.get('IsActiveMember') == 0:
        suggestions.append('Launch a personalized digital engagement campaign in the next 7 days.')
    if customer.get('NumOfProducts', 0) <= 1:
        suggestions.append('Bundle one additional product with loyalty pricing to improve relationship depth.')
    if customer.get('Balance', 0) > 100000:
        suggestions.append('Assign a relationship manager for proactive high-value account outreach.')
    if customer.get('Tenure', 0) < 3:
        suggestions.append('Offer onboarding retention benefits and milestone rewards for early tenure.')

    if risk_level == 'High':
        suggestions.append('Trigger immediate churn-prevention workflow with outbound call escalation.')

    if not suggestions:
        suggestions.append('Maintain current service quality and monitor engagement indicators monthly.')

    return suggestions[:5]