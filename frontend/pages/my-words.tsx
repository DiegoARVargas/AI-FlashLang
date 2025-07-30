// ✅ frontend/pages/my-words.tsx (mejora dinámica de deck + restauración botón delete)
"use client";

import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import Navbar from "@/components/Navbar";
import ProtectedRoute from "@/components/ProtectedRoute";
import VerifiedRoute from "@/components/VerifiedRoute";

interface WordEntry {
  id: number;
  deck: string;
  created_at: string;
  shared_word?: {
    word: string;
    translation: string;
  };
  custom_content?: {
    word: string;
    translation: string;
  };
}

export default function MyWordsPage() {
  const [words, setWords] = useState<WordEntry[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [deckFilter, setDeckFilter] = useState<string>("");
  const [allowDuplicates, setAllowDuplicates] = useState<boolean>(false);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const itemsPerPage = 20;

  useEffect(() => {
    const fetchWords = async () => {
      const token = Cookies.get("access_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}vocabulary/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await res.json();
      setWords(data);
    };
    fetchWords();
  }, []);

  const toggleSelection = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    const visibleIds = paginatedWords.map((entry) => entry.id);
    const allSelected = visibleIds.every((id) => selectedIds.includes(id));
    if (allSelected) {
      setSelectedIds((prev) => prev.filter((id) => !visibleIds.includes(id)));
    } else {
      const newIds = visibleIds.filter((id) => !selectedIds.includes(id));
      setSelectedIds((prev) => [...prev, ...newIds]);
    }
  };

  const handleDeleteSelected = async () => {
    if (!selectedIds.length) return;
    const confirmed = confirm("⚠️ Are you sure you want to delete the selected words?");
    if (!confirmed) return;

    const token = Cookies.get("access_token");
    await Promise.all(
      selectedIds.map((id) =>
        fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}vocabulary/${id}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      )
    );
    setWords((prev) => prev.filter((entry) => !selectedIds.includes(entry.id)));
    setSelectedIds([]);
  };

  const handleDownloadSelected = async () => {
    if (!selectedIds.length) return;

    const selectedWords = words.filter((entry) => selectedIds.includes(entry.id));
    const uniqueDecks = new Set(selectedWords.map((entry) => entry.deck.trim()));

    let finalDeckName = "custom";

    if (uniqueDecks.size === 1) {
      finalDeckName = [...uniqueDecks][0] || "custom";
    } else {
      const userInput = prompt(
        "You selected words from multiple decks. Please enter a name for the new deck:",
        ""
      );
      finalDeckName = userInput?.trim() || "custom";
    }

    const token = Cookies.get("access_token");
    const filename = `aiflashlang_${finalDeckName}.apkg`;

    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}vocabulary/download-apkg/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        ids: selectedIds,
        deck_name: finalDeckName,
        allow_duplicates: allowDuplicates,
      }),
    });

    if (!res.ok) {
      alert("❌ Failed to download selected deck.");
      return;
    }

    const blob = await res.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(downloadUrl);
  };

  const filteredWords = words.filter((entry) =>
    deckFilter.trim() === ""
      ? true
      : entry.deck.toLowerCase().includes(deckFilter.trim().toLowerCase())
  );

  const hasOrphanWords = words.some((entry) => !entry.shared_word && !entry.custom_content);

  const getWordText = (entry: WordEntry) => {
    if (entry.custom_content?.word) return entry.custom_content.word;
    if (entry.shared_word?.word) return entry.shared_word.word;
    return "❌ Invalid word";
  };

  const getTranslationText = (entry: WordEntry) => {
    if (entry.custom_content?.translation) return entry.custom_content.translation;
    if (entry.shared_word?.translation) return entry.shared_word.translation;
    return "❌ No translation";
  };

  const totalPages = Math.ceil(filteredWords.length / itemsPerPage);
  const paginatedWords = filteredWords.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <ProtectedRoute>
      <VerifiedRoute>
        <div className="p-8 bg-black text-white min-h-screen">
          <Navbar />

          <h1 className="text-3xl font-bold mb-4">My Words</h1>

          {hasOrphanWords && (
            <div className="bg-yellow-900 text-yellow-300 p-4 rounded mb-6 border border-yellow-600">
              ⚠️ Some words are incomplete (missing shared or custom content).
            </div>
          )}

          <div className="flex gap-4 mb-6">
            <button
              className="bg-red-700 hover:bg-red-800 text-white px-4 rounded"
              onClick={handleDeleteSelected}
            >
              Delete Selected
            </button>
            <input
              type="text"
              placeholder="Filter by deck name"
              value={deckFilter}
              onChange={(e) => setDeckFilter(e.target.value)}
              className="p-2 bg-neutral-800 text-white rounded border border-purple-500"
            />
            <button
              className="bg-red-700 hover:bg-red-800 text-white px-4 rounded"
              onClick={handleDeleteSelected}
            >
              Delete Selected
            </button>
            <button
              className="bg-blue-700 hover:bg-blue-800 text-white px-4 rounded"
              onClick={handleDownloadSelected}
            >
              Download Selected
            </button>
            <label className="flex items-center gap-2 text-sm text-gray-300">
              <input
                type="checkbox"
                checked={allowDuplicates}
                onChange={(e) => setAllowDuplicates(e.target.checked)}
              />
              Allow duplicates
            </label>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead className="sticky top-0 bg-black z-10">
                <tr className="text-purple-400 border-b border-purple-700">
                  <th className="p-2">
                    <input
                      type="checkbox"
                      onChange={toggleSelectAll}
                      checked={
                        paginatedWords.length > 0 &&
                        paginatedWords.every((entry) => selectedIds.includes(entry.id))
                      }
                    />
                  </th>
                  <th className="p-2">Word</th>
                  <th className="p-2">Translation</th>
                  <th className="p-2">Deck</th>
                  <th className="p-2">Created</th>
                </tr>
              </thead>
              <tbody>
                {paginatedWords.map((entry) => (
                  <tr key={entry.id} className="border-b border-neutral-800">
                    <td className="p-2">
                      <input
                        type="checkbox"
                        checked={selectedIds.includes(entry.id)}
                        onChange={() => toggleSelection(entry.id)}
                      />
                    </td>
                    <td className="p-2">{getWordText(entry)}</td>
                    <td className="p-2">{getTranslationText(entry)}</td>
                    <td className="p-2">{entry.deck}</td>
                    <td className="p-2">
                      {new Date(entry.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex justify-center gap-2 mt-6">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-3 py-1 rounded border ${
                  page === currentPage
                    ? "bg-purple-700 text-white border-purple-500"
                    : "bg-neutral-800 text-gray-300 border-neutral-700 hover:bg-neutral-700"
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        </div>
      </VerifiedRoute>
    </ProtectedRoute>
  );
}