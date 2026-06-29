import { useEffect, useState } from "react";
import API from "../api/client";

export default function Members() {
  const [members, setMembers] = useState([]);

  useEffect(() => {
    API.get("/members/members/").then((r) => setMembers(r.data.results || r.data));
  }, []);

  return (
    <>
      <div className="page-head">
        <div className="eyebrow">People</div>
        <h1>Members</h1>
        <p>Registered borrowers and their current loan activity.</p>
      </div>
      <div className="card">
        <table>
          <thead>
            <tr><th>Name</th><th>Email</th><th>Membership</th><th>Active loans</th><th>Status</th></tr>
          </thead>
          <tbody>
            {members.map((m) => (
              <tr key={m.id}>
                <td>{m.name}</td>
                <td className="muted">{m.email}</td>
                <td>{m.membership_name}</td>
                <td>{m.active_loan_count}</td>
                <td><span className={`badge ${m.status}`}>{m.status}</span></td>
              </tr>
            ))}
            {members.length === 0 && <tr><td colSpan="5" className="empty">No members yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
