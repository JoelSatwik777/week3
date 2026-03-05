import { useState } from "react";

function CustomerForm({ onResult }) {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
  const [formData, setFormData] = useState({
    CreditScore: 600,
    Geography: "Germany",
    Gender: "Female",
    Age: 45,
    Tenure: 2,
    Balance: 150000,
    NumOfProducts: 1,
    HasCrCard: 1,
    IsActiveMember: 0,
    EstimatedSalary: 80000,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: isNaN(value) ? value : Number(value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      onResult(data);
    } catch (error) {
      onResult({
        churn_probability: 0,
        churn_prediction: 0,
        retention_suggestions: [
          `Unable to fetch prediction: ${error.message}`,
          "Make sure backend server is running on port 8000.",
        ],
      });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label>{key}</label>
          <input
            name={key}
            value={formData[key]}
            onChange={handleChange}
          />
        </div>
      ))}
      <button type="submit">Predict</button>
    </form>
  );
}

export default CustomerForm;
