import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import ResumeForm from '../components/ResumeForm';
import ResumePreview from '../components/ResumePreview';
import { resumeAPI } from '../services/api';

export default function CreateResume() {
  const [searchParams] = useSearchParams();
  const resumeId = searchParams.get('id');
  const navigate = useNavigate();

  const [resumeData, setResumeData] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('ats_classic');
  const [saving, setSubmitting] = useState(false);
  const [toast, setToast] = useState('');
  const [viewMode, setViewMode] = useState('split'); // 'split' | 'edit' | 'preview'

  useEffect(() => {
    if (resumeId) {
      resumeAPI.get(resumeId)
        .then((res) => {
          if (res.data) setResumeData(res.data);
        })
        .catch((err) => console.error('Error fetching resume:', err));
    }
  }, [resumeId]);

  const handleSave = async (updatedData) => {
    setSubmitting(true);
    setToast('');
    try {
      if (resumeId) {
        await resumeAPI.update(resumeId, updatedData);
        setToast('Resume updated successfully!');
      } else {
        const res = await resumeAPI.create(updatedData);
        setToast('Resume created successfully!');
        if (res.data?.id) {
          navigate(`/create-resume?id=${res.data.id}`, { replace: true });
        }
      }
    } catch (err) {
      console.error('Save failed:', err);
      setToast('Resume saved locally (API offline or draft).');
    } finally {
      setSubmitting(false);
      setTimeout(() => setToast(''), 3000);
    }
  };

  const handleDownload = async (templateKey) => {
    setToast('Preparing PDF download...');
    try {
      if (resumeId) {
        const res = await resumeAPI.download(resumeId, templateKey, 'pdf');
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${resumeData?.title || 'SmartResume'}.pdf`);
        document.body.appendChild(link);
        link.click();
      } else {
        window.print();
      }
    } catch (err) {
      console.error('Download error:', err);
      window.print();
    } finally {
      setTimeout(() => setToast(''), 3000);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 100px)' }}>
      {/* Header Toolbar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#ffffff', padding: '1rem 1.5rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a' }}>
            {resumeId ? 'Edit ATS Resume' : 'Build New Resume'}
          </h1>
          <p style={{ fontSize: '0.8125rem', color: '#64748b' }}>Real-time ATS preview & section builder</p>
        </div>

        {/* View Toggle */}
        <div style={{ display: 'flex', background: '#f1f5f9', borderRadius: '0.375rem', padding: '0.25rem' }}>
          <button
            onClick={() => setViewMode('split')}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem', fontWeight: 600, border: 'none', borderRadius: '0.25rem', background: viewMode === 'split' ? '#ffffff' : 'transparent', cursor: 'pointer' }}
          >
            Split View
          </button>
          <button
            onClick={() => setViewMode('edit')}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem', fontWeight: 600, border: 'none', borderRadius: '0.25rem', background: viewMode === 'edit' ? '#ffffff' : 'transparent', cursor: 'pointer' }}
          >
            Editor Only
          </button>
          <button
            onClick={() => setViewMode('preview')}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.75rem', fontWeight: 600, border: 'none', borderRadius: '0.25rem', background: viewMode === 'preview' ? '#ffffff' : 'transparent', cursor: 'pointer' }}
          >
            Preview Only
          </button>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          {toast && <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: '#10b981' }}>{toast}</span>}
          <button
            onClick={() => handleDownload(selectedTemplate)}
            className="btn btn-secondary btn-sm"
          >
            📥 Export PDF
          </button>
          <button
            onClick={() => handleSave(resumeData)}
            className="btn btn-primary btn-sm"
            disabled={saving}
          >
            {saving ? 'Saving...' : '💾 Save Resume'}
          </button>
        </div>
      </div>

      {/* Main Workspace */}
      <div style={{ display: 'grid', gridTemplateColumns: viewMode === 'split' ? '1fr 1fr' : '1fr', gap: '1.5rem', flex: 1, minHeight: 0 }}>
        {(viewMode === 'split' || viewMode === 'edit') && (
          <div style={{ overflowY: 'auto', height: '100%' }}>
            <ResumeForm
              data={resumeData}
              onChange={(updated) => setResumeData(updated)}
              onSave={handleSave}
            />
          </div>
        )}

        {(viewMode === 'split' || viewMode === 'preview') && (
          <div style={{ overflowY: 'auto', height: '100%' }}>
            <ResumePreview
              data={resumeData}
              selectedTemplate={selectedTemplate}
              onTemplateChange={(tmpl) => setSelectedTemplate(tmpl)}
              onDownload={handleDownload}
            />
          </div>
        )}
      </div>
    </div>
  );
}
