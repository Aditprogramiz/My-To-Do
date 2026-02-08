from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    # Get the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Create Flask app with explicit template folder
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app

