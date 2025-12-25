export default function Card({ title, subtitle, children, className = '' }) {
  return (
    <div className={`card ${className}`.trim()}>
      {(title || subtitle) && (
        <header className="card-header">
          {title && <h3>{title}</h3>}
          {subtitle && <p>{subtitle}</p>}
        </header>
      )}
      <div className="card-body">{children}</div>
    </div>
  );
}
