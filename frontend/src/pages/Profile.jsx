import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.js';

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="page">
      <div className="section-header">
        <h2>Profile</h2>
        <Link to="/logout" className="ghost small">
          Sign out
        </Link>
      </div>
      <div className="panel profile-panel">
        <div>
          <p className="profile-label">Username</p>
          <p className="profile-value">{user?.username || '—'}</p>
        </div>
        <div>
          <p className="profile-label">Email</p>
          <p className="profile-value">{user?.email || '—'}</p>
        </div>
        <div>
          <p className="profile-label">Access Level</p>
          <p className="profile-value">Analyst</p>
        </div>
        <div>
          <p className="profile-label">Workspace</p>
          <p className="profile-value">Default Harvest Lab</p>
        </div>
      </div>
    </div>
  );
}
