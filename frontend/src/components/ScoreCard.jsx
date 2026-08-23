import React from 'react';

export default function ScoreCard({ title = "ATS Score", score = 85, breakdown = {} }) {
  const getScoreColor = (val) => {
    if (val >= 80) return { main: '#10b981', light: '#ecfdf5', text: 'Excellent Match' };
    if (val >= 60) return { main: '#f59e0b', light: '#fffbeb', text: 'Good Alignment' };
    return { main: '#ef4444', light: '#fef2f2', text: 'Needs Improvement' };
  };

  const status = getScoreColor(score);
  const strokeDashoffset = 283 - (283 * score) / 100;

  const defaultBreakdown = {
    "Keyword Match": breakdown.keyword_match || 88,
    "Formatting & Structure": breakdown.formatting || 92,
    "Experience Alignment": breakdown.experience || 80,
    "Skills Coverage": breakdown.skills || 85,
    "Impact Metrics": breakdown.impact || 75
  };

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#0f172a' }}>{title}</h3>
        <span className="badge" style={{ backgroundColor: status.light, color: status.main }}>
          {status.text}
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
        {/* Ring Chart */}
        <div style={{ position: 'relative', width: '110px', height: '110px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <svg width="110" height="110" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" strokeWidth="8" />
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke={status.main}
              strokeWidth="8"
              strokeDasharray="283"
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              transform="rotate(-90 50 50)"
              style={{ transition: 'stroke-dashoffset 0.8s ease' }}
            />
          </svg>
          <div style={{ position: 'absolute', textAlign: 'center' }}>
            <span style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a' }}>{score}%</span>
          </div>
        </div>

        {/* Quick Summary */}
        <div style={{ flex: 1 }}>
          <p style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '0.75rem' }}>
            {score >= 80
              ? 'Your resume is highly optimized for applicant tracking systems and top HR screeners.'
              : 'Add missing keywords and quantify achievements to boost your callback rate.'}
          </p>
          <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 500 }}>
            Scanned using Enterprise ATS Algorithm v4.2
          </div>
        </div>
      </div>

      {/* Sub-Scores Breakdown */}
      <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {Object.entries(defaultBreakdown).map(([label, val]) => (
          <div key={label}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8125rem', fontWeight: 600, color: '#334155', marginBottom: '0.25rem' }}>
              <span>{label}</span>
              <span>{val}%</span>
            </div>
            <div style={{ width: '100%', height: '6px', background: '#f1f5f9', borderRadius: '3px', overflow: 'hidden' }}>
              <div
                style={{
                  width: `${val}%`,
                  height: '100%',
                  backgroundColor: val >= 80 ? '#10b981' : val >= 60 ? '#f59e0b' : '#ef4444',
                  borderRadius: '3px',
                  transition: 'width 0.5s ease'
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
