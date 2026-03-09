import { useState } from 'react';
import { fetchRetentionMessage } from '../../api/client';

function riskClass(riskLevel) {
  if (riskLevel === 'High') return 'risk-badge high';
  if (riskLevel === 'Medium') return 'risk-badge medium';
  return 'risk-badge low';
}

function renderBoldInline(text) {
  const parts = text.split(/(\*\*.*?\*\*)/g).filter(Boolean);
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={`${part}-${index}`}>{part.slice(2, -2)}</strong>;
    }
    return <span key={`${part}-${index}`}>{part}</span>;
  });
}

function renderAdvisory(text) {
  if (!text) return null;
  const lines = text.split('\n').map((line) => line.trim()).filter(Boolean);

  return (
    <div className="advisory-list">
      {lines.map((line, index) => {
        if (line.endsWith(':')) {
          return (
            <h4 key={`${line}-${index}`} className="advisory-heading">
              {renderBoldInline(line)}
            </h4>
          );
        }

        const isBullet = line.startsWith('- ') || line.startsWith('* ');
        const content = isBullet ? line.slice(2).trim() : line;

        return (
          <p key={`${line}-${index}`} className={isBullet ? 'advisory-item' : 'advisory-text'}>
            {isBullet ? <span className="advisory-icon">→</span> : null}
            <span>{renderBoldInline(content)}</span>
          </p>
        );
      })}
    </div>
  );
}

function SingleResultCard({ result, lastSubmittedCustomer }) {
  const [retentionMessage, setRetentionMessage] = useState(null);
  const [retentionLoading, setRetentionLoading] = useState(false);
  const [retentionError, setRetentionError] = useState('');

  const handleGenerateRetentionMessage = async () => {
    if (!result || !lastSubmittedCustomer) return;
    setRetentionError('');
    setRetentionLoading(true);
    try {
      const data = await fetchRetentionMessage(lastSubmittedCustomer, result);
      setRetentionMessage(data.retention_message);
    } catch (err) {
      setRetentionMessage(null);
      setRetentionError(err.message || 'Failed to generate message.');
    } finally {
      setRetentionLoading(false);
    }
  };

  if (!result) return null;

  const probabilityPercent = Math.round((result.churn_probability || 0) * 1000) / 10;

  return (
    <section className="card result-card">
      <div className="card-header-row">
        <h2>Executive Risk Summary</h2>
        <span className={riskClass(result.risk_level)}>{result.risk_level} Risk</span>
      </div>

      <div className="progress-wrap">
        <div className="progress-top">
          <span>Churn Probability</span>
          <strong>{probabilityPercent}%</strong>
        </div>
        <div className="progress-track" role="progressbar" aria-valuenow={probabilityPercent}>
          <div className="progress-fill" style={{ width: `${Math.min(probabilityPercent, 100)}%` }} />
        </div>
      </div>

      <div className="result-stack">
        <article className="insight-panel suggestions-panel">
          <h3>Retention Suggestions</h3>
          <ul>
            {(result.retention_suggestions || []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </article>
        <article className="insight-panel advisory-panel">
          <h3>AI Advisory Report</h3>
          {renderAdvisory(result.ai_advisory_report)}
        </article>
      </div>

      <div className="retention-message-section">
        <div className="retention-message-header">
          <h3>Retention message</h3>
          <button
            type="button"
            className="secondary-btn retention-message-btn"
            onClick={handleGenerateRetentionMessage}
            disabled={retentionLoading || !lastSubmittedCustomer}
          >
            {retentionLoading ? 'Generating…' : 'Generate retention message'}
          </button>
        </div>
        {retentionError ? <p className="panel-error">{retentionError}</p> : null}
        {retentionMessage ? (
          <div className="retention-message-card">
            <p className="retention-message-text">{retentionMessage}</p>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export default SingleResultCard;
