import Button from '../common/Button.jsx';

export default function QuickActions() {
  return (
    <div className="panel quick-actions">
      <h3>Quick Actions</h3>
      <div className="hero-actions">
        <Button type="button">New Scan</Button>
        <Button type="button" className="btn-ghost">Compare Results</Button>
        <Button type="button" className="btn-ghost">Export Report</Button>
      </div>
    </div>
  );
}
