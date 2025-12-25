import StatusBadge from '../common/StatusBadge.jsx';

export default function JobCard({ job }) {
  return (
    <div className="card">
      <div className="card-header">
        <h3>{job.url}</h3>
        <StatusBadge status={job.status} />
      </div>
      <div className="card-body">
        <p>Created: {new Date(job.created_at).toLocaleString()}</p>
        <p>Priority: {job.priority || 5}</p>
      </div>
    </div>
  );
}
