// pages/login.tsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import api from '../services/api';
import Cookies from 'js-cookie';

export default function LoginPage() {
  const router = useRouter();

  // ✅ CAMBIO: Renombrar 'email' a 'username'
  const [username, setUsername] = useState(''); // ✅ CAMBIO
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // ✅ CAMBIO: Enviar 'username' en vez de 'email'
      const response = await api.post('/token/', { username, password }); // ✅ CAMBIO
      Cookies.set('access_token', response.data.access);
      Cookies.set('refresh_token', response.data.refresh);
      router.push('/');
    } catch (error) {
      setErrorMsg('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <form onSubmit={handleLogin} className="bg-white shadow-md rounded px-8 pt-6 pb-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>

        {errorMsg && <p className="text-red-500 mb-4">{errorMsg}</p>}

        <input
          type="text"
          placeholder="Username" // ✅ CAMBIO: placeholder más claro
          value={username}       // ✅ CAMBIO
          onChange={(e) => setUsername(e.target.value)} // ✅ CAMBIO
          className="w-full px-4 py-2 mb-4 border rounded"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 mb-6 border rounded"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Login
        </button>
      </form>
    </div>
  );
}