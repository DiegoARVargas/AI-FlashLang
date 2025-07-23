"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function ResendVerificationPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleResend = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}users/resend-verification/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      const result = await res.json();
      if (!res.ok) {
        setError(result.detail || "Error al reenviar el correo.");
      } else {
        setMessage("📬 Correo de verificación reenviado correctamente.");
      }
    } catch (err) {
      setError("Error de conexión. Intenta nuevamente.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-gradient-to-br from-[#0d0d0d] to-[#1a1a1a] text-white">
      <Navbar />

      <main className="flex flex-grow items-center justify-center px-4 py-10">
        <form onSubmit={handleResend} className="bg-[#111111] shadow-lg rounded-xl px-8 pt-6 pb-8 w-full max-w-md">
          <h1 className="text-2xl font-bold mb-6 text-center">Reenviar verificación</h1>

          {message && <p className="text-green-500 mb-4 text-center">{message}</p>}
          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

          <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 mb-6 rounded bg-[#1a1a1a] border border-gray-600 text-white"
          />

          <button
            type="submit"
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
          >
            Reenviar correo
          </button>
        </form>
      </main>

      <Footer />
    </div>
  );
}