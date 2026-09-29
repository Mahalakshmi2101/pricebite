import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach token to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pb_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const searchDishes = async (params = {}) => {
  const response = await api.get('/dishes/search', { params });
  return response.data;
};

export const registerUser = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const getMe = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const getNotifications = async () => {
  const response = await api.get('/notifications');
  return response.data;
};

export const markNotificationRead = async (id) => {
  const response = await api.patch(`/notifications/${id}/read`);
  return response.data;
};

export const markAllRead = async () => {
  const response = await api.patch('/notifications/read-all');
  return response.data;
};

export const seedNotifications = async () => {
  const response = await api.post('/notifications/seed');
  return response.data;
};

export const getPartnerPrefs = async () => {
  const response = await api.get('/partner/preferences');
  return response.data;
};

export const updatePartnerPrefs = async (body) => {
  const response = await api.patch('/partner/preferences', body);
  return response.data;
};

export default api;