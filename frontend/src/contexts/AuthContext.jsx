import { createContext, useEffect, useMemo, useState } from 'react';
import { authAPI } from '../services/api.js';

export const AuthContext = createContext({
  user: null,
  token: null,
  signIn: () => {},
  signOut: () => {},
  setUser: () => {},
});

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('auth_token'));
  const [user, setUserState] = useState(() => {
    const storedUser = localStorage.getItem('auth_user');
    return storedUser ? JSON.parse(storedUser) : null;
  });

  useEffect(() => {
    if (!token) {
      setUserState(null);
      localStorage.removeItem('auth_user');
      return;
    }

    authAPI
      .me()
      .then((response) => {
        setUserState(response.data);
        localStorage.setItem('auth_user', JSON.stringify(response.data));
      })
      .catch(() => {
        setToken(null);
        setUserState(null);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
      });
  }, [token]);

  useEffect(() => {
    const handleLogout = () => {
      setToken(null);
      setUserState(null);
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('auth_user');
    };

    window.addEventListener('auth:logout', handleLogout);
    return () => window.removeEventListener('auth:logout', handleLogout);
  }, []);

  const value = useMemo(
    () => ({
      user,
      token,
      signIn: ({ access, refresh, user: nextUser }) => {
        setToken(access);
        if (nextUser) {
          setUserState(nextUser);
          localStorage.setItem('auth_user', JSON.stringify(nextUser));
        }
        localStorage.setItem('auth_token', access);
        if (refresh) {
          localStorage.setItem('refresh_token', refresh);
        }
      },
      signOut: () => {
        setToken(null);
        setUserState(null);
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('auth_user');
      },
      setUser: (nextUser) => {
        setUserState(nextUser);
        if (nextUser) {
          localStorage.setItem('auth_user', JSON.stringify(nextUser));
        } else {
          localStorage.removeItem('auth_user');
        }
      },
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
