import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const authClient = axios.create({
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

let isRefreshing = false;
let pendingRequests = [];

const resolvePending = (token) => {
  pendingRequests.forEach((callback) => callback(token));
  pendingRequests = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refresh_token');

    if (error.response?.status === 401 && refreshToken && !originalRequest?._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          pendingRequests.push((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const response = await authClient.post('/auth/refresh/', { refresh: refreshToken });
        const newToken = response.data.access;
        localStorage.setItem('auth_token', newToken);
        resolvePending(newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        resolvePending(null);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
        window.dispatchEvent(new Event('auth:logout'));
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

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

export const authAPI = {
  register: (data) => authClient.post('/auth/register/', data),
  login: (data) => authClient.post('/auth/login/', data),
  refresh: (data) => authClient.post('/auth/refresh/', data),
  me: () => api.get('/auth/me/'),
};

export default api;
