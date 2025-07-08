// /frontend/pages/_app.tsx
import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { QueryClientProvider } from '@tanstack/react-query';
import queryClient from '@/lib/react-query-client';
import { AuthProvider } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ProtectedRoute>
          <Component {...pageProps} />
        </ProtectedRoute>
      </AuthProvider>
    </QueryClientProvider>
  );
}