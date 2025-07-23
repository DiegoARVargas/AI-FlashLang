"use client";

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema } from '@/schemas/zodSchemas';
import { z } from 'zod';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Cookies from 'js-cookie';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer'; // ✅ Footer import

export default function RegisterPage() {
  const router = useRouter();
  const { login, isAuthenticated, loading } = useAuth();
  const [errorMsg, setErrorMsg] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
  });

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, loading, router]);

  if (loading || isAuthenticated) return null;

  const onSubmit = async (data: z.infer<typeof registerSchema>) => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!res.ok) throw new Error('Error registering user');

      setErrorMsg("Account created! Please verify your email before logging in.");
    } catch (err) {
      setErrorMsg('Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-gradient-to-br from-[#0d0d0d] to-[#1a1a1a] text-white">
      <Navbar />

      <div className="flex items-center justify-center px-4 py-10">
        <form onSubmit={handleSubmit(onSubmit)} className="bg-[#111111] shadow-lg rounded-xl px-8 pt-6 pb-8 w-full max-w-md">
          <h1 className="text-2xl font-bold mb-6 text-center">Create Account</h1>

          {errorMsg && <p className="text-red-500 mb-4">{errorMsg}</p>}

          <input type="text" placeholder="Username" {...register('username')} className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white" />
          {errors.username && <p className="text-red-500 text-sm">{errors.username.message}</p>}

          <input type="email" placeholder="Email" {...register('email')} className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white" />
          {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}

          <input type="text" placeholder="Display Name" {...register('display_name')} className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white" />
          {errors.display_name && <p className="text-red-500 text-sm">{errors.display_name.message}</p>}

          <select {...register('preferred_language')} className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white">
            <option value="es">Spanish</option>
            <option value="en">English</option>
            <option value="fr">French</option>
          </select>
          {errors.preferred_language && <p className="text-red-500 text-sm">{errors.preferred_language.message}</p>}

          <input type="password" placeholder="Password" {...register('password')} className="w-full px-4 py-2 mb-4 rounded bg-[#1a1a1a] border border-gray-600 text-white" />
          {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}

          <input type="password" placeholder="Confirm Password" {...register('confirm_password')} className="w-full px-4 py-2 mb-6 rounded bg-[#1a1a1a] border border-gray-600 text-white" />
          {errors.confirm_password && <p className="text-red-500 text-sm">{errors.confirm_password.message}</p>}

          <button type="submit" disabled={isSubmitting} className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
            {isSubmitting ? 'Creating account...' : 'Sign up'}
          </button>

          <p className="mt-4 text-sm text-center text-gray-400">
            Already have an account?{' '}
            <Link href="/login" className="text-purple-400 hover:underline font-medium">
              Log in
            </Link>
          </p>
        </form>
      </div>

      <Footer />
    </div>
  );
}