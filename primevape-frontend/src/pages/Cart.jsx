import { Link } from 'react-router-dom';
import { FiTrash2 } from 'react-icons/fi';

function Cart({ cart, removeFromCart, updateQuantity }) {
  const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const shipping = subtotal > 0 ? 150 : 0; // ₱150 flat rate
  const total = subtotal + shipping;

  if (cart.length === 0) {
    return (
      <div className="cart-page">
        <div className="container">
          <div className="empty-state">
            <h2>Your Cart is Empty</h2>
            <p>Add some items to your cart to get started</p>
            <Link to="/products" className="btn">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <div className="container">
        <h1 className="section-title">Shopping Cart</h1>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>
          <div className="cart-items">
            {cart.map(item => (
              <div key={item.id} className="cart-item">
                <div className="cart-item-image">
                  <img src={item.image} alt={item.name} />
                </div>

                <div className="cart-item-details">
                  <h3 className="cart-item-name">{item.name}</h3>
                  <div className="product-category">{item.category}</div>
                  <div className="cart-item-price">₱{item.price.toFixed(2)}</div>

                  <div className="quantity-controls">
                    <button
                      className="quantity-btn"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      -
                    </button>
                    <span className="quantity">{item.quantity}</span>
                    <button
                      className="quantity-btn"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      +
                    </button>
                  </div>

                  <button
                    className="remove-btn"
                    onClick={() => removeFromCart(item.id)}
                  >
                    <FiTrash2 style={{ marginRight: '0.25rem', verticalAlign: 'middle' }} />
                    Remove Item
                  </button>
                </div>

                <div style={{ fontWeight: 700, fontSize: '1.25rem' }}>
                  ₱{(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary">
            <h3>Order Summary</h3>

            <div style={{
              borderBottom: '2px solid var(--gray-light)',
              paddingBottom: '1rem',
              marginBottom: '1rem'
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

            <div className="cart-total">
              <span>Total</span>
              <span>₱{total.toFixed(2)}</span>
            </div>

            <Link to="/checkout" className="btn checkout-btn">
              Proceed to Checkout
            </Link>

            <Link
              to="/products"
              style={{
                display: 'block',
                textAlign: 'center',
                marginTop: '1rem',
                color: 'var(--gray-medium)',
                textDecoration: 'underline'
              }}
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Cart;
