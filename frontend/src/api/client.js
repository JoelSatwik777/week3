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

export function getDownloadUrl(relativeUrl) {
  if (!relativeUrl) return '';
  if (relativeUrl.startsWith('http')) return relativeUrl;
  return `${API_BASE_URL}${relativeUrl}`;
}

