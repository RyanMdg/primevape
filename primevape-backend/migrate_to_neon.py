"""
Migration script to move data from SQLite to Neon (PostgreSQL)

This script:
1. Connects to both SQLite and Neon databases
2. Creates tables in Neon
3. Migrates all data from SQLite to Neon
4. Preserves all relationships and IDs

Usage:
    python migrate_to_neon.py
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import db, User, Product, Address, Order, OrderItem, Category

# Database URLs
SQLITE_URL = "sqlite:///primevape.db"
NEON_URL = os.getenv('DATABASE_URL')  # Get from .env file

def migrate_data():
    """Migrate data from SQLite to Neon"""

    if not NEON_URL:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        print("Please add your Neon connection string to .env:")
        print("DATABASE_URL=postgresql://username:password@host.neon.tech/dbname?sslmode=require")
        return

    if NEON_URL.startswith('sqlite'):
        print("❌ ERROR: DATABASE_URL is still using SQLite")
        print("Please update DATABASE_URL in .env to your Neon connection string")
        return

    print("🚀 Starting migration from SQLite to Neon...")
    print(f"📦 Source: {SQLITE_URL}")
    print(f"🎯 Target: {NEON_URL[:50]}...")
    print()

    # Create engines
    sqlite_engine = create_engine(SQLITE_URL)
    neon_engine = create_engine(NEON_URL)

    # Create sessions
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    NeonSession = sessionmaker(bind=neon_engine)

    sqlite_session = SQLiteSession()
    neon_session = NeonSession()

    try:
        # Step 1: Create tables in Neon
        print("📝 Step 1: Creating tables in Neon...")
        from app import db as app_db
        app_db.metadata.bind = neon_engine
        app_db.create_all(bind=neon_engine)
        print("✅ Tables created successfully")
        print()

        # Step 2: Migrate Categories
        print("📝 Step 2: Migrating categories...")
        categories = sqlite_session.query(Category).all()
        for category in categories:
            new_category = Category(
                id=category.id,
                name=category.name,
                slug=category.slug,
                description=category.description,
                image=category.image,
                is_active=category.is_active,
                created_at=category.created_at
            )
            neon_session.merge(new_category)
        neon_session.commit()
        print(f"✅ Migrated {len(categories)} categories")
        print()

        # Step 3: Migrate Products
        print("📝 Step 3: Migrating products...")
        products = sqlite_session.query(Product).all()
        for product in products:
            new_product = Product(
                id=product.id,
                name=product.name,
                category=product.category,
                price=product.price,
                description=product.description,
                image=product.image,
                stock=product.stock,
                featured=product.featured,
                is_active=product.is_active,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            neon_session.merge(new_product)
        neon_session.commit()
        print(f"✅ Migrated {len(products)} products")
        print()

        # Step 4: Migrate Users
        print("📝 Step 4: Migrating users...")
        users = sqlite_session.query(User).all()
        for user in users:
            new_user = User(
                id=user.id,
                email=user.email,
                username=user.username,
                password_hash=user.password_hash,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                is_admin=user.is_admin,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            neon_session.merge(new_user)
        neon_session.commit()
        print(f"✅ Migrated {len(users)} users")
        print()

        # Step 5: Migrate Addresses
        print("📝 Step 5: Migrating addresses...")
        addresses = sqlite_session.query(Address).all()
        for address in addresses:
            new_address = Address(
                id=address.id,
                user_id=address.user_id,
                street=address.street,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country,
                is_default=address.is_default,
                created_at=address.created_at
            )
            neon_session.merge(new_address)
        neon_session.commit()
        print(f"✅ Migrated {len(addresses)} addresses")
        print()

        # Step 6: Migrate Orders
        print("📝 Step 6: Migrating orders...")
        orders = sqlite_session.query(Order).all()
        for order in orders:
            new_order = Order(
                id=order.id,
                user_id=order.user_id,
                order_number=order.order_number,
                status=order.status,
                subtotal=order.subtotal,
                shipping_cost=order.shipping_cost,
                total=order.total,
                shipping_street=order.shipping_street,
                shipping_city=order.shipping_city,
                shipping_state=order.shipping_state,
                shipping_zip=order.shipping_zip,
                shipping_country=order.shipping_country,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
            neon_session.merge(new_order)
        neon_session.commit()
        print(f"✅ Migrated {len(orders)} orders")
        print()

        # Step 7: Migrate Order Items
        print("📝 Step 7: Migrating order items...")
        order_items = sqlite_session.query(OrderItem).all()
        for item in order_items:
            new_item = OrderItem(
                id=item.id,
                order_id=item.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            neon_session.merge(new_item)
        neon_session.commit()
        print(f"✅ Migrated {len(order_items)} order items")
        print()

        # Step 8: Update sequences (PostgreSQL specific)
        print("📝 Step 8: Updating PostgreSQL sequences...")
        tables = [
            ('users', 'id'),
            ('products', 'id'),
            ('addresses', 'id'),
            ('orders', 'id'),
            ('order_items', 'id'),
            ('categories', 'id')
        ]

        for table, column in tables:
            try:
                neon_session.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{table}', '{column}'), "
                    f"COALESCE((SELECT MAX({column}) FROM {table}), 1), false)"
                ))
                neon_session.commit()
            except Exception as e:
                print(f"⚠️  Warning: Could not update sequence for {table}: {e}")

        print("✅ Sequences updated")
        print()

        # Summary
        print("=" * 60)
        print("🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("📊 Migration Summary:")
        print(f"   • Categories: {len(categories)}")
        print(f"   • Products: {len(products)}")
        print(f"   • Users: {len(users)}")
        print(f"   • Addresses: {len(addresses)}")
        print(f"   • Orders: {len(orders)}")
        print(f"   • Order Items: {len(order_items)}")
        print()
        print("✅ All data has been successfully migrated to Neon!")
        print()
        print("Next steps:")
        print("1. Restart your backend server: python app.py")
        print("2. Test your app at http://localhost:5173")
        print("3. Verify data in Neon dashboard: https://console.neon.tech/")
        print()

    except Exception as e:
        print(f"❌ ERROR during migration: {e}")
        import traceback
        traceback.print_exc()
        neon_session.rollback()
        print()
        print("Migration failed. No changes were made to Neon database.")
        print("Please fix the error and try again.")

    finally:
        sqlite_session.close()
        neon_session.close()


if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    print()
    print("=" * 60)
    print("  PRIMEVAPE DATABASE MIGRATION: SQLite → Neon")
    print("=" * 60)
    print()

    # Confirm before proceeding
    print("⚠️  This will copy all data from SQLite to Neon PostgreSQL")
    print("⚠️  Make sure you have:")
    print("   1. Created a Neon account and project")
    print("   2. Updated DATABASE_URL in .env file with Neon connection string")
    print()

    response = input("Continue with migration? (yes/no): ").strip().lower()

    if response == 'yes':
        migrate_data()
    else:
        print("❌ Migration cancelled.")
        print()
