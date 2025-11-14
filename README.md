# PrimeVape - Full Stack E-Commerce Application

A modern, full-stack e-commerce web application for a vape shop, featuring a sleek black and white aesthetic design.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- npm
- pip

### Option 1: Use Start Scripts

**Terminal 1 - Start Backend:**
```bash
cd /Users/rcdeguia/Documents/PrimeVapers
./start-backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /Users/rcdeguia/Documents/PrimeVapers
./start-frontend.sh
```

### Option 2: Manual Setup

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions.

## 📋 Project Overview

### Frontend (React)
- **Location:** `primevape-frontend/`
- **Port:** http://localhost:5173
- **Tech Stack:** React 18, Vite, React Router, CSS3

### Backend (Flask)
- **Location:** `primevape-backend/`
- **Port:** http://localhost:5001
- **Tech Stack:** Flask 3.0, SQLAlchemy, JWT, SQLite

## ✨ Features

### Customer Features
- 🛍️ Product catalog with category filtering
- 🔍 Product search and details
- 🛒 Shopping cart management
- 📦 Order creation and tracking
- 👤 User authentication and profile
- 📱 Fully responsive design

### Admin Features
- ➕ Create/Update/Delete products
- 📊 View all orders
- ✏️ Update order status
- 📈 Manage inventory

## 🎨 Design

- **Theme:** Minimalist black and white
- **Typography:** Modern sans-serif with uppercase headings
- **Layout:** Grid-based responsive design
- **Animations:** Smooth transitions and hover effects

## 📁 Project Structure

```
PrimeVapers/
├── primevape-frontend/          # React Frontend
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── ProductCard.jsx
│   │   ├── pages/               # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Products.jsx
│   │   │   ├── ProductDetail.jsx
│   │   │   └── Cart.jsx
│   │   ├── data/                # Static data
│   │   │   └── products.js
│   │   ├── App.jsx              # Main app component
│   │   ├── index.css            # Global styles
│   │   └── main.jsx             # Entry point
│   └── package.json
│
├── primevape-backend/           # Flask Backend
│   ├── routes/                  # API routes
│   │   ├── products.py          # Product endpoints
│   │   ├── auth.py              # Authentication
│   │   └── orders.py            # Order management
│   ├── models.py                # Database models
│   ├── config.py                # Configuration
│   ├── app.py                   # Flask application
│   ├── seed.py                  # Database seeding
│   └── requirements.txt         # Python dependencies
│
├── SETUP_GUIDE.md               # Detailed setup guide
├── start-backend.sh             # Backend start script
└── start-frontend.sh            # Frontend start script
```

## 🔐 Default Credentials

After running the seed script:

**Admin User:**
- Email: `admin@primevape.com`
- Password: `admin123`

**Test User:**
- Email: `test@example.com`
- Password: `password123`

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/<id>` - Update product (admin)
- `DELETE /api/products/<id>` - Delete product (admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/<id>` - Get order details
- `POST /api/orders/<id>/cancel` - Cancel order

## 🧪 Testing the API

**Get all products:**
```bash
curl http://localhost:5001/api/products
```

**Login:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Create order (with auth token):**
```bash
curl -X POST http://localhost:5001/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "items": [{"product_id": 1, "quantity": 2}],
    "shipping_address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001"
    }
  }'
```

## 📦 Database Schema

### User
- Email, username, password (hashed)
- First name, last name, phone
- Admin flag
- Timestamps

### Product
- Name, category, price
- Description, image URL
- Stock quantity
- Featured flag, active flag
- Timestamps

### Order
- Order number, status
- Subtotal, shipping cost, total
- Shipping address
- User relationship
- Timestamps

### OrderItem
- Product reference
- Quantity, price (at time of order)
- Order relationship

## 🔄 Current Status

### ✅ Completed
- Frontend UI with all pages
- Backend API with all endpoints
- User authentication (JWT)
- Product management (CRUD)
- Order creation and management
- Database models and seeding
- CORS configuration
- Responsive design

### 🚧 Future Enhancements
- Connect frontend to backend API
- Payment gateway integration
- Email notifications
- Product reviews
- Wishlist functionality
- Admin dashboard UI
- Image upload for products
- Password reset
- Advanced search/filters

## 📚 Documentation

- [Setup Guide](./SETUP_GUIDE.md) - Detailed setup instructions
- [Frontend README](./primevape-frontend/README.md) - Frontend documentation
- [Backend README](./primevape-backend/README.md) - API documentation

## 🛡️ Security Notes

1. Change default secrets in production
2. Use HTTPS in production
3. Update CORS origins for production
4. Use PostgreSQL/MySQL in production
5. Implement rate limiting
6. Add input validation
7. Enable CSRF protection

## 🚀 Deployment

### Backend
```bash
# Use Gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Frontend
```bash
# Build for production
npm run build

# Serve with Nginx/Apache
```

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask team for the lightweight backend
- Unsplash for placeholder images
- Feather Icons for the icon set

---

**Made with ❤️ for PrimeVape**
# primevape
