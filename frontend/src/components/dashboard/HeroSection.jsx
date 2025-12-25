import Button from '../common/Button.jsx';
import Input from '../common/Input.jsx';

export default function HeroSection({ onHarvestSubmit }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const url = form.get('url');
    if (url) {
      onHarvestSubmit?.(url.toString());
      event.currentTarget.reset();
    }
  };

  return (
    <section className="hero">
      <div className="hero-content">
        <div className="eyebrow">Frontend Intelligence</div>
        <h1>Harvest the web. Map tech stacks. Surface insights.</h1>
        <p className="subhead">
          GOharveST is your command center for scanning public websites,
          profiling performance, and extracting component libraries.
        </p>
        <form className="hero-actions" onSubmit={handleSubmit}>
          <Input name="url" placeholder="https://example.com" aria-label="URL" />
          <Button type="submit">Start Harvest</Button>
        </form>
      </div>
      <div className="hero-card">
        <h2>Quick Actions</h2>
        <p>Kick off a new scan, compare results, or review recent activity.</p>
        <div className="hero-actions">
          <Button type="button">Batch Scan</Button>
          <Button type="button" className="btn-ghost">View Reports</Button>
        </div>
      </div>
    </section>
  );
}
