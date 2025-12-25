import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.js';

export default function Landing() {
  const { token } = useAuth();

  if (token) {
    return <Navigate to="/app" replace />;
  }

  return (
    <div className="landing">
      <header className="landing-nav">
        <Link className="brand" to="/">
          <span className="brand-mark">GO</span>
          <span>harveST</span>
        </Link>
        <nav className="landing-links">
          <a href="#story">Story</a>
          <a href="#features">Capabilities</a>
          <a href="#testimonials">Teams</a>
          <Link to="/login" className="ghost small">
            Login
          </Link>
          <Link to="/register" className="primary">
            Get started
          </Link>
        </nav>
      </header>

      <section className="landing-hero">
        <div className="hero-copy">
          <span className="landing-badge">Harvest intelligence, not just HTML</span>
          <h1>Turn any website into a living product brief.</h1>
          <p className="landing-subtitle">
            GOharveST captures structure, design systems, assets, and performance signals so you can
            benchmark, rebuild, or study competitors in hours instead of weeks.
          </p>
          <div className="landing-cta">
            <Link to="/register" className="primary">
              Start your first harvest
            </Link>
            <Link to="/login" className="ghost">
              I already have access
            </Link>
          </div>
          <div className="landing-metrics">
            <div>
              <strong>2 min</strong>
              <span>Average harvest kickoff</span>
            </div>
            <div>
              <strong>40+</strong>
              <span>Signals per site</span>
            </div>
            <div>
              <strong>100%</strong>
              <span>Traceable outputs</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-card">
            <p className="hero-card-title">Live Harvest Feed</p>
            <div className="hero-card-row">
              <span className="pill running">Running</span>
              <span>brandsite.com</span>
            </div>
            <div className="hero-card-row">
              <span className="pill success">Completed</span>
              <span>fintech.io</span>
            </div>
            <div className="hero-card-row">
              <span className="pill pending">Queued</span>
              <span>productlab.ai</span>
            </div>
            <div className="hero-card-highlight">
              <h3>Design system extracted</h3>
              <p>Buttons, inputs, navs, and layouts cataloged in 9s.</p>
            </div>
          </div>
          <div className="hero-glow" />
        </div>
      </section>

      <section className="landing-story" id="story">
        <div className="section-header">
          <h2>Built for teams who need clarity fast.</h2>
          <p>
            From discovery to delivery, GOharveST turns the unknown into a decision-ready narrative.
          </p>
        </div>
        <div className="story-grid">
          <div className="story-step">
            <span>01</span>
            <h3>Seed the source</h3>
            <p>Drop a URL and choose a depth. We map structure, assets, and technologies.</p>
          </div>
          <div className="story-step">
            <span>02</span>
            <h3>Track the signals</h3>
            <p>Performance, metadata, and component libraries are captured in one session.</p>
          </div>
          <div className="story-step">
            <span>03</span>
            <h3>Share the harvest</h3>
            <p>Export, compare, and build reports for your team or clients instantly.</p>
          </div>
        </div>
      </section>

      <section className="landing-features" id="features">
        <div className="section-header">
          <h2>Everything you need to reverse the web with confidence.</h2>
          <p>Design intelligence, tech detection, and asset inventory in one workflow.</p>
        </div>
        <div className="feature-grid">
          <div className="feature-card">
            <h3>Component Library</h3>
            <p>Extract reusable UI elements and categorize them by purpose and usage.</p>
          </div>
          <div className="feature-card">
            <h3>Tech Stack Radar</h3>
            <p>Detect frameworks, hosting layers, and integrations powering the experience.</p>
          </div>
          <div className="feature-card">
            <h3>Performance Signals</h3>
            <p>Capture timing, weight, and asset counts to spot friction and opportunity.</p>
          </div>
          <div className="feature-card">
            <h3>Diff & Compare</h3>
            <p>Track changes across snapshots and compare competitors side by side.</p>
          </div>
        </div>
      </section>

      <section className="landing-testimonials" id="testimonials">
        <div className="section-header">
          <h2>Trusted by builders, strategists, and growth teams.</h2>
        </div>
        <div className="testimonial-grid">
          <div className="testimonial-card">
            <p>
              “GOharveST turned our competitor review from a week-long task into a morning ritual.”
            </p>
            <span>— Ada N., Product Research</span>
          </div>
          <div className="testimonial-card">
            <p>“We exported assets and rebuilt an onboarding flow in two days.”</p>
            <span>— Miles T., Design Lead</span>
          </div>
          <div className="testimonial-card">
            <p>“The tech stack insights saved our dev team from guessing.”</p>
            <span>— Priya S., CTO</span>
          </div>
        </div>
      </section>

      <section className="landing-cta-panel">
        <div>
          <h2>Ready to harvest your next advantage?</h2>
          <p>Bring your first URL and let GOharveST map the rest.</p>
        </div>
        <Link to="/register" className="primary">
          Create free account
        </Link>
      </section>

      <footer className="landing-footer">
        <span>GOharveST Platform</span>
        <span>Harvest intelligence for modern teams.</span>
      </footer>
    </div>
  );
}
