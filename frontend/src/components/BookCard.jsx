export default function BookCard({ book }) {
  return (
    <div className="rounded-2xl shadow bg-white p-4 grid grid-cols-1 sm:grid-cols-[120px,1fr] gap-4">
      <div>
        {book.cover_image ? (
          <img
            src={book.cover_image}
            alt={book.title || "cover"}
            className="h-[500px] rounded-xl w-full object-contain"
          />
        ) : (
          <div className="h-[200px] bg-slate-100 rounded-xl grid place-items-center text-slate-400">
            No cover
          </div>
        )}
      </div>
      <div className="space-y-1">
        <h3 className="text-xl font-semibold">{book.title || "Unknown title"}</h3>
        <p className="text-sm text-slate-600">{(book.authors || []).join(", ")}</p>
        <p className="text-sm text-slate-500">
          {book.publisher || "Unknown publisher"}{" "}
          {book.published_date ? `• ${book.published_date}` : ""}
        </p>
        <p className="text-xs text-slate-400">
          Source: {book.source.toUpperCase()} • ISBN: {book.isbn}
        </p>
      </div>
    </div>
  );
}
