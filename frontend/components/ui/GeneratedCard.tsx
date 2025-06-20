"use client";

import { useState } from "react";
import { Save, Download } from "lucide-react";
import AudioButton from "@/components/ui/AudioButton";

interface GeneratedCardProps {
  word: string;
  translation: string;
  example: string;
  exampleTranslation: string;
  imageUrl?: string;
  audioWordUrl?: string;
  audioSentenceUrl?: string;
  onSave?: () => void;
  onDownload?: () => void;
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
  onDownload,
}: GeneratedCardProps) {
  const [showTranslation, setShowTranslation] = useState(false);
  return (
    <div className="relative flex flex-col w-full max-w-[560px] bg-[#130322] border border-purple-700 rounded-2xl shadow-xl text-white p-6">

      {/* Header */}
      <div className="mb-3">
        <div className="flex items-center gap-8">
          <h1 className="text-3xl font-bold">{word}</h1>
          {audioWordUrl && <AudioButton src={audioWordUrl} size={28} />}
        </div>
      </div>

      {/* Línea separadora */}
      <div className="border-t border-gray-700 my-4" />

      {/* Traducción */}
      <div className="mb-3">
        <p className="text-sm text-neutral-400 mb-1">Traducción:</p>
        <p className="text-purple-400 text-lg font-semibold">{translation}</p>
      </div>

      {/* Línea separadora */}
      <div className="border-t border-gray-700 my-4" />

      {/* Imagen */}
      {imageUrl && (
        <div className="mb-4">
          <img
            src={imageUrl}
            alt="Imagen generada"
            className="w-full h-[140px] object-contain rounded-md border border-neutral-800"
          />
        </div>
      )}

      {/* Ejemplo */}
      <div className="mb-3">
        <p className="text-sm text-neutral-400 mb-1">Ejemplo:</p>
        <div className="flex items-center gap-2">
          <p className="text-white leading-tight">{example}</p>
          {audioSentenceUrl && <AudioButton src={audioSentenceUrl} size={24} />}
        </div>
        <p
          className="italic text-sm text-neutral-500 cursor-pointer hover:text-purple-300 transition"
          onClick={() => setShowTranslation((prev) => !prev)}
        >
          {showTranslation ? exampleTranslation : "translate"}
        </p>
      </div>

      {/* Línea separadora */}
      <div className="border-t border-gray-700 my-4" />

      {/* Acciones */}
      <div className="flex justify-end gap-4 mt-4">
        {onDownload && (
          <button
            onClick={onDownload}
            className="flex items-center gap-2 border border-purple-500 text-purple-300 hover:bg-purple-800/10 px-4 py-2 rounded-full text-sm transition"
          >
            <Download size={16} /> Descargar
          </button>
        )}
        {onSave && (
          <button
            onClick={onSave}
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full font-semibold text-sm shadow"
          >
            <Save size={16} /> Guardar
          </button>
        )}
      </div>
    </div>
  );
}
