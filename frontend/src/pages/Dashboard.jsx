import { useEffect, useState } from "react";
import API from "../api/client";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [popular, setPopular] = useState([]);

  useEffect(() => {
    API.get("/reporting/reports/").then((r) => setSummary(r.data));
    API.get("/reporting/reports/popular/").then((r) => setPopular(r.data));
  }, []);

  if (!summary) return <div className="empty">Loading…</div>;

  const stats = [
    { label: "Titles", num: summary.total_books },
    { label: "Copies", num: summary.total_copies },
    { label: "Members", num: summary.total_members },
    { label: "Active loans", num: summary.active_loans },
    { label: "Overdue", num: summary.overdue_loans, alert: true },
    { label: "Pending holds", num: summary.pending_reservations },
    { label: "Unpaid fines (RM)", num: Number(summary.unpaid_fines).toFixed(2), alert: true },
  ];

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">Overview</div>
        <h1>Dashboard</h1>
        <p>A live snapshot of the collection and circulation.</p>
      </div>
      <div className="stat-grid">
        {stats.map((s) => (
          <div key={s.label} className={`stat ${s.alert ? "alert" : ""}`}>
            <div className="num">{s.num}</div>
            <div className="label">{s.label}</div>
          </div>
        ))}
      </div>
      <div className="card" style={{ marginTop: 28 }}>
        <h3 style={{ marginTop: 0 }}>Most borrowed titles</h3>
        <table>
          <thead><tr><th>Title</th><th className="right">Times loaned</th></tr></thead>
          <tbody>
            {popular.map((b) => (
              <tr key={b.title}><td>{b.title}</td><td className="right">{b.loans}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
