import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.js';

export default function Logout() {
  const navigate = useNavigate();
  const { signOut } = useAuth();

  useEffect(() => {
    signOut();
    navigate('/login', { replace: true });
  }, [navigate, signOut]);

  return null;
}
