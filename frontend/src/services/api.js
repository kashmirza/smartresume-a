import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register' && window.location.pathname !== '/') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
  updateProfile: (data) => api.put('/auth/profile', data),
  changePassword: (data) => api.put('/auth/change-password', data),
};

export const resumeAPI = {
  list: () => api.get('/resumes'),
  create: (data) => api.post('/resumes', data),
  get: (id) => api.get(`/resumes/${id}`),
  update: (id, data) => api.put(`/resumes/${id}`, data),
  delete: (id) => api.delete(`/resumes/${id}`),
  atsAnalysis: (id) => api.post(`/resumes/${id}/ats-analysis`),
  optimize: (id, jobDescription) => api.post(`/resumes/${id}/optimize`, { job_description: jobDescription }),
  download: (id, template = 'ats_classic', format = 'pdf') =>
    api.get(`/resumes/${id}/download?template=${template}&format=${format}`, { responseType: 'blob' }),
};

export const jobAPI = {
  analyze: (jobDescription) => api.post('/jobs/analyze', { job_description: jobDescription }),
  list: () => api.get('/jobs'),
  get: (id) => api.get(`/jobs/${id}`),
  match: (resumeId, jobDescription) => api.post('/jobs/match', { resume_id: resumeId, job_description: jobDescription }),
  delete: (id) => api.delete(`/jobs/${id}`),
};

export const analysisAPI = {
  skillGap: (resumeId, jobDescription) => api.post('/analysis/skill-gap', { resume_id: resumeId, job_description: jobDescription }),
  recommendations: (resumeId) => api.get(`/analysis/recommendations/${resumeId}`),
  history: () => api.get('/analysis/history'),
};

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
};

export default api;
