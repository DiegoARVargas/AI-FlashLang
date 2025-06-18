"use client";

import { Volume2, Save } from "lucide-react";
import clsx from "clsx";
import { useRef } from "react";

interface GeneratedCardProps {
  word: string;
  translation: string;
  example: string;
  exampleTranslation: string;
  imageUrl?: string;
  audioWordUrl?: string;
  audioSentenceUrl?: string;
  onSave?: () => void;
}

export default function GeneratedCard({
  word,
  translation,
  example,
  exampleTranslation,
  imageUrl,
  audioWordUrl,
  audioSentenceUrl,
  onSave,
}: GeneratedCardProps) {
  const audioWordRef = useRef<HTMLAudioElement | null>(null);
  const audioSentenceRef = useRef<HTMLAudioElement | null>(null);

  return (
    <div className="bg-[#130322] text-white p-6 rounded-2xl border border-purple-700 shadow-lg max-w-2xl w-full relative">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-3xl font-bold">
          {word}
        </h2>
        {audioWordUrl && (
          <button onClick={() => audioWordRef.current?.play()} className="text-purple-400 hover:text-purple-300">
            <Volume2 size={20} />
            <audio ref={audioWordRef} src={audioWordUrl} />
          </button>
        )}
      </div>

      {/* Definiciones / traducciones */}
      <div className="mb-4">
        <p className="text-sm text-neutral-400">Traducción:</p>
        <p className="text-purple-400 font-semibold text-lg">{translation}</p>
      </div>

      {/* Imagen */}
      {imageUrl && (
        <div className="flex justify-center mb-4">
          <img src={imageUrl} alt="Visual" className="rounded-lg w-full max-h-48 object-contain border border-neutral-800" />
        </div>
      )}

      {/* Ejemplo */}
      <div>
        <p className="text-sm text-neutral-400">Ejemplo:</p>
        <div className="flex items-center gap-2">
          <p className="text-white leading-tight">{example}</p>
          {audioSentenceUrl && (
            <button onClick={() => audioSentenceRef.current?.play()} className="text-purple-400 hover:text-purple-300">
              <Volume2 size={18} />
              <audio ref={audioSentenceRef} src={audioSentenceUrl} />
            </button>
          )}
        </div>
        <p className="italic text-purple-300 text-sm mt-1">{exampleTranslation}</p>
      </div>

      {/* Guardar botón */}
      {onSave && (
        <div className="flex justify-end mt-6">
          <button
            onClick={onSave}
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full font-semibold text-sm shadow"
          >
            <Save size={16} /> Guardar
          </button>
        </div>
      )}
    </div>
  );
}
