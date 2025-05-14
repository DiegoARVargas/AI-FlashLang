// pages/index.tsx
import Image from 'next/image';
import { useRouter } from 'next/router';
import { motion } from 'framer-motion';

export default function Home() {
  const router = useRouter();

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#0a0a0a] to-[#111827] text-white font-sans">
      {/* Hero section */}
      <section className="flex flex-col-reverse lg:flex-row items-center justify-between px-6 py-20 max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center lg:text-left max-w-xl"
        >
          <h1 className="text-4xl sm:text-6xl font-extrabold mb-6 leading-tight">
            Aprende Vocabulario con IA
            <span className="block text-blue-500">de Forma Contextual</span>
          </h1>
          <p className="text-lg text-gray-300 mb-8">
            AI FlashLang crea tarjetas inteligentes a partir de textos reales para mejorar tu fluidez en inglés, francés, portugués y más. Aprende con ejemplos reales, audios, traducciones y mucho más.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <button
              onClick={() => router.push('/login')}
              className="bg-blue-600 hover:bg-blue-700 transition text-white px-6 py-3 rounded-full font-semibold shadow-lg"
            >
              Empieza ahora
            </button>
            <button
              onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
              className="border border-gray-500 hover:border-white hover:text-white transition px-6 py-3 rounded-full font-semibold text-gray-300"
            >
              Ver ventajas
            </button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          className="mb-10 lg:mb-0"
        >
          <Image
            src="/mascot.png"
            alt="FlashLang Mascot"
            width={320}
            height={320}
            priority
          />
        </motion.div>
      </section>

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

      {/* Footer */}
      <footer className="bg-[#0a0a0a] py-8 text-center text-gray-500 text-sm">
        AI FlashLang © {new Date().getFullYear()} · Aprende mejor, aprende con contexto.
      </footer>
    </main>
  );
}
