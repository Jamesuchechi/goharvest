import HeroSection from '../components/dashboard/HeroSection.jsx';
import StatsCards from '../components/dashboard/StatsCards.jsx';
import RecentJobs from '../components/dashboard/RecentJobs.jsx';
import QuickActions from '../components/dashboard/QuickActions.jsx';
import { useNavigate } from 'react-router-dom';
import { useJobs } from '../hooks/useJobs.js';
import { useWebSocket } from '../hooks/useWebSocket.js';
import { jobsAPI } from '../services/api.js';

export default function Dashboard() {
  const { jobs, stats, loading, refresh } = useJobs({ limit: 10 });
  const navigate = useNavigate();
  const { isConnected } = useWebSocket({
    onMessage: (data) => {
      if (data.type === 'job_updated') {
        refresh();
      }
    },
  });

  const handleHarvestSubmit = async (url) => {
    await jobsAPI.create({ url, options: { mode: 'full', depth: 1 } });
    refresh();
  };

  return (
    <div className="page">
      <HeroSection onHarvestSubmit={handleHarvestSubmit} />
      <StatsCards stats={stats} loading={loading} />
      <div className="section">
        <div className="section-header">
          <h2>Recent Harvests</h2>
          {isConnected && <span className="status-pill">Live</span>}
        </div>
        <RecentJobs jobs={jobs} loading={loading} onSelect={(job) => navigate(`/jobs/${job.id}`)} />
      </div>
      <QuickActions />
    </div>
  );
}
