// /frontend/components/Navbar.tsx
"use client";

import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";
import { useEffect, useState } from "react";
import { getMediaUrl } from "@/lib/media";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const { isAuthenticated, username, logout } = useAuth();
  const [avatarUrl, setAvatarUrl] = useState<string | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const avatarPath = localStorage.getItem("avatar");
    if (avatarPath) {
      setAvatarUrl(getMediaUrl(avatarPath));
    }
  }, []);

  return (
    <nav className="w-full bg-black/80 backdrop-blur-sm sticky top-0 z-50 border-b border-neutral-800">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo: always visible */}
        <Link
          href="/"
          className="text-white text-xl font-bold hover:text-purple-400 transition-all duration-300 hover:rotate-[1deg] hover:scale-105"
        >
          AIFlashLang
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-6 text-sm font-medium text-white">
          {!pathname.startsWith("/create") && (
            <Link
              href="/create"
              className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
            >
              Create Words
            </Link>
          )}
          {!pathname.startsWith("/my-words") && (
            <Link
              href="/my-words"
              className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
            >
              My Words
            </Link>
          )}
          {!pathname.startsWith("/my-account") && (
            <Link
              href="/my-account"
              className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
            >
              My Account
            </Link>
          )}

          {isAuthenticated ? (
            <>
              {avatarUrl ? (
                <img
                  src={avatarUrl}
                  alt="Avatar"
                  className="w-8 h-8 rounded-full border border-purple-500 object-cover"
                />
              ) : (
                <span className="text-sm text-purple-400">
                  Welcome, <strong>{username}</strong>
                </span>
              )}
              <button
                onClick={logout}
                className="text-white hover:text-red-500 transition duration-200"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              {!pathname.startsWith("/login") && (
                <Link
                  href="/login"
                  className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
                >
                  Log In
                </Link>
              )}
              {!pathname.startsWith("/register") && (
                <Link
                  href="/register"
                  className="relative hover:text-[#a855f7] transition duration-200 electric-hover hover:rotate-[1deg] hover:scale-105"
                >
                  Sign Up
                </Link>
              )}
            </>
          )}
        </div>
      </div>
    </nav>
  );
}