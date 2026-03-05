function RiskDistributionChart({ summary }) {
  if (!summary || summary.total_customers === 0) return null;

  const data = [
    { label: 'High', count: summary.high_risk_count, color: 'var(--risk-high)' },
    { label: 'Medium', count: summary.medium_risk_count, color: 'var(--risk-medium)' },
    { label: 'Low', count: summary.low_risk_count, color: 'var(--risk-low)' },
  ];

  return (
    <div className="distribution">
      <h3>Risk Distribution</h3>
      {data.map((item) => {
        const percent = (item.count / summary.total_customers) * 100;
        return (
          <div key={item.label} className="dist-row">
            <div className="dist-label">
              <span>{item.label}</span>
              <span>{Math.round(percent)}%</span>
            </div>
            <div className="dist-track">
              <div className="dist-fill" style={{ width: `${percent}%`, backgroundColor: item.color }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default RiskDistributionChart;

