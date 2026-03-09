import { useEffect, useState } from 'react';

import './App.css';
import ModeToggle from './components/common/ModeToggle';
import Navbar from './components/layout/Navbar';
import PortfolioUpload from './components/batch/PortfolioUpload';
import SinglePredictionForm from './components/single/SinglePredictionForm';
import SingleResultCard from './components/single/SingleResultCard';

function App() {
  const [theme, setTheme] = useState('light');
  const [mode, setMode] = useState('single');
  const [singleResult, setSingleResult] = useState(null);
  const [lastSubmittedCustomer, setLastSubmittedCustomer] = useState(null);
  const [singleError, setSingleError] = useState('');
  const [loadingSingle, setLoadingSingle] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <div className="app-shell">
      <Navbar
        theme={theme}
        onToggleTheme={() => setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))}
      />

      <main className="app-main">
        <ModeToggle mode={mode} onChange={setMode} />

        <section
          className={
            mode === 'single'
              ? 'panel-enter mode-panel mode-panel-visible'
              : 'panel-enter mode-panel mode-panel-hidden'
          }
        >
          <SinglePredictionForm
            onResult={(result, customer) => {
              setSingleResult(result);
              setLastSubmittedCustomer(customer ?? null);
            }}
            onError={setSingleError}
            loading={loadingSingle}
            setLoading={setLoadingSingle}
          />
          {singleError ? <p className="panel-error">{singleError}</p> : null}
          <SingleResultCard result={singleResult} lastSubmittedCustomer={lastSubmittedCustomer} />
        </section>

        <section
          className={
            mode === 'batch'
              ? 'panel-enter mode-panel mode-panel-visible'
              : 'panel-enter mode-panel mode-panel-hidden'
          }
        >
          <PortfolioUpload />
        </section>
      </main>
    </div>
  );
}

export default App;
