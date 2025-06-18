"use client";

import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import ProtectedRoute from "@/components/ProtectedRoute";
import Navbar from "@/components/Navbar";
import GeneratedCard from "@/components/ui/GeneratedCard";

interface Language {
  id: number;
  name: string;
  code: string;
}

interface Result {
  word: string;
  translation: string;
  example_sentence: string;
  translated_sentence: string;
  image_url?: string;
  audio_word_url?: string;
  audio_sentence_url?: string;
}

export default function CreatePage() {
  const [word, setWord] = useState("");
  const [sourceLang, setSourceLang] = useState<number>(1);
  const [targetLang, setTargetLang] = useState<number>(2);
  const [context, setContext] = useState("");
  const [deck, setDeck] = useState("MyDeck");
  const [languages, setLanguages] = useState<Language[]>([]);
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        const token = Cookies.get("access_token");
        const res = await fetch("http://localhost:8010/api/languages/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!res.ok) throw new Error("Error al cargar lenguajes");
        const data = await res.json();
        setLanguages(data);
      } catch (err) {
        setErrorMsg("No se pudieron cargar los lenguajes. Verifica tu autenticación.");
        console.error(err);
      }
    };
    fetchLanguages();
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const token = Cookies.get("access_token");
      const res = await fetch("http://localhost:8010/api/vocabulary/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          word,
          source_lang: sourceLang,
          target_lang: targetLang,
          context: context || undefined,
          deck,
        }),
      });

      if (res.status === 401) throw new Error("Token inválido o expirado. Inicia sesión nuevamente.");
      if (res.status === 403) throw new Error("No tienes permisos para usar esta función (quizás contexto premium?)");

      const data = await res.json();
      const shared = data.shared_word;
      setResult({
        word: shared.word,
        translation: shared.translation,
        example_sentence: shared.example_sentence,
        translated_sentence: shared.example_translation,
        image_url: shared.image_url,
        audio_word_url: shared.audio_word,
        audio_sentence_url: shared.audio_sentence,
      });
    } catch (err: any) {
      setErrorMsg(err.message || "Error al generar palabra.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <>
        <Navbar />
        <main className="min-h-screen bg-black text-white p-6">
          <h1 className="text-3xl font-bold mb-6">Crear nueva palabra</h1>

          {errorMsg && (
            <div className="bg-red-800 text-red-200 p-4 rounded mb-6">
              {errorMsg}
            </div>
          )}

          <section className="flex flex-col lg:flex-row gap-12">
            {/* Formulario */}
            <div className="space-y-4 w-full lg:w-1/2">
              <input
                type="text"
                placeholder="Enter word"
                value={word}
                onChange={(e) => setWord(e.target.value)}
                className="w-full p-2 rounded bg-neutral-900 border border-neutral-700"
              />

              <div className="flex gap-4">
                <select
                  value={sourceLang}
                  onChange={(e) => setSourceLang(Number(e.target.value))}
                  className="w-full p-2 rounded bg-neutral-900 border border-neutral-700"
                >
                  {languages.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
                </select>

                <select
                  value={targetLang}
                  onChange={(e) => setTargetLang(Number(e.target.value))}
                  className="w-full p-2 rounded bg-neutral-900 border border-neutral-700"
                >
                  {languages.map((lang) => (
                    <option key={lang.id} value={lang.id}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <textarea
                placeholder="Context (optional, premium only)"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                className="w-full p-2 rounded bg-neutral-900 border border-neutral-700 min-h-[100px]"
              />

              <button
                onClick={handleGenerate}
                disabled={loading || !word}
                className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-white font-bold disabled:opacity-50"
              >
                {loading ? "Generando..." : "Generar"}
              </button>
            </div>

            {/* Card Preview y acciones */}
            {result && (
              <div className="w-full lg:w-1/2 flex flex-col items-end">
                <h2 className="text-lg text-white mb-2 font-semibold">Card Preview</h2>
                <GeneratedCard
                  word={result.word}
                  translation={result.translation}
                  example={result.example_sentence}
                  exampleTranslation={result.translated_sentence}
                  imageUrl={result.image_url}
                  audioWordUrl={result.audio_word_url}
                  audioSentenceUrl={result.audio_sentence_url}
                />
                <div className="flex gap-4 mt-4">
                  <button className="bg-purple-600 hover:bg-purple-700 text-white font-semibold px-4 py-2 rounded-full text-sm">
                    Guardar
                  </button>
                  <button className="bg-purple-600 hover:bg-purple-700 text-white font-semibold px-4 py-2 rounded-full text-sm">
                    Download
                  </button>
                </div>
              </div>
            )}
          </section>
        </main>
      </>
    </ProtectedRoute>
  );
}
