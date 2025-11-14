from flask import Blueprint, request, jsonify
from models import db, Product
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

def admin_required(fn):
    """Decorator to require admin access"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        from models import User
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


@products_bp.route('', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        # Get query parameters
        category = request.args.get('category')
        featured = request.args.get('featured')
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)

        # Build query
        query = Product.query.filter_by(is_active=True)

        # Apply filters
        if category:
            query = query.filter_by(category=category)
        if featured:
            query = query.filter_by(featured=True)
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))

        # Paginate
        products = query.order_by(Product.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'products': [p.to_dict() for p in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': products.page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify(product.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create a new product (Admin only)"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'category', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create product
        product = Product(
            name=data['name'],
            category=data['category'],
            price=data['price'],
            description=data.get('description', ''),
            image=data.get('image', ''),
            stock=data.get('stock', 0),
            featured=data.get('featured', False)
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update a product (Admin only)"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = data['price']
        if 'description' in data:
            product.description = data['description']
        if 'image' in data:
            product.image = data['image']
        if 'stock' in data:
            product.stock = data['stock']
        if 'featured' in data:
            product.featured = data['featured']
        if 'is_active' in data:
            product.is_active = data['is_active']

        db.session.commit()

        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete a product (soft delete - Admin only)"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Soft delete - just mark as inactive
        product.is_active = False
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        from models import Category
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify({
            'categories': [c.to_dict() for c in categories]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
