from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db, bcrypt
import os

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Configure JWT to not use CSRF protection
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    jwt = JWTManager(app)

    # Configure CORS - Allow all origins
    CORS(app,
         resources={r"/api/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["Content-Type", "Authorization"],
         supports_credentials=False,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         send_wildcard=True,
         always_send=True
    )

    # Register blueprints
    from routes.products import products_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.admin import admin_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'PrimeVape API',
            'version': '1.0.0',
            'endpoints': {
                'products': '/api/products',
                'auth': '/api/auth',
                'orders': '/api/orders'
            }
        }), 200

    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'message': 'Please login again'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")  # Debug log
        return jsonify({
            'error': 'Invalid token',
            'message': 'Please provide a valid token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization required',
            'message': 'Please provide an access token'
        }), 401

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


# Create app instance for gunicorn
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    # For local development, create app with environment-specific config
    dev_app = create_app(os.getenv('FLASK_ENV', 'development'))
    dev_app.run(debug=True, host='0.0.0.0', port=5001)
