// pages/index.tsx
import { useAuth } from '@/contexts/AuthContext';

export default function Home() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold">
        {isAuthenticated ? 'Welcome back!' : 'Please log in'}
      </h1>

      {isAuthenticated && (
        <button onClick={logout} className="mt-4 px-4 py-2 bg-red-500 text-white rounded">
          Logout
        </button>
      )}
    </main>
  );
}
