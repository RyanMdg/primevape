import { useLocation, useNavigate, Link } from 'react-router-dom';
import { FiCheckCircle } from 'react-icons/fi';

function OrderSuccess() {
  const location = useLocation();
  const navigate = useNavigate();
  const order = location.state?.order;

  if (!order) {
    navigate('/');
    return null;
  }

  return (
    <div className="order-success-page">
      <div className="container">
        <div className="success-container">
          <FiCheckCircle style={{ fontSize: '4rem', color: 'var(--primary-black)', marginBottom: '1rem' }} />
          <h1>ORDER PLACED SUCCESSFULLY!</h1>
          <p style={{ fontSize: '1.125rem', color: 'var(--gray-medium)', marginBottom: '2rem' }}>
            Thank you for your order. We'll send you a confirmation email shortly.
          </p>

          <div className="order-details-card">
            <h3>Order Details</h3>
            <div className="order-info">
              <div className="order-info-row">
                <span className="label">Order Number:</span>
                <span className="value">{order.order_number}</span>
              </div>
              <div className="order-info-row">
                <span className="label">Status:</span>
                <span className="value" style={{ textTransform: 'capitalize' }}>{order.status}</span>
              </div>
              <div className="order-info-row">
                <span className="label">Total Amount:</span>
                <span className="value" style={{ fontWeight: 700, fontSize: '1.25rem' }}>
                  ₱{order.total.toFixed(2)}
                </span>
              </div>
            </div>

            <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '2px solid var(--gray-light)' }}>
              <h4 style={{ marginBottom: '1rem' }}>Shipping Address:</h4>
              <p>{order.shipping_address.street}</p>
              <p>{order.shipping_address.city}, {order.shipping_address.state}</p>
              <p>{order.shipping_address.zip_code}, {order.shipping_address.country}</p>
            </div>

            <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '2px solid var(--gray-light)' }}>
              <h4 style={{ marginBottom: '1rem' }}>Items Ordered:</h4>
              {order.items && order.items.map((item, index) => (
                <div key={index} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: '0.75rem',
                  fontSize: '0.9rem'
                }}>
                  <span>{item.product_name} × {item.quantity}</span>
                  <span>₱{item.subtotal.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem', justifyContent: 'center' }}>
            <Link to="/products" className="btn btn-outline">
              Continue Shopping
            </Link>
            <Link to="/" className="btn">
              Back to Home
            </Link>
          </div>

          <div style={{
            marginTop: '3rem',
            padding: '1.5rem',
            backgroundColor: 'var(--gray-lighter)',
            textAlign: 'center',
            fontSize: '0.875rem'
          }}>
            <p><strong>What's Next?</strong></p>
            <p style={{ marginTop: '0.5rem', color: 'var(--gray-medium)' }}>
              We'll prepare your order and ship it as soon as possible.
              You'll receive tracking information via email once your order is shipped.
            </p>
            <p style={{ marginTop: '0.5rem', color: 'var(--gray-medium)' }}>
              Payment will be collected upon delivery (Cash on Delivery).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default OrderSuccess;
