// /frontend/components/FeatureTimeline.tsx

"use client";

import { motion } from "framer-motion";
import {
  Brain,
  AudioLines,
  BookOpenCheck,
  Download,
  CheckCircle,
} from "lucide-react";
import Link from "next/link";

const features = [
  {
    icon: <Brain className="w-6 h-6 text-purple-400" />,
    title: "AI-Powered Learning",
    description:
      "Create flashcards with automatic translation, grammar, and example generation.",
  },
  {
    icon: <AudioLines className="w-6 h-6 text-purple-400" />,
    title: "Instant Pronunciation",
    description: "Each word and sentence comes with audio so you can listen anytime.",
  },
  {
    icon: <BookOpenCheck className="w-6 h-6 text-purple-400" />,
    title: "Spaced Repetition",
    description: "Master long-term memory using your Anki-compatible cards.",
  },
  {
    icon: <Download className="w-6 h-6 text-purple-400" />,
    title: "One-Click Export",
    description: "Download your vocabulary decks with embedded audio and images.",
  },
  {
    icon: <CheckCircle className="w-6 h-6 text-purple-400" />,
    title: "Your Learning, Your Style",
    description: "Customize your examples, decks, languages and more.",
  },
];

export default function FeatureTimeline() {
  return (
    <section className="relative py-24 bg-gradient-to-b from-black to-neutral-900 text-white">
      {/* Falling card animation */}
      <motion.div
        className="absolute top-[-100px] left-1/2 z-10 w-[120px] h-[180px] bg-[#1a1a1a] border border-purple-500 rounded-xl shadow-lg"
        style={{
          backgroundImage: `url('/logo_white.svg')`,
          backgroundSize: "60%",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
        animate={{
          top: "100vh",
          rotateY: 1080,
          rotateZ: 360,
          opacity: [1, 0],
        }}
        transition={{
          duration: 5,
          ease: "easeOut",
          repeat: Infinity,
        }}
      />

      {/* Section title */}
      <div className="text-center mb-20 relative z-20">
        <h2 className="text-4xl font-bold mb-4">
          Key Features of <span className="text-purple-400">AI FlashLang</span>
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          Explore how AI FlashLang helps you learn smarter with personalized vocabulary.
        </p>
      </div>

      {/* Vertical line */}
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 h-full w-1 bg-purple-800/20 z-0 pointer-events-none" />

      {/* Timeline features */}
      <div className="relative z-10 max-w-5xl mx-auto px-6">
        {features.map((feat, index) => (
          <motion.div
            key={index}
            className={`relative mb-10 md:mb-16 flex flex-col md:flex-row ${
              index % 2 === 0 ? "md:flex-row-reverse" : ""
            } items-center gap-6 group cursor-pointer`}
            initial={{ opacity: 0, x: index % 2 === 0 ? 100 : -100 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: index * 0.1 }}
            viewport={{ once: true }}
          >
            {/* Line connector dot */}
            <div className="w-6 h-6 bg-purple-500 rounded-full border-4 border-white shadow-md z-20" />

            {/* Text block wrapped in Link */}
            <Link
              href="/features"
              className="bg-[#111111] p-6 rounded-xl border border-neutral-800 w-full md:w-1/2 shadow-md group-hover:shadow-[0_0_35px_5px_rgba(168,85,247,0.6)] transition-all duration-300 transform group-hover:scale-[1.02]"
            >
              <div className="flex items-center gap-3 mb-2">
                {feat.icon}
                <h3 className="text-xl font-semibold">{feat.title}</h3>
              </div>
              <p className="text-gray-400 text-sm">{feat.description}</p>
            </Link>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
