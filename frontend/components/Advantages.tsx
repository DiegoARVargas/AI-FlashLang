"use client";

import { motion } from "framer-motion";

export default function Advantages() {
  return (
    <section className="bg-black py-20 px-6 mt-12">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">Why Learn with AI FlashLang?</h2>
        <p className="text-gray-400 mb-12">
          Our AI-based method transforms vocabulary learning.
        </p>

        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg hover:shadow-[0_0_20px_#60a5fa]">
            <h3 className="text-xl font-semibold text-blue-400 mb-2">Contextual Learning</h3>
            <p className="text-gray-300 text-sm">
              Learn words in the context of real sentences. Improve your natural understanding of the language.
            </p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg hover:shadow-[0_0_20px_#34d399]">
            <h3 className="text-xl font-semibold text-green-400 mb-2">Automated Flashcards</h3>
            <p className="text-gray-300 text-sm">
              AI automatically generates examples, translations, audio, and Anki-style flashcards.
            </p>
          </motion.div>

          <motion.div whileHover={{ scale: 1.05 }} className="bg-[#111111] p-6 rounded-xl shadow-lg hover:shadow-[0_0_20px_#f472b6]">
            <h3 className="text-xl font-semibold text-pink-400 mb-2">Multilingual Learning</h3>
            <p className="text-gray-300 text-sm">
              Compatible with multiple languages. Learn English, French, Portuguese, Spanish and more based on your native language.
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}