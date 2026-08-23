import React, { useState } from 'react';

const initialResumeState = {
  title: 'Senior Software Engineer CV',
  personal: {
    fullName: 'Alex Morgan',
    jobTitle: 'Senior Full Stack Engineer',
    email: 'alex.morgan@techdev.io',
    phone: '+1 (555) 019-2834',
    location: 'San Francisco, CA',
    linkedin: 'linkedin.com/in/alexmorgan',
    github: 'github.com/alexmorgan',
    portfolio: 'alexmorgan.dev'
  },
  summary: 'Results-driven Senior Full Stack Engineer with 6+ years of experience designing and scaling web applications, microservices, and AI-enabled platforms. Proven track record in React, Node.js, and Python, improving system throughput by 40%.',
  sectionsEnabled: {
    education: true,
    skills: true,
    experience: true,
    projects: true,
    certifications: true,
    languages: true,
    achievements: true,
    volunteer: false,
    publications: false,
    references: false
  },
  education: [
    {
      id: 1,
      institution: 'University of California, Berkeley',
      degree: 'Bachelor of Science',
      field: 'Computer Science',
      startDate: '2015',
      endDate: '2019',
      gpa: '3.8',
      description: 'Dean’s Honor List. Machine Learning Lead.'
    }
  ],
  skills: [
    { id: 1, name: 'React.js', category: 'Technical' },
    { id: 2, name: 'Node.js', category: 'Technical' },
    { id: 3, name: 'Python', category: 'Technical' },
    { id: 4, name: 'TypeScript', category: 'Technical' },
    { id: 5, name: 'PostgreSQL', category: 'Tools' },
    { id: 6, name: 'AWS & Docker', category: 'Tools' },
    { id: 7, name: 'System Architecture', category: 'Soft' },
    { id: 8, name: 'Agile Leadership', category: 'Soft' }
  ],
  experience: [
    {
      id: 1,
      company: 'Apex Cloud Solutions',
      position: 'Senior Software Engineer',
      location: 'San Francisco, CA',
      startDate: '2021-03',
      endDate: 'Present',
      current: true,
      description: '• Architected high-throughput REST & GraphQL APIs processing 5M daily requests.\n• Led migration from legacy monolith to React micro-frontends, cutting page load time by 35%.\n• Mentored 6 junior engineers and implemented CI/CD pipelines reducing deployment friction.'
    },
    {
      id: 2,
      company: 'ByteTech Inc.',
      position: 'Full Stack Developer',
      location: 'San Jose, CA',
      startDate: '2019-06',
      endDate: '2021-02',
      current: false,
      description: '• Developed customer-facing React dashboard used by 120,000 active monthly users.\n• Integrated stripe payment workflows and real-time analytics using Python/FastAPI.'
    }
  ],
  projects: [
    {
      id: 1,
      name: 'SmartResume AI Platform',
      role: 'Lead Developer',
      techStack: 'React, Python FastAPI, OpenAI API',
      link: 'github.com/alexmorgan/smartresume',
      description: 'Built an AI-powered resume analyzer matching resumes to job descriptions with ATS skill gap highlighting.'
    }
  ],
  certifications: [
    { id: 1, name: 'AWS Certified Solutions Architect - Associate', issuer: 'Amazon Web Services', date: '2023' }
  ],
  languages: [
    { id: 1, language: 'English', proficiency: 'Native' },
    { id: 2, language: 'Spanish', proficiency: 'Intermediate' }
  ],
  achievements: [
    { id: 1, title: 'Hackathon Winner - Top AI Application', issuer: 'SF Tech Summit', date: '2023' }
  ],
  volunteer: [
    { id: 1, organization: 'Code for Good', role: 'Volunteer Web Mentor', dates: '2022 - Present', description: 'Taught web dev to underrepresented youth.' }
  ],
  publications: [
    { id: 1, title: 'Optimizing React Rendering for High-Frequency Data Streams', publisher: 'Medium Tech Blog', date: '2022', link: 'https://medium.com' }
  ],
  references: [
    { id: 1, name: 'Sarah Jenkins', title: 'VP of Engineering', company: 'Apex Cloud', contact: 's.jenkins@apex.io' }
  ]
};

