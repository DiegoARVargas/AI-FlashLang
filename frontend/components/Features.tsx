"use client";

import { motion } from "framer-motion";

export default function Features() {
  return (
    <section className="bg-black py-20 px-6 mt-12">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">¿Por qué aprender con AI FlashLang?</h2>
        <p className="text-gray-400 mb-12">
          Nuestro método basado en inteligencia artificial transforma el aprendizaje de vocabulario.
        </p>

        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold text-blue-400 mb-2">Aprendizaje Contextual</h3>
            <p className="text-gray-300 text-sm">
              Aprende palabras en el contexto de frases reales. Mejora tu comprensión natural del idioma.
            </p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold text-green-400 mb-2">Tarjetas Automatizadas</h3>
            <p className="text-gray-300 text-sm">
              La IA genera automáticamente ejemplos, traducciones, audios y tarjetas tipo Anki.
            </p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold text-pink-400 mb-2">Aprendizaje Multilingüe</h3>
            <p className="text-gray-300 text-sm">
              Compatible con varios idiomas. Aprende inglés, francés, portugués y más según tu idioma nativo.
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
