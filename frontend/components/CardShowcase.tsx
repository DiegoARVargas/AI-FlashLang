"use client";

import Image from "next/image";

export default function CardShowcase() {
  return (
    <section className="px-4 py-20 bg-black">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-8">Así se ve una tarjeta FlashLang</h2>
        <div className="flex flex-col md:flex-row justify-center gap-20 items-center">
          <Image
            src="/tarjeta_inicial.png"
            alt="Tarjeta inicial"
            width={240}
            height={280}
            className="rounded-xl shadow-lg border-2 border-[#A020F0] transition-all duration-300 hover:border-purple-400 hover:scale-105 hover:rotate-[1deg] hover:shadow-[0_0_20px_#A020F0]"
          />
          <Image
            src="/tarjeta_click.png"
            alt="Tarjeta click"
            width={240}
            height={280}
            className="rounded-xl shadow-lg border-2 border-[#A020F0] transition-all duration-300 hover:border-purple-400 hover:scale-105 hover:shadow-[0_0_20px_#A020F0]"
          />
          <Image
            src="/tarjeta_traduccion.png"
            alt="Tarjeta traducción"
            width={240}
            height={280}
            className="rounded-xl shadow-lg border-2 border-[#A020F0] transition-all duration-300 hover:border-purple-400 hover:scale-105 hover:rotate-[-1deg] hover:shadow-[0_0_20px_#A020F0]"
          />
        </div>
      </div>
    </section>
  );
}
