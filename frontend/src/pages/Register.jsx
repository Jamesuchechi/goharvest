import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api.js';
import { useAuth } from '../hooks/useAuth.js';

export default function Register() {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setIsSubmitting(false);
      return;
    }

    const payload = {
      username: formData.get('username'),
      email: formData.get('email'),
      password,
    };

    try {
      const response = await authAPI.register(payload);
      signIn({
        access: response.data.access,
        refresh: response.data.refresh,
        user: response.data.user,
      });
      navigate('/app', { replace: true });
    } catch (err) {
      setError('Registration failed. Try a different username or email.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Create your account</h1>
        <p className="auth-subtext">Track harvests, results, and analytics across sessions.</p>
        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Username
            <input name="username" type="text" required autoComplete="username" />
          </label>
          <label>
            Email
            <input name="email" type="email" autoComplete="email" />
          </label>
          <label>
            Password
            <input name="password" type="password" required autoComplete="new-password" />
          </label>
          <label>
            Confirm password
            <input name="confirmPassword" type="password" required autoComplete="new-password" />
          </label>
          {error ? <p className="auth-error">{error}</p> : null}
          <button className="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account...' : 'Create account'}
          </button>
        </form>
        <div className="auth-links">
          <span>Already have an account?</span>
          <Link to="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
