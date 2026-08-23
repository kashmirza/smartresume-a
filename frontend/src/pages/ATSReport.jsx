import React, { useState } from 'react';
import ScoreCard from '../components/ScoreCard';
import SkillBadge from '../components/SkillBadge';

export default function ATSReport() {
  const [selectedResume, setSelectedResume] = useState('Senior Software Engineer CV');

  const reportData = {
    overallScore: 88,
    breakdown: {
      formatting: 95,
      keyword_match: 82,
      structure: 90,
      impact: 85
    },
    parseChecklist: [
      { name: 'Contact Information Parseable', status: 'pass', details: 'Email, Phone, Location correctly extracted.' },
      { name: 'Standard Section Headings', status: 'pass', details: 'Found Experience, Education, Skills, Summary headers.' },
      { name: 'File Format Compatibility', status: 'pass', details: 'High-density PDF / Plain Text compliance verified.' },
      { name: 'Table / Graphic Obfuscation', status: 'pass', details: 'Zero complex non-scannable tables or shapes.' }
    ],
    foundKeywords: ['React.js', 'Node.js', 'Python', 'AWS', 'PostgreSQL', 'Microservices', 'REST APIs', 'CI/CD'],
    missingKeywords: ['Docker', 'Kubernetes', 'GraphQL', 'System Architecture', 'Agile Leadership'],
    recommendations: [
      { priority: 'High', text: "Incorporate 'Kubernetes' into Technical Skills or Project descriptions." },
      { priority: 'Medium', text: "Add 1-2 quantifiable outcomes to your second experience entry." },
      { priority: 'Low', text: "Keep summary text under 4 lines for optimal top-half scanner emphasis." }
    ]
  };

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a' }}>Detailed ATS Audit Report</h1>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Granular scanner parseability, header validation, and keyword impact.</p>
        </div>
        <select
          className="form-select"
          style={{ width: '280px' }}
          value={selectedResume}
          onChange={(e) => setSelectedResume(e.target.value)}
        >
          <option>Senior Software Engineer CV</option>
          <option>Full Stack Developer - Fintech</option>
          <option>Tech Lead / Architect Profile</option>
        </select>
      </div>

      <div className="grid-2" style={{ marginBottom: '2rem' }}>
        <ScoreCard
          title="Overall ATS Pass Score"
          score={reportData.overallScore}
          breakdown={reportData.breakdown}
        />

        {/* Scanner Checklist */}
        <div className="card">
          <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', color: '#0f172a' }}>
            Scanner Parseability Checklist
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
            {reportData.parseChecklist.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', background: '#f8fafc', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
                <span style={{ color: '#10b981', fontWeight: 800, fontSize: '1rem' }}>✓</span>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.875rem', color: '#0f172a' }}>{item.name}</div>
                  <div style={{ fontSize: '0.8125rem', color: '#64748b' }}>{item.details}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Keyword Diagnostic */}
      <div className="grid-2" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', color: '#047857' }}>
            ✓ Detected High-Value Keywords ({reportData.foundKeywords.length})
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
            {reportData.foundKeywords.map((kw) => (
              <SkillBadge key={kw} name={kw} variant="matched" />
            ))}
          </div>
        </div>

        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', color: '#b91c1c' }}>
            ✕ Missing Recommended Keywords ({reportData.missingKeywords.length})
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem' }}>
            {reportData.missingKeywords.map((kw) => (
              <SkillBadge key={kw} name={kw} variant="missing" />
            ))}
          </div>
        </div>
      </div>

      {/* Priorities List */}
      <div className="card">
        <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1rem', color: '#0f172a' }}>Actionable Fix Recommendations</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {reportData.recommendations.map((rec, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.875rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0', background: rec.priority === 'High' ? '#fef2f2' : '#f8fafc' }}>
              <span className={`badge ${rec.priority === 'High' ? 'badge-danger' : rec.priority === 'Medium' ? 'badge-warning' : 'badge-neutral'}`}>
                {rec.priority} Priority
              </span>
              <span style={{ fontSize: '0.875rem', fontWeight: 500, color: '#334155' }}>{rec.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
