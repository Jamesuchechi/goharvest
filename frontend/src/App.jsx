import { useEffect, useMemo, useState } from 'react';
import {
  BrowserRouter,
  Link,
  Route,
  Routes,
  useNavigate,
  useParams,
} from 'react-router-dom';
import {
  createJob,
  fetchJob,
  fetchJobs,
  fetchResult,
  techDetect,
} from './services/api.js';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

const MODES = [
  { value: 'content', label: 'Content' },
  { value: 'media', label: 'Media' },
  { value: 'full', label: 'Full Snapshot' },
  { value: 'tech', label: 'Tech Only' },
];

function resolveMediaUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  if (!path.startsWith('/')) return `${API_BASE}/${path}`;
  return `${API_BASE}${path}`;
}

function formatDate(value) {
  if (!value) return '-';
  const date = new Date(value);
  return date.toLocaleString();
}

function statusTone(status) {
  switch (status) {
    case 'completed':
      return 'status status-success';
    case 'running':
      return 'status status-running';
    case 'failed':
      return 'status status-failed';
    default:
      return 'status status-pending';
  }
}

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [result, setResult] = useState(null);
  const [loadingJobs, setLoadingJobs] = useState(true);
  const [loadingResult, setLoadingResult] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    url: '',
    mode: 'content',
    depth: 1,
  });
  const [techUrl, setTechUrl] = useState('');
  const [techData, setTechData] = useState(null);
  const [techError, setTechError] = useState('');
  const [techLoading, setTechLoading] = useState(false);
  const navigate = useNavigate();

  const refreshJobs = async ({ silent = false } = {}) => {
    if (!silent) setLoadingJobs(true);
    try {
      const data = await fetchJobs();
      setJobs(data);
      setSelectedJob((prev) => prev || data[0] || null);
    } catch (err) {
      if (!silent) setError(err.message || 'Failed to refresh jobs.');
    } finally {
      if (!silent) setLoadingJobs(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    setLoadingJobs(true);
    fetchJobs()
      .then((data) => {
        if (isMounted) {
          setJobs(data);
          setSelectedJob(data[0] || null);
        }
      })
      .catch((err) => {
        if (isMounted) setError(err.message || 'Failed to load jobs.');
      })
      .finally(() => {
        if (isMounted) setLoadingJobs(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedJob) {
      setResult(null);
      return;
    }

    setLoadingResult(true);
    fetchResult(selectedJob.id)
      .then((data) => setResult(data))
      .catch(() => setResult(null))
      .finally(() => setLoadingResult(false));
  }, [selectedJob]);

  useEffect(() => {
    if (!selectedJob) return undefined;
    if (selectedJob.status === 'completed' || selectedJob.status === 'failed') {
      return undefined;
    }
    const interval = setInterval(() => {
      refreshJobs({ silent: true });
      fetchResult(selectedJob.id)
        .then((data) => setResult(data))
        .catch(() => setResult(null));
    }, 5000);
    return () => clearInterval(interval);
  }, [selectedJob]);

  const selectedSummary = useMemo(() => {
    if (!result) return null;
    const tech = result.technologies || {};
    const techGroups = Object.keys(tech);
    return {
      assets: Array.isArray(result.assets) ? result.assets.length : 0,
      techCount: techGroups.length,
      title: result.metadata?.title || 'Untitled',
      excerpt: result.content ? result.content.slice(0, 220) : '',
    };
  }, [result]);

  const stats = useMemo(() => {
    const total = jobs.length;
    const completed = jobs.filter((job) => job.status === 'completed').length;
    const running = jobs.filter((job) => job.status === 'running').length;
    return { total, completed, running };
  }, [jobs]);

  const handleFormChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!form.url.trim()) {
      setError('Please enter a URL to harvest.');
      return;
    }

    try {
      const payload = {
        url: form.url.trim(),
        options: {
          mode: form.mode,
          depth: Number(form.depth) || 1,
        },
      };
      const created = await createJob(payload);
      setJobs((prev) => [created, ...prev]);
      setSelectedJob(created);
      setForm((prev) => ({ ...prev, url: '' }));
    } catch (err) {
      setError(err.message || 'Failed to create harvest job.');
    }
  };

  const handleRefresh = async () => {
    setError('');
    await refreshJobs();
  };

  const runTechDetect = async () => {
    if (!techUrl.trim()) {
      setTechError('Enter a URL to run a tech scan.');
      return;
    }

    setTechLoading(true);
    setTechError('');
    try {
      const data = await techDetect(techUrl.trim());
      setTechData(data);
    } catch (err) {
      setTechError(err.message || 'Tech detection failed.');
      setTechData(null);
    } finally {
      setTechLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <p className="eyebrow">GOharveST Control Center</p>
          <h1>Harvest public frontend intelligence with precision.</h1>
          <p className="subhead">
            Launch harvest jobs, track progress in real time, and export clean snapshots of
            public-facing web assets.
          </p>
          <div className="hero-actions">
            <button className="ghost" type="button" onClick={handleRefresh}>
              Refresh Jobs
            </button>
            <span className="status-pill">API: {API_BASE}</span>
          </div>
          <div className="stats-row">
            <div className="stat-card">
              <span>Total Jobs</span>
              <strong>{stats.total}</strong>
            </div>
            <div className="stat-card">
              <span>Completed</span>
              <strong>{stats.completed}</strong>
            </div>
            <div className="stat-card">
              <span>Running</span>
              <strong>{stats.running}</strong>
            </div>
          </div>
        </div>
        <div className="hero-card">
          <h2>New Harvest</h2>
          <p className="card-subtext">Choose a mode and let the engine do the rest.</p>
          <form className="harvest-form" onSubmit={handleSubmit}>
            <label>
              Target URL
              <input
                type="url"
                placeholder="https://example.com"
                value={form.url}
                onChange={(event) => handleFormChange('url', event.target.value)}
                required
              />
            </label>
            <div className="form-row">
              <label>
                Mode
                <select
                  value={form.mode}
                  onChange={(event) => handleFormChange('mode', event.target.value)}
                >
                  {MODES.map((mode) => (
                    <option key={mode.value} value={mode.value}>
                      {mode.label}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Depth
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={form.depth}
                  onChange={(event) => handleFormChange('depth', event.target.value)}
                />
              </label>
            </div>
            <button className="primary" type="submit">
              Launch Harvest
            </button>
            {error ? <p className="error">{error}</p> : null}
          </form>
        </div>
      </header>

      <main className="dashboard">
        <section className="panel jobs-panel">
          <div className="panel-header">
            <div>
              <h3>Recent Jobs</h3>
              <p>Track every harvest request and drill into results.</p>
            </div>
            <button className="ghost small" type="button" onClick={handleRefresh}>
              {loadingJobs ? 'Loading...' : 'Reload'}
            </button>
          </div>
          <div className="job-list">
            {jobs.length === 0 && !loadingJobs ? (
              <p className="empty">No jobs yet. Start your first harvest.</p>
            ) : null}
            {jobs.map((job, index) => (
              <button
                key={job.id}
                type="button"
                className={`job-card ${selectedJob?.id === job.id ? 'active' : ''}`}
                style={{ animationDelay: `${index * 0.06}s` }}
                onClick={() => setSelectedJob(job)}
              >
                <div>
                  <p className="job-url">{job.url}</p>
                  <p className="job-meta">Created {formatDate(job.created_at)}</p>
                </div>
                <span className={statusTone(job.status)}>{job.status}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel detail-panel">
          <div className="panel-header">
            <div>
              <h3>Result Detail</h3>
              <p>Preview the output and download artifacts.</p>
            </div>
            {selectedJob ? <span className="pill">Job {selectedJob.id}</span> : null}
          </div>

          {!selectedJob ? (
            <div className="empty-state">Select a job to inspect the output.</div>
          ) : loadingResult ? (
            <div className="empty-state">Fetching results...</div>
          ) : !result ? (
            <div className="empty-state">Result not ready yet.</div>
          ) : (
            <div className="result-grid">
              <div className="result-card">
                <h4>{selectedSummary?.title}</h4>
                <p className="result-excerpt">
                  {selectedSummary?.excerpt || 'No extracted content available yet.'}
                </p>
                <div className="result-metrics">
                  <div>
                    <span>Assets</span>
                    <strong>{selectedSummary?.assets}</strong>
                  </div>
                  <div>
                    <span>Tech Groups</span>
                    <strong>{selectedSummary?.techCount}</strong>
                  </div>
                </div>
                <div className="result-actions">
                  {result.zip_file ? (
                    <a
                      className="primary link"
                      href={resolveMediaUrl(result.zip_file)}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Download Snapshot
                    </a>
                  ) : (
                    <button className="ghost" type="button" disabled>
                      Snapshot pending
                    </button>
                  )}
                  <Link className="ghost" to={`/jobs/${selectedJob.id}`}>
                    Open Detail
                  </Link>
                </div>
              </div>

              <div className="result-card">
                <h4>Detected Technologies</h4>
                <div className="tech-grid">
                  {result.technologies && Object.keys(result.technologies).length > 0 ? (
                    Object.entries(result.technologies).map(([group, values]) => (
                      <div key={group} className="tech-group">
                        <span>{group}</span>
                        <p>{Array.isArray(values) ? values.join(', ') : String(values)}</p>
                      </div>
                    ))
                  ) : (
                    <p className="muted">No technology data available yet.</p>
                  )}
                </div>
              </div>

              <div className="result-card">
                <h4>Metadata</h4>
                <pre className="json-block">
                  {JSON.stringify(result.metadata || {}, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </section>

        <section className="panel tech-panel">
          <div className="panel-header">
            <div>
              <h3>Instant Tech Detect</h3>
              <p>Run a lightweight scan without launching a full harvest.</p>
            </div>
          </div>
          <div className="tech-form">
            <input
              type="url"
              placeholder="https://example.com"
              value={techUrl}
              onChange={(event) => setTechUrl(event.target.value)}
            />
            <button className="primary" type="button" onClick={runTechDetect}>
              {techLoading ? 'Scanning...' : 'Scan URL'}
            </button>
          </div>
          {techError ? <p className="error">{techError}</p> : null}
          {techData ? (
            <pre className="json-block">{JSON.stringify(techData, null, 2)}</pre>
          ) : (
            <p className="muted">Tech detection results will appear here.</p>
          )}
        </section>
      </main>
    </div>
  );
}

function JobDetail() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError('');

    Promise.all([fetchJob(jobId), fetchResult(jobId)])
      .then(([jobData, resultData]) => {
        if (!isMounted) return;
        setJob(jobData);
        setResult(resultData);
      })
      .catch((err) => {
        if (!isMounted) return;
        setError(err.message || 'Failed to load job details.');
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [jobId]);

  const assets = Array.isArray(result?.assets) ? result.assets : [];
  const metadata = result?.metadata || {};
  const technologies = result?.technologies || {};
  const imageAssets = assets.filter((asset) =>
    /\.(png|jpe?g|gif|webp|svg)$/i.test(asset)
  );

  return (
    <div className="detail-page">
      <div className="detail-header">
        <div>
          <button className="ghost" type="button" onClick={() => navigate('/')}>
            Back to Dashboard
          </button>
          <h2>Job Detail</h2>
          <p className="muted">Deep dive into harvest output and exports.</p>
        </div>
        {job ? (
          <div className="job-header-card">
            <span className={statusTone(job.status)}>{job.status}</span>
            <p className="job-url">{job.url}</p>
            <p className="job-meta">Created {formatDate(job.created_at)}</p>
          </div>
        ) : null}
      </div>

      {loading ? (
        <div className="panel">Loading job data...</div>
      ) : error ? (
        <div className="panel error-panel">{error}</div>
      ) : (
        <div className="detail-grid">
          <section className="panel detail-card">
            <h3>Snapshot</h3>
            <p className="muted">Export the full harvest package.</p>
            {result?.zip_file ? (
              <a
                className="primary link"
                href={resolveMediaUrl(result.zip_file)}
                target="_blank"
                rel="noreferrer"
              >
                Download ZIP
              </a>
            ) : (
              <button className="ghost" type="button" disabled>
                Snapshot pending
              </button>
            )}
            <div className="detail-metrics">
              <div>
                <span>Assets</span>
                <strong>{assets.length}</strong>
              </div>
              <div>
                <span>Tech Groups</span>
                <strong>{Object.keys(technologies).length}</strong>
              </div>
            </div>
          </section>

          <section className="panel detail-card">
            <h3>Metadata</h3>
            <pre className="json-block">
              {JSON.stringify(metadata, null, 2)}
            </pre>
          </section>

          <section className="panel detail-card">
            <h3>Technologies</h3>
            <div className="tech-grid">
              {Object.keys(technologies).length > 0 ? (
                Object.entries(technologies).map(([group, values]) => (
                  <div key={group} className="tech-group">
                    <span>{group}</span>
                    <p>{Array.isArray(values) ? values.join(', ') : String(values)}</p>
                  </div>
                ))
              ) : (
                <p className="muted">No technology data available yet.</p>
              )}
            </div>
          </section>

          <section className="panel detail-card">
            <h3>Assets</h3>
            {assets.length === 0 ? (
              <p className="muted">No assets listed for this job.</p>
            ) : (
              <>
                {imageAssets.length > 0 ? (
                  <div className="asset-gallery">
                    {imageAssets.slice(0, 8).map((asset) => (
                      <a
                        key={asset}
                        href={asset}
                        target="_blank"
                        rel="noreferrer"
                        className="asset-thumb"
                      >
                        <img src={asset} alt="Asset preview" />
                      </a>
                    ))}
                  </div>
                ) : null}
                <ul className="asset-list">
                  {assets.slice(0, 25).map((asset) => (
                    <li key={asset}>
                      <a href={asset} target="_blank" rel="noreferrer">
                        {asset}
                      </a>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </section>

          <section className="panel detail-card">
            <h3>HTML Preview</h3>
            <pre className="code-block">{result?.html || 'HTML not available yet.'}</pre>
          </section>
        </div>
      )}
    </div>
  );
}

function TopBar() {
  return (
    <nav className="topbar">
      <div className="brand">
        <span className="brand-mark">GO</span>
        <span>harveST</span>
      </div>
      <div className="nav-links">
        <Link to="/">Dashboard</Link>
        <a href="https://github.com/Jamesuchechi/goharvest" target="_blank" rel="noreferrer">
          GitHub
        </a>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <TopBar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/jobs/:jobId" element={<JobDetail />} />
      </Routes>
    </BrowserRouter>
  );
}
