import Button from '../components/common/Button.jsx';

export default function BatchProcessor() {
  return (
    <div className="page">
      <div className="section-header">
        <h2>Batch Processor</h2>
      </div>
      <div className="panel">
        <p>Paste URLs or upload a CSV to run batch harvests.</p>
        <textarea className="textarea" rows="8" placeholder="https://example.com\nhttps://another.com" />
        <div className="hero-actions">
          <Button type="button">Validate</Button>
          <Button type="button" className="btn-ghost">Start Batch</Button>
        </div>
      </div>
    </div>
  );
}
