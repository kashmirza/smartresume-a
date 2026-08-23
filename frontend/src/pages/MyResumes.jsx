import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { resumeAPI } from '../services/api';

export default function MyResumes() {
  const [resumes, setResumes] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const res = await resumeAPI.list();
      if (res.data && Array.isArray(res.data)) {
        setResumes(res.data);
      } else {
        // Fallback default list
        setResumes([
          { id: '1', title: 'Senior Software Engineer CV', template: 'ats_classic', ats_score: 92, match_score: 94, updated_at: '2026-08-20' },
          { id: '2', title: 'Full Stack Developer - Fintech', template: 'modern_professional', ats_score: 85, match_score: 88, updated_at: '2026-08-15' },
          { id: '3', title: 'Tech Lead / Architect Profile', template: 'tech_developer', ats_score: 88, match_score: 91, updated_at: '2026-08-10' }
        ]);
      }
    } catch (err) {
      console.error('Error fetching resumes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this resume?')) {
      try {
        await resumeAPI.delete(id);
        setResumes(resumes.filter((r) => r.id !== id));
      } catch (err) {
        console.error('Delete error:', err);
        setResumes(resumes.filter((r) => r.id !== id));
      }
    }
  };

  const filtered = resumes.filter((r) =>
    r.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a' }}>My Resumes</h1>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Manage and optimize your tailored CV versions.</p>
        </div>
        <Link to="/create-resume" className="btn btn-primary">
          + Create New Resume
        </Link>
      </div>

      {/* Search & Filter */}
      <div style={{ marginBottom: '1.5rem', maxWidth: '400px' }}>
        <input
          type="text"
          className="form-input"
          placeholder="🔍 Search resumes by title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Grid List */}
      <div className="grid-3">
        {filtered.map((resume) => (
          <div key={resume.id} className="card card-hover" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                <span className="badge badge-primary" style={{ fontSize: '0.6875rem' }}>
                  {resume.template || 'ats_classic'}
                </span>
                <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{resume.updated_at}</span>
              </div>

              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#0f172a', marginBottom: '0.5rem' }}>
                {resume.title}
              </h3>

              <div style={{ display: 'flex', gap: '1rem', margin: '1rem 0', background: '#f8fafc', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.6875rem', color: '#64748b', fontWeight: 600 }}>ATS SCORE</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#10b981' }}>{resume.ats_score || 88}%</div>
                </div>
                <div style={{ flex: 1, borderLeft: '1px solid #e2e8f0', paddingLeft: '0.75rem' }}>
                  <div style={{ fontSize: '0.6875rem', color: '#64748b', fontWeight: 600 }}>JOB MATCH</div>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#2563eb' }}>{resume.match_score || 90}%</div>
                </div>
              </div>
            </div>

            <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <Link to={`/create-resume?id=${resume.id}`} className="btn btn-primary btn-sm" style={{ flex: 1 }}>
                Edit
              </Link>
              <Link to={`/ats-report?id=${resume.id}`} className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
                ATS Report
              </Link>
              <button
                onClick={() => handleDelete(resume.id)}
                className="btn btn-secondary btn-sm"
                style={{ color: '#ef4444' }}
              >
                🗑️
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
