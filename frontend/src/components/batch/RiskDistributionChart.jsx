import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = {
  Low: 'var(--risk-low)',
  Medium: 'var(--risk-medium)',
  High: 'var(--risk-high)',
};

function RiskDistributionChart({ summary }) {
  if (!summary || summary.total_customers === 0) return null;

  const data = [
    { name: 'Low', value: summary.low_risk_count, color: COLORS.Low },
    { name: 'Medium', value: summary.medium_risk_count, color: COLORS.Medium },
    { name: 'High', value: summary.high_risk_count, color: COLORS.High },
  ];

  return (
    <div className="chart-container">
      <h3>Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RiskDistributionChart;

