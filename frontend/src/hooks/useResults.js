import { useCallback, useEffect, useState } from 'react';
import { resultsAPI } from '../services/api.js';

export function useResults(params = {}) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await resultsAPI.list(params);
      const data = response.data?.results || response.data || [];
      setResults(data);
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

  return { results, loading, error, refresh };
}
