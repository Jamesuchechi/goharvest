import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.js';

const navItems = [
  { label: 'Dashboard', to: '/app' },
  { label: 'Jobs', to: '/app/jobs' },
  { label: 'Results', to: '/app/results' },
  { label: 'Tech Explorer', to: '/app/tech-explorer' },
  { label: 'Analytics', to: '/app/analytics' },
  { label: 'Settings', to: '/app/settings' },
];

export default function Navbar() {
  const { user } = useAuth();

  return (
    <header className="topbar">
      <Link className="brand" to="/app">
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
        <span className="nav-user">
          {user?.username ? `Hi, ${user.username}` : 'Account'}
        </span>
        <Link className="ghost small" to="/logout">
          Logout
        </Link>
      </nav>
    </header>
  );
}
