// /frontend/components/MyAccount/EditProfileForm.tsx
// This component allows users to edit their profile information, including their display name and preferred language.
// It uses React Hook Form for form handling and Zod for validation.
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useEffect, useState } from 'react';
import { editProfileSchema } from '@/schemas/zodSchemas';
import Cookies from 'js-cookie';

interface Props {
  user: any;
  refetch: () => void;
}

type EditProfileFormData = z.infer<typeof editProfileSchema>;

export default function EditProfileForm({ user, refetch }: Props) {
  const [languages, setLanguages] = useState<{ id: number; code: string; name: string }[]>([]);
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<EditProfileFormData>({
    resolver: zodResolver(editProfileSchema),
  });

  useEffect(() => {
    setValue('display_name', user.display_name || '');
    setValue('preferred_language', user.preferred_language || 'en');

    const token = Cookies.get('access_token');
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}languages/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then(setLanguages)
      .catch(() =>
        setLanguages([
          { id: 1, code: 'en', name: 'English' },
          { id: 2, code: 'es', name: 'Español' },
          { id: 3, code: 'fr', name: 'Français' },
        ])
      );
  }, [user, setValue]);

  const onSubmit = async (data: EditProfileFormData) => {
    const token = Cookies.get('access_token');
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/me/`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          display_name: data.display_name,
          preferred_language: data.preferred_language,
        }),
      });

      if (!res.ok) throw new Error('Error updating profile');

      setSuccess(true);
      refetch();
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-[#111111] p-6 rounded-xl shadow-lg space-y-4">
      <h2 className="text-xl font-semibold mb-2">Edit Profile</h2>

      <div>
        <label className="block text-sm mb-1">Display Name</label>
        <input
          {...register('display_name')}
          className="w-full p-2 rounded bg-[#1a1a1a] border border-gray-600 text-white"
        />
        {errors.display_name && <p className="text-red-500 text-sm">{errors.display_name.message}</p>}
      </div>

      <div>
        <label className="block text-sm mb-1">Preferred Language</label>
        <select
          {...register('preferred_language')}
          className="w-full p-2 rounded bg-[#1a1a1a] border border-gray-600 text-white"
        >
          {languages.map((lang) => (
            <option key={lang.id} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        {errors.preferred_language && (
          <p className="text-red-500 text-sm">{errors.preferred_language.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
      >
        Save Changes
      </button>

      {success && <p className="text-green-400 mt-2">✅ Changes saved</p>}
    </form>
  );
}