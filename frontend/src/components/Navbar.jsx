import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  ["/", "Dashboard"],
  ["/catalog", "Catalog"],
  ["/members", "Members"],
  ["/loans", "Loans"],
  ["/reservations", "Reservations"],
  ["/reports", "Reports & Fines"],
];

export default function Navbar() {
  const { username, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">❦</span>
        <div>
          <div className="brand-name">Reading Room</div>
          <div className="brand-sub">Library Management</div>
        </div>
      </div>
      <nav>
        {links.map(([to, label]) => (
          <NavLink key={to} to={to} end={to === "/"} className="nav-link">
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-foot">
        <span className="user-chip">{username}</span>
        <button className="btn-text" onClick={() => { logout(); navigate("/login"); }}>
          Sign out
        </button>
      </div>
    </aside>
  );
}
