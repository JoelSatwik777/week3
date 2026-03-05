function ResultCard({ result }) {
  if (!result) return null;

  const riskLevel =
    result.churn_probability > 0.6
        ? "High Risk"
        : result.churn_probability > 0.35
        ? "Medium Risk"
        : "Low Risk";

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Prediction Result</h3>
      <p>
        Churn Probability: {(result.churn_probability * 100).toFixed(1)}%
      </p>
      <p>Prediction: {riskLevel}</p>

      <h4>Retention Suggestions:</h4>
      <ul>
        {result.retention_suggestions.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}

export default ResultCard;
