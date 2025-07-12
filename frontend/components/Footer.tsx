"use client";

import { Github, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-black border-t border-neutral-800 text-sm text-neutral-400 py-8 px-4">
      <div className="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-6 items-start text-center sm:text-left">

        {/* Column 1: Brand and tagline */}
        <div>
          <p className="font-semibold text-white">AI FlashLang</p>
          <p className="mt-1">Learn better, learn with context.</p>
          <p className="mt-2">© {new Date().getFullYear()} All rights reserved.</p>
        </div>

        {/* Column 2: Navigation / Resources */}
        <div>
          <p className="font-semibold text-white mb-1">Resources</p>
          <ul className="space-y-1">
            <li>
              <a href="/terminos" className="hover:text-white transition">Terms of Use</a>
            </li>
            <li>
              <a href="/privacidad" className="hover:text-white transition">Privacy Policy</a>
            </li>
            <li>
              <a href="/ayuda" className="hover:text-white transition">Help / FAQ</a>
            </li>
          </ul>
        </div>

        {/* Column 3: Social and options */}
        <div className="flex flex-col items-center sm:items-end gap-3">
          <div className="flex gap-4">
            <a href="https://github.com/tu-repo" target="_blank" rel="noopener noreferrer">
              <Github className="w-5 h-5 hover:text-white transition" />
            </a>
            <a href="mailto:contacto@aiflashlang.com">
              <Mail className="w-5 h-5 hover:text-white transition" />
            </a>
          </div>

          <select
            className="mt-2 bg-neutral-900 text-white text-sm border border-neutral-700 rounded px-2 py-1"
            defaultValue="es"
          >
            <option value="es">Español</option>
            <option value="en">English</option>
            <option value="fr">Français</option>
          </select>
        </div>
      </div>
    </footer>
  );
}