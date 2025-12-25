import { useNavigate } from 'react-router-dom';
import JobFilters from '../components/jobs/JobFilters.jsx';
import JobTable from '../components/jobs/JobTable.jsx';
import BulkActions from '../components/jobs/BulkActions.jsx';
import { useJobs } from '../hooks/useJobs.js';

export default function JobList() {
  const { jobs, loading } = useJobs();
  const navigate = useNavigate();

  return (
    <div className="page two-column">
      <JobFilters />
      <div className="panel">
        <div className="section-header">
          <h2>All Harvest Jobs</h2>
          <BulkActions />
        </div>
        {loading ? <p>Loading jobs...</p> : <JobTable jobs={jobs} onSelect={(job) => navigate(`/app/jobs/${job.id}`)} />}
      </div>
    </div>
  );
}
