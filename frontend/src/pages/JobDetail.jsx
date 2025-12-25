import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import StatusBadge from '../components/common/StatusBadge.jsx';
import AssetGallery from '../components/results/AssetGallery.jsx';
import { jobsAPI } from '../services/api.js';

export default function JobDetail() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    let mounted = true;
    jobsAPI.get(id).then((response) => {
      if (mounted) setJob(response.data);
    }).catch(() => {});
    jobsAPI.getResult(id).then((response) => {
      if (mounted) setResult(response.data);
    }).catch(() => {});
    return () => {
      mounted = false;
    };
  }, [id]);

  return (
    <div className="page">
      <div className="section-header">
        <h2>Job Detail</h2>
        {job && <StatusBadge status={job.status} />}
      </div>
      {job && (
        <div className="panel">
          <p><strong>URL:</strong> {job.url}</p>
          <p><strong>Created:</strong> {job.created_at}</p>
          <p><strong>Options:</strong> {JSON.stringify(job.options)}</p>
        </div>
      )}
      {result && (
        <div className="panel">
          <h3>Assets</h3>
          <AssetGallery assets={result.assets || []} />
        </div>
      )}
    </div>
  );
}
