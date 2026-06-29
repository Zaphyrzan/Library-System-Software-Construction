import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("librarian");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit() {
    setError("");
    setBusy(true);
    try {
      await login(username, password);
      navigate("/");
    } catch {
      setError("Incorrect username or password.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="card login-card">
      <div className="eyebrow">Staff access</div>
      <h1>Reading Room</h1>
      <p className="sub">Sign in to manage the library.</p>
      <div className="field">
        <label>Username</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div className="field">
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        />
      </div>
      <button className="btn" style={{ width: "100%" }} onClick={handleSubmit} disabled={busy}>
        {busy ? "Signing in…" : "Sign in"}
      </button>
      {error && <div className="error">{error}</div>}
      <div className="hint">Demo: librarian / library123</div>
    </div>
  );
}
