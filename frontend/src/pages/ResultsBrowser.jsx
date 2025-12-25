import ResultGrid from '../components/results/ResultGrid.jsx';
import { useResults } from '../hooks/useResults.js';

export default function ResultsBrowser() {
  const { results, loading } = useResults();

  return (
    <div className="page">
      <div className="section-header">
        <h2>Results Browser</h2>
      </div>
      {loading ? <p>Loading results...</p> : <ResultGrid results={results} />}
    </div>
  );
}
