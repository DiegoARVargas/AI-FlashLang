"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";

export default function Navbar() {
  const { isAuthenticated, username, logout } = useAuth();

  return (
    <nav className="w-full bg-black/80 backdrop-blur-sm sticky top-0 z-50 border-b border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo */}
        <Link
          href="/"
          className="text-white text-xl font-bold hover:text-purple-400 transition-all duration-300 hover:rotate-[1deg] hover:scale-105"
        >
          AIFlashLang
        </Link>

        {/* Navegación */}
        <div className="flex items-center gap-6 text-sm font-medium text-white">
          <Link
            href="/create"
            className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
          >
            Create Words
          </Link>
          <Link
            href="/words"
            className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
          >
            My Words
          </Link>
          <Link
            href="/account"
            className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
          >
            My Account
          </Link>

          {isAuthenticated ? (
            <>
              <span className="text-sm text-purple-400">
                Welcome, <strong>{username}</strong>
              </span>
              <button
                onClick={logout}
                className="text-white hover:text-red-500 transition duration-200"
              >
                Logout
              </button>
            </>
          ) : (
            <Link
              href="/login"
              className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
            >
              Iniciar sesión
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
