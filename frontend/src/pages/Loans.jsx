import { useEffect, useState } from "react";
import API, { unwrapList } from "../api/client";

export default function Loans() {
  const [loans, setLoans] = useState([]);
  const [members, setMembers] = useState([]);
  const [copies, setCopies] = useState([]);
  const [memberId, setMemberId] = useState("");
  const [copyId, setCopyId] = useState("");
  const [message, setMessage] = useState(null);

  function loadAll() {
    API.get("/circulation/loans/").then((r) => setLoans(unwrapList(r)));
    API.get("/members/members/").then((r) => setMembers(unwrapList(r)));
    API.get("/catalog/copies/").then((r) => setCopies(unwrapList(r)));
  }

  useEffect(() => { loadAll(); }, []);

  async function checkout() {
    setMessage(null);
    try {
      await API.post("/circulation/loans/checkout/", { member_id: memberId, copy_id: copyId });
      setMessage({ type: "ok", text: "Loan issued." });
      setMemberId(""); setCopyId("");
      loadAll();
    } catch (err) {
      setMessage({ type: "err", text: err.response?.data?.error || "Checkout failed." });
    }
  }

  async function returnLoan(id) {
    await API.post(`/circulation/loans/${id}/return/`);
    loadAll();
  }

  const availableCopies = copies.filter((c) => c.status === "AVAILABLE");

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Circulation</div>
        <h1>Loans</h1>
        <p>Check books out and in. Returns automatically raise fines and release holds.</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>New checkout</h3>
        <div className="row">
          <select value={memberId} onChange={(e) => setMemberId(e.target.value)} style={{ maxWidth: 220 }}>
            <option value="">Select member…</option>
            {members.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
          </select>
          <select value={copyId} onChange={(e) => setCopyId(e.target.value)} style={{ maxWidth: 320 }}>
            <option value="">Select available copy…</option>
            {availableCopies.map((c) => <option key={c.id} value={c.id}>{c.book_title} — {c.barcode}</option>)}
          </select>
          <button className="btn" onClick={checkout} disabled={!memberId || !copyId}>Issue loan</button>
        </div>
        {message && <div className={message.type === "ok" ? "muted" : "error"} style={{ marginTop: 12 }}>{message.text}</div>}
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Loan history</h3>
        <table>
          <thead>
            <tr><th>Book</th><th>Member</th><th>Due</th><th>Status</th><th></th></tr>
          </thead>
          <tbody>
            {loans.map((l) => (
              <tr key={l.id}>
                <td>{l.book_title}</td>
                <td className="muted">{l.member_name}</td>
                <td className="muted">{l.due_date}</td>
                <td>
                  <span className={`badge ${l.is_overdue ? "OVERDUE" : l.status}`}>
                    {l.is_overdue ? "OVERDUE" : l.status}
                  </span>
                </td>
                <td className="right">
                  {l.status === "ACTIVE" && (
                    <button className="btn btn-sm" onClick={() => returnLoan(l.id)}>Return</button>
                  )}
                </td>
              </tr>
            ))}
            {loans.length === 0 && <tr><td colSpan="5" className="empty">No loans yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
