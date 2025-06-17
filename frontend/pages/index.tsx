import Hero from "@/components/Hero";
import Image from "next/image";
import Link from "next/link";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white font-sans">
      {/* Hero con video de Flashy */}
      <Hero />

      {/* Features */}
      <section className="bg-[#1f2937] py-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">¿Por qué aprender con AI FlashLang?</h2>
          <p className="text-gray-400 mb-12">
            Nuestro método basado en inteligencia artificial transforma el aprendizaje de vocabulario.
          </p>

          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
            <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111827] p-6 rounded-xl shadow-lg">
              <h3 className="text-xl font-semibold text-blue-400 mb-2">Aprendizaje Contextual</h3>
              <p className="text-gray-300 text-sm">
                Aprende palabras en el contexto de frases reales. Mejora tu comprensión natural del idioma.
              </p>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111827] p-6 rounded-xl shadow-lg">
              <h3 className="text-xl font-semibold text-green-400 mb-2">Tarjetas Automatizadas</h3>
              <p className="text-gray-300 text-sm">
                La IA genera automáticamente ejemplos, traducciones, audios y tarjetas tipo Anki.
              </p>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111827] p-6 rounded-xl shadow-lg">
              <h3 className="text-xl font-semibold text-pink-400 mb-2">Aprendizaje Multilingüe</h3>
              <p className="text-gray-300 text-sm">
                Compatible con varios idiomas. Aprende inglés, francés, portugués y más según tu idioma nativo.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Ejemplo de tarjeta */}
      <section className="px-4 py-20 bg-[#120a24]">
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

      {/* CTA Final */}
      <section className="bg-[#1f152f] py-20 px-4 text-center">
        <h2 className="text-3xl font-bold">Empieza a aprender con FlashLang</h2>
        <p className="text-gray-300 mt-4 mb-6">Conviértete en un maestro del vocabulario con la ayuda de la IA</p>
        <Link href="/login">
          <button className="bg-purple-600 hover:bg-purple-700 text-white text-lg px-6 py-3 rounded-full font-semibold shadow-xl">
            Crear cuenta gratis
          </button>
        </Link>
        <div className="mt-8 flex justify-center">
          <Image
            src="/mascot.png"
            alt="Flashy celebrando"
            width={160}
            height={160}
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#0a0a0a] py-8 text-center text-gray-500 text-sm">
        AI FlashLang © {new Date().getFullYear()} · Aprende mejor, aprende con contexto.
      </footer>
    </main>
  );
}
