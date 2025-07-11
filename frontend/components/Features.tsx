// /frontend/components/Features.tsx

import { CheckCircle, Brain, AudioLines, BookOpenCheck, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

const features = [
  {
    icon: <Brain className="w-8 h-8 text-purple-400" aria-hidden="true" />,
    title: 'AI-Powered Learning',
    description:
      'Generate vocabulary flashcards with artificial intelligence: automatic translations, example sentences, and grammar classification.',
  },
  {
    icon: <AudioLines className="w-8 h-8 text-purple-400" aria-hidden="true" />,
    title: 'Automatic Audio',
    description:
      'Listen to the pronunciation of each word and example in English with instantly generated audio.',
  },
  {
    icon: <BookOpenCheck className="w-8 h-8 text-purple-400" aria-hidden="true" />,
    title: 'Spaced Repetition',
    description:
      'Integrate your flashcards into Anki to leverage the power of long-term memory with smart review.',
  },
  {
    icon: <Download className="w-8 h-8 text-purple-400" aria-hidden="true" />,
    title: 'Export Your Decks',
    description:
      'Download decks in .apkg format compatible with Anki, including audio and images with a single click.',
  },
  {
    icon: <CheckCircle className="w-8 h-8 text-purple-400" aria-hidden="true" />,
    title: 'Fully Customizable',
    description:
      'Control your decks, language, phrases, and examples. AI FlashLang adapts to your learning style.',
  },
];

export default function Features() {
  return (
    <section className="max-w-6xl mx-auto px-6 py-20">
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-4xl md:text-5xl font-extrabold mb-4 text-center"
      >
        What You Can Do With <span className="text-purple-400">AI FlashLang</span>
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-gray-400 text-center mb-12 max-w-3xl mx-auto"
      >
        A smart learning platform designed for those who want to learn vocabulary efficiently, visually, and in a personalized way.
      </motion.p>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((feat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-[#111111] rounded-xl p-6 shadow hover:shadow-xl transition-all duration-300 border border-neutral-800"
          >
            <div className="mb-4">{feat.icon}</div>
            <h3 className="text-xl font-semibold mb-2">{feat.title}</h3>
            <p className="text-gray-400 text-sm leading-relaxed">{feat.description}</p>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.6 }}
        className="text-center mt-16"
      >
        <Link
          href="/register"
          className="inline-block bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-300 shadow-md"
        >
          Start Now for Free!
        </Link>
      </motion.div>
    </section>
  );
}
