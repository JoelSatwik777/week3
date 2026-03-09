from __future__ import annotations

import json
from typing import Optional

import requests

from backend.config.settings import get_settings
from backend.utils.logging import get_logger

logger = get_logger(__name__)


def _truncate(text: str) -> str:
    """Make sure the LLM response isn't excessively long.

    The previous implementation simply sliced at the character limit which
    sometimes cut a bullet point or sentence in half. That led to the
    frontend showing only "half" of the recommendations or executive
    summary (the remainder had been silently dropped).

    To avoid that we now truncate on the last newline boundary before the
    limit so that partial lines are removed, and we strip off any trailing
    whitespace. The cap is still controlled by the ``LLM_MAX_CHARS``
    environment variable.
    """
    limit = get_settings().llm_max_chars
    if len(text) <= limit:
        return text.strip()

    # try to cut on the last newline so we don't end up with half a bullet
    truncated = text[:limit]
    last_newline = truncated.rfind("\n")
    if last_newline != -1:
        truncated = truncated[:last_newline]
    return truncated.strip()


def _build_single_prompt(customer_data: dict, churn_probability: float, risk_level: str, suggestions: list[str]) -> str:
    return (
        'You are a banking retention advisor. '
        'Use the ML prediction as fixed truth and only explain risk drivers and actions. '
        'Return plain text only in the exact structure below, with short bullet points and simple language.\n\n'
        'Customer Snapshot:\n'
        '- <one short point>\n'
        '- <one short point>\n'
        'Risk Drivers:\n'
        '- <one short point>\n'
        '- <one short point>\n'
        'Recommended Actions:\n'
        '- <one short point>\n'
        '- <one short point>\n'
        '- <one short point>\n\n'
        f'Customer: {json.dumps(customer_data)}\n'
        f'Churn probability: {churn_probability:.4f}\n'
        f'Risk level: {risk_level}\n'
        f'Retention suggestions: {json.dumps(suggestions)}\n'
    )


def _build_portfolio_prompt(summary: dict) -> str:
    # include summary metrics and analytics breakdowns
    metrics = summary.get('summary', {})
    # manually format metrics into text
    formatted_metrics = (
        f"Total customers: {metrics.get('total_customers')} "
        f"Average churn probability: {metrics.get('average_churn_probability')} "
        f"High/Medium/Low risk counts: {metrics.get('high_risk_count')}/{metrics.get('medium_risk_count')}/{metrics.get('low_risk_count')} "
    )
    analytics = summary
    return (
        "You are a portfolio retention strategist. "
        "Use the ML outputs as fixed truth. You MUST provide two parts: (1) a short summary of the portfolio, and (2) concrete recommendations to reduce churn. "
        "Return plain text only in the exact structure below, using short bullet points and simple language.\n\n"
        "Summary of Portfolio:\n"
        "- <short bullet summarising overall churn and key segments>\n"
        "- <short bullet about notable risk concentrations>\n"
        "- <short bullet about any stabilising segments>\n"
        "- <short bullet about overall health of the book>\n\n"
        "Recommendations to Reduce Churn:\n"
        "(Give at least 4–5 specific, actionable suggestions. Base each on the data: which geography or age group or product segment has higher churn. "
        "Examples: target the geography with highest churn with retention offers; run campaigns for the age group with highest risk; "
        "bundle products for customers with only 1 product; offer credit-building support for poor/fair credit bands; "
        "trigger outbound calls or incentives for high-risk count; improve onboarding for low-tenure segments.)\n"
        "- <action based on geography with high churn>\n"
        "- <action based on age group or tenure>\n"
        "- <action based on number of products>\n"
        "- <action based on credit score bands>\n"
        "- <one more portfolio-level retention action>\n\n"
        "Use the following metrics and segment analytics as evidence. Do NOT repeat the numbers verbatim. "
        "Do NOT skip the Recommendations section—it is required.\n\n"
        "Portfolio Metrics:\n"
        f"{formatted_metrics}\n\n"
        "Breakdowns:\n"
        f"Risk distribution: {json.dumps(analytics.get('risk_distribution', []))}\n"
        f"Churn by geography: {json.dumps(analytics.get('churn_by_geography', []))}\n"
        f"Churn by age group: {json.dumps(analytics.get('churn_by_age_group', []))}\n"
        f"Churn by num of products: {json.dumps(analytics.get('churn_by_num_of_products', []))}\n"
        f"Churn by credit score band: {json.dumps(analytics.get('churn_by_credit_score_band', []))}\n"
    )


