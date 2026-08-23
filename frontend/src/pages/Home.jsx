import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div style={{ background: '#f8fafc', color: '#0f172a' }}>
      {/* Hero Section */}
      <section style={{ padding: '5rem 1.5rem 4rem', maxWidth: '1200px', margin: '0 auto', textAlign: 'center' }}>
        <div className="badge badge-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
          ⚡ Powered by Advanced AI ATS Scoring Algorithms
        </div>
        <h1 style={{ fontSize: '3rem', fontWeight: 800, lineHeight: 1.15, letterSpacing: '-0.03em', marginBottom: '1.25rem', color: '#0f172a' }}>
          Land 3x More Interviews with <br />
          <span style={{ color: '#2563eb' }}>ATS-Optimized Resumes</span>
        </h1>
        <p style={{ fontSize: '1.125rem', color: '#475569', maxWidth: '720px', margin: '0 auto 2.5rem', lineHeight: 1.6 }}>
          SmartResume AI benchmarks your CV against job descriptions, identifies critical skill gaps, and formats your resume to pass enterprise Applicant Tracking Systems effortless.
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link to={isAuthenticated ? "/dashboard" : "/register"} className="btn btn-primary btn-lg">
            Build Your Resume Free →
          </Link>
          <Link to={isAuthenticated ? "/job-analyzer" : "/login"} className="btn btn-secondary btn-lg">
            Try Job Matcher
          </Link>
        </div>

        {/* Stats Banner */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', marginTop: '4rem', padding: '2rem', background: '#ffffff', borderRadius: '1rem', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#2563eb' }}>98%</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: '#64748b' }}>ATS Parse Success Rate</div>
          </div>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#10b981' }}>3.5x</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: '#64748b' }}>More Interview Callbacks</div>
          </div>
          <div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#0f172a' }}>15,000+</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: '#64748b' }}>Resumes & Job Matches</div>
          </div>
        </div>
      </section>

      {/* Feature Showcase */}
      <section style={{ padding: '4rem 1.5rem', background: '#ffffff', borderTop: '1px solid #e2e8f0', borderBottom: '1px solid #e2e8f0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a' }}>Everything You Need to Beat the ATS</h2>
            <p style={{ color: '#64748b', fontSize: '1rem', marginTop: '0.5rem' }}>Designed for engineers, product managers, data scientists, and ambitious professionals.</p>
          </div>

          <div className="grid-3">
            <div className="card">
              <div style={{ width: '48px', height: '48px', background: '#eff6ff', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#2563eb', fontWeight: 800, fontSize: '1.25rem', marginBottom: '1rem' }}>
                📄
              </div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Multi-Template Resume Builder</h3>
              <p style={{ fontSize: '0.875rem', color: '#64748b', lineHeight: 1.6 }}>
                Choose from ATS Classic, Modern Pro, Tech Developer, and Data templates built specifically to adhere to ATS parsing rules.
              </p>
            </div>

            <div className="card">
              <div style={{ width: '48px', height: '48px', background: '#ecfdf5', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#10b981', fontWeight: 800, fontSize: '1.25rem', marginBottom: '1rem' }}>
                🎯
              </div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Job Description Analyzer</h3>
              <p style={{ fontSize: '0.875rem', color: '#64748b', lineHeight: 1.6 }}>
                Paste any job listing to extract key requirements, missing technical skills, and essential industry keywords instantly.
              </p>
            </div>

            <div className="card">
              <div style={{ width: '48px', height: '48px', background: '#fffbeb', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#f59e0b', fontWeight: 800, fontSize: '1.25rem', marginBottom: '1rem' }}>
                📊
              </div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '0.5rem' }}>Detailed ATS Score Breakdown</h3>
              <p style={{ fontSize: '0.875rem', color: '#64748b', lineHeight: 1.6 }}>
                Get an instant overall ATS score with granular feedback on formatting, keyword density, section headers, and measurable impact.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section style={{ padding: '4rem 1.5rem', maxWidth: '1200px', margin: '0 auto', textAlign: 'center' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: 800, color: '#0f172a', marginBottom: '2.5rem' }}>3 Simple Steps to Your Next Role</h2>
        <div className="grid-3">
          <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
            <span className="badge badge-primary" style={{ marginBottom: '0.75rem' }}>Step 1</span>
            <h4 style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '0.5rem' }}>Input Experience</h4>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>Enter your work history, skills, education, and achievements into our structured builder.</p>
          </div>
          <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
            <span className="badge badge-primary" style={{ marginBottom: '0.75rem' }}>Step 2</span>
            <h4 style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '0.5rem' }}>Scan Job Description</h4>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>Paste the job listing to automatically identify missing skills and match percentage.</p>
          </div>
          <div style={{ background: '#ffffff', padding: '1.5rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}>
            <span className="badge badge-primary" style={{ marginBottom: '0.75rem' }}>Step 3</span>
            <h4 style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '0.5rem' }}>Optimize & Apply</h4>
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>Export your ATS-tested PDF and apply with confidence to land interviews faster.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
