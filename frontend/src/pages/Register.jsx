import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [careerLevel, setCareerLevel] = useState('Mid Level (3-5 yrs)');
  const [targetRole, setTargetRole] = useState('Senior Full Stack Developer');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const suggestions = [
    'Software Engineer',
    'Full Stack Engineer',
    'Data Scientist',
    'Product Manager',
    'DevOps Engineer',
    'AI / ML Engineer'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    try {
      await register({
        full_name: fullName,
        email,
        password,
        career_level: careerLevel,
        target_role: targetRole
      });
      navigate('/dashboard');
    } catch (err) {
      console.error('Registration failed:', err);
      setError(err.response?.data?.message || err.response?.data?.detail || 'Registration failed. Please check your information.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ minHeight: 'calc(100vh - 64px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem 1rem', background: '#f8fafc' }}>
      <div className="card" style={{ maxWidth: '480px', width: '100%', padding: '2rem' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#0f172a' }}>Create Free Account</h1>
          <p style={{ fontSize: '0.875rem', color: '#64748b', marginTop: '0.25rem' }}>
            Build ATS-optimized resumes in seconds
          </p>
        </div>

        {error && (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: '0.75rem', borderRadius: '0.5rem', fontSize: '0.8125rem', marginBottom: '1rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              className="form-input"
              required
              placeholder="Alex Morgan"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              className="form-input"
              required
              placeholder="alex@techdev.io"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Career Level</label>
            <select
              className="form-select"
              value={careerLevel}
              onChange={(e) => setCareerLevel(e.target.value)}
            >
              <option value="Entry Level (0-2 yrs)">Entry Level (0-2 yrs)</option>
              <option value="Mid Level (3-5 yrs)">Mid Level (3-5 yrs)</option>
              <option value="Senior Level (6-10 yrs)">Senior Level (6-10 yrs)</option>
              <option value="Lead / Executive (10+ yrs)">Lead / Executive (10+ yrs)</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Target Role</label>
            <input
              type="text"
              className="form-input"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Senior Frontend Developer"
            />
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem', marginTop: '0.5rem' }}>
              {suggestions.map((sug) => (
                <button
                  type="button"
                  key={sug}
                  onClick={() => setTargetRole(sug)}
                  style={{
                    border: 'none',
                    background: '#f1f5f9',
                    color: '#475569',
                    borderRadius: '0.25rem',
                    padding: '0.125rem 0.5rem',
                    fontSize: '0.75rem',
                    cursor: 'pointer'
                  }}
                >
                  + {sug}
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '1rem' }}
            disabled={submitting}
          >
            {submitting ? 'Creating Account...' : 'Get Started'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.875rem', color: '#64748b' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#2563eb', fontWeight: 600 }}>
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}
