import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const jobsAPI = {
  list: (params) => api.get('/jobs/', { params }),
  get: (id) => api.get(`/jobs/${id}/`),
  create: (data) => api.post('/jobs/', data),
  delete: (id) => api.delete(`/jobs/${id}/`),
  retry: (id) => api.post(`/jobs/${id}/retry/`),
  cancel: (id) => api.post(`/jobs/${id}/cancel/`),
  getResult: (id) => api.get(`/jobs/${id}/result/`),
  download: (id) => api.get(`/jobs/${id}/download/`),
  batch: (data) => api.post('/jobs/batch/', data),
  statistics: () => api.get('/jobs/statistics/'),
};

export const resultsAPI = {
  list: (params) => api.get('/results/', { params }),
  get: (id) => api.get(`/results/${id}/`),
  export: (id, format) => api.get(`/results/${id}/export/`, { params: { format } }),
  search: (tech) => api.get('/results/search/', { params: { tech } }),
  compare: (id1, id2) => api.post(`/results/${id1}/compare/`, { compare_with: id2 }),
};

export const techAPI = {
  detect: (url) => api.post('/tech-detect/', { url }),
};

export default api;
