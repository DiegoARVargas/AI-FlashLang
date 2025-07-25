// ✅ EditableTable.tsx
"use client";

import { useState } from "react";
import AudioButton from "@/components/ui/AudioButton";
import Cookies from "js-cookie";

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
  const [rows, setRows] = useState<Row[]>([{ word: "", translation: "", example: "", exampleTrans: "", deck: "" }]);
  const [sourceLang, setSourceLang] = useState<number>(languages[0]?.id || 1);
  const [targetLang, setTargetLang] = useState<number>(languages[1]?.id || 2);
  const [context, setContext] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [generatedIds, setGeneratedIds] = useState<number[]>([]);

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
    setRows([...rows, { word: "", translation: "", example: "", exampleTrans: "", deck: "" }]);
  };

  const clearAllRows = () => {
    setRows([]);
    setGeneratedIds([]);
  };

  const applyGlobalsToRows = () => {
    const updated = rows.map((row) => ({
      ...row,
      source_lang: sourceLang,
      target_lang: targetLang,
      context,
    }));
    setRows(updated);
    alert("🌍 Global values applied to all rows.");
  };

  const handleGenerateAll = async () => {
    setLoading(true);
    const token = Cookies.get("access_token");

    const newRows = await Promise.all(
      rows.map(async (row) => {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}vocabulary/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              word: row.word,
              source_lang: row.source_lang ?? sourceLang,
              target_lang: row.target_lang ?? targetLang,
              context: row.context ?? (context || undefined),
              deck: row.deck || "MyDeck",
            }),
          });

          const data = await response.json();
          const content = data.shared_word || data.custom_content;

          setGeneratedIds((prev) => [...prev, data.id]);

          return {
            ...row,
            translation: content.translation,
            example: content.example_sentence,
            exampleTrans: content.example_translation,
            audioWordUrl: content.audio_word,
            audioSentenceUrl: content.audio_sentence,
          };
        } catch (err) {
          console.error("❌ Error generating row:", row.word);
          return row;
        }
      })
    );

    setRows(newRows);
    alert("✅ Bulk generation complete");
    setLoading(false);
  };

  const handleDownloadDeck = async () => {
    if (generatedIds.length === 0) {
      alert("⚠️ No generated words to download.");
      return;
    }

    try {
      const token = Cookies.get("access_token");
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}vocabulary/download-apkg/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ ids: generatedIds }),
      });

      if (!response.ok) throw new Error("Error generating deck");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "aiflashlang_deck.apkg";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      alert("📦 Deck downloaded successfully");
    } catch (err) {
      console.error("❌ Error downloading deck", err);
      alert("Error downloading the deck.");
    }
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
            <option key={lang.id} value={lang.id}>{lang.name}</option>
          ))}
        </select>
        <select
          value={targetLang}
          onChange={(e) => setTargetLang(Number(e.target.value))}
          className="p-2 bg-neutral-800 text-white rounded border border-purple-500"
        >
          {languages.map((lang) => (
            <option key={lang.id} value={lang.id}>{lang.name}</option>
          ))}
        </select>
        <input
          type="text"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Context (optional)"
          className="p-2 bg-neutral-800 text-white rounded border border-purple-500 flex-1"
        />
        <button
          onClick={applyGlobalsToRows}
          className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm"
        >
          Apply to All Rows
        </button>
        <button
          onClick={handleGenerateAll}
          className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded text-sm disabled:opacity-40"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate All"}
        </button>
        <button
          onClick={clearAllRows}
          className="bg-red-700 hover:bg-red-800 text-white px-4 py-2 rounded text-sm"
        >
          Clear All
        </button>
        <button
          onClick={handleDownloadDeck}
          className="bg-[#2323ff] hover:bg-blue-700 text-white px-4 py-2 rounded text-sm"
        >
          📦 Download Deck
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
                  Delete
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
          + Add Row
        </button>
      </div>
    </div>
  );
}