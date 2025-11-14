from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, Product
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()

        # Validate required fields
        if 'items' not in data or not data['items']:
            return jsonify({'error': 'Order items are required'}), 400

        # Calculate totals and validate products
        subtotal = 0
        order_items = []

        for item in data['items']:
            product = Product.query.get(item.get('product_id'))
            if not product or not product.is_active:
                return jsonify({'error': f'Product {item.get("product_id")} not found'}), 404

            quantity = item.get('quantity', 1)

            # Check stock
            if product.stock < quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400

            item_subtotal = product.price * quantity
            subtotal += item_subtotal

            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })

        # Calculate shipping and total
        shipping_cost = data.get('shipping_cost', 5.99)
        total = subtotal + shipping_cost

        # Generate unique order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

        # Create order
        order = Order(
            user_id=current_user_id,
            order_number=order_number,
            status='pending',
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            shipping_street=data.get('shipping_address', {}).get('street'),
            shipping_city=data.get('shipping_address', {}).get('city'),
            shipping_state=data.get('shipping_address', {}).get('state'),
            shipping_zip=data.get('shipping_address', {}).get('zip_code'),
            shipping_country=data.get('shipping_address', {}).get('country', 'USA')
        )

        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items and update stock
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)

            # Update product stock
            item['product'].stock -= item['quantity']

        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get all orders for the current user"""
    try:
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        orders = Order.query.filter_by(user_id=current_user_id)\
            .order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': orders.page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order"""
    try:
        current_user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Check if order belongs to user
        if order.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(order.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        current_user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Check if order belongs to user
        if order.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Only pending orders can be cancelled
        if order.status != 'pending':
            return jsonify({'error': 'Only pending orders can be cancelled'}), 400

        # Update status
        order.status = 'cancelled'

        # Restore product stock
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity

        db.session.commit()

        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/admin/all', methods=['GET'])
@jwt_required()
def get_all_orders():
    """Get all orders (Admin only)"""
    try:
        from models import User
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')

        query = Order.query

        if status:
            query = query.filter_by(status=status)

        orders = query.order_by(Order.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': orders.page
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (Admin only)"""
    try:
        from models import User
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user or not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403

        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        data = request.get_json()
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400

        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400

        order.status = data['status']
        db.session.commit()

        return jsonify({
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
