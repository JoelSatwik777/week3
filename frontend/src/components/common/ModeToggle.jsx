function ModeToggle({ mode, onChange }) {
  return (
    <div className="mode-toggle" role="tablist" aria-label="Prediction mode">
      <button
        type="button"
        role="tab"
        aria-selected={mode === 'single'}
        className={mode === 'single' ? 'mode-btn active' : 'mode-btn'}
        onClick={() => onChange('single')}
      >
        Single Customer
      </button>
      <button
        type="button"
        role="tab"
        aria-selected={mode === 'batch'}
        className={mode === 'batch' ? 'mode-btn active' : 'mode-btn'}
        onClick={() => onChange('batch')}
      >
        Portfolio Upload
      </button>
    </div>
  );
}

export default ModeToggle;

