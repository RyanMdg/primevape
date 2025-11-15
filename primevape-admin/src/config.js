const API_URL = import.meta.env.VITE_API_URL || 'https://primevape.onrender.com';

export { API_URL };

export const API_ENDPOINTS = {
  login: `${API_URL}/api/auth/login`,
  register: `${API_URL}/api/auth/register`,
  products: `${API_URL}/api/products`,
  orders: `${API_URL}/api/orders`,
  admin: {
    stats: `${API_URL}/api/admin/stats`,
    products: `${API_URL}/api/admin/products`,
    orders: `${API_URL}/api/admin/orders`,
    users: `${API_URL}/api/admin/users`
  }
};
