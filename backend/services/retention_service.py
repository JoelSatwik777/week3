def build_retention_suggestions(customer: dict, risk_level: str) -> list[str]:
    suggestions = []

    # Personalized based on activity
    if customer.get('IsActiveMember') == 0:
        suggestions.append('Launch a personalized digital engagement campaign in the next 7 days.')

    # Based on products
    num_products = customer.get('NumOfProducts', 0)
    if num_products <= 1:
        suggestions.append('Bundle one additional product with loyalty pricing to improve relationship depth.')
    elif num_products >= 3:
        suggestions.append('Review product complexity and offer simplified premium packages.')

    # Based on balance
    balance = customer.get('Balance', 0)
    if balance > 150000:
        suggestions.append('Assign a dedicated relationship manager for proactive high-value account outreach.')
    elif balance < 50000:
        suggestions.append('Offer low-balance incentives and educational content on savings growth.')

    # Based on tenure
    tenure = customer.get('Tenure', 0)
    if tenure < 2:
        suggestions.append('Provide enhanced onboarding support and milestone rewards for early tenure.')
    elif tenure > 8:
        suggestions.append('Recognize long-term loyalty with exclusive perks and anniversary communications.')

    # Based on age
    age = customer.get('Age', 0)
    if age < 30:
        suggestions.append('Target with digital-first initiatives and mobile app engagement features.')
    elif age > 55:
        suggestions.append('Offer personalized senior benefits and simplified service options.')

    # Based on geography
    geography = customer.get('Geography', '')
    if geography == 'Germany':
        suggestions.append('Leverage local market insights for tailored German-language communications.')
    elif geography == 'France':
        suggestions.append('Incorporate French cultural preferences in marketing and service delivery.')
    elif geography == 'Spain':
        suggestions.append('Highlight community-focused initiatives popular in Spanish markets.')

    # Based on gender (if available)
    gender = customer.get('Gender', '')
    if gender == 'Female':
        suggestions.append('Personalize communications with female-focused financial empowerment content.')
    elif gender == 'Male':
        suggestions.append('Offer investment-focused education and growth-oriented financial planning.')

    # Based on credit score
    credit_score = customer.get('CreditScore', 0)
    if credit_score < 600:
        suggestions.append('Provide credit-building resources and supportive financial guidance.')
    elif credit_score > 750:
        suggestions.append('Offer premium investment opportunities and advanced financial tools.')

    # Risk-based
    if risk_level == 'High':
        suggestions.append('Trigger immediate churn-prevention workflow with outbound call escalation.')
    elif risk_level == 'Medium':
        suggestions.append('Schedule follow-up engagement within 14 days to reinforce relationship.')

    # Fallback
    if not suggestions:
        suggestions.append('Maintain current service quality and monitor engagement indicators monthly.')

    # Shuffle and limit to 5, but ensure variety
    import random
    random.shuffle(suggestions)
    return suggestions[:5]