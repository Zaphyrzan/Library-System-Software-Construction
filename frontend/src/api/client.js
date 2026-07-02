import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

// Attach the JWT access token to every request, if present.
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// DRF paginates list endpoints under `.results`, but not every viewset
// enables pagination — this normalizes both shapes for callers.
export function unwrapList(response) {
  return response.data.results || response.data;
}

export default API;