export default function ResumeForm({ data, onChange, onSave }) {
  const formData = data || initialResumeState;
  const [activeTab, setActiveTab] = useState('personal');

  const updatePersonal = (field, value) => {
    onChange({
      ...formData,
      personal: { ...formData.personal, [field]: value }
    });
  };

  const toggleSection = (sectionKey) => {
    onChange({
      ...formData,
      sectionsEnabled: {
        ...formData.sectionsEnabled,
        [sectionKey]: !formData.sectionsEnabled[sectionKey]
      }
    });
  };

  const handleArrayAdd = (key, defaultItem) => {
    const list = formData[key] || [];
    onChange({
      ...formData,
      [key]: [...list, { ...defaultItem, id: Date.now() }]
    });
  };

  const handleArrayUpdate = (key, id, field, value) => {
    const list = formData[key] || [];
    const updated = list.map((item) => (item.id === id ? { ...item, [field]: value } : item));
    onChange({ ...formData, [key]: updated });
  };

  const handleArrayRemove = (key, id) => {
    const list = formData[key] || [];
    onChange({ ...formData, [key]: list.filter((item) => item.id !== id) });
  };

  const tabs = [
    { id: 'personal', label: 'Personal Info' },
    { id: 'summary', label: 'Summary' },
    { id: 'experience', label: 'Experience' },
    { id: 'education', label: 'Education' },
    { id: 'skills', label: 'Skills' },
    { id: 'projects', label: 'Projects' },
    { id: 'more', label: 'More Sections' }
  ];

  return (
    <div style={{ background: '#ffffff', borderRadius: '0.5rem', border: '1px solid #e2e8f0', overflow: 'hidden' }}>
      {/* Header & Section Tabs */}
      <div style={{ padding: '1.25rem', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#f8fafc' }}>
        <div>
          <h2 style={{ fontSize: '1.125rem', fontWeight: 700, color: '#0f172a' }}>Resume Details</h2>
          <p style={{ fontSize: '0.8125rem', color: '#64748b' }}>Fill in your credentials to build an ATS-scannable CV.</p>
        </div>
        <button
          onClick={() => onChange(initialResumeState)}
          className="btn btn-secondary btn-sm"
        >
          Load Demo Sample
        </button>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', borderBottom: '1px solid #e2e8f0', background: '#ffffff', overflowX: 'auto' }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '0.75rem 1rem',
              fontSize: '0.8125rem',
              fontWeight: 600,
              color: activeTab === tab.id ? '#2563eb' : '#64748b',
              borderBottom: activeTab === tab.id ? '2px solid #2563eb' : '2px solid transparent',
              background: 'none',
              borderLeft: 'none',
              borderRight: 'none',
              borderTop: 'none',
              cursor: 'pointer',
              whiteSpace: 'nowrap'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Form Content */}
      <div style={{ padding: '1.5rem' }}>
        {/* Personal Info Tab */}
        {activeTab === 'personal' && (
          <div>
            <div className="form-group">
              <label className="form-label">Resume Title</label>
              <input
                type="text"
                className="form-input"
                value={formData.title || ''}
                onChange={(e) => onChange({ ...formData, title: e.target.value })}
                placeholder="e.g. Senior Frontend Engineer Resume"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Full Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.fullName || ''}
                  onChange={(e) => updatePersonal('fullName', e.target.value)}
                  placeholder="John Doe"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Job Title / Target Role</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.jobTitle || ''}
                  onChange={(e) => updatePersonal('jobTitle', e.target.value)}
                  placeholder="Software Engineer"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-input"
                  value={formData.personal.email || ''}
                  onChange={(e) => updatePersonal('email', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Phone</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.phone || ''}
                  onChange={(e) => updatePersonal('phone', e.target.value)}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Location (City, State/Country)</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.location || ''}
                  onChange={(e) => updatePersonal('location', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">LinkedIn URL</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.linkedin || ''}
                  onChange={(e) => updatePersonal('linkedin', e.target.value)}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">GitHub URL</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.github || ''}
                  onChange={(e) => updatePersonal('github', e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Portfolio Website</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.personal.portfolio || ''}
                  onChange={(e) => updatePersonal('portfolio', e.target.value)}
                />
              </div>
            </div>
          </div>
        )}

        {/* Summary Tab */}
        {activeTab === 'summary' && (
          <div>
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <label className="form-label" style={{ marginBottom: 0 }}>Professional Summary</label>
                <button
                  type="button"
                  className="btn btn-outline btn-sm"
                  onClick={() => {
                    onChange({
                      ...formData,
                      summary: `High-performing ${formData.personal.jobTitle || 'Professional'} with proven success driving impactful initiatives, streamlining workflows, and optimizing core operational metrics. Skilled in cross-functional collaboration and technical innovation.`
                    });
                  }}
                >
                  ✨ AI Auto-Generate
                </button>
              </div>
              <textarea
                className="form-textarea"
                rows="5"
                value={formData.summary || ''}
                onChange={(e) => onChange({ ...formData, summary: e.target.value })}
                placeholder="Write 2-4 sentences highlighting your years of experience, core expertise, and key measurable achievements..."
              />
            </div>
          </div>
        )}

        {/* Work Experience Tab */}
        {activeTab === 'experience' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Work Experience</h3>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() =>
                  handleArrayAdd('experience', {
                    company: '',
                    position: '',
                    location: '',
                    startDate: '',
                    endDate: '',
                    current: false,
                    description: ''
                  })
                }
              >
                + Add Experience
              </button>
            </div>

            {(formData.experience || []).map((exp, index) => (
              <div key={exp.id || index} style={{ border: '1px solid #e2e8f0', borderRadius: '0.5rem', padding: '1rem', marginBottom: '1rem', background: '#fafafa' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.875rem' }}>Position #{index + 1}</span>
                  <button
                    type="button"
                    onClick={() => handleArrayRemove('experience', exp.id)}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '0.8125rem' }}
                  >
                    Delete
                  </button>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Company Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={exp.company}
                      onChange={(e) => handleArrayUpdate('experience', exp.id, 'company', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Position Title</label>
                    <input
                      type="text"
                      className="form-input"
                      value={exp.position}
                      onChange={(e) => handleArrayUpdate('experience', exp.id, 'position', e.target.value)}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Start Date</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="e.g. 2021-03"
                      value={exp.startDate}
                      onChange={(e) => handleArrayUpdate('experience', exp.id, 'startDate', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">End Date</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="e.g. Present"
                      value={exp.endDate}
                      onChange={(e) => handleArrayUpdate('experience', exp.id, 'endDate', e.target.value)}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Key Responsibilities & Measurable Achievements</label>
                  <textarea
                    className="form-textarea"
                    rows="3"
                    value={exp.description}
                    onChange={(e) => handleArrayUpdate('experience', exp.id, 'description', e.target.value)}
                    placeholder="• Achieved 30% speedup by optimizing database queries&#10;• Led team of 5 engineers..."
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Education Tab */}
        {activeTab === 'education' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Education</h3>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() =>
                  handleArrayAdd('education', {
                    institution: '',
                    degree: '',
                    field: '',
                    startDate: '',
                    endDate: '',
                    gpa: '',
                    description: ''
                  })
                }
              >
                + Add Education
              </button>
            </div>

            {(formData.education || []).map((edu, index) => (
              <div key={edu.id || index} style={{ border: '1px solid #e2e8f0', borderRadius: '0.5rem', padding: '1rem', marginBottom: '1rem', background: '#fafafa' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.875rem' }}>Education #{index + 1}</span>
                  <button
                    type="button"
                    onClick={() => handleArrayRemove('education', edu.id)}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '0.8125rem' }}
                  >
                    Delete
                  </button>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Institution / University</label>
                    <input
                      type="text"
                      className="form-input"
                      value={edu.institution}
                      onChange={(e) => handleArrayUpdate('education', edu.id, 'institution', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Degree</label>
                    <input
                      type="text"
                      className="form-input"
                      value={edu.degree}
                      onChange={(e) => handleArrayUpdate('education', edu.id, 'degree', e.target.value)}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Field of Study</label>
                    <input
                      type="text"
                      className="form-input"
                      value={edu.field}
                      onChange={(e) => handleArrayUpdate('education', edu.id, 'field', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Graduation Year</label>
                    <input
                      type="text"
                      className="form-input"
                      value={edu.endDate}
                      onChange={(e) => handleArrayUpdate('education', edu.id, 'endDate', e.target.value)}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Skills Tab */}
        {activeTab === 'skills' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Categorized Skills</h3>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() =>
                  handleArrayAdd('skills', { name: '', category: 'Technical' })
                }
              >
                + Add Skill
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
              {(formData.skills || []).map((sk, index) => (
                <div key={sk.id || index} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', background: '#f8fafc', padding: '0.5rem', borderRadius: '0.375rem', border: '1px solid #e2e8f0' }}>
                  <input
                    type="text"
                    className="form-input"
                    style={{ flex: 1, padding: '0.375rem 0.5rem' }}
                    value={sk.name}
                    onChange={(e) => handleArrayUpdate('skills', sk.id, 'name', e.target.value)}
                    placeholder="Skill name"
                  />
                  <select
                    className="form-select"
                    style={{ width: '110px', padding: '0.375rem 0.25rem' }}
                    value={sk.category || 'Technical'}
                    onChange={(e) => handleArrayUpdate('skills', sk.id, 'category', e.target.value)}
                  >
                    <option value="Technical">Technical</option>
                    <option value="Tools">Tools</option>
                    <option value="Soft">Soft</option>
                  </select>
                  <button
                    type="button"
                    onClick={() => handleArrayRemove('skills', sk.id)}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '0 4px' }}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Projects Tab */}
        {activeTab === 'projects' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Key Projects</h3>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() =>
                  handleArrayAdd('projects', { name: '', role: '', techStack: '', link: '', description: '' })
                }
              >
                + Add Project
              </button>
            </div>

            {(formData.projects || []).map((proj, index) => (
              <div key={proj.id || index} style={{ border: '1px solid #e2e8f0', borderRadius: '0.5rem', padding: '1rem', marginBottom: '1rem', background: '#fafafa' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.875rem' }}>Project #{index + 1}</span>
                  <button
                    type="button"
                    onClick={() => handleArrayRemove('projects', proj.id)}
                    style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '0.8125rem' }}
                  >
                    Delete
                  </button>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">Project Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={proj.name}
                      onChange={(e) => handleArrayUpdate('projects', proj.id, 'name', e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Tech Stack</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="React, Python, AWS"
                      value={proj.techStack}
                      onChange={(e) => handleArrayUpdate('projects', proj.id, 'techStack', e.target.value)}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Project Summary & Impact</label>
                  <textarea
                    className="form-textarea"
                    rows="2"
                    value={proj.description}
                    onChange={(e) => handleArrayUpdate('projects', proj.id, 'description', e.target.value)}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* More Sections Toggles */}
        {activeTab === 'more' && (
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>Enable Optional Resume Sections</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
              {[
                { key: 'certifications', label: 'Certifications' },
                { key: 'languages', label: 'Languages' },
                { key: 'achievements', label: 'Achievements & Awards' },
                { key: 'volunteer', label: 'Volunteer Experience' },
                { key: 'publications', label: 'Publications' },
                { key: 'references', label: 'References' }
              ].map((sec) => (
                <label
                  key={sec.key}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.75rem 1rem',
                    border: '1px solid #e2e8f0',
                    borderRadius: '0.5rem',
                    cursor: 'pointer',
                    background: formData.sectionsEnabled[sec.key] ? '#eff6ff' : '#ffffff'
                  }}
                >
                  <input
                    type="checkbox"
                    checked={!!formData.sectionsEnabled[sec.key]}
                    onChange={() => toggleSection(sec.key)}
                  />
                  <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#0f172a' }}>{sec.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Action Button */}
        <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
          {onSave && (
            <button type="button" onClick={() => onSave(formData)} className="btn btn-primary">
              💾 Save Resume Changes
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
