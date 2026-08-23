import React, { useState } from 'react';

export default function ResumePreview({ data, selectedTemplate, onTemplateChange, onDownload }) {
  const [template, setTemplate] = useState(selectedTemplate || 'ats_classic');

  const handleTemplateSelect = (tmplKey) => {
    setTemplate(tmplKey);
    if (onTemplateChange) onTemplateChange(tmplKey);
  };

  const resume = data || {};
  const personal = resume.personal || {};
  const enabled = resume.sectionsEnabled || { education: true, skills: true, experience: true, projects: true, certifications: true, languages: true };

  const templatesList = [
    { id: 'ats_classic', name: 'ATS Classic', badge: 'Recommended' },
    { id: 'modern_professional', name: 'Modern Pro', badge: 'Popular' },
    { id: 'minimal', name: 'Minimal', badge: 'Clean' },
    { id: 'tech_developer', name: 'Tech Developer', badge: 'Code Focus' },
    { id: 'data_analytics', name: 'Data / Analytics', badge: 'Metrics' }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Template Selector Toolbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#ffffff', padding: '0.875rem 1.25rem', border: '1px solid #e2e8f0', borderRadius: '0.5rem 0.5rem 0 0', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: '#64748b' }}>TEMPLATE:</span>
          <div style={{ display: 'flex', gap: '0.375rem', flexWrap: 'wrap' }}>
            {templatesList.map((t) => (
              <button
                key={t.id}
                onClick={() => handleTemplateSelect(t.id)}
                style={{
                  padding: '0.375rem 0.75rem',
                  borderRadius: '0.375rem',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  border: '1px solid',
                  borderColor: template === t.id ? '#2563eb' : '#cbd5e1',
                  background: template === t.id ? '#eff6ff' : '#ffffff',
                  color: template === t.id ? '#2563eb' : '#475569',
                  cursor: 'pointer'
                }}
              >
                {t.name}
              </button>
            ))}
          </div>
        </div>

        {onDownload && (
          <button onClick={() => onDownload(template)} className="btn btn-primary btn-sm">
            📥 Export PDF
          </button>
        )}
      </div>

      {/* Render Canvas */}
      <div style={{ flex: 1, background: '#e2e8f0', padding: '1.5rem', overflowY: 'auto', border: '1px solid #e2e8f0', borderTop: 'none', borderRadius: '0 0 0.5rem 0.5rem' }}>
        <div
          id="resume-canvas"
          style={{
            maxWidth: '800px',
            margin: '0 auto',
            background: '#ffffff',
            boxShadow: '0 10px 25px -5px rgba(0,0,0,0.15)',
            padding: template === 'minimal' ? '3rem 2.5rem' : '2.5rem 2.25rem',
            fontFamily: template === 'tech_developer' ? "'JetBrains Mono', monospace, sans-serif" : "'Inter', sans-serif",
            color: '#1e293b',
            lineHeight: 1.5,
            minHeight: '900px'
          }}
        >
          {/* Header */}
          <header style={{ borderBottom: template === 'modern_professional' ? '3px solid #2563eb' : '1px solid #cbd5e1', paddingBottom: '1rem', marginBottom: '1.25rem', textAlign: template === 'ats_classic' ? 'center' : 'left' }}>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.025em' }}>
              {personal.fullName || 'YOUR NAME'}
            </h1>
            <div style={{ fontSize: '1.0625rem', fontWeight: 600, color: '#2563eb', marginTop: '0.25rem' }}>
              {personal.jobTitle || 'Target Professional Role'}
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', justifyContent: template === 'ats_classic' ? 'center' : 'flex-start', fontSize: '0.8125rem', color: '#64748b', marginTop: '0.5rem' }}>
              {personal.email && <span>{personal.email}</span>}
              {personal.phone && <span>• {personal.phone}</span>}
              {personal.location && <span>• {personal.location}</span>}
              {personal.linkedin && <span>• {personal.linkedin}</span>}
              {personal.github && <span>• {personal.github}</span>}
            </div>
          </header>

          {/* Summary */}
          {resume.summary && (
            <section style={{ marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.25rem', marginBottom: '0.5rem' }}>
                Professional Summary
              </h2>
              <p style={{ fontSize: '0.84375rem', color: '#334155' }}>{resume.summary}</p>
            </section>
          )}

          {/* Experience */}
          {enabled.experience && resume.experience && resume.experience.length > 0 && (
            <section style={{ marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.25rem', marginBottom: '0.75rem' }}>
                Work Experience
              </h2>
              {resume.experience.map((exp, idx) => (
                <div key={idx} style={{ marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.875rem', color: '#0f172a' }}>{exp.position}</span>
                    <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>{exp.startDate} – {exp.endDate}</span>
                  </div>
                  <div style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#2563eb', marginBottom: '0.25rem' }}>
                    {exp.company} {exp.location ? `| ${exp.location}` : ''}
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: '#334155', whiteSpace: 'pre-line' }}>
                    {exp.description}
                  </div>
                </div>
              ))}
            </section>
          )}

          {/* Skills */}
          {enabled.skills && resume.skills && resume.skills.length > 0 && (
            <section style={{ marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.25rem', marginBottom: '0.5rem' }}>
                Skills & Technical Expertise
              </h2>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {resume.skills.map((sk, idx) => (
                  <span
                    key={idx}
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: 600,
                      background: '#f1f5f9',
                      color: '#0f172a',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.25rem',
                      border: '1px solid #e2e8f0'
                    }}
                  >
                    {sk.name}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* Education */}
          {enabled.education && resume.education && resume.education.length > 0 && (
            <section style={{ marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.25rem', marginBottom: '0.5rem' }}>
                Education
              </h2>
              {resume.education.map((edu, idx) => (
                <div key={idx} style={{ marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.84375rem', color: '#0f172a' }}>{edu.degree} in {edu.field}</div>
                    <div style={{ fontSize: '0.8125rem', color: '#64748b' }}>{edu.institution}</div>
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>{edu.endDate}</div>
                </div>
              ))}
            </section>
          )}

          {/* Projects */}
          {enabled.projects && resume.projects && resume.projects.length > 0 && (
            <section style={{ marginBottom: '1.25rem' }}>
              <h2 style={{ fontSize: '0.9375rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '0.25rem', marginBottom: '0.5rem' }}>
                Projects
              </h2>
              {resume.projects.map((p, idx) => (
                <div key={idx} style={{ marginBottom: '0.75rem' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.84375rem', color: '#0f172a' }}>
                    {p.name} <span style={{ fontWeight: 500, color: '#64748b', fontSize: '0.75rem' }}>({p.techStack})</span>
                  </div>
                  <div style={{ fontSize: '0.8125rem', color: '#334155' }}>{p.description}</div>
                </div>
              ))}
            </section>
          )}
        </div>
      </div>
    </div>
  );
}
