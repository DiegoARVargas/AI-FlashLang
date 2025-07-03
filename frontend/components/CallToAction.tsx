"use client";

import Image from "next/image";
import Link from "next/link";

export default function CallToAction() {
  return (
    <section className="bg-black py-20 px-4 text-center">
      <h2 className="text-3xl font-bold">Empieza a aprender con FlashLang</h2>
      <p className="text-gray-300 mt-4 mb-6">
        Conviértete en un maestro del vocabulario con la ayuda de la IA
      </p>
      <Link href="/login">
        <button className="bg-purple-600 hover:bg-purple-700 text-white text-lg px-6 py-3 rounded-full font-semibold shadow-xl">
          Crear cuenta gratis
        </button>
      </Link>
      <div className="mt-8 flex justify-center">
      </div>
    </section>
  );
}
