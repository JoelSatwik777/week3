import { useMemo, useState } from 'react';

import { predictSingleCustomer } from '../../api/client';
import { singleFormDefaults, singleFormFields } from '../../constants/formConfig';

function toNumber(value) {
  const parsed = Number(value);
  return Number.isNaN(parsed) ? value : parsed;
}

function validate(values) {
  const errors = {};

  for (const [key, value] of Object.entries(values)) {
    if (value === '' || value === null || value === undefined) {
      errors[key] = 'Required field.';
    }
  }

  if (Object.keys(errors).length > 0) return errors;

  if (values.CreditScore < 300 || values.CreditScore > 900) errors.CreditScore = 'Use 300 to 900.';
  if (values.Age < 18 || values.Age > 100) errors.Age = 'Use 18 to 100.';
  if (values.Tenure < 0 || values.Tenure > 20) errors.Tenure = 'Use 0 to 20.';
  if (values.Balance < 0) errors.Balance = 'Cannot be negative.';
  if (values.EstimatedSalary < 0) errors.EstimatedSalary = 'Cannot be negative.';

  return errors;
}

function SinglePredictionForm({ onResult, onError, loading, setLoading }) {
  const [values, setValues] = useState(singleFormDefaults);
  const [errors, setErrors] = useState({});

  const canSubmit = useMemo(() => Object.keys(validate(values)).length === 0, [values]);

  const updateField = (key, value) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const clearAll = () => {
    const empty = Object.fromEntries(
      Object.keys(singleFormDefaults).map((key) => [key, ''])
    );
    setValues(empty);
    setErrors({});
    onResult(null, null);
    onError('');
  };

  const onSubmit = async (event) => {
    event.preventDefault();
    const nextErrors = validate(values);
    setErrors(nextErrors);

    if (Object.keys(nextErrors).length > 0) {
      onError('Please correct highlighted fields before submission.');
      return;
    }

    onError('');
    setLoading(true);
    try {
      const response = await predictSingleCustomer(values);
      onResult(response, values);
    } catch (error) {
      onResult(null, null);
      onError(error.message || 'Prediction failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="card form-card" onSubmit={onSubmit}>
      <div className="card-header-row">
        <h2>Single Customer Assessment</h2>
        {loading ? <span className="spinner" aria-label="Loading" /> : null}
      </div>
      <div className="form-grid single-grid">
        {singleFormFields.map((field) => {
          const hasDescription = Boolean(field.description);
          return (
            <label
              key={field.key}
              className="field"
              title={hasDescription ? field.description : undefined}
            >
              <span className={hasDescription ? 'field-label has-help' : 'field-label'}>
                {field.label}
                {hasDescription ? <span className="field-help-icon">?</span> : null}
              </span>
              {field.type === 'select' ? (
                <select
                  value={values[field.key]}
                  onChange={(event) => updateField(field.key, toNumber(event.target.value))}
                >
                  <option value="">Select</option>
                  {field.options.map((option) => {
                    if (typeof option === 'string') {
                      return (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      );
                    }
                    return (
                      <option key={`${field.key}-${option.value}`} value={option.value}>
                        {option.label}
                      </option>
                    );
                  })}
                </select>
              ) : (
                <input
                  type="number"
                  min={field.min}
                  max={field.max}
                  value={values[field.key]}
                  onChange={(event) => updateField(field.key, toNumber(event.target.value))}
                />
              )}
              {errors[field.key] ? <small className="field-error">{errors[field.key]}</small> : null}
            </label>
          );
        })}
      </div>
      <button className="primary-btn" type="submit" disabled={!canSubmit || loading}>
        Predict Churn
      </button>
      <button className="secondary-btn" type="button" onClick={clearAll} disabled={loading}>
        Clear All Fields
      </button>
    </form>
  );
}

export default SinglePredictionForm;
