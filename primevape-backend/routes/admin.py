from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Product, Order, Category
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        return fn(*args, **kwargs)
    return wrapper


# ============ ORDER MANAGEMENT ============

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def get_all_orders():
    """Get all orders with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status_filter = request.args.get('status', None)

        query = Order.query

        if status_filter:
            query = query.filter_by(status=status_filter)

        orders = query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/orders/<int:order_id>', methods=['GET'])
@admin_required
def get_order_details(order_id):
    """Get detailed information about a specific order"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        order = Order.query.get_or_404(order_id)

        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        new_status = data.get('status')

        if new_status not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400

        order.status = new_status
        db.session.commit()

        return jsonify({
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@admin_required
def delete_order(order_id):
    """Delete an order"""
    try:
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ PRODUCT MANAGEMENT ============

@admin_bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()

        required_fields = ['name', 'description', 'price', 'category', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        product = Product(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            category=data['category'],
            stock=int(data['stock']),
            image=data.get('image', ''),
            featured=data.get('featured', False),
            is_active=data.get('is_active', True)
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


@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update an existing product"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # Update allowed fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'category' in data:
            product.category = data['category']
        if 'stock' in data:
            product.stock = int(data['stock'])
        if 'image' in data:
            product.image = data['image']
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


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete a product"""
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============ DASHBOARD STATS ============

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        total_orders = Order.query.count()
        total_products = Product.query.count()
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
        pending_orders = Order.query.filter_by(status='pending').count()

        return jsonify({
            'total_orders': total_orders,
            'total_products': total_products,
            'total_revenue': float(total_revenue),
            'pending_orders': pending_orders
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ CATEGORY MANAGEMENT ============

@admin_bp.route('/categories', methods=['GET'])
@admin_required
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ USER MANAGEMENT ============

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        users = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_details(user_id):
    """Get detailed information about a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user information"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        # Update allowed fields
        if 'email' in data:
            # Check if email already exists for another user
            existing = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing:
                return jsonify({'error': 'Email already in use'}), 400
            user.email = data['email']

        if 'name' in data:
            user.name = data['name']

        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        db.session.commit()

        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user"""
    try:
        current_user_id = get_jwt_identity()

        # Prevent admin from deleting themselves
        if user_id == current_user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()

        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(
            email=data['email'],
            name=data['name'],
            is_admin=data.get('is_admin', False)
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
