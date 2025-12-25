import { NavLink } from 'react-router-dom';

const links = [
  { label: 'Dashboard', to: '/' },
  { label: 'Jobs', to: '/jobs' },
  { label: 'Results', to: '/results' },
  { label: 'Batch', to: '/batch' },
  { label: 'Visual Inspector', to: '/visual/preview' },
  { label: 'Comparison', to: '/compare' },
  { label: 'Components', to: '/components' },
  { label: 'Docs', to: '/docs' },
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
