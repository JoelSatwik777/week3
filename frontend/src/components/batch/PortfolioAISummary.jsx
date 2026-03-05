import React from 'react';

// Render the AI summary text as a set of sections with headings and bullet lists
function PortfolioAISummary({ report }) {
  if (!report) return null;

  const sections = [];
  let current = { title: 'Overview', items: [] };
  sections.push(current);

  report.split('\n').forEach((raw) => {
    const line = raw.trim();
    if (!line) return;

    if (line.startsWith('**') && line.endsWith('**')) {
      const title = line.slice(2, -2);
      current = { title, items: [] };
      sections.push(current);
    } else if (line.startsWith('- ')) {
      current.items.push({ type: 'bullet', text: line.slice(2) });
    } else {
      current.items.push({ type: 'text', text: line });
    }
  });

  return (
    <div className="ai-summary-report">
      {sections.map((sec, idx) => (
        <div key={idx} className="ai-summary-section">
          <div className="summary-section-header">
            <span className="section-icon">📌</span>
            <h4 className="summary-section-title">{sec.title}</h4>
          </div>
          <div className="summary-section-content">
            {sec.items.some((it) => it.type === 'bullet') ? (
              <ul className="summary-list">
                {sec.items.map((it, iidx) =>
                  it.type === 'bullet' ? (
                    <li key={iidx} className="summary-bullet">
                      {it.text}
                    </li>
                  ) : (
                    <p key={iidx}>{it.text}</p>
                  )
                )}
              </ul>
            ) : (
              sec.items.map((it, iidx) => (
                <p key={iidx}>{it.text}</p>
              ))
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default PortfolioAISummary;
