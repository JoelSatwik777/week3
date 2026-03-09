import React from 'react';

// A redesigned AI summary component using card layout for each section
function PortfolioAISummary({ report }) {
  if (!report) return null;

  const rawLines = report.split('\n');
  const cleanText = (s) => s.replace(/\*+/g, '').trim();

  const looksLikeUnavailable = (text) => {
    const t = (text || '').toLowerCase();
    return (
      t.includes('ollama is offline') ||
      t.includes('offline or timed out') ||
      t.includes('summary unavailable') ||
      t.includes('advisory unavailable')
    );
  };

  const joined = cleanText(report || '');
  if (looksLikeUnavailable(joined)) {
    return (
      <div className="ai-summary-report">
        <div className="ai-summary-card wide">
          <div className="summary-card-body">
            <div className="ai-summary-alert" role="status" aria-live="polite">
              <div className="ai-summary-alert-title">AI summary unavailable</div>
              <div className="ai-summary-alert-body">{joined}</div>
              <div className="ai-summary-alert-hint">
                Start Ollama, then re-run the portfolio with “Generate optional portfolio AI summary report” enabled.
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Parse the LLM output into two logical buckets based on headings:
  // "Summary of Portfolio:" and "Recommendations to Reduce Churn:".
  //
  // The model sometimes returns numbered lists ("1. …", "2) …") instead
  // of hyphen bullets.  The original regex only recognised hyphens, which
  // meant half of the recommendations could be silently ignored.  Accept
  // any of the common list markers and strip them when collecting items.
  const summaryItems = [];
  const recommendationItems = [];
  let section = 'summary';

  // regex matching a leading list marker (dash, star, bullet, digit + [.\)])
  const bulletRegex = /^\s*(?:[-*•]|\d+[\.)])\s+/;

  rawLines.forEach((raw) => {
    const line = cleanText(raw);
    if (!line) return;

    // remove any leading bullet/number prefix for easier comparisons
    const normalized = line.replace(bulletRegex, '');
    const heading = normalized.toLowerCase();

    if (heading.startsWith('summary of portfolio') && heading.endsWith(':')) {
      section = 'summary';
      return;
    }

    if (heading.startsWith('recommendations to reduce churn') && heading.endsWith(':')) {
      section = 'recommendations';
      return;
    }

    if (bulletRegex.test(raw)) {
      if (section === 'recommendations') {
        recommendationItems.push(normalized);
      } else {
        summaryItems.push(normalized);
      }
    }
  });

  // Fallback: if parsing fails, treat all lines as a simple bullet list in one card
  const hasStructured =
    summaryItems.length > 0 || recommendationItems.length > 0;
  const twoEqualCards =
    hasStructured && summaryItems.length > 0 && recommendationItems.length > 0;

  return (
    <div className={`ai-summary-report${twoEqualCards ? ' two-cols' : ''}`}>
      {hasStructured ? (
        <>
          {summaryItems.length > 0 && (
            <div className="ai-summary-card">
              <h4 className="summary-card-title">Summary of uploaded portfolio</h4>
              <div className="summary-card-body">
                <ul className="summary-list">
                  {summaryItems.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
          {recommendationItems.length > 0 && (
            <div className="ai-summary-card">
              <h4 className="summary-card-title">Recommendations to reduce churn</h4>
              <div className="summary-card-body">
                <ul className="summary-list">
                  {recommendationItems.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="ai-summary-card wide">
          <h4 className="summary-card-title">Portfolio AI recommendations</h4>
          <div className="summary-card-body">
            <ul className="summary-list">
              {rawLines
                .map((ln) => cleanText(ln))
                .filter(Boolean)
                .map((item, idx) => (
                  <li key={idx}>{item.replace(/^[-*•]\s+/, '')}</li>
                ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default PortfolioAISummary;
