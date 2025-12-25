import TechnologyBadges from './TechnologyBadges.jsx';

export default function ResultCard({ result, onSelect }) {
  return (
    <button className="card result-card" onClick={() => onSelect?.(result)}>
      <h3>{result.job?.url || 'Untitled'}</h3>
      <p>Assets: {result.total_assets}</p>
      <TechnologyBadges technologies={result.technologies} />
    </button>
  );
}
