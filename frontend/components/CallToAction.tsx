"use client";

import Image from "next/image";
import Link from "next/link";

export default function CallToAction() {
  return (
    <section className="bg-black py-20 px-4 text-center">
      <h2 className="text-3xl font-bold">Start Learning with FlashLang</h2>
      <p className="text-gray-300 mt-4 mb-6">
        Become a vocabulary master with the help of AI
      </p>
      <Link href="/register">
        <button className="bg-purple-600 hover:bg-purple-700 text-white text-lg px-6 py-3 rounded-full font-semibold shadow-xl">
          Create Free Account
        </button>
      </Link>
      <div className="mt-8 flex justify-center">
      </div>
    </section>
  );
}