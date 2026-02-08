from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
try:
    from dotenv import load_dotenv
    try:
        load_dotenv()
    except Exception:
        pass
except ImportError:
    # python-dotenv not installed in this environment; continue without loading .env
    pass

db = SQLAlchemy()

def create_app():
    # Get the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(basedir)
    
    # Create Flask app with explicit template folder
    template_folder = os.path.join(parent_dir, 'templates')
    app = Flask(__name__, template_folder=template_folder, static_folder=os.path.join(parent_dir, 'static'))

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

