import { useParams, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { productsAPI } from '../services/api';
import { FiArrowLeft } from 'react-icons/fi';

function ProductDetail({ addToCart }) {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const data = await productsAPI.getById(id);
        setProduct(data);

        // Fetch all products to get related ones
        const allProducts = await productsAPI.getAll({ category: data.category });
        const related = (allProducts.products || [])
          .filter(p => p.id !== data.id)
          .slice(0, 4);
        setRelatedProducts(related);
      } catch (error) {
        console.error('Failed to fetch product:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="loading-spinner">
        Loading product...
      </div>
    );
  }

  if (!product) {
    return (
      <div className="container" style={{ padding: '4rem 0', textAlign: 'center' }}>
        <h2>Product not found</h2>
        <Link to="/products" className="btn" style={{ marginTop: '2rem' }}>
          Back to Products
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="product-detail">
        <div className="container">
          <Link
            to="/products"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              color: 'var(--primary-black)',
              textDecoration: 'none',
              marginBottom: '2rem',
              fontWeight: 600
            }}
          >
            <FiArrowLeft /> Back to Products
          </Link>

          <div className="product-detail-grid">
            <div className="product-detail-image">
              <img src={product.image} alt={product.name} />
            </div>

            <div className="product-detail-info">
              <div className="product-category">{product.category}</div>
              <h1>{product.name}</h1>
              <div className="product-detail-price">₱{product.price.toFixed(2)}</div>
              <p className="product-description">{product.description}</p>

              <div style={{ marginBottom: '2rem' }}>
                <h4 style={{ marginBottom: '1rem' }}>Product Features:</h4>
                <ul style={{ lineHeight: '2', color: 'var(--gray-medium)', paddingLeft: '1.5rem' }}>
                  <li>Premium quality materials</li>
                  <li>Long-lasting performance</li>
                  <li>Easy to use and maintain</li>
                  <li>Satisfaction guaranteed</li>
                </ul>
              </div>

              <button
                className="btn"
                onClick={() => addToCart(product)}
                style={{ width: '100%', marginBottom: '1rem' }}
              >
                Add to Cart
              </button>

              <div style={{
                backgroundColor: 'var(--gray-lighter)',
                padding: '1.5rem',
                borderRadius: '0',
                border: '2px solid var(--gray-light)'
              }}>
                <h4 style={{ marginBottom: '1rem' }}>Product Information</h4>
                <div style={{ fontSize: '0.875rem', color: 'var(--gray-medium)' }}>
                  <p style={{ marginBottom: '0.5rem' }}><strong>Category:</strong> {product.category}</p>
                  <p style={{ marginBottom: '0.5rem' }}><strong>SKU:</strong> PV-{product.id.toString().padStart(4, '0')}</p>
                  <p><strong>Availability:</strong> In Stock</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Related Products */}
      {relatedProducts.length > 0 && (
        <section className="products-section" style={{ backgroundColor: 'var(--gray-lighter)' }}>
          <div className="container">
            <h2 className="section-title">You May Also Like</h2>
            <div className="products-grid">
              {relatedProducts.map(relatedProduct => (
                <Link
                  key={relatedProduct.id}
                  to={`/product/${relatedProduct.id}`}
                  style={{ textDecoration: 'none', color: 'inherit' }}
                >
                  <div className="product-card">
                    <div className="product-image">
                      <img src={relatedProduct.image} alt={relatedProduct.name} />
                    </div>
                    <div className="product-info">
                      <div className="product-category">{relatedProduct.category}</div>
                      <h3 className="product-name">{relatedProduct.name}</h3>
                      <div className="product-price">₱{relatedProduct.price.toFixed(2)}</div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

export default ProductDetail;
