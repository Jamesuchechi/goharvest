export default function TechnologyBadges({ technologies = {} }) {
  const list = Object.keys(technologies || {}).slice(0, 4);
  if (!list.length) return <span className="muted">No tech tags</span>;

  return (
    <div className="badge-row">
      {list.map((tech) => (
        <span key={tech} className="badge">{tech}</span>
      ))}
    </div>
  );
}
