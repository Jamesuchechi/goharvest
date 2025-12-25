import Card from '../common/Card.jsx';

export default function StatsCards({ stats = {}, loading }) {
  const { total_jobs = 0, completed = 0, failed = 0, running = 0 } = stats;

  return (
    <div className="stats-row">
      <Card title="Total Jobs" subtitle="All time">
        <strong>{loading ? '...' : total_jobs}</strong>
      </Card>
      <Card title="Completed" subtitle="Successful">
        <strong>{loading ? '...' : completed}</strong>
      </Card>
      <Card title="Running" subtitle="In progress">
        <strong>{loading ? '...' : running}</strong>
      </Card>
      <Card title="Failed" subtitle="Needs attention">
        <strong>{loading ? '...' : failed}</strong>
      </Card>
    </div>
  );
}
