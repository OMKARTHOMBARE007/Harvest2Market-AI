import axios from 'axios';
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 60000
});
api.interceptors.request.use((config) => { const token = localStorage.getItem('h2m_token'); if (token) config.headers.Authorization = `Bearer ${token}`; return config; });
export function getErrorMessage(error) { return error.response?.data?.detail || error.message || 'Something went wrong. Please try again.'; }
export default api;
