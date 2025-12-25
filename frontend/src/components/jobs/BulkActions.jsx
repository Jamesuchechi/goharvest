import Button from '../common/Button.jsx';

export default function BulkActions() {
  return (
    <div className="panel bulk-actions">
      <Button type="button">Retry Selected</Button>
      <Button type="button" className="btn-ghost">Delete Selected</Button>
    </div>
  );
}
