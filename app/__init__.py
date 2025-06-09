from flask import Flask
from .routes import register_routes
from .models import init_db

def create_app():
    app = Flask(__name__)
    init_db()
    register_routes(app)
    return app
