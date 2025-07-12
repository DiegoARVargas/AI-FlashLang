// /frontend/components/MyAccount/DeleteAccountSection.tsx
// This component provides a section for users to delete their account.
// It prompts the user to confirm the deletion and handles the API request to delete the account.
// If the deletion is successful, it clears cookies and redirects the user to the login page.

import { useState } from 'react';
import { useRouter } from 'next/router';
import Cookies from 'js-cookie';

export default function DeleteAccountSection() {
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleDelete = async () => {
    const token = Cookies.get('access_token');

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/me/delete/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data?.detail || 'Failed to delete account');
      }

      // Clear auth cookies
      Cookies.remove('access_token');
      Cookies.remove('refresh_token');
      Cookies.remove('username');

      router.push('/login');
    } catch (err: any) {
      setError(err.message || 'Failed to delete account');
    }
  };

  return (
    <div className="bg-[#111111] p-6 rounded-xl shadow-lg text-white">
      <h2 className="text-xl font-semibold mb-2 text-red-400">⚠️ Delete Account</h2>
      <p className="text-sm mb-4">This action is irreversible. All your data will be deleted.</p>

      {!confirming ? (
        <button
          onClick={() => setConfirming(true)}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
        >
          Delete my account
        </button>
      ) : (
        <div className="space-y-2">
          <p>
            Are you sure? This action{' '}
            <span className="text-red-500 font-bold">cannot be undone</span>.
          </p>
          <div className="flex gap-4">
            <button
              onClick={handleDelete}
              className="bg-red-700 hover:bg-red-800 text-white px-4 py-2 rounded"
            >
              Confirm deletion
            </button>
            <button
              onClick={() => setConfirming(false)}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
            >
              Cancel
            </button>
          </div>
          {error && <p className="text-red-400 mt-2">❌ {error}</p>}
        </div>
      )}
    </div>
  );
}