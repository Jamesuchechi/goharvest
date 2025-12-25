import StatusBadge from '../common/StatusBadge.jsx';

export default function RecentJobs({ jobs = [], loading, onSelect }) {
  if (loading) {
    return <div className="panel">Loading recent jobs...</div>;
  }

  if (!jobs.length) {
    return <div className="panel">No jobs yet. Start a new harvest.</div>;
  }

  return (
    <div className="panel list-panel">
      {jobs.map((job) => (
        <button key={job.id} className="list-item" onClick={() => onSelect?.(job)}>
          <div>
            <strong>{job.url}</strong>
            <span>{new Date(job.created_at).toLocaleString()}</span>
          </div>
          <StatusBadge status={job.status} />
        </button>
      ))}
    </div>
  );
}
