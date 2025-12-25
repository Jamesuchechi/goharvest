export default function LoadingSpinner({ label = 'Loading...' }) {
  return (
    <div className="spinner">
      <div className="spinner-dot" />
      <span>{label}</span>
    </div>
  );
}
