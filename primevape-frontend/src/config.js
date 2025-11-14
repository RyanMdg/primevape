/**
 * Application Configuration
 *
 * This file centralizes all configuration values, especially API URLs.
 * Uses environment variables that are different for local dev and production.
 */

// API Base URL - automatically switches between local and production
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

// API Endpoints
export const API_ENDPOINTS = {
  // Products
  products: `${API_URL}/api/products`,
  productById: (id) => `${API_URL}/api/products/${id}`,

  // Authentication
  register: `${API_URL}/api/auth/register`,
  login: `${API_URL}/api/auth/login`,
  profile: `${API_URL}/api/auth/profile`,

  // Orders
  orders: `${API_URL}/api/orders`,
  createOrder: `${API_URL}/api/orders`,
  orderById: (id) => `${API_URL}/api/orders/${id}`,

  // Chatbot
  chatbot: `${API_URL}/api/chatbot/chat`,
};

// Environment info (useful for debugging)
export const ENV = {
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  apiUrl: API_URL,
};

// Log configuration on load (only in development)
if (ENV.isDevelopment) {
  console.log('🔧 App Configuration:', {
    environment: ENV.isDevelopment ? 'Development' : 'Production',
    apiUrl: API_URL,
  });
}

export default {
  API_URL,
  API_ENDPOINTS,
  ENV,
};
