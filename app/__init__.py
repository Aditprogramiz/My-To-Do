from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
try:
    from dotenv import load_dotenv
except Exception:
    # If python-dotenv isn't available, provide a no-op loader
    def load_dotenv():
        return None

# Attempt to load environment from a .env file if present
try:
    load_dotenv()
except Exception:
    pass

db = SQLAlchemy()

def create_app():
    # Get the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Use package-relative templates and static folders (Flask will resolve them
    # relative to this package's location)
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Support for Flask SQLAlchemy 3.0+ with SQLAlchemy 2.0
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app

