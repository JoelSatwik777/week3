const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

async function handleResponse(response) {
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const errorJson = await response.json();
      message = errorJson.detail || message;
    } catch {
      // Ignore JSON parse errors and use fallback message.
    }
    throw new Error(message);
  }
  return response.json();
}

export async function predictSingleCustomer(payload) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleResponse(response);
}

export async function predictPortfolio(file, includeAISummary = false) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('include_portfolio_ai_summary', includeAISummary ? 'true' : 'false');

  const response = await fetch(`${API_BASE_URL}/predict-batch`, {
    method: 'POST',
    body: formData,
  });

  return handleResponse(response);
}

/** Request portfolio AI summary separately so batch charts can show first. */
export async function fetchPortfolioAISummary(summary, analytics) {
  const response = await fetch(`${API_BASE_URL}/predict-batch/portfolio-ai-summary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ summary, analytics }),
  });
  return handleResponse(response);
}

/** Generate executive summary for batch results (for leadership). */
export async function fetchExecutiveSummary(summary, analytics) {
  const response = await fetch(`${API_BASE_URL}/predict-batch/executive-summary`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ summary, analytics }),
  });
  return handleResponse(response);
}

/** Generate personalised retention message (email/SMS) for a single customer. */
export async function fetchRetentionMessage(customer, result) {
  const response = await fetch(`${API_BASE_URL}/retention-message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      customer,
      churn_probability: result.churn_probability,
      risk_level: result.risk_level,
      retention_suggestions: result.retention_suggestions || [],
    }),
  });
  return handleResponse(response);
}

export async function predictFollowUp(sessionId, question) {
  const response = await fetch(`${API_BASE_URL}/follow-up`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, question }),
  });
  return handleResponse(response);
}

export function getDownloadUrl(relativeUrl) {
  if (!relativeUrl) return '';
  if (relativeUrl.startsWith('http')) return relativeUrl;
  return `${API_BASE_URL}${relativeUrl}`;
}

