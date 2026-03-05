import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function ChurnByNumOfProductsChart({ data }) {
  if (!data || data.length === 0) return null;

  const formattedData = data.map((item) => ({
    numOfProducts: item.num_of_products,
    churnRate: item.churn_rate * 100, // Convert to percentage
  }));

  return (
    <div className="chart-container">
      <h3>Churn by Number of Products</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={formattedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="numOfProducts" />
          <YAxis label={{ value: 'Churn Rate (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip formatter={(value) => [`${value.toFixed(2)}%`, 'Churn Rate']} />
          <Bar dataKey="churnRate" fill="var(--accent)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ChurnByNumOfProductsChart;