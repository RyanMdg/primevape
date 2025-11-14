from flask import Flask
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MzA4NTIxMywianRpIjoiNGIzMzI4ZGYtMjBlYS00YTdlLTg0ZjEtZjljYTM3ODkwNGY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzYzMDg1MjEzLCJleHAiOjE3NjMwODg4MTN9.sKZ74xSwk3pp5kcJOeSFSmXlx6msBYDs-qIAH0t7KmY"

with app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        print(f"Token is valid! User ID: {user_id}")
    except Exception as e:
        print(f"Token verification failed: {type(e).__name__}: {e}")
