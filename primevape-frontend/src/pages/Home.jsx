import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ProductCard from '../components/ProductCard';
import { productsAPI } from '../services/api';

function Home({ addToCart }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await productsAPI.getAll();
        setProducts(data.products || []);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const featuredProducts = products.filter(product => product.featured);

  if (loading) {
    return (
      <div className="loading-spinner">
        Loading products...
      </div>
    );
  }

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>ELEVATE YOUR VAPING</h1>
            <p>
              Discover premium vaping products curated for the ultimate experience.
              Quality, style, and satisfaction in every puff.
            </p>
            <Link to="/products" className="btn">
              Shop Now
            </Link>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="categories-section">
        <div className="container">
          <h2 className="section-title">Shop by Category</h2>
          <div className="categories-grid">
            <Link to="/products?category=pods" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="category-card">
                <span>Vape Pods</span>
              </div>
            </Link>
            <Link to="/products?category=liquids" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="category-card">
                <span>E-Liquids</span>
              </div>
            </Link>
            <Link to="/products?category=accessories" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="category-card">
                <span>Accessories</span>
              </div>
            </Link>
            <Link to="/products" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="category-card">
                <span>All Products</span>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="featured-products">
        <div className="container">
          <h2 className="section-title">Featured Products</h2>
          <div className="products-grid">
            {featuredProducts.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                addToCart={addToCart}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Banner Section */}
      <section className="hero" style={{ padding: '4rem 0' }}>
        <div className="container">
          <div className="hero-content">
            <h2>NEW TO VAPING?</h2>
            <p style={{ maxWidth: '700px' }}>
              Not sure where to start? Check out our beginner-friendly starter kits
              and explore our comprehensive guides to find the perfect setup for you.
            </p>
            <Link to="/products?category=pods" className="btn">
              View Starter Kits
            </Link>
          </div>
        </div>
      </section>

      {/* All Products Preview */}
      <section className="products-section">
        <div className="container">
          <h2 className="section-title">Popular Products</h2>
          <div className="products-grid">
            {products.slice(0, 6).map(product => (
              <ProductCard
                key={product.id}
                product={product}
                addToCart={addToCart}
              />
            ))}
          </div>
          <div style={{ textAlign: 'center', marginTop: '3rem' }}>
            <Link to="/products" className="btn btn-outline">
              View All Products
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
