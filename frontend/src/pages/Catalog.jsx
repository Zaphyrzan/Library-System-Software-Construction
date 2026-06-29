import { useEffect, useState } from "react";
import API from "../api/client";

export default function Catalog() {
  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  function load(q = "") {
    setLoading(true);
    API.get("/catalog/books/", { params: q ? { search: q } : {} })
      .then((r) => setBooks(r.data.results || r.data))
      .finally(() => setLoading(false));
  }

  useEffect(() => { load(); }, []);

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Collection</div>
        <h1>Catalog</h1>
        <p>Search titles and check availability across all copies.</p>
      </div>
      <div className="toolbar">
        <input
          className="search"
          placeholder="Search by title, author, or ISBN…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && load(search)}
        />
        <button className="btn" onClick={() => load(search)}>Search</button>
        {search && <button className="btn-ghost btn" onClick={() => { setSearch(""); load(); }}>Clear</button>}
      </div>
      <div className="card">
        {loading ? <div className="empty">Loading…</div> : (
          <table>
            <thead>
              <tr><th>Title</th><th>Author</th><th>ISBN</th><th className="right">Available</th></tr>
            </thead>
            <tbody>
              {books.map((b) => (
                <tr key={b.id}>
                  <td>{b.title}</td>
                  <td className="muted">{b.authors.map((a) => a.name).join(", ")}</td>
                  <td className="muted">{b.isbn}</td>
                  <td className="right">
                    <span className={`badge ${b.available_copies > 0 ? "AVAILABLE" : "ON_LOAN"}`}>
                      {b.available_copies} / {b.total_copies}
                    </span>
                  </td>
                </tr>
              ))}
              {books.length === 0 && <tr><td colSpan="4" className="empty">No titles found.</td></tr>}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}
