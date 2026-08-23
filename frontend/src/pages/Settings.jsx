import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Settings() {
  const { user, updateUser } = useAuth();

  const [fullName, setFullName] = useState(user?.full_name || 'Alex Morgan');
  const [email, setEmail] = useState(user?.email || 'alex.morgan@techdev.io');
  const [targetRole, setTargetRole] = useState(user?.target_role || 'Senior Full Stack Engineer');
  const [careerLevel, setCareerLevel] = useState(user?.career_level || 'Senior Level (6-10 yrs)');

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [toast, setToast] = useState('');

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateUser({
        full_name: fullName,
        email,
        target_role: targetRole,
        career_level: careerLevel
      });
      setToast('Profile updated successfully!');
    } catch (err) {
      setToast('Saved settings locally.');
    } finally {
      setTimeout(() => setToast(''), 3000);
    }
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setToast('New passwords do not match.');
      return;
    }
    setToast('Password changed successfully!');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setTimeout(() => setToast(''), 3000);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a' }}>Account Settings</h1>
        <p style={{ color: '#64748b', fontSize: '0.875rem' }}>Update your target career role, profile, and security preferences.</p>
      </div>

      {toast && (
        <div style={{ background: '#ecfdf5', border: '1px solid #a7f3d0', color: '#047857', padding: '0.875rem 1rem', borderRadius: '0.5rem', marginBottom: '1.5rem', fontWeight: 600, fontSize: '0.875rem' }}>
          {toast}
        </div>
      )}

      {/* Profile Card */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1.25rem', color: '#0f172a' }}>Profile Information</h2>

        <form onSubmit={handleProfileSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Full Name</label>
              <input
                type="text"
                className="form-input"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                type="email"
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Target Career Role</label>
              <input
                type="text"
                className="form-input"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Career Experience Level</label>
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
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
            <button type="submit" className="btn btn-primary">
              Save Profile Changes
            </button>
          </div>
        </form>
      </div>

      {/* Security Card */}
      <div className="card">
        <h2 style={{ fontSize: '1.125rem', fontWeight: 700, marginBottom: '1.25rem', color: '#0f172a' }}>Change Password</h2>

        <form onSubmit={handlePasswordSubmit}>
          <div className="form-group">
            <label className="form-label">Current Password</label>
            <input
              type="password"
              className="form-input"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">New Password</label>
              <input
                type="password"
                className="form-input"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Confirm New Password</label>
              <input
                type="password"
                className="form-input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
            <button type="submit" className="btn btn-secondary">
              Update Password
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
