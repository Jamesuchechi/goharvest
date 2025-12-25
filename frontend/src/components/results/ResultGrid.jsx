import ResultCard from './ResultCard.jsx';

export default function ResultGrid({ results = [], onSelect }) {
  return (
    <div className="grid">
      {results.map((result) => (
        <ResultCard key={result.id} result={result} onSelect={onSelect} />
      ))}
    </div>
  );
}
