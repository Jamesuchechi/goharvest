import { createContext, useMemo, useState } from 'react';

export const AuthContext = createContext({
  user: null,
  token: null,
  signIn: () => {},
  signOut: () => {},
});

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('auth_token'));
  const [user, setUser] = useState(null);

  const value = useMemo(
    () => ({
      user,
      token,
      signIn: (nextToken, nextUser) => {
        setToken(nextToken);
        setUser(nextUser);
        localStorage.setItem('auth_token', nextToken);
      },
      signOut: () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('auth_token');
      },
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
