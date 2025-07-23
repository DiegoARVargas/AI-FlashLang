// ✅ /frontend/pages/verified.tsx

import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

export default function VerifiedPage() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-[#0d0d0d] to-[#1a1a1a] text-white">
      <Navbar />

      <main className="flex flex-grow flex-col items-center justify-center text-center px-4">
        <h1 className="text-3xl font-bold mb-4">✅ Your email has been verified!</h1>
        <p className="text-lg mb-6">
          You can now log in to your account and start using AI FlashLang.
        </p>

        <Link href="/login">
          <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded">
            Go to Login
          </button>
        </Link>
      </main>

      <Footer />
    </div>
  );
}