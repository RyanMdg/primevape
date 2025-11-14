# PrimeVape Backend API

A robust REST API backend for the PrimeVape e-commerce platform built with Flask and SQLAlchemy.

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Product Management**: Full CRUD operations for products
- **Order Management**: Create, view, and manage orders
- **Category Management**: Organize products by categories
- **Admin Panel**: Admin-only routes for managing products and orders
- **Database**: SQLite for development (easily switchable to PostgreSQL/MySQL)
- **CORS Support**: Configured for frontend integration
- **Security**: Password hashing with bcrypt, JWT tokens

## Tech Stack

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - CORS support
- **Flask-Bcrypt** - Password hashing
- **SQLite** - Database (development)

## Installation

1. Navigate to the backend directory:
```bash
cd primevape-backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Initialize the database with seed data:
```bash
python seed.py
```

7. Run the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login user | No |
| POST | `/refresh` | Refresh access token | Yes (Refresh) |
| GET | `/me` | Get current user profile | Yes |
| PUT | `/me` | Update user profile | Yes |
| POST | `/change-password` | Change password | Yes |

### Products (`/api/products`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Get all products | No |
| GET | `/<id>` | Get product by ID | No |
| POST | `/` | Create product | Yes (Admin) |
| PUT | `/<id>` | Update product | Yes (Admin) |
| DELETE | `/<id>` | Delete product | Yes (Admin) |
| GET | `/categories` | Get all categories | No |

**Query Parameters for GET `/api/products`:**
- `category` - Filter by category
- `featured` - Filter featured products
- `search` - Search by product name
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 100)

### Orders (`/api/orders`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create new order | Yes |
| GET | `/` | Get user's orders | Yes |
| GET | `/<id>` | Get order by ID | Yes |
| POST | `/<id>/cancel` | Cancel order | Yes |
| GET | `/admin/all` | Get all orders | Yes (Admin) |
| PUT | `/<id>/status` | Update order status | Yes (Admin) |

## Request/Response Examples

### Register User

**Request:**
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Login

**Request:**
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Products

**Request:**
```bash
GET /api/products?category=Pods&featured=true
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "RELX Infinity",
      "category": "Pods",
      "price": 29.99,
      "description": "Premium pod system...",
      "image": "https://...",
      "stock": 50,
      "featured": true
    }
  ],
  "total": 10,
  "pages": 1,
  "current_page": 1
}
```

### Create Order

**Request:**
```bash
POST /api/orders
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 4,
      "quantity": 1
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  }
}
```

**Response:**
```json
{
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "order_number": "ORD-20241114-A1B2C3D4",
    "status": "pending",
    "subtotal": 79.97,
    "shipping_cost": 5.99,
    "total": 85.96,
    "items": [...]
  }
}
```

## Database Models

### User
- `id` - Primary key
- `email` - Unique email
- `username` - Unique username
- `password_hash` - Hashed password
- `first_name` - First name
- `last_name` - Last name
- `phone` - Phone number
- `is_admin` - Admin flag
- `created_at` - Timestamp

### Product
- `id` - Primary key
- `name` - Product name
- `category` - Product category
- `price` - Product price
- `description` - Description
- `image` - Image URL
- `stock` - Stock quantity
- `featured` - Featured flag
- `is_active` - Active flag

### Order
- `id` - Primary key
- `user_id` - Foreign key to User
- `order_number` - Unique order number
- `status` - Order status
- `subtotal` - Subtotal amount
- `shipping_cost` - Shipping cost
- `total` - Total amount
- `shipping_*` - Shipping address fields

### OrderItem
- `id` - Primary key
- `order_id` - Foreign key to Order
- `product_id` - Foreign key to Product
- `quantity` - Quantity ordered
- `price` - Price at time of order

## Default Credentials

After running the seed script:

**Admin User:**
- Email: `admin@primevape.com`
- Password: `admin123`

**Test User:**
- Email: `test@example.com`
- Password: `password123`

## Environment Variables

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///primevape.db
CORS_ORIGINS=http://localhost:5173
```

## Security Notes

1. **Change default secrets** in production
2. **Use HTTPS** in production
3. **Update CORS_ORIGINS** to match your frontend domain
4. **Use PostgreSQL or MySQL** in production instead of SQLite
5. **Set strong passwords** for admin users
6. **Enable rate limiting** for API endpoints

## Development

To run in development mode:
```bash
python app.py
```

To run with Flask CLI:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production-grade database (PostgreSQL/MySQL)
3. Use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
4. Set up reverse proxy (Nginx/Apache)
5. Enable HTTPS
6. Set secure environment variables

## Testing

To test the API endpoints, you can use:
- **Postman** - Import the collection
- **cURL** - Command line testing
- **HTTPie** - User-friendly CLI tool

Example with cURL:
```bash
# Test health endpoint
curl http://localhost:5000/health

# Get products
curl http://localhost:5000/api/products

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## Future Enhancements

- Payment gateway integration (Stripe/PayPal)
- Email notifications for orders
- Password reset functionality
- Product reviews and ratings
- Wishlist functionality
- Image upload for products
- Analytics and reporting
- Rate limiting
- Caching with Redis

## License

This project is for educational purposes.
