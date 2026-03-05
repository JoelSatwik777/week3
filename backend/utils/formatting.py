def format_probability(probability: float) -> float:
    return round(max(0.0, min(1.0, float(probability))), 4)