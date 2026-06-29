import { useEffect, useState } from "react";
import API from "../api/client";

export default function Reports() {
  const [fines, setFines] = useState([]);
  const [overdue, setOverdue] = useState([]);

  function loadAll() {
    API.get("/reporting/fines/").then((r) => setFines(r.data.results || r.data));
    API.get("/reporting/reports/overdue/").then((r) => setOverdue(r.data));
  }

  useEffect(() => { loadAll(); }, []);

  async function pay(id) {
    await API.post(`/reporting/fines/${id}/pay/`);
    loadAll();
  }

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Reporting</div>
        <h1>Reports & Fines</h1>
        <p>Outstanding penalties and currently overdue loans.</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <h3 style={{ marginTop: 0 }}>Fines</h3>
        <table>
          <thead>
            <tr><th>Member</th><th>Title</th><th>Reason</th><th className="right">Amount (RM)</th><th>Status</th><th></th></tr>
          </thead>
          <tbody>
            {fines.map((f) => (
              <tr key={f.id}>
                <td>{f.member_name}</td>
                <td className="muted">{f.book_title}</td>
                <td>{f.reason}</td>
                <td className="right">{Number(f.amount).toFixed(2)}</td>
                <td><span className={`badge ${f.paid ? "ACTIVE" : "PENDING"}`}>{f.paid ? "PAID" : "UNPAID"}</span></td>
                <td className="right">
                  {!f.paid && <button className="btn btn-sm" onClick={() => pay(f.id)}>Mark paid</button>}
                </td>
              </tr>
            ))}
            {fines.length === 0 && <tr><td colSpan="6" className="empty">No fines on record.</td></tr>}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3 style={{ marginTop: 0 }}>Overdue loans</h3>
        <table>
          <thead>
            <tr><th>Member</th><th>Title</th><th>Due date</th><th className="right">Days late</th></tr>
          </thead>
          <tbody>
            {overdue.map((o) => (
              <tr key={o.loan_id}>
                <td>{o.member}</td>
                <td className="muted">{o.book}</td>
                <td>{o.due_date}</td>
                <td className="right"><span className="badge OVERDUE">{o.days_late}</span></td>
              </tr>
            ))}
            {overdue.length === 0 && <tr><td colSpan="4" className="empty">Nothing overdue right now.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
