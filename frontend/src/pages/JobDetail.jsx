import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import StatusBadge from '../components/common/StatusBadge.jsx';
import AssetGallery from '../components/results/AssetGallery.jsx';
import { jobsAPI } from '../services/api.js';

export default function JobDetail() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      try {
        const jobRes = await jobsAPI.get(id);
        if (mounted) setJob(jobRes.data);
        try {
          const resultRes = await jobsAPI.getResult(id);
          if (mounted) setResult(resultRes.data);
        } catch {
          if (mounted) setResult(null);
        }
      } catch (err) {
        if (mounted) setError('Could not load this job.');
      }
    };
    load();
    const timer = setInterval(load, 4000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, [id]);

  const download = async () => {
    const response = await jobsAPI.download(id);
    const url = response.data?.download_url;
    if (url) window.open(url, '_blank');
  };

  return (
    <div className="page">
      <div className="section-header">
        <h2>Job Detail</h2>
        {job && <StatusBadge status={job.status} />}
      </div>
      {error && <p className="auth-error">{error}</p>}
      {job && (
        <div className="panel">
          <p><strong>URL:</strong> {job.url}</p>
          <p><strong>Created:</strong> {job.created_at}</p>
          {job.error_message && <p className="auth-error">{job.error_message}</p>}
          {job.status === 'completed' && (
            <button className="btn" type="button" onClick={download}>Download ZIP</button>
          )}
        </div>
      )}
      {result && (
        <div className="panel">
          <h3>Stack</h3>
          <p className="muted">
            {(result.frontend_framework || 'Unknown framework')}
            {result.css_framework ? ` · ${result.css_framework}` : ''}
          </p>
          <h3>Assets</h3>
          <AssetGallery assets={result.assets || []} />
        </div>
      )}
      {job && !result && job.status !== 'failed' && (
        <p className="muted">Harvest still running. This page refreshes automatically.</p>
      )}
    </div>
  );
}
