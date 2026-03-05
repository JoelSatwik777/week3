from __future__ import annotations

import json
from typing import Optional

import requests

from backend.config.settings import get_settings
from backend.utils.logging import get_logger

logger = get_logger(__name__)


def _truncate(text: str) -> str:
    limit = get_settings().llm_max_chars
    return text[:limit].strip()


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
    return (
        'You are a portfolio retention strategist. '
        'Summarize this portfolio in short plain-text bullets using this structure:\n'
        'Portfolio Snapshot:\n- ...\n- ...\n'
        'Top Priorities:\n- ...\n- ...\n- ...\n\n'
        f'Portfolio summary: {json.dumps(summary)}\n'
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


def _call_ollama(prompt: str) -> Optional[str]:
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
                    'num_predict': 180,
                },
            },
            timeout=settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        raw = _truncate(response.json().get('response', '').strip())
        return _normalize_bullet_report(raw)
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
