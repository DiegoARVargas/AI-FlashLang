// /frontend/components/MyAccount/ProfileCard.tsx
// Muestra el avatar, nombre y correo del usuario, y permite cambiar la foto de perfil.

import { useState } from 'react';
import Cookies from 'js-cookie';
import { getMediaUrl } from '@/lib/media'; // ✅ nueva importación

interface Props {
  user: any;
  refetch: () => void;
}

export default function ProfileCard({ user, refetch }: Props) {
  const [uploading, setUploading] = useState(false);

  const handleAvatarChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('avatar', file);

    const token = Cookies.get('access_token');

    try {
      setUploading(true);
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/me/`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) throw new Error('Error al subir imagen');

      refetch();
    } catch (error) {
      console.error('Error uploading avatar:', error);
    } finally {
      setUploading(false);
    }
  };

  const avatarUrl = user.avatar ? getMediaUrl(user.avatar) : '/default-avatar.png';

  return (
    <div className="bg-[#111111] p-6 rounded-xl shadow-lg text-white flex flex-col items-center gap-4">
      <div className="relative w-32 h-32">
        <img
          src={avatarUrl}
          alt="Avatar"
          className="w-32 h-32 rounded-full object-cover border border-gray-600"
        />
        <label className="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-xs px-2 py-1 rounded cursor-pointer">
          📷
          <input
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            className="hidden"
          />
        </label>
      </div>

      <div className="text-center">
        <p className="text-lg font-semibold">{user.display_name || user.username}</p>
        <p className="text-sm text-gray-400">{user.email}</p>
        <p className="text-sm text-green-400 mt-1">
          Plan: {user.is_premium ? 'Premium' : 'Gratuito'}
        </p>
        {uploading && <p className="text-blue-400 text-sm mt-2">Subiendo imagen...</p>}
      </div>
    </div>
  );
}
