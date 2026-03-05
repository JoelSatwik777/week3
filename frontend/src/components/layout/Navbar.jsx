function Navbar({ theme, onToggleTheme }) {
  return (
    <header className="top-nav">
      <div>
        <p className="nav-kicker">Hybrid AI Banking</p>
        <h1>Customer Churn Intelligence</h1>
      </div>
      <button className="theme-toggle" onClick={onToggleTheme} type="button">
        {theme === 'light' ? 'Switch to Dark' : 'Switch to Light'}
      </button>
    </header>
  );
}

export default Navbar;

