import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ordersAPI } from '../services/api';

function Checkout({ cart, clearCart }) {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    street: '',
    city: '',
    state: '',
    zip_code: '',
    country: 'Philippines'
  });

  const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const shipping = subtotal > 0 ? 150 : 0; // ₱150 flat rate
  const total = subtotal + shipping;

  if (!isAuthenticated) {
    return (
      <div className="checkout-page">
        <div className="container">
          <div className="empty-state">
            <h2>Please Login to Checkout</h2>
            <p>You need to be logged in to place an order</p>
            <button className="btn" onClick={() => navigate('/login')}>
              Go to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (cart.length === 0) {
    return (
      <div className="checkout-page">
        <div className="container">
          <div className="empty-state">
            <h2>Your Cart is Empty</h2>
            <p>Add some items to your cart before checkout</p>
            <button className="btn" onClick={() => navigate('/products')}>
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const orderData = {
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        })),
        shipping_address: formData,
        shipping_cost: shipping
      };

      console.log('Creating order with data:', orderData);
      const result = await ordersAPI.create(orderData);
      console.log('Order created successfully:', result);

      // Clear cart and redirect to success page
      clearCart();
      navigate('/order-success', { state: { order: result.order } });
    } catch (err) {
      console.error('Order creation failed:', err);
      const errorMessage = err.message || 'Failed to create order. Please try again.';
      if (errorMessage.includes('login')) {
        setError('Please login first to place an order.');
      } else {
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="checkout-page">
      <div className="container">
        <h1 className="section-title">CHECKOUT</h1>

        {error && (
          <div className="error-message" style={{ marginBottom: '2rem' }}>
            {error}
          </div>
        )}

        <div className="checkout-grid">
          <div className="checkout-form-section">
            <h2>Shipping Information</h2>
            <form onSubmit={handleSubmit} className="checkout-form">
              <div className="form-group">
                <label htmlFor="street">Street Address *</label>
                <input
                  type="text"
                  id="street"
                  name="street"
                  value={formData.street}
                  onChange={handleChange}
                  required
                  placeholder="123 Main Street, Barangay Name"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="city">City *</label>
                  <input
                    type="text"
                    id="city"
                    name="city"
                    value={formData.city}
                    onChange={handleChange}
                    required
                    placeholder="Manila"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="state">Province/State *</label>
                  <input
                    type="text"
                    id="state"
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    required
                    placeholder="Metro Manila"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="zip_code">Zip Code *</label>
                  <input
                    type="text"
                    id="zip_code"
                    name="zip_code"
                    value={formData.zip_code}
                    onChange={handleChange}
                    required
                    placeholder="1000"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="country">Country *</label>
                  <input
                    type="text"
                    id="country"
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    required
                    readOnly
                  />
                </div>
              </div>

              <button
                type="submit"
                className="btn"
                style={{ width: '100%', marginTop: '2rem' }}
                disabled={loading}
              >
                {loading ? 'Placing Order...' : 'Place Order'}
              </button>
            </form>
          </div>

          <div className="order-summary-section">
            <div className="cart-summary">
              <h3>Order Summary</h3>

              <div className="order-items">
                {cart.map(item => (
                  <div key={item.id} className="order-item">
                    <div>
                      <div style={{ fontWeight: 600 }}>{item.name}</div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--gray-medium)' }}>
                        Qty: {item.quantity}
                      </div>
                    </div>
                    <div style={{ fontWeight: 600 }}>
                      ₱{(item.price * item.quantity).toFixed(2)}
                    </div>
                  </div>
                ))}
              </div>

              <div style={{
                borderTop: '2px solid var(--gray-light)',
                paddingTop: '1rem',
                marginTop: '1rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span>Subtotal</span>
                  <span>₱{subtotal.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span>Shipping</span>
                  <span>₱{shipping.toFixed(2)}</span>
                </div>
              </div>

              <div className="cart-total" style={{ marginTop: '1rem' }}>
                <span>Total</span>
                <span>₱{total.toFixed(2)}</span>
              </div>

              <div style={{
                marginTop: '2rem',
                padding: '1rem',
                backgroundColor: 'var(--gray-lighter)',
                fontSize: '0.875rem'
              }}>
                <p><strong>Payment Method:</strong></p>
                <p>Cash on Delivery (COD)</p>
                <p style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--gray-medium)' }}>
                  *Payment will be collected upon delivery
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Checkout;
