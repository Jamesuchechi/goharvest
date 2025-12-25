import { useCallback, useEffect, useState } from 'react';
import { jobsAPI } from '../services/api.js';

export function useJobs(params = {}) {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [jobsResponse, statsResponse] = await Promise.all([
        jobsAPI.list(params),
        jobsAPI.statistics(),
      ]);
      const jobsData = jobsResponse.data?.results || jobsResponse.data || [];
      setJobs(jobsData);
      setStats(statsResponse.data || {});
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [params]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { jobs, stats, loading, error, refresh };
}
