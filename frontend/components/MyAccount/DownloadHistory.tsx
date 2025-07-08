// /frontend/components/MyAccount/DownloadHistory.tsx
// This component fetches and displays the user's download history, including the deck name, date of export, and a link to download the file.
// It uses Axios to make a GET request to the backend API and handles loading and error states.
// The download history is displayed in a table format, with each record showing the deck name, export date, and a download link.
// The date is formatted to be more readable using the `toLocaleDateString` method with Spanish locale settings.
"use client";

import { useEffect, useState } from 'react';
import Cookies from 'js-cookie';

interface Download {
  id: number;
  deck_name: string;
  download_date: string;
}

export default function DownloadHistory() {
  const [downloads, setDownloads] = useState<Download[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDownloads = async () => {
      try {
        const token = Cookies.get('access_token');
        console.log("TOKEN ENVIADO:", token);
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/download-history/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error('Error al cargar el historial de descargas');

        const data = await res.json();
        setDownloads(data);
      } catch (err) {
        setError('No se pudo cargar el historial.');
      } finally {
        setLoading(false);
      }
    };

    fetchDownloads();
  }, []);

  if (loading) return <p className="text-white">Cargando historial...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Historial de Descargas</h2>
      {downloads.length === 0 ? (
        <p className="text-gray-400">No has descargado ningún mazo aún.</p>
      ) : (
        <ul className="space-y-2">
          {downloads.map((d) => (
            <li key={d.id} className="bg-[#1a1a1a] p-3 rounded border border-gray-700">
              <p className="font-semibold">Deck: {d.deck_name}</p>
              <p className="text-sm text-gray-400">Fecha: {new Date(d.download_date).toLocaleString()}</p>
            </li>
          ))}

        </ul>
      )}
    </div>
  );
}
