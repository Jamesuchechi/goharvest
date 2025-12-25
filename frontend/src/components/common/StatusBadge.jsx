const toneMap = {
  pending: 'status status-pending',
  scheduled: 'status status-scheduled',
  running: 'status status-running',
  completed: 'status status-success',
  failed: 'status status-failed',
  cancelled: 'status status-cancelled',
};

export default function StatusBadge({ status }) {
  const className = toneMap[status] || 'status status-pending';
  return <span className={className}>{status}</span>;
}
