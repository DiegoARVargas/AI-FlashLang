// ✅ VerifiedRoute.tsx
import { useRouter } from 'next/router';
import { useAuth } from '@/contexts/AuthContext';
import { useEffect } from 'react';

export default function VerifiedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, loading, user } = useAuth();

  useEffect(() => {
    if (loading) return;

    if (!isAuthenticated) {
      router.push('/login');
    } else if (user && user.is_active === false) {
      router.push('/resend-verification');
    }
  }, [isAuthenticated, loading, user, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-white">
        <div className="w-16 h-16 border-4 border-purple-600 border-dashed rounded-full animate-spin" />
      </div>
    );
  }

  return <>{children}</>;
}