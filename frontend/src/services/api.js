const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export async function fetchJobs() {
  const data = await request('/api/jobs/');
  return Array.isArray(data) ? data : data.results || [];
}

export async function createJob(payload) {
  return request('/api/harvest/', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function fetchJob(id) {
  return request(`/api/jobs/${id}/`);
}

export async function fetchResult(id) {
  return request(`/api/jobs/${id}/result/`);
}

export async function techDetect(url) {
  return request(`/api/tech-detect/?url=${encodeURIComponent(url)}`);
}
