// /frontend/components/MyAccount/ChangePasswordForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useState } from 'react';

// Validation schema for changing password
const schema = z
  .object({
    current_password: z.string().min(6, 'Must be at least 6 characters'),
    new_password: z.string().min(6, 'Must be at least 6 characters'),
    confirm_password: z.string().min(6, 'Must be at least 6 characters'),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: 'Passwords do not match',
    path: ['confirm_password'],
  });

type ChangePasswordFormData = z.infer<typeof schema>;

export default function ChangePasswordForm() {
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ChangePasswordFormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: ChangePasswordFormData) => {
    try {
      const token = Cookies.get('access_token');

      await axios.put(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}users/change-password/`,
        {
          current_password: data.current_password,
          new_password: data.new_password,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSuccess(true);
      setErrorMsg('');
      reset();
      setTimeout(() => setSuccess(false), 3000);
    } catch (error: any) {
      console.error(error);
      setSuccess(false);
      setErrorMsg('Error changing password. Please check your current password.');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-[#111111] p-6 rounded-xl shadow-lg space-y-4 mt-10">
      <h2 className="text-xl font-semibold mb-2">Change Password</h2>

      <div>
        <label className="block text-sm mb-1">Current Password</label>
        <input
          type="password"
          {...register('current_password')}
          className="w-full p-2 rounded bg-[#1a1a1a] border border-gray-600 text-white"
        />
        {errors.current_password && <p className="text-red-500 text-sm">{errors.current_password.message}</p>}
      </div>

      <div>
        <label className="block text-sm mb-1">New Password</label>
        <input
          type="password"
          {...register('new_password')}
          className="w-full p-2 rounded bg-[#1a1a1a] border border-gray-600 text-white"
        />
        {errors.new_password && <p className="text-red-500 text-sm">{errors.new_password.message}</p>}
      </div>

      <div>
        <label className="block text-sm mb-1">Confirm New Password</label>
        <input
          type="password"
          {...register('confirm_password')}
          className="w-full p-2 rounded bg-[#1a1a1a] border border-gray-600 text-white"
        />
        {errors.confirm_password && <p className="text-red-500 text-sm">{errors.confirm_password.message}</p>}
      </div>

      {errorMsg && <p className="text-red-400 text-sm">{errorMsg}</p>}
      {success && <p className="text-green-400 text-sm">✅ Password changed successfully</p>}

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
      >
        Change Password
      </button>
    </form>
  );
}