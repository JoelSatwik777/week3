import { useRef, useState } from 'react';

import { fetchExecutiveSummary, fetchPortfolioAISummary, getDownloadUrl, predictPortfolio } from '../../api/client';
import ChurnByAgeGroupChart from './ChurnByAgeGroupChart';
import ChurnByCreditScoreBandChart from './ChurnByCreditScoreBandChart';
import ChurnByGeographyChart from './ChurnByGeographyChart';
import ChurnByNumOfProductsChart from './ChurnByNumOfProductsChart';
import PortfolioSummaryCard from './PortfolioSummaryCard';
import RiskDistributionChart from './RiskDistributionChart';
import PortfolioAISummary from './PortfolioAISummary';

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
  /** Whether the user had "Generate AI summary" checked when they last ran (so we always show the card). */
  const [lastRunRequestedAiSummary, setLastRunRequestedAiSummary] = useState(false);
  const [aiSummaryReport, setAiSummaryReport] = useState(null);
  const [aiSummaryLoading, setAiSummaryLoading] = useState(false);
  const [aiSummaryError, setAiSummaryError] = useState('');
  const [executiveSummary, setExecutiveSummary] = useState(null);
  const [executiveSummaryLoading, setExecutiveSummaryLoading] = useState(false);
  const [executiveSummaryError, setExecutiveSummaryError] = useState('');

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
    setAiSummaryReport(null);
    setAiSummaryError('');
    setExecutiveSummary(null);
    setExecutiveSummaryError('');

    try {
      const response = await predictPortfolio(file, includeAiSummary);
      setResult(response);
      setLastRunRequestedAiSummary(includeAiSummary);

      if (includeAiSummary) {
        setAiSummaryLoading(true);
        fetchPortfolioAISummary(response.summary, response.analytics)
          .then((data) => {
            setAiSummaryReport(data.portfolio_ai_summary_report);
          })
          .catch((err) => {
            setAiSummaryError(err.message || 'AI summary failed.');
          })
          .finally(() => {
            setAiSummaryLoading(false);
          });
      }
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

          {/* Always show AI summary card when there are results so user sees loading or prompt. */}
          <div className="ai-summary-panel">
            <div className="panel-header">
              <span className="advisory-icon">🤖</span>
              <h3>Portfolio AI Recommendations</h3>
              {aiSummaryLoading ? <span className="spinner" aria-label="Generating AI summary" /> : null}
            </div>
            {!lastRunRequestedAiSummary ? (
              <div className="ai-summary-loading">
                <p>Check &quot;Generate optional portfolio AI summary report&quot; above and run the prediction again to get AI recommendations.</p>
              </div>
            ) : aiSummaryLoading ? (
              <div className="ai-summary-loading ai-summary-loading-active" aria-live="polite">
                <p>Generating AI summary… This may take a moment.</p>
              </div>
            ) : aiSummaryError ? (
              <p className="panel-error">{aiSummaryError}</p>
            ) : aiSummaryReport ? (
              <PortfolioAISummary report={aiSummaryReport} />
            ) : null}
          </div>

          <div className="executive-summary-section">
            <div className="executive-summary-header">
              <h3>Executive summary</h3>
              <button
                type="button"
                className="secondary-btn"
                onClick={async () => {
                  setExecutiveSummaryError('');
                  setExecutiveSummaryLoading(true);
                  try {
                    const data = await fetchExecutiveSummary(result.summary, result.analytics);
                    setExecutiveSummary(data.executive_summary);
                  } catch (err) {
                    setExecutiveSummary(null);
                    setExecutiveSummaryError(err.message || 'Failed to generate executive summary.');
                  } finally {
                    setExecutiveSummaryLoading(false);
                  }
                }}
                disabled={executiveSummaryLoading}
              >
                {executiveSummaryLoading ? 'Generating…' : 'Generate executive summary'}
              </button>
            </div>
            {executiveSummaryError ? <p className="panel-error">{executiveSummaryError}</p> : null}
            {executiveSummary ? (
              <div className="executive-summary-card">
                <p className="executive-summary-text">{executiveSummary}</p>
              </div>
            ) : null}
          </div>

          <a className="primary-btn download-btn" href={getDownloadUrl(result.download_url)}>
            Download Processed File
          </a>
        </article>
      ) : null}
    </section>
  );
}

export default PortfolioUpload;
