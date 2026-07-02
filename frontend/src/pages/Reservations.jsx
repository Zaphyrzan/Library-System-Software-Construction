import { useEffect, useState } from "react";
import API, { unwrapList } from "../api/client";

export default function Reservations() {
  const [reservations, setReservations] = useState([]);
  const [members, setMembers] = useState([]);
  const [books, setBooks] = useState([]);
  const [memberId, setMemberId] = useState("");
  const [bookId, setBookId] = useState("");
  const [message, setMessage] = useState(null);

  function loadAll() {
    API.get("/reservations/reservations/").then((r) => setReservations(unwrapList(r)));
    API.get("/members/members/").then((r) => setMembers(unwrapList(r)));
    API.get("/catalog/books/").then((r) => setBooks(unwrapList(r)));
  }

  useEffect(() => { loadAll(); }, []);

  async function reserve() {
    setMessage(null);
    try {
      await API.post("/reservations/reservations/reserve/", { member_id: memberId, book_id: bookId });
      setMessage({ type: "ok", text: "Hold placed." });
      setMemberId(""); setBookId("");
      loadAll();
    } catch (err) {
      setMessage({ type: "err", text: err.response?.data?.error || "Reservation failed." });
    }
  }

  async function cancel(id) {
    await API.post(`/reservations/reservations/${id}/cancel/`);
    loadAll();
  }

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Holds</div>
        <h1>Reservations</h1>
        <p>Place holds on titles. The queue advances automatically when a copy is returned.</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>New reservation</h3>
        <div className="row">
          <select value={memberId} onChange={(e) => setMemberId(e.target.value)} style={{ maxWidth: 220 }}>
            <option value="">Select member…</option>
            {members.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
          </select>
          <select value={bookId} onChange={(e) => setBookId(e.target.value)} style={{ maxWidth: 320 }}>
            <option value="">Select title…</option>
            {books.map((b) => <option key={b.id} value={b.id}>{b.title}</option>)}
          </select>
          <button className="btn" onClick={reserve} disabled={!memberId || !bookId}>Place hold</button>
        </div>
        {message && <div className={message.type === "ok" ? "muted" : "error"} style={{ marginTop: 12 }}>{message.text}</div>}
      </div>

      <div className="card">
        <table>
          <thead>
            <tr><th>Title</th><th>Member</th><th>Position</th><th>Status</th><th></th></tr>
          </thead>
          <tbody>
            {reservations.map((r) => (
              <tr key={r.id}>
                <td>{r.book_title}</td>
                <td className="muted">{r.member_name}</td>
                <td>#{r.queue_position}</td>
                <td><span className={`badge ${r.status}`}>{r.status}</span></td>
                <td className="right">
                  {(r.status === "PENDING" || r.status === "READY") && (
                    <button className="btn btn-sm btn-ghost" onClick={() => cancel(r.id)}>Cancel</button>
                  )}
                </td>
              </tr>
            ))}
            {reservations.length === 0 && <tr><td colSpan="5" className="empty">No reservations.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
