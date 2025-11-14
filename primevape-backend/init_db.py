"""
Initialize Neon database with tables and sample data for PrimeVape
"""

from app import create_app
from models import db, Product, Category, User
from datetime import datetime
import os

def init_database():
    """Initialize database with tables and sample data"""

    app = create_app(os.getenv('FLASK_ENV', 'development'))

    with app.app_context():
        print("🚀 Initializing Neon database...")
        print()

        # Create all tables
        print("📝 Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully")
        print()

        # Check if products already exist
        existing_products = Product.query.count()
        if existing_products > 0:
            print(f"⚠️  Database already has {existing_products} products")
            print("Skipping sample data creation.")
            return

        # Create sample categories
        print("📝 Creating categories...")
        categories_data = [
            {
                'name': 'Pod Systems',
                'slug': 'pod-systems',
                'description': 'Compact and portable vaping devices',
                'image': 'https://images.unsplash.com/photo-1609647959831-e2d53e2b4f35?w=500'
            },
            {
                'name': 'E-Liquids',
                'slug': 'e-liquids',
                'description': 'Premium e-liquid flavors',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500'
            },
            {
                'name': 'Accessories',
                'slug': 'accessories',
                'description': 'Vaping accessories and essentials',
                'image': 'https://images.unsplash.com/photo-1611433050288-86e1af5e7f38?w=500'
            }
        ]

        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)

        db.session.commit()
        print(f"✅ Created {len(categories_data)} categories")
        print()

        # Create sample products
        print("📝 Creating sample products...")
        products_data = [
            # Pod Systems
            {
                'name': 'RELX Infinity Pod System',
                'category': 'Pods',
                'price': 1299.00,
                'description': 'Premium pod system with leak-resistant design and smooth vapor production. Features SmartPace vibration alerts.',
                'image': 'https://images.unsplash.com/photo-1609647959831-e2d53e2b4f35?w=500',
                'stock': 25,
                'featured': True
            },
            {
                'name': 'Vaporesso XROS 3 Pod Kit',
                'category': 'Pods',
                'price': 899.00,
                'description': 'Sleek and powerful pod system with adjustable airflow and long-lasting battery.',
                'image': 'https://images.unsplash.com/photo-1609647959831-e2d53e2b4f35?w=500',
                'stock': 30,
                'featured': True
            },
            {
                'name': 'JUUL2 Pod System',
                'category': 'Pods',
                'price': 1499.00,
                'description': 'Next-generation pod system with improved battery life and enhanced flavor.',
                'image': 'https://images.unsplash.com/photo-1609647959831-e2d53e2b4f35?w=500',
                'stock': 20,
                'featured': False
            },

            # E-Liquids
            {
                'name': 'Strawberry Ice E-Liquid 30ml',
                'category': 'Liquids',
                'price': 299.00,
                'description': 'Sweet strawberry with refreshing menthol finish. 50mg nicotine salt.',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500',
                'stock': 50,
                'featured': True
            },
            {
                'name': 'Mango Ice E-Liquid 30ml',
                'category': 'Liquids',
                'price': 299.00,
                'description': 'Tropical mango flavor with cooling menthol. 50mg nicotine salt.',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500',
                'stock': 45,
                'featured': True
            },
            {
                'name': 'Grape Ice E-Liquid 30ml',
                'category': 'Liquids',
                'price': 299.00,
                'description': 'Juicy grape with icy menthol finish. 50mg nicotine salt.',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500',
                'stock': 40,
                'featured': False
            },
            {
                'name': 'Classic Tobacco E-Liquid 30ml',
                'category': 'Liquids',
                'price': 299.00,
                'description': 'Authentic tobacco flavor for traditional taste. 50mg nicotine salt.',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500',
                'stock': 35,
                'featured': False
            },

            # Accessories
            {
                'name': 'USB-C Charging Cable',
                'category': 'Accessories',
                'price': 149.00,
                'description': 'Fast charging USB-C cable compatible with most pod systems.',
                'image': 'https://images.unsplash.com/photo-1611433050288-86e1af5e7f38?w=500',
                'stock': 100,
                'featured': False
            },
            {
                'name': 'Replacement Pods (3-Pack)',
                'category': 'Accessories',
                'price': 399.00,
                'description': 'Pack of 3 replacement pods for RELX devices.',
                'image': 'https://images.unsplash.com/photo-1611433050288-86e1af5e7f38?w=500',
                'stock': 60,
                'featured': True
            },
            {
                'name': 'Vape Carrying Case',
                'category': 'Accessories',
                'price': 249.00,
                'description': 'Protective carrying case for your vape and accessories.',
                'image': 'https://images.unsplash.com/photo-1611433050288-86e1af5e7f38?w=500',
                'stock': 40,
                'featured': False
            },
            {
                'name': 'Silicone Protective Sleeve',
                'category': 'Accessories',
                'price': 99.00,
                'description': 'Durable silicone sleeve to protect your device from drops and scratches.',
                'image': 'https://images.unsplash.com/photo-1611433050288-86e1af5e7f38?w=500',
                'stock': 75,
                'featured': False
            },
        ]

        for prod_data in products_data:
            product = Product(**prod_data)
            db.session.add(product)

        db.session.commit()
        print(f"✅ Created {len(products_data)} products")
        print()

        # Create admin user
        print("📝 Creating admin user...")
        admin_user = User(
            email='admin@primevape.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin user created")
        print("   Email: admin@primevape.com")
        print("   Password: admin123")
        print()

        # Summary
        print("=" * 60)
        print("🎉 DATABASE INITIALIZATION COMPLETED!")
        print("=" * 60)
        print()
        print("📊 Summary:")
        print(f"   • Categories: {len(categories_data)}")
        print(f"   • Products: {len(products_data)}")
        print(f"   • Admin Users: 1")
        print()
        print("✅ Your Neon database is ready!")
        print()
        print("Next steps:")
        print("1. Restart backend: python app.py")
        print("2. Open app: http://localhost:5173")
        print("3. Browse products and test features")
        print("4. Login as admin: admin@primevape.com / admin123")
        print()

if __name__ == '__main__':
    init_database()
