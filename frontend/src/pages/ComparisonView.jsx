import Button from '../components/common/Button.jsx';

export default function ComparisonView() {
  return (
    <div className="page">
      <div className="section-header">
        <h2>Comparison View</h2>
      </div>
      <div className="panel">
        <p>Select two results to compare HTML, tech stack, and performance.</p>
        <div className="hero-actions">
          <Button type="button">Select Result A</Button>
          <Button type="button" className="btn-ghost">Select Result B</Button>
        </div>
      </div>
    </div>
  );
}
