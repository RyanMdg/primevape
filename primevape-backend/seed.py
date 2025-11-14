"""
Seed script to populate the database with initial data
Run this script after creating the database
"""

from app import create_app
from models import db, Product, Category, User

def seed_database():
    """Seed the database with initial data"""
    app = create_app()

    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()

        # Create categories
        print("Creating categories...")
        categories = [
            Category(
                name='Vape Pods',
                slug='pods',
                description='Premium vape pod systems',
                image='https://placehold.co/600x400/000000/FFFFFF/png?text=Vape+Pods'
            ),
            Category(
                name='E-Liquids',
                slug='liquids',
                description='High-quality e-liquid flavors',
                image='https://placehold.co/600x400/1a1a1a/FFFFFF/png?text=E-Liquids'
            ),
            Category(
                name='Accessories',
                slug='accessories',
                description='Essential vaping accessories',
                image='https://placehold.co/600x400/2a2a2a/FFFFFF/png?text=Accessories'
            ),
            Category(
                name='New Arrivals',
                slug='new',
                description='Latest products',
                image='https://placehold.co/600x400/000000/FFFFFF/png?text=New+Arrivals'
            )
        ]

        for category in categories:
            db.session.add(category)

        # Create products
        print("Creating products...")
        products = [
            Product(
                name='RELX Infinity',
                category='Pods',
                price=1499.00,
                image='https://placehold.co/400x400/000000/FFFFFF/png?text=RELX+Infinity',
                description='Premium pod system with smooth vapor production and long-lasting battery life.',
                stock=50,
                featured=True
            ),
            Product(
                name='JUUL Starter Kit',
                category='Pods',
                price=1299.00,
                image='https://placehold.co/400x400/1a1a1a/FFFFFF/png?text=JUUL+Starter',
                description='Sleek and portable vaping device with satisfying nicotine delivery.',
                stock=45,
                featured=True
            ),
            Product(
                name='Vaporesso XROS',
                category='Pods',
                price=1799.00,
                image='https://placehold.co/400x400/2a2a2a/FFFFFF/png?text=Vaporesso+XROS',
                description='Adjustable airflow pod system with mesh coil technology.',
                stock=30,
                featured=False
            ),
            Product(
                name='Classic Tobacco 50ml',
                category='Liquids',
                price=599.00,
                image='https://placehold.co/400x400/000000/FFFFFF/png?text=Classic+Tobacco',
                description='Rich tobacco flavor with smooth finish. Available in multiple nicotine strengths.',
                stock=100,
                featured=True
            ),
            Product(
                name='Strawberry Mint 50ml',
                category='Liquids',
                price=699.00,
                image='https://placehold.co/400x400/1a1a1a/FFFFFF/png?text=Strawberry+Mint',
                description='Sweet strawberry with a refreshing mint twist.',
                stock=85,
                featured=False
            ),
            Product(
                name='Mango Ice 50ml',
                category='Liquids',
                price=699.00,
                image='https://placehold.co/400x400/2a2a2a/FFFFFF/png?text=Mango+Ice',
                description='Tropical mango flavor with cooling menthol sensation.',
                stock=90,
                featured=True
            ),
            Product(
                name='USB-C Charging Cable',
                category='Accessories',
                price=299.00,
                image='https://placehold.co/400x400/000000/FFFFFF/png?text=USB-C+Cable',
                description='Fast charging cable compatible with most vape devices.',
                stock=200,
                featured=False
            ),
            Product(
                name='Replacement Pod Pack (3pcs)',
                category='Accessories',
                price=499.00,
                image='https://placehold.co/400x400/1a1a1a/FFFFFF/png?text=Pod+Pack',
                description='Pack of 3 replacement pods for extended vaping enjoyment.',
                stock=150,
                featured=False
            ),
            Product(
                name='SMOK Nord 4',
                category='Pods',
                price=1999.00,
                image='https://placehold.co/400x400/2a2a2a/FFFFFF/png?text=SMOK+Nord+4',
                description='Powerful pod mod with large battery capacity and versatile coil options.',
                stock=40,
                featured=True
            ),
            Product(
                name='Blue Razz Lemonade 50ml',
                category='Liquids',
                price=749.00,
                image='https://placehold.co/400x400/000000/FFFFFF/png?text=Blue+Razz',
                description='Tangy blue raspberry mixed with zesty lemonade.',
                stock=75,
                featured=False
            ),
            Product(
                name='Protective Carrying Case',
                category='Accessories',
                price=399.00,
                image='https://placehold.co/400x400/1a1a1a/FFFFFF/png?text=Case',
                description='Durable case to protect your device on the go.',
                stock=120,
                featured=False
            ),
            Product(
                name='Premium Coil Pack (5pcs)',
                category='Accessories',
                price=599.00,
                image='https://placehold.co/400x400/2a2a2a/FFFFFF/png?text=Coil+Pack',
                description='High-quality replacement coils for optimal flavor.',
                stock=180,
                featured=True
            )
        ]

        for product in products:
            db.session.add(product)

        # Create admin user
        print("Creating admin user...")
        admin = User(
            email='admin@primevape.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create test user
        print("Creating test user...")
        test_user = User(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            phone='1234567890'
        )
        test_user.set_password('password123')
        db.session.add(test_user)

        # Commit all changes
        db.session.commit()

        print("\n✅ Database seeded successfully!")
        print("\nAdmin credentials:")
        print("Email: admin@primevape.com")
        print("Password: admin123")
        print("\nTest user credentials:")
        print("Email: test@example.com")
        print("Password: password123")
        print(f"\nCreated {len(products)} products")
        print(f"Created {len(categories)} categories")


if __name__ == '__main__':
    seed_database()
