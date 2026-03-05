import sys
import json
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.predict import predict_customer


def _extract_suggestions(text):
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            cleaned = [str(item).strip() for item in parsed if str(item).strip()]
            if cleaned:
                return cleaned[:5]
    except (json.JSONDecodeError, TypeError):
        pass

    lines = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if cleaned:
            lines.append(cleaned)
    return lines[:5]


def generate_ai_suggestions(customer_data, prediction):
    prompt = f"""
    You are a senior banking retention strategist.

    Customer data:
    {customer_data}

    Model output:
    {prediction}

    Provide 4 concise retention actions tailored to this customer.
    Return only a valid JSON array of strings. No markdown, no explanation.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=25,
        )
        response.raise_for_status()
        text = response.json().get("response", "")
        suggestions = _extract_suggestions(text)
        if suggestions:
            return suggestions
    except requests.RequestException:
        pass

    return [
        "AI suggestions unavailable: ensure Ollama server is running with llama3.",
        "Retry prediction after starting Ollama.",
    ]


def generate_ai_report(customer_data, prediction):

    prompt = f"""
    You are a senior banking risk analyst.

    Customer Details:
    {customer_data}

    Model Output:
    {prediction}

    Generate:
    1. Risk explanation
    2. Business reasoning
    3. Recommended retention actions
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json().get("response", "AI report unavailable.")
    except requests.RequestException:
        return "AI advisory report unavailable (local LLM service not reachable)."

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Customer(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

@app.post("/predict")
def predict(customer: Customer):
    customer_input = customer.model_dump()
    try:
        result = predict_customer(customer_input)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {exc}") from exc

    ai_suggestions = generate_ai_suggestions(customer_input, result)
    ai_report = generate_ai_report(customer_input, result)
    return {
        **result,
        "retention_suggestions": ai_suggestions,
        "ai_advisory_report": ai_report,
    }
