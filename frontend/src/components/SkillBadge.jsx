import React from 'react';

export default function SkillBadge({ name, skill, variant = 'matched', category, removable = false, onRemove, onClick }) {
  const skillName = name || skill || 'Skill';

  const styles = {
    matched: { bg: '#ecfdf5', text: '#047857', border: '#a7f3d0', icon: '✓' },
    missing: { bg: '#fef2f2', text: '#b91c1c', border: '#fecaca', icon: '✕' },
    partial: { bg: '#fffbeb', text: '#b45309', border: '#fde68a', icon: '!' },
    default: { bg: '#eff6ff', text: '#1d4ed8', border: '#bfdbfe', icon: '•' }
  };

  const currentStyle = styles[variant] || styles.default;

  return (
    <span
      onClick={onClick}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.375rem',
        padding: '0.3125rem 0.625rem',
        borderRadius: '0.375rem',
        fontSize: '0.8125rem',
        fontWeight: 600,
        backgroundColor: currentStyle.bg,
        color: currentStyle.text,
        border: `1px solid ${currentStyle.border}`,
        cursor: onClick ? 'pointer' : 'default',
        transition: 'all 0.15s ease'
      }}
    >
      <span style={{ fontSize: '0.75rem', fontWeight: 800 }}>{currentStyle.icon}</span>
      <span>{skillName}</span>
      {category && (
        <span style={{ opacity: 0.6, fontSize: '0.6875rem', fontWeight: 500 }}>({category})</span>
      )}
      {removable && onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove(skillName);
          }}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '0 2px',
            color: 'inherit',
            fontSize: '0.875rem',
            lineHeight: 1
          }}
        >
          &times;
        </button>
      )}
    </span>
  );
}
