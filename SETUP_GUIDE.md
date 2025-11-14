# PrimeVape Full Stack Setup Guide

Complete setup guide for running both frontend and backend of the PrimeVape e-commerce application.

## Project Structure

```
PrimeVapers/
├── primevape-frontend/     # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
└── primevape-backend/      # Flask backend API
    ├── routes/
    ├── models.py
    ├── app.py
    └── requirements.txt
```

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.9 or higher)
- npm or yarn
- pip

## Backend Setup (Flask API)

### 1. Navigate to backend directory
```bash
cd primevape-backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
```

### 3. Activate virtual environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up environment variables
```bash
cp .env.example .env
# Edit .env if needed (default values work for local development)
```

### 6. Initialize database with seed data
```bash
python seed.py
```

This will create:
- 12 sample products
- 4 categories
- 1 admin user
- 1 test user

### 7. Start the backend server
```bash
python app.py
```

Backend will run at: **http://localhost:5001**

### Default Credentials

**Admin User:**
- Email: `admin@primevape.com`
- Password: `admin123`

**Test User:**
- Email: `test@example.com`
- Password: `password123`

---

## Frontend Setup (React)

### 1. Navigate to frontend directory
```bash
cd primevape-frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start development server
```bash
npm run dev
```

Frontend will run at: **http://localhost:5173**

---

## Testing the Application

### 1. Access the frontend
Open your browser and navigate to: **http://localhost:5173**

### 2. Browse products
- View home page with featured products
- Navigate to products page
- Filter by category (Pods, E-Liquids, Accessories)
- Click on products to view details

### 3. Shopping cart
- Add products to cart
- View cart
- Update quantities
- Remove items

### 4. Test API endpoints

**Get all products:**
```bash
curl http://localhost:5001/api/products
```

**Login:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Get categories:**
```bash
curl http://localhost:5001/api/products/categories
```

---

## Connecting Frontend to Backend

The frontend is currently using mock data. To connect it to the backend API:

### 1. Update API base URL

Create an API service file in the frontend:

**src/services/api.js:**
```javascript
const API_BASE_URL = 'http://localhost:5001/api';

export const api = {
  // Products
  getProducts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/products?${queryString}`);
    return response.json();
  },

  getProduct: async (id) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}`);
    return response.json();
  },

  // Auth
  login: async (credentials) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    return response.json();
  },

  register: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  },

  // Orders
  createOrder: async (orderData, token) => {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(orderData)
    });
    return response.json();
  }
};
```

### 2. Update frontend pages to use API

Replace the static product data imports with API calls:

```javascript
// In Home.jsx, Products.jsx, etc.
import { api } from '../services/api';
import { useEffect, useState } from 'react';

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProducts().then(data => {
      setProducts(data.products);
      setLoading(false);
    });
  }, []);

  // Rest of component...
}
```

---

## Available API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user (requires auth)
- `PUT /api/auth/me` - Update profile (requires auth)
- `POST /api/auth/change-password` - Change password (requires auth)

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create product (admin only)
- `PUT /api/products/<id>` - Update product (admin only)
- `DELETE /api/products/<id>` - Delete product (admin only)
- `GET /api/products/categories` - Get all categories

### Orders
- `POST /api/orders` - Create order (requires auth)
- `GET /api/orders` - Get user orders (requires auth)
- `GET /api/orders/<id>` - Get single order (requires auth)
- `POST /api/orders/<id>/cancel` - Cancel order (requires auth)
- `GET /api/orders/admin/all` - Get all orders (admin only)
- `PUT /api/orders/<id>/status` - Update order status (admin only)

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in app.py (line 98) or kill the process using the port
lsof -ti:5001 | xargs kill -9
```

**Database errors:**
```bash
# Reset database
rm primevape.db
python seed.py
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
Make sure the backend is configured to allow requests from `http://localhost:5173` in the `.env` file:
```
CORS_ORIGINS=http://localhost:5173
```

---

## Production Deployment

### Backend
1. Use PostgreSQL or MySQL instead of SQLite
2. Set `FLASK_ENV=production`
3. Use Gunicorn or uWSGI:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```
4. Set up Nginx reverse proxy
5. Enable HTTPS
6. Use environment variables for secrets

### Frontend
1. Build production bundle:
   ```bash
   npm run build
   ```
2. Serve static files with Nginx/Apache
3. Update API base URL to production backend
4. Enable HTTPS

---

## Technology Stack

### Frontend
- React 18
- Vite
- React Router DOM
- React Icons
- CSS3

### Backend
- Flask 3.0
- SQLAlchemy 2.0
- Flask-JWT-Extended
- Flask-CORS
- Flask-Bcrypt
- SQLite (development)

---

## Support

For issues or questions:
1. Check the README files in each directory
2. Review the API documentation
3. Check the console for error messages

---

## License

Educational purposes only.
