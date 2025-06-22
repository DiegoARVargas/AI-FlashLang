"use client";

import { useState } from "react";
import AudioButton from "@/components/ui/AudioButton";

interface Language {
  id: number;
  name: string;
  code: string;
}

interface Row {
  word: string;
  translation: string;
  example: string;
  exampleTrans: string;
  deck: string;
  source_lang?: number;
  target_lang?: number;
  context?: string;
  audioWordUrl?: string;
  audioSentenceUrl?: string;
}

export default function EditableTable({ languages }: { languages: Language[] }) {
  const [rows, setRows] = useState<Row[]>([
    { word: "", translation: "", example: "", exampleTrans: "", deck: "" },
  ]);
  const [sourceLang, setSourceLang] = useState<number>(languages[0]?.id || 1);
  const [targetLang, setTargetLang] = useState<number>(languages[1]?.id || 2);
  const [context, setContext] = useState<string>("");

  const updateCell = (
    index: number,
    key: "word" | "translation" | "example" | "exampleTrans" | "deck",
    value: string
  ) => {  
    const updated = [...rows];
    updated[index][key] = value;
    setRows(updated);
  };

  const removeRow = (index: number) => {
    const updated = rows.filter((_, i) => i !== index);
    setRows(updated);
  };

  const addRow = () => {
    setRows([
      ...rows,
      { word: "", translation: "", example: "", exampleTrans: "", deck: "" },
    ]);
  };

  const applyGlobalsToRows = () => {
    const updated = rows.map((row) => ({
      ...row,
      source_lang: sourceLang,
      target_lang: targetLang,
      context,
    }));
    setRows(updated);
  };

  return (
    <div className="bg-neutral-900 p-6 rounded-xl shadow-xl border border-purple-700">
      <div className="flex gap-4 mb-4 flex-wrap">
        <select
          value={sourceLang}
          onChange={(e) => setSourceLang(Number(e.target.value))}
          className="p-2 bg-neutral-800 text-white rounded border border-purple-500"
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
          className="p-2 bg-neutral-800 text-white rounded border border-purple-500"
        >
          {languages.map((lang) => (
            <option key={lang.id} value={lang.id}>
              {lang.name}
            </option>
          ))}
        </select>
        <input
          type="text"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Context (opcional)"
          className="p-2 bg-neutral-800 text-white rounded border border-purple-500 flex-1"
        />
        <button
          onClick={applyGlobalsToRows}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm"
        >
          Aplicar a todas las filas
        </button>
      </div>

      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="text-purple-400 border-b border-purple-700">
            <th className="p-2">Word</th>
            <th className="p-2">Translation</th>
            <th className="p-2">Example</th>
            <th className="p-2">Example Trans</th>
            <th className="p-2">Deck</th>
            <th className="p-2">🔊 Word</th>
            <th className="p-2">🔊 Sentence</th>
            <th className="p-2">❌</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b border-neutral-800">
              <td className="p-2">
                <input
                  value={row.word}
                  onChange={(e) => updateCell(i, "word", e.target.value)}
                  className="bg-transparent text-white border border-neutral-700 p-1 rounded w-full"
                />
              </td>
              <td className="p-2">
                <input
                  value={row.translation}
                  onChange={(e) => updateCell(i, "translation", e.target.value)}
                  className="bg-transparent text-white border border-neutral-700 p-1 rounded w-full"
                />
              </td>
              <td className="p-2">
                <input
                  value={row.example}
                  onChange={(e) => updateCell(i, "example", e.target.value)}
                  className="bg-transparent text-white border border-neutral-700 p-1 rounded w-full"
                />
              </td>
              <td className="p-2">
                <input
                  value={row.exampleTrans}
                  onChange={(e) => updateCell(i, "exampleTrans", e.target.value)}
                  className="bg-transparent text-white border border-neutral-700 p-1 rounded w-full"
                />
              </td>
              <td className="p-2">
                <input
                  value={row.deck}
                  onChange={(e) => updateCell(i, "deck", e.target.value)}
                  className="bg-transparent text-white border border-neutral-700 p-1 rounded w-full"
                />
              </td>
              <td className="p-2">
                {row.audioWordUrl && <AudioButton src={row.audioWordUrl} size={18} />}
              </td>
              <td className="p-2">
                {row.audioSentenceUrl && <AudioButton src={row.audioSentenceUrl} size={18} />}
              </td>
              <td className="p-2">
                <button
                  onClick={() => removeRow(i)}
                  className="text-red-400 hover:text-red-600"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-4">
        <button
          onClick={addRow}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm"
        >
          + Agregar fila
        </button>
      </div>
    </div>
  );
}
