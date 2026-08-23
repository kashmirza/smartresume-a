import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav style={{ background: '#ffffff', borderBottom: '1px solid #e2e8f0', position: 'sticky', top: 0, zIndex: 50 }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 1.5rem', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        
        {/* Brand */}
        <Link to={isAuthenticated ? "/dashboard" : "/"} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontWeight: 800, fontSize: '1.25rem', color: '#0f172a' }}>
          <div style={{ background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)', width: '36px', height: '36px', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff' }}>
            <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <span>SmartResume <span style={{ color: '#2563eb' }}>AI</span></span>
        </Link>

        {/* Desktop Nav Links */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" style={{ fontWeight: 500, fontSize: '0.875rem', color: isActive('/dashboard') ? '#2563eb' : '#475569' }}>
                Dashboard
              </Link>
              <Link to="/create-resume" style={{ fontWeight: 500, fontSize: '0.875rem', color: isActive('/create-resume') ? '#2563eb' : '#475569' }}>
                Build CV
              </Link>
              <Link to="/my-resumes" style={{ fontWeight: 500, fontSize: '0.875rem', color: isActive('/my-resumes') ? '#2563eb' : '#475569' }}>
                My CVs
              </Link>
              <Link to="/job-analyzer" style={{ fontWeight: 500, fontSize: '0.875rem', color: isActive('/job-analyzer') ? '#2563eb' : '#475569' }}>
                Job Analyzer
              </Link>
              <Link to="/ats-report" style={{ fontWeight: 500, fontSize: '0.875rem', color: isActive('/ats-report') ? '#2563eb' : '#475569' }}>
                ATS Report
              </Link>
            </>
          ) : (
            <>
              <Link to="/" style={{ fontWeight: 500, fontSize: '0.875rem', color: '#475569' }}>Home</Link>
              <Link to="/login" style={{ fontWeight: 500, fontSize: '0.875rem', color: '#475569' }}>Sign In</Link>
              <Link to="/register" className="btn btn-primary" style={{ fontSize: '0.875rem' }}>
                Get Started Free
              </Link>
            </>
          )}

          {/* User Menu */}
          {isAuthenticated && (
            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                style={{ background: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '9999px', padding: '0.25rem 0.75rem 0.25rem 0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}
              >
                <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: '#2563eb', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.875rem' }}>
                  {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
                </div>
                <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#0f172a' }}>{user?.full_name || 'User'}</span>
                <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {dropdownOpen && (
                <div style={{ position: 'absolute', right: 0, marginTop: '0.5rem', width: '220px', background: '#ffffff', borderRadius: '8px', boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)', border: '1px solid #e2e8f0', overflow: 'hidden', zIndex: 100 }}>
                  <div style={{ padding: '0.75rem 1rem', borderBottom: '1px solid #f1f5f9' }}>
                    <div style={{ fontSize: '0.875rem', fontWeight: 600, color: '#0f172a' }}>{user?.full_name}</div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{user?.email}</div>
                    {user?.target_role && (
                      <span className="badge badge-primary" style={{ marginTop: '0.375rem', fontSize: '0.6875rem' }}>
                        {user.target_role}
                      </span>
                    )}
                  </div>
                  <Link
                    to="/settings"
                    onClick={() => setDropdownOpen(false)}
                    style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.625rem 1rem', fontSize: '0.875rem', color: '#334155' }}
                  >
                    <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    </svg>
                    Settings & Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    style={{ width: '100%', textAlign: 'left', display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.625rem 1rem', fontSize: '0.875rem', color: '#ef4444', background: 'none', border: 'none', cursor: 'pointer', borderTop: '1px solid #f1f5f9' }}
                  >
                    <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
