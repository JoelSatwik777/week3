import { useState } from "react";
import CustomerForm from "./components/CustomerForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Banking Customer Churn Predictor</h1>
      <CustomerForm onResult={setResult} />
      <ResultCard result={result} />
    </div>
  );
}

export default App;