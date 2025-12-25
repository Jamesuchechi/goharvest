import { useCallback, useEffect, useMemo, useState } from 'react';
import { resultsAPI } from '../services/api.js';

export function useResults(params = {}) {
  const paramsKey = useMemo(() => JSON.stringify(params), [params]);
  const stableParams = useMemo(() => params, [paramsKey]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await resultsAPI.list(stableParams);
      const data = response.data?.results || response.data || [];
      setResults(data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [stableParams]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { results, loading, error, refresh };
}
