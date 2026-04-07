"""
Home Expense Tracker - Flask Application
A single-page application for managing home expenses with reporting capabilities.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(config_name=None):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        db_path = os.environ.get('DATABASE_URL', 'sqlite:///expenses.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
