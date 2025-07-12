import { motion } from "framer-motion";
import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative px-4 py-20 md:py-32 max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between text-center lg:text-left overflow-hidden">
      {/* Main Text */}
      <motion.div className="lg:w-1/2 z-10 mb-10 lg:mb-0">
        <h1 className="text-3xl md:text-5xl font-extrabold leading-tight mb-6">
          Learn Vocabulary with AI
          <span className="block text-purple-400">in Contextual Ways</span>
        </h1>
        <p className="text-lg text-gray-300 mb-8">
          FlashLang generates smart flashcards with examples, audio, and automatic translations so you can learn in context.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
          <Link href="/login">
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold px-6 py-3 rounded-full">
              Start Now
            </button>
          </Link>
          <button
            onClick={() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })}
            className="border border-gray-500 text-gray-300 hover:text-white px-6 py-3 rounded-full text-base w-auto max-w-[220px] mx-auto sm:mx-0"
          >
            See Features
          </button>
        </div>
      </motion.div>

      {/* Flashy video with seamless integration */}
      <motion.div
        initial={{ opacity: 0, x: 100, scale: 0.8 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
        className="lg:w-1/2 z-10 flex justify-center"
      >
        <div className="relative w-full max-w-[700px] aspect-video min-h-[220px] overflow-hidden">
          <video
            src="/videos/flashy-hero_hq_transparent.mp4"
            autoPlay
            muted
            loop
            playsInline
            className="absolute top-0 left-0 w-full h-full object-cover scale-[1.02] translate-y-2 lg:translate-y-0"
          />
        </div>
      </motion.div>
    </section>
  );
}