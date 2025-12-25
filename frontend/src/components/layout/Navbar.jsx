import { Link, NavLink } from 'react-router-dom';

const navItems = [
  { label: 'Dashboard', to: '/' },
  { label: 'Jobs', to: '/jobs' },
  { label: 'Results', to: '/results' },
  { label: 'Tech Explorer', to: '/tech-explorer' },
  { label: 'Analytics', to: '/analytics' },
  { label: 'Settings', to: '/settings' },
];

export default function Navbar() {
  return (
    <header className="topbar">
      <Link className="brand" to="/">
        <span className="brand-mark">GO</span>
        <span>harveST</span>
      </Link>
      <nav className="nav-links">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => (isActive ? 'active' : undefined)}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
