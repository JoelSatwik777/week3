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

        {mode === 'single' ? (
          <section className="panel-enter">
            <SinglePredictionForm
              onResult={setSingleResult}
              onError={setSingleError}
              loading={loadingSingle}
              setLoading={setLoadingSingle}
            />
            {singleError ? <p className="panel-error">{singleError}</p> : null}
            <SingleResultCard result={singleResult} />
          </section>
        ) : (
          <section className="panel-enter">
            <PortfolioUpload />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
