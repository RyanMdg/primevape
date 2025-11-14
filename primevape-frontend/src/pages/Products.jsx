import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { productsAPI } from '../services/api';

function Products({ addToCart }) {
  const [searchParams] = useSearchParams();
  const categoryFilter = searchParams.get('category');
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const params = categoryFilter ? { category: categoryFilter } : {};
        const data = await productsAPI.getAll(params);
        setProducts(data.products || []);
        setFilteredProducts(data.products || []);
        setSelectedCategory(categoryFilter || 'all');
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [categoryFilter]);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    if (category === 'all') {
      setFilteredProducts(products);
    } else {
      const filtered = products.filter(
        product => product.category.toLowerCase() === category.toLowerCase()
      );
      setFilteredProducts(filtered);
    }
  };

  if (loading) {
    return (
      <div className="loading-spinner">
        Loading products...
      </div>
    );
  }

  return (
    <div className="products-section">
      <div className="container">
        <h1 className="section-title">Our Products</h1>

        {/* Category Filter */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1rem',
          marginBottom: '3rem',
          flexWrap: 'wrap'
        }}>
          <button
            className={selectedCategory === 'all' ? 'btn' : 'btn btn-outline'}
            onClick={() => handleCategoryChange('all')}
          >
            All Products
          </button>
          <button
            className={selectedCategory === 'pods' ? 'btn' : 'btn btn-outline'}
            onClick={() => handleCategoryChange('pods')}
          >
            Pods
          </button>
          <button
            className={selectedCategory === 'liquids' ? 'btn' : 'btn btn-outline'}
            onClick={() => handleCategoryChange('liquids')}
          >
            E-Liquids
          </button>
          <button
            className={selectedCategory === 'accessories' ? 'btn' : 'btn btn-outline'}
            onClick={() => handleCategoryChange('accessories')}
          >
            Accessories
          </button>
        </div>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <div className="products-grid">
            {filteredProducts.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                addToCart={addToCart}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <h2>No products found</h2>
            <p>Try adjusting your filters</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Products;
