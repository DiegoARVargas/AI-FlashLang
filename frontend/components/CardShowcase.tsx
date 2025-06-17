"use client";

import Image from "next/image";

export default function CardShowcase() {
  return (
    <section className="px-4 py-20 bg-black">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-8">Así funciona una tarjeta FlashLang</h2>
        <div className="flex flex-col md:flex-row justify-center gap-6 items-center">
          <Image
            src="/tarjeta_inicial.png"
            alt="Tarjeta inicial"
            width={180}
            height={240}
            className="rounded-xl shadow-lg"
          />
          <Image
            src="/tarjeta_click.png"
            alt="Tarjeta click"
            width={180}
            height={240}
            className="rounded-xl shadow-lg"
          />
          <Image
            src="/tarjeta_traduccion.png"
            alt="Tarjeta traducción"
            width={180}
            height={240}
            className="rounded-xl shadow-lg"
          />
        </div>
      </div>
    </section>
  );
}
