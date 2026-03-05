from __future__ import annotations

import pandas as pd

from backend.config.constants import AGE_BUCKETS, CREDIT_SCORE_BANDS
from backend.schemas.prediction import (
    AgeGroupChurnPoint,
    BatchAnalytics,
    BatchSummary,
    CreditBandChurnPoint,
    GeographyChurnPoint,
    ProductChurnPoint,
    RiskDistributionPoint,
)
from backend.utils.formatting import format_probability


def _normalize_rate(value: float) -> float:
    return format_probability(float(value))


def _build_summary(frame: pd.DataFrame) -> BatchSummary:
    return BatchSummary(
        total_customers=len(frame),
        high_risk_count=int((frame['risk_level'] == 'High').sum()),
        medium_risk_count=int((frame['risk_level'] == 'Medium').sum()),
        low_risk_count=int((frame['risk_level'] == 'Low').sum()),
        average_churn_probability=_normalize_rate(frame['churn_probability'].mean()),
    )


def _risk_distribution(frame: pd.DataFrame) -> list[RiskDistributionPoint]:
    ordered = ['Low', 'Medium', 'High']
    return [
        RiskDistributionPoint(risk=risk, count=int((frame['risk_level'] == risk).sum()))
        for risk in ordered
    ]


def _churn_by_geography(frame: pd.DataFrame) -> list[GeographyChurnPoint]:
    grouped = (
        frame.groupby('Geography', dropna=False)['churn_probability']
        .mean()
        .reset_index()
        .sort_values('churn_probability', ascending=False)
    )
    return [
        GeographyChurnPoint(geography=str(row['Geography']), churn_rate=_normalize_rate(row['churn_probability']))
        for _, row in grouped.iterrows()
    ]


def _age_bucket(age: int) -> str:
    for label, low, high in AGE_BUCKETS:
        if low <= age <= high:
            return label
    return AGE_BUCKETS[-1][0]


def _churn_by_age_group(frame: pd.DataFrame) -> list[AgeGroupChurnPoint]:
    age_grouped = frame.copy()
    age_grouped['age_group'] = age_grouped['Age'].astype(int).map(_age_bucket)

    grouped = age_grouped.groupby('age_group')['churn_probability'].mean()

    ordered = []
    for label, *_ in AGE_BUCKETS:
        ordered.append(
            AgeGroupChurnPoint(
                age_group=label,
                churn_rate=_normalize_rate(float(grouped.get(label, 0.0))),
            )
        )
    return ordered


def _churn_by_num_of_products(frame: pd.DataFrame) -> list[ProductChurnPoint]:
    grouped = (
        frame.groupby('NumOfProducts')['churn_probability']
        .mean()
        .reset_index()
        .sort_values('NumOfProducts')
    )
    return [
        ProductChurnPoint(
            num_of_products=int(row['NumOfProducts']),
            churn_rate=_normalize_rate(row['churn_probability']),
        )
        for _, row in grouped.iterrows()
    ]


def _credit_band(score: int) -> str:
    for label, low, high in CREDIT_SCORE_BANDS:
        if low <= score <= high:
            return label
    return CREDIT_SCORE_BANDS[0][0]


def _churn_by_credit_band(frame: pd.DataFrame) -> list[CreditBandChurnPoint]:
    credit_grouped = frame.copy()
    credit_grouped['credit_score_band'] = credit_grouped['CreditScore'].astype(int).map(_credit_band)

    grouped = credit_grouped.groupby('credit_score_band')['churn_probability'].mean()

    ordered = []
    for label, *_ in CREDIT_SCORE_BANDS:
        ordered.append(
            CreditBandChurnPoint(
                credit_score_band=label,
                churn_rate=_normalize_rate(float(grouped.get(label, 0.0))),
            )
        )
    return ordered


def build_portfolio_analytics(frame: pd.DataFrame) -> tuple[BatchSummary, BatchAnalytics]:
    summary = _build_summary(frame)
    analytics = BatchAnalytics(
        risk_distribution=_risk_distribution(frame),
        churn_by_geography=_churn_by_geography(frame),
        churn_by_age_group=_churn_by_age_group(frame),
        churn_by_num_of_products=_churn_by_num_of_products(frame),
        churn_by_credit_score_band=_churn_by_credit_band(frame),
    )
    return summary, analytics