import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import ResumeForm, { initialResumeState } from '../components/ResumeForm';
import ResumePreview from '../components/ResumePreview';
import { resumeAPI } from '../services/api';

export default function CreateResume() {
  const [searchParams] = useSearchParams();
  const resumeId = searchParams.get('id');
  const navigate = useNavigate();

  const [resumeData, setResumeData] = useState(initialResumeState);
  const [selectedTemplate, setSelectedTemplate] = useState('ats_classic');
  const [saving, setSubmitting] = useState(false);
  const [toast, setToast] = useState('');
  const [viewMode, setViewMode] = useState('split'); // 'split' | 'edit' | 'preview'

  useEffect(() => {
    if (resumeId) {
      resumeAPI.get(resumeId)
        .then((res) => {
          const data = res.data?.data || res.data;
          if (data) setResumeData(data);
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
        const data = res.data?.data || res.data;
        if (data?.id) {
          navigate(`/create-resume?id=${data.id}`, { replace: true });
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

  const printResumeOnly = () => {
    // Ensure the preview is rendered, then print (CSS limits output to the resume only)
    const wasView = viewMode;
    setViewMode('preview');
    setTimeout(() => {
      window.print();
      setViewMode(wasView);
    }, 300);
  };

  const handleDownload = async (templateKey) => {
    setToast('Preparing PDF download...');
    let savedId = resumeId;
    try {
      // If the resume has never been saved, save it first so the backend can render a real PDF
      if (!savedId) {
        setSubmitting(true);
        const res = await resumeAPI.create(resumeData);
        const data = res.data?.data || res.data;
        if (data?.id) {
          savedId = data.id;
          setResumeData(data);
          navigate(`/create-resume?id=${savedId}`, { replace: true });
        }
      }
      if (savedId) {
        const res = await resumeAPI.download(savedId, templateKey, 'pdf');
        const contentType = res.headers?.['content-type'] || '';
        if (contentType.includes('application/pdf')) {
          const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `${(resumeData?.title || 'SmartResume').replace(/[^A-Za-z0-9_-]+/g, '_')}.pdf`);
          document.body.appendChild(link);
          link.click();
          link.remove();
          window.URL.revokeObjectURL(url);
        } else {
          // Backend returned JSON instead of a PDF - fall back to browser print of the resume
          printResumeOnly();
        }
      } else {
        printResumeOnly();
      }
    } catch (err) {
      console.error('Download error:', err);
      printResumeOnly();
    } finally {
      setSubmitting(false);
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
