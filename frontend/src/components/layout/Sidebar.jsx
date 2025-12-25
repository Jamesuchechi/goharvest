import { NavLink } from 'react-router-dom';

const links = [
  { label: 'Dashboard', to: '/app' },
  { label: 'Jobs', to: '/app/jobs' },
  { label: 'Results', to: '/app/results' },
  { label: 'Batch', to: '/app/batch' },
  { label: 'Visual Inspector', to: '/app/visual/preview' },
  { label: 'Comparison', to: '/app/compare' },
  { label: 'Components', to: '/app/components' },
  { label: 'Analytics', to: '/app/analytics' },
  { label: 'Profile', to: '/app/profile' },
  { label: 'Docs', to: '/app/docs' },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">Workspace</div>
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
}
