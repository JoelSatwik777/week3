import { useRef, useState } from 'react';

import { getDownloadUrl, predictPortfolio } from '../../api/client';
import ChurnByAgeGroupChart from './ChurnByAgeGroupChart';
import ChurnByCreditScoreBandChart from './ChurnByCreditScoreBandChart';
import ChurnByGeographyChart from './ChurnByGeographyChart';
import ChurnByNumOfProductsChart from './ChurnByNumOfProductsChart';
import PortfolioSummaryCard from './PortfolioSummaryCard';
import RiskDistributionChart from './RiskDistributionChart';

const allowedExtensions = ['.csv', '.xlsx', '.xls'];

function isValidFile(file) {
  const fileName = file?.name?.toLowerCase() || '';
  return allowedExtensions.some((ext) => fileName.endsWith(ext));
}

function PortfolioUpload() {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [includeAiSummary, setIncludeAiSummary] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleSelectedFile = (nextFile) => {
    if (!nextFile) return;
    if (!isValidFile(nextFile)) {
      setError('Upload CSV or Excel file (.csv, .xlsx, .xls).');
      setFile(null);
      return;
    }
    setError('');
    setFile(nextFile);
  };

  const submit = async () => {
    if (!file) {
      setError('Please choose a portfolio file first.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await predictPortfolio(file, includeAiSummary);
      setResult(response);
    } catch (uploadError) {
      setResult(null);
      setError(uploadError.message || 'Batch prediction failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="batch-layout">
      <article className="card upload-card">
        <div className="card-header-row">
          <h2>Portfolio Risk Processing</h2>
          {loading ? <span className="spinner" aria-label="Processing" /> : null}
        </div>

        <div
          className={dragOver ? 'drop-zone active' : 'drop-zone'}
          onDragOver={(event) => {
            event.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(event) => {
            event.preventDefault();
            setDragOver(false);
            handleSelectedFile(event.dataTransfer.files?.[0]);
          }}
        >
          {!file ? (
            <>
              <p>Drag and drop portfolio file here</p>
              <small>or</small>
              <button type="button" className="secondary-btn" onClick={() => inputRef.current?.click()}>
                Browse Files
              </button>
            </>
          ) : (
            <>
              <p>File uploaded successfully</p>
              <button
                type="button"
                className="secondary-btn"
                onClick={() => {
                  setFile(null);
                  if (inputRef.current) inputRef.current.value = '';
                }}
              >
                Remove File
              </button>
            </>
          )}
          <input
            ref={inputRef}
            type="file"
            className="hidden-input"
            accept=".csv,.xlsx,.xls"
            onChange={(event) => handleSelectedFile(event.target.files?.[0])}
          />
          <p className="filename">{file ? file.name : 'No file selected'}</p>
        </div>

        <label className="check-row">
          <input
            type="checkbox"
            checked={includeAiSummary}
            onChange={(event) => setIncludeAiSummary(event.target.checked)}
          />
          <span>Generate optional portfolio AI summary report</span>
        </label>

        {error ? <p className="panel-error">{error}</p> : null}

        <button type="button" className="primary-btn" onClick={submit} disabled={loading}>
          Run Portfolio Prediction
        </button>
      </article>

      {result ? (
        <article className="card analytics-card">
          <PortfolioSummaryCard summary={result.summary} />
          <div className="charts-grid">
            <RiskDistributionChart summary={result.summary} />
            <ChurnByGeographyChart data={result.analytics.churn_by_geography} />
            <ChurnByAgeGroupChart data={result.analytics.churn_by_age_group} />
            <ChurnByNumOfProductsChart data={result.analytics.churn_by_num_of_products} />
            <ChurnByCreditScoreBandChart data={result.analytics.churn_by_credit_score_band} />
          </div>

          {result.portfolio_ai_summary_report ? (
            <div className="ai-summary-panel">
              <div className="panel-header">
                <span className="advisory-icon">🤖</span>
                <h3>Portfolio AI Summary Report</h3>
              </div>
              <div className="ai-summary-content">
                {result.portfolio_ai_summary_report.split('\n').map((line, index) => {
                  const trimmed = line.trim();
                  if (!trimmed) return null;
                  if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
                    return <h4 key={index} className="summary-section">{trimmed.slice(2, -2)}</h4>;
                  }
                  if (trimmed.startsWith('- ')) {
                    return <li key={index} className="summary-bullet">{trimmed.slice(2)}</li>;
                  }
                  return <p key={index}>{trimmed}</p>;
                })}
              </div>
            </div>
          ) : null}

          <a className="primary-btn download-btn" href={getDownloadUrl(result.download_url)}>
            Download Processed File
          </a>
        </article>
      ) : null}
    </section>
  );
}

export default PortfolioUpload;
