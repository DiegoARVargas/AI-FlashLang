// ✅ AuthContext.tsx
import { createContext, useContext, useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/router';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  loading: boolean; // ✅ Nuevo campo
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true); // ✅ Nuevo estado
  const router = useRouter();

  useEffect(() => {
    const storedToken = Cookies.get('access_token');
    if (storedToken) {
      console.log('🔐 Found token in cookies:', storedToken); // 👈 AÑADE ESTO
      setToken(storedToken);
    }
    setLoading(false); // ✅ Indica que ya terminó de cargar
  }, []);

  const login = (token: string) => {
    Cookies.set('access_token', token);
    setToken(token);
  };

  const logout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    setToken(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, loading, login, logout }}>
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
