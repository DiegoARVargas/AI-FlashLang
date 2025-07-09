// /frontend/pages/login.tsx

"use client";

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { loginSchema } from '@/schemas/zodSchemas';
import { useAuth } from '@/contexts/AuthContext';
import Cookies from 'js-cookie';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [errorMsg, setErrorMsg] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
  });

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, loading, router]);

  const onSubmit = async (data: z.infer<typeof loginSchema>) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Credenciales inválidas');

      const result = await response.json();
      Cookies.set('access_token', result.access);
      Cookies.set('refresh_token', result.refresh);
      Cookies.set('username', data.username);

      login(result.access, data.username);
      router.push('/');
    } catch (error) {
      setErrorMsg('Credenciales incorrectas. Intenta nuevamente.');
    }
  };

  if (loading || isAuthenticated) return null;

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-[#0d0d0d] to-[#1a1a1a] text-white">
      <Navbar />

      <main className="flex flex-grow items-center justify-center px-4 py-10">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="bg-[#111111] shadow-lg rounded-xl px-8 pt-6 pb-8 w-full max-w-md"
        >
          <h1 className="text-2xl font-bold mb-6 text-center">Iniciar Sesión</h1>

          {errorMsg && <p className="text-red-500 mb-4">{errorMsg}</p>}

          <input
            type="text"
            placeholder="Nombre de usuario"
            {...register('username')}
            className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white"
          />
          {errors.username && <p className="text-red-500 text-sm">{errors.username.message}</p>}

          <input
            type="password"
            placeholder="Contraseña"
            {...register('password')}
            className="w-full px-4 py-2 mb-6 rounded bg-[#1a1a1a] border border-gray-600 text-white"
          />
          {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
          >
            {isSubmitting ? 'Iniciando...' : 'Iniciar sesión'}
          </button>
        </form>
      </main>

      <Footer />
    </div>
  );
}