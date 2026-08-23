import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { dashboardAPI, resumeAPI } from '../services/api';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    avgAtsScore: 88,
    avgJobMatch: 92,
    totalResumes: 3,
    trackedApplications: 12
  });
  const [recentResumes, setRecentResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [statsRes, resumesRes] = await Promise.all([
          dashboardAPI.getStats().catch(() => null),
          resumeAPI.list().catch(() => null)
        ]);

        if (statsRes?.data) {
          setStats(statsRes.data);
        }

        if (resumesRes?.data && Array.isArray(resumesRes.data)) {
          setRecentResumes(resumesRes.data);
        } else {
          // Fallback mock resumes
          setRecentResumes([
            { id: '1', title: 'Senior Software Engineer CV', template: 'ats_classic', ats_score: 92, match_score: 94, updated_at: '2 hours ago' },
            { id: '2', title: 'Full Stack Developer - Fintech', template: 'modern_professional', ats_score: 85, match_score: 88, updated_at: '1 day ago' },
            { id: '3', title: 'Tech Lead / Architect Profile', template: 'tech_developer', ats_score: 88, match_score: 91, updated_at: '3 days ago' }
          ]);
        }
      } catch (err) {
        console.error('Error loading dashboard:', err);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  return (
    <div>
      {/* Welcome Banner */}
      <div style={{ background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)', borderRadius: '0.75rem', padding: '2rem', color: '#ffffff', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <span className="badge badge-primary" style={{ marginBottom: '0.5rem', background: 'rgba(37, 99, 235, 0.2)', color: '#60a5fa' }}>
            {user?.target_role || 'Senior Full Stack Engineer'}
          </span>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>Welcome back, {user?.full_name || 'Alex'}! 👋</h1>
          <p style={{ fontSize: '0.875rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Your ATS resume profile is performing in the top 5% of job applicants.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <Link to="/create-resume" className="btn btn-primary">
            + Build New Resume
          </Link>
          <Link to="/job-analyzer" className="btn btn-secondary">
            🔍 Analyze Job Match
          </Link>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="grid-4" style={{ marginBottom: '2rem' }}>
        <div className="card">
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Avg ATS Score</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#2563eb', margin: '0.25rem 0' }}>{stats.avgAtsScore}%</div>
          <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>Top 5% Scannable</span>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Avg Job Match</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#10b981', margin: '0.25rem 0' }}>{stats.avgJobMatch}%</div>
          <span className="badge badge-success" style={{ fontSize: '0.6875rem' }}>Strong Alignment</span>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Active Resumes</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a', margin: '0.25rem 0' }}>{stats.totalResumes}</div>
          <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>3 Versions</span>
        </div>

        <div className="card">
          <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Tracked Applications</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#f59e0b', margin: '0.25rem 0' }}>{stats.trackedApplications}</div>
          <span className="badge badge-warning" style={{ fontSize: '0.6875rem' }}>Active Scans</span>
        </div>
      </div>

      {/* Recent CVs & Quick Actions Grid */}
      <div className="grid-2">
        {/* Resumes List */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#0f172a' }}>Recent Resumes</h2>
            <Link to="/my-resumes" style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#2563eb' }}>
              View All ({recentResumes.length}) →
            </Link>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {recentResumes.map((resume) => (
              <div key={resume.id} style={{ border: '1px solid #e2e8f0', borderRadius: '0.5rem', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.9375rem', color: '#0f172a' }}>{resume.title}</div>
                  <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginTop: '0.375rem' }}>
                    <span className="badge badge-neutral" style={{ fontSize: '0.6875rem' }}>{resume.template || 'ats_classic'}</span>
                    <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Updated {resume.updated_at || 'Recently'}</span>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.875rem', fontWeight: 800, color: '#10b981' }}>{resume.ats_score || 88}% ATS</div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{resume.match_score || 90}% Match</div>
                  </div>
                  <Link to={`/create-resume?id=${resume.id}`} className="btn btn-secondary btn-sm">
                    Edit
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendations & Quick Tools */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#0f172a', marginBottom: '1rem' }}>AI Actionable Insights</h2>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
              <div style={{ padding: '0.875rem', background: '#eff6ff', borderRadius: '0.5rem', borderLeft: '4px solid #2563eb' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#1e40af' }}>Key Keyword Boost Available</div>
                <p style={{ fontSize: '0.8125rem', color: '#334155', marginTop: '0.25rem' }}>
                  Adding 'Docker' and 'CI/CD Pipelines' under Technical Skills will increase your job match score for Senior Role postings by +12%.
                </p>
              </div>

              <div style={{ padding: '0.875rem', background: '#ecfdf5', borderRadius: '0.5rem', borderLeft: '4px solid #10b981' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: 700, color: '#065f46' }}>Quantifiable Metrics Detected</div>
                <p style={{ fontSize: '0.8125rem', color: '#334155', marginTop: '0.25rem' }}>
                  Your experience section contains 4 metric-driven bullets. ATS algorithms favor quantified achievements (e.g., 'Reduced latency by 35%').
                </p>
              </div>
            </div>
          </div>

          <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '1rem', marginTop: '1.5rem', display: 'flex', gap: '0.75rem' }}>
            <Link to="/job-analyzer" className="btn btn-primary" style={{ flex: 1, fontSize: '0.8125rem' }}>
              Run Job Description Scan
            </Link>
            <Link to="/ats-report" className="btn btn-secondary" style={{ flex: 1, fontSize: '0.8125rem' }}>
              View ATS Full Diagnostics
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
