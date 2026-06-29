import { createContext, useContext, useState } from "react";
import API from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [username, setUsername] = useState(localStorage.getItem("username") || null);

  async function login(user, password) {
    const { data } = await API.post("/auth/token/", { username: user, password });
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    localStorage.setItem("username", user);
    setUsername(user);
  }

  function logout() {
    localStorage.clear();
    setUsername(null);
  }

  return (
    <AuthContext.Provider value={{ username, login, logout, isAuthed: !!username }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
