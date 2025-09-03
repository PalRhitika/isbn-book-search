import { useState } from "react";
import BookCard from "./components/BookCard";

const API_BASE = import.meta.env.BOOKS_API_BASE_URL || "http://localhost:8000";

function normalizeIsbn(s) {
  return s.replace(/[^0-9Xx]/g, "").toUpperCase();
}

function App() {
  const [isbn, setIsbn] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [book, setBook] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setBook(null);

    const cleaned = normalizeIsbn(isbn);
    if (cleaned.length !== 10 && cleaned.length !== 13) {
      setError("Enter a valid ISBN10 or ISBN13");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/books/${cleaned}/`);
      if (!res.ok) throw new Error("Not found");
      const data = await res.json();
      setBook(data);
    } catch {
      setError("Book not found");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-slate-100 p-6">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold">ISBN Book Search</h1>
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={isbn}
            onChange={(e) => setIsbn(e.target.value)}
            placeholder="Enter ISBN10 or ISBN13"
            className="flex-1 rounded-xl border border-slate-400 px-4 py-3 focus:outline-none focus:ring-1 focus:ring-slate-400"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-xl bg-blue-800 text-white px-5 py-3 shadow hover:opacity-90"
          >
            {loading ? "Searching…" : "Search"}
          </button>
        </form>

        {error && <div className="text-red-600">{error}</div>}
        {book && <BookCard book={book} />}
        {!book && !error && !loading && (
          <p className="text-sm text-slate-800">Tip: try 9781419729072</p>
        )}
      </div>
    </div>
  );
}

export default App;
