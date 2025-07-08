// /frontend/pages/my-account.tsx
// Página de "Mi Cuenta" que carga los datos del perfil usando cookies (como en create.tsx)

"use client";

import { useQuery } from '@tanstack/react-query';
import { useEffect } from 'react';
import Cookies from 'js-cookie';
import ProfileCard from '@/components/MyAccount/ProfileCard';
import EditProfileForm from '@/components/MyAccount/EditProfileForm';
import ChangePasswordForm from '@/components/MyAccount/ChangePasswordForm';
import DownloadHistory from '@/components/MyAccount/DownloadHistory';
import DeleteAccountSection from '@/components/MyAccount/DeleteAccountSection';
import Navbar from '@/components/Navbar';
import Footer from "@/components/Footer";

export default function MyAccountPage() {
  const {
    data,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const token = Cookies.get('access_token'); // ✅ lee de cookies
      if (!token) throw new Error("Token no encontrado en cookies");

      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/me/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error('Error al cargar el perfil');

      const userData = await res.json();

      // ✅ Guarda avatar en localStorage si está disponible
      if (userData.avatar) {
        localStorage.setItem('avatar', userData.avatar);
      } else {
        localStorage.removeItem('avatar');
      }

      return userData;
    },
  });

  useEffect(() => {
    document.title = 'Mi Cuenta | AI FlashLang';
  }, []);

  if (isLoading) return <p className="text-white text-center">Cargando...</p>;
  if (error || !data) return <p className="text-red-500 text-center">Error al cargar tu perfil.</p>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0d0d0d] to-[#1a1a1a] text-white">
      <Navbar />

      <div className="max-w-4xl mx-auto p-4 space-y-10">
        <h1 className="text-4xl font-extrabold mb-10 text-white">Mi Cuenta</h1>

        <section className="grid md:grid-cols-2 gap-6 items-start">
          <ProfileCard user={data} refetch={refetch} />
          <EditProfileForm user={data} refetch={refetch} />
        </section>

        <section>
          <ChangePasswordForm />
        </section>

        <section>
          <DownloadHistory />
        </section>

        <section>
          <DeleteAccountSection />
        </section>
      </div>
      <Footer />
    </div>
  );
}
