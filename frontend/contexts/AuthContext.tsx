// /frontend/contexts/AuthContext.tsx

import { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/router';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  username: string | null;
  loading: boolean;
  login: (token: string, username: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const storedToken = Cookies.get('access_token');
    const storedUsername = Cookies.get('username');
    if (storedToken) {
      console.log('🔐 Found token in cookies:', storedToken);
      setToken(storedToken);
      if (storedUsername) setUsername(storedUsername);
    }
    setLoading(false);
  }, []);

  const login = (token: string, username: string) => {
    Cookies.set('access_token', token);
    Cookies.set('username', username);
    setToken(token);
    setUsername(username);
  };

  const logout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    Cookies.remove('username');
    localStorage.removeItem('avatar'); // ✅ eliminamos avatar del localStorage
    setToken(null);
    setUsername(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        username,
        isAuthenticated: !!token,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
