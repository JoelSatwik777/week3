from typing import List, Optional

from pydantic import BaseModel, Field


class PredictResponse(BaseModel):
    churn_probability: float = Field(..., ge=0, le=1)
    confidence: float = Field(..., ge=0, le=1)
    risk_level: str
    retention_suggestions: List[str]
    ai_advisory_report: str
    session_id: Optional[str] = None


class BatchSummary(BaseModel):
    total_customers: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    average_churn_probability: float


class RiskDistributionPoint(BaseModel):
    risk: str
    count: int


class GeographyChurnPoint(BaseModel):
    geography: str
    churn_rate: float


class AgeGroupChurnPoint(BaseModel):
    age_group: str
    churn_rate: float


class ProductChurnPoint(BaseModel):
    num_of_products: int
    churn_rate: float


class CreditBandChurnPoint(BaseModel):
    credit_score_band: str
    churn_rate: float


class BatchAnalytics(BaseModel):
    risk_distribution: List[RiskDistributionPoint]
    churn_by_geography: List[GeographyChurnPoint]
    churn_by_age_group: List[AgeGroupChurnPoint]
    churn_by_num_of_products: List[ProductChurnPoint]
    churn_by_credit_score_band: List[CreditBandChurnPoint]


class BatchPredictResponse(BaseModel):
    summary: BatchSummary
    analytics: BatchAnalytics
    download_file_id: str
    download_url: str
    portfolio_ai_summary_report: Optional[str] = None


class PortfolioAISummaryRequest(BaseModel):
    """Payload for requesting portfolio AI summary separately (so batch results can show first)."""
    summary: BatchSummary
    analytics: BatchAnalytics


class PortfolioAISummaryResponse(BaseModel):
    portfolio_ai_summary_report: str


class ExecutiveSummaryRequest(BaseModel):
    summary: BatchSummary
    analytics: BatchAnalytics


class ExecutiveSummaryResponse(BaseModel):
    executive_summary: str


class RetentionMessageRequest(BaseModel):
    customer: dict  # same shape as CustomerInput
    churn_probability: float
    risk_level: str
    retention_suggestions: List[str]


class RetentionMessageResponse(BaseModel):
    retention_message: str


class FollowUpRequest(BaseModel):
    session_id: str
    question: str


class FollowUpResponse(BaseModel):
    advisory: str
