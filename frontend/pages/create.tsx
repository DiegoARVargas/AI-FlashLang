"use client";

import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import ProtectedRoute from "@/components/ProtectedRoute";
import Navbar from "@/components/Navbar";
import GeneratedCard from "@/components/ui/GeneratedCard";
import EditableTable from "@/components/ui/EditableTable";

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
      if (res.status === 403) throw new Error("No tienes permisos para usar esta función (¿quizás contexto premium?)");

      const data = await res.json();
      const content = data.shared_word || data.custom_content;

      if (!content) {
        throw new Error("La respuesta del servidor no contiene datos válidos.");
      }

      setResult({
        word: content.word,
        translation: content.translation,
        example_sentence: content.example_sentence,
        translated_sentence: content.example_translation,
        image_url: content.image_url,
        audio_word_url: content.audio_word,
        audio_sentence_url: content.audio_sentence,
      });
    } catch (err: any) {
      setErrorMsg(err.message || "Error al generar palabra.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = () => {
    console.log("✅ Palabra guardada. Acción futura.");
  };

  return (
    <ProtectedRoute>
      <>
        <Navbar />
        <main className="min-h-screen bg-black text-white p-6">
          <div className="flex flex-col lg:flex-row justify-between gap-12 items-start w-full max-w-7xl mx-auto">
            <div className="w-full lg:w-1/2">
              <h1 className="text-3xl font-bold mb-6">Crear nueva palabra</h1>

              {errorMsg && (
                <div className="bg-red-800 text-red-200 p-4 rounded mb-6">
                  {errorMsg}
                </div>
              )}

              <div className="space-y-4">
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

                <input
                  type="text"
                  placeholder="Nombre del mazo (deck)"
                  value={deck}
                  onChange={(e) => setDeck(e.target.value)}
                  className="w-full p-2 rounded bg-neutral-900 border border-neutral-700"
                />

                <button
                  onClick={handleGenerate}
                  disabled={loading || !word}
                  className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-white font-bold disabled:opacity-50"
                >
                  {loading ? "Generando..." : "Generar"}
                </button>
              </div>
            </div>

            {result && (
              <div className="w-full lg:w-1/2 flex flex-col items-center lg:items-end">
                <h2 className="text-3xl font-bold mb-6">Card Preview</h2>
                <GeneratedCard
                  word={result.word}
                  translation={result.translation}
                  example={result.example_sentence}
                  exampleTranslation={result.translated_sentence}
                  imageUrl={result.image_url}
                  audioWordUrl={result.audio_word_url}
                  audioSentenceUrl={result.audio_sentence_url}
                  deckName={deck}
                  onSave={handleSave}
                />
              </div>
            )}
          </div>

          {/* Línea divisoria */}
          <div className="w-full border-t border-blue-500/40 my-12" />

          {/* Carga Masiva */}
          <div className="w-full max-w-7xl mx-auto mb-16">
            <h2 className="text-3xl font-bold mb-4">Carga Masiva de Palabras (.csv)</h2>

            <div
              className="w-full p-10 border-2 border-dashed border-purple-500/40 rounded-xl text-center bg-neutral-900 text-neutral-300 hover:border-purple-500 transition cursor-pointer"
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files?.[0];
                if (file && file.name.endsWith(".csv")) {
                  alert(`📁 Archivo recibido: ${file.name}`);
                } else {
                  alert("❌ Solo se permiten archivos CSV.");
                }
              }}
              onClick={() => document.getElementById("csvInput")?.click()}
            >
              <p className="text-lg">Arrastra aquí tu archivo .csv o haz clic para seleccionarlo</p>
              <p className="text-sm text-neutral-500 mt-2">Formato: word, source_lang_id, target_lang_id, context, deck</p>
            </div>

            <input
              id="csvInput"
              type="file"
              accept=".csv"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file && file.name.endsWith(".csv")) {
                  alert(`📁 Archivo seleccionado: ${file.name}`);
                } else {
                  alert("❌ Solo se permiten archivos CSV.");
                }
              }}
            />
          </div>

          {/* Línea divisoria */}
          <div className="w-full border-t border-blue-500/40 my-12" />

          {/* Carga Manual tipo Excel */}
          <div className="w-full max-w-7xl mx-auto mb-12">
            <h2 className="text-3xl font-bold mb-4 text-white">Carga Manual</h2>
            <EditableTable languages={languages} />
          </div>
        </main>
      </>
    </ProtectedRoute>
  );
}
