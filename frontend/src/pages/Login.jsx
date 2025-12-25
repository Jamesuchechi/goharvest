import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api.js';
import { useAuth } from '../hooks/useAuth.js';

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const { signIn, setUser } = useAuth();
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);
    const payload = {
      username: formData.get('username'),
      password: formData.get('password'),
    };

    try {
      const response = await authAPI.login(payload);
      signIn({
        access: response.data.access,
        refresh: response.data.refresh,
      });
      const meResponse = await authAPI.me();
      setUser(meResponse.data);
      const destination = location.state?.from?.pathname || '/app';
      navigate(destination, { replace: true });
    } catch (err) {
      setError('Login failed. Check your credentials and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Welcome back</h1>
        <p className="auth-subtext">Sign in to start harvesting again.</p>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Username
            <input name="username" type="text" required autoComplete="username" />
          </label>
          <label>
            Password
            <input name="password" type="password" required autoComplete="current-password" />
          </label>
          {error ? <p className="auth-error">{error}</p> : null}
          <button className="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
        <div className="auth-links">
          <span>New here?</span>
          <Link to="/register">Create an account</Link>
        </div>
      </div>
    </div>
  );
}
