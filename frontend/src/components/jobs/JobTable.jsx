import StatusBadge from '../common/StatusBadge.jsx';

export default function JobTable({ jobs = [], onSelect }) {
  return (
    <div className="table">
      <div className="table-row table-header">
        <span>URL</span>
        <span>Status</span>
        <span>Created</span>
        <span>Actions</span>
      </div>
      {jobs.map((job) => (
        <div key={job.id} className="table-row">
          <span>{job.url}</span>
          <span><StatusBadge status={job.status} /></span>
          <span>{new Date(job.created_at).toLocaleString()}</span>
          <button className="link-button" onClick={() => onSelect?.(job)}>View</button>
        </div>
      ))}
    </div>
  );
}
