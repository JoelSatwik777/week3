from __future__ import annotations
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse

from backend.schemas.customer import CustomerInput
from backend.schemas.prediction import BatchPredictResponse, PredictResponse
from backend.services.analytics_service import build_portfolio_analytics
from backend.services.file_processing_service import (
    get_processed_file_path,
    parse_upload_file,
    save_processed_frame,
)
from backend.services.llm_service import build_portfolio_report, build_single_customer_report
from backend.services.prediction_service import apply_batch_predictions, predict_single_customer

router = APIRouter(tags=['predictions'])


@router.post('/predict', response_model=PredictResponse)
def predict_customer(customer: CustomerInput):
    customer_payload = customer.model_dump()
    prediction = predict_single_customer(customer_payload)
    ai_report = build_single_customer_report(
        customer_payload,
        prediction['churn_probability'],
        prediction['risk_level'],
        prediction['retention_suggestions'],
    )

    return PredictResponse(
        churn_probability=prediction['churn_probability'],
        confidence=prediction['confidence'],
        risk_level=prediction['risk_level'],
        retention_suggestions=prediction['retention_suggestions'],
        ai_advisory_report=ai_report,
    )


@router.post('/predict-batch', response_model=BatchPredictResponse)
def predict_batch(
    file: UploadFile = File(...),
    include_portfolio_ai_summary: bool = Form(default=False),
):
    raw_frame = parse_upload_file(file)
    enriched_frame = apply_batch_predictions(raw_frame)
    summary, analytics = build_portfolio_analytics(enriched_frame)
    file_id, download_url = save_processed_frame(enriched_frame)

    portfolio_report = None
    if include_portfolio_ai_summary:
        portfolio_report = build_portfolio_report(
            {
                'summary': summary.model_dump(),
                'risk_distribution': [item.model_dump() for item in analytics.risk_distribution],
                'churn_by_geography': [item.model_dump() for item in analytics.churn_by_geography],
                'churn_by_age_group': [item.model_dump() for item in analytics.churn_by_age_group],
                'churn_by_num_of_products': [
                    item.model_dump() for item in analytics.churn_by_num_of_products
                ],
                'churn_by_credit_score_band': [
                    item.model_dump() for item in analytics.churn_by_credit_score_band
                ],
            }
        )

    return BatchPredictResponse(
        summary=summary,
        analytics=analytics,
        download_file_id=file_id,
        download_url=download_url,
        portfolio_ai_summary_report=portfolio_report,
    )


@router.get('/predict-batch/download/{file_id}')
def download_processed_file(file_id: str):
    output_path = get_processed_file_path(file_id)
    return FileResponse(
        path=output_path,
        media_type='text/csv',
        filename=f'processed_churn_predictions_{file_id}.csv',
    )