def _normalize_bullet_report(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    normalized: list[str] = []

    for line in lines:
        if line.endswith(':'):
            normalized.append(line)
            continue
        clean = line.lstrip('-*0123456789. ').strip()
        if clean:
            normalized.append(f'- {clean}')

    return '\n'.join(normalized)


def _call_ollama(prompt: str, normalize: bool = True) -> Optional[str]:
    """Send a prompt to Ollama and return trimmed text.

    By default the returned text is passed through
    ``_normalize_bullet_report`` because most of our prompts use simple
    bullet‑list output.  The executive summary is one exception: it needs to
    be plain prose, so callers can disable normalization by passing
    ``normalize=False``.
    """
    settings = get_settings()
    url = f"{settings.ollama_base_url.rstrip('/')}/api/generate"

    try:
        response = requests.post(
            url,
            json={
                'model': settings.ollama_model,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.2,
                    'num_predict': settings.llm_num_predict,
                    'num_ctx': settings.llm_num_ctx,
                },
            },
            timeout=settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        raw = _truncate(response.json().get('response', '').strip())
        if normalize:
            return _normalize_bullet_report(raw)
        return raw
    except requests.RequestException as exc:
        logger.warning('Ollama request failed: %s', exc)
        return None


def build_single_customer_report(customer_data: dict, churn_probability: float, risk_level: str, suggestions: list[str]) -> str:
    prompt = _build_single_prompt(customer_data, churn_probability, risk_level, suggestions)
    response = _call_ollama(prompt)
    if response:
        return response
    return 'AI advisory unavailable: Ollama is offline or timed out. Start Ollama and retry.'


def build_portfolio_report(summary: dict) -> str:
    prompt = _build_portfolio_prompt(summary)
    response = _call_ollama(prompt)
    if response:
        return response
    return 'Portfolio AI summary unavailable: Ollama is offline or timed out.'


def _build_executive_summary_prompt(summary: dict) -> str:
    metrics = summary.get('summary', {})
    formatted_metrics = (
        f"Total customers: {metrics.get('total_customers')} "
        f"Average churn probability: {metrics.get('average_churn_probability')} "
        f"High/Medium/Low risk counts: {metrics.get('high_risk_count')}/{metrics.get('medium_risk_count')}/{metrics.get('low_risk_count')}"
    )
    analytics = summary
    return (
        "You are writing a brief executive summary for leadership. "
        "Use the following portfolio metrics and segment breakdowns. "
        "Write exactly 3 to 4 short sentences only: (1) overall portfolio health, (2) main risk concentrations, (3) key segment to watch, (4) one recommended priority. "
        "Each sentence must end with a period and the final sentence should include a clear recommendation phrase such as 'we should...' or 'we recommend...'. "
        "Do not leave any sentence hanging or end with a comma. "
        "Use plain language. Do not use bullet points—write flowing sentences.\n\n"
        f"Portfolio Metrics: {formatted_metrics}\n\n"
        f"Risk distribution: {json.dumps(analytics.get('risk_distribution', []))}\n"
        f"Churn by geography: {json.dumps(analytics.get('churn_by_geography', []))}\n"
        f"Churn by age group: {json.dumps(analytics.get('churn_by_age_group', []))}\n"
        f"Churn by num of products: {json.dumps(analytics.get('churn_by_num_of_products', []))}\n"
        f"Churn by credit score band: {json.dumps(analytics.get('churn_by_credit_score_band', []))}\n"
    )


def build_executive_summary(summary: dict) -> str:
    prompt = _build_executive_summary_prompt(summary)
    # executive summary is intended as flowing prose; don't force bullet
    # normalisation which was turning every sentence into "- …" and
    # confusing the frontend.
    response = _call_ollama(prompt, normalize=False)
    if response:
        return response
    return 'Executive summary unavailable: Ollama is offline or timed out.'


def _build_retention_message_prompt(
    customer_data: dict,
    churn_probability: float,
    risk_level: str,
    suggestions: list[str],
) -> str:
    return (
        "You are writing a short, professional retention message (email or SMS) for one customer. "
        "Use the customer data and risk info below. Write 2 to 3 sentences only: "
        "a personalised opening, why we value them, and one clear retention offer or next step. "
        "Tone: warm and professional. No bullet points—plain paragraphs.\n\n"
        f"Customer: {json.dumps(customer_data)}\n"
        f"Churn probability: {churn_probability:.4f}\n"
        f"Risk level: {risk_level}\n"
        f"Retention suggestions: {json.dumps(suggestions)}\n"
    )


def build_retention_message(
    customer_data: dict,
    churn_probability: float,
    risk_level: str,
    suggestions: list[str],
) -> str:
    prompt = _build_retention_message_prompt(
        customer_data, churn_probability, risk_level, suggestions
    )
    response = _call_ollama(prompt)
    if response:
        return response
    return 'Retention message unavailable: Ollama is offline or timed out.'
