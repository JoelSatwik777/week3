function toPercent(value) {
  return `${Math.round((value || 0) * 1000) / 10}%`;
}

function PortfolioSummaryCard({ summary }) {
  if (!summary) return null;

  const cards = [
    { label: 'Total Customers', value: summary.total_customers },
    { label: 'High Risk', value: summary.high_risk_count, tone: 'high' },
    { label: 'Medium Risk', value: summary.medium_risk_count, tone: 'medium' },
    { label: 'Low Risk', value: summary.low_risk_count, tone: 'low' },
    { label: 'Average Churn', value: toPercent(summary.average_churn_probability) },
  ];

  return (
    <div>
      <h3>Portfolio Summary</h3>
      <div className="summary-grid">
        {cards.map((item) => (
          <article
            key={item.label}
            className={item.tone ? `summary-item ${item.tone}` : 'summary-item'}
          >
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </article>
        ))}
      </div>
    </div>
  );
}

export default PortfolioSummaryCard;

