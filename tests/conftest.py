"""
Pytest configuration and fixtures.
"""
import pytest
from datetime import datetime, date
from app import create_app, db
from app.models import ExpenseType, Expense


@pytest.fixture(scope='function')
def app():
    """Create application for the tests."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize database with test data."""
    with app.app_context():
        # Create expense types
        food_type = ExpenseType(
            name='Food',
            description='Food and dining expenses',
            color='#ff6b6b',
            icon='bi-cup-hot'
        )
        transport_type = ExpenseType(
            name='Transport',
            description='Transportation expenses',
            color='#4ecdc4',
            icon='bi-car-front'
        )
        utilities_type = ExpenseType(
            name='Utilities',
            description='Utility bills',
            color='#45b7d1',
            icon='bi-lightning'
        )
        
        db.session.add_all([food_type, transport_type, utilities_type])
        db.session.commit()
        
        # Create expenses
        expense1 = Expense(
            amount=25.50,
            description='Lunch at restaurant',
            date=date.today(),
            type_id=food_type.id
        )
        expense2 = Expense(
            amount=50.00,
            description='Gas refill',
            date=date.today(),
            type_id=transport_type.id
        )
        expense3 = Expense(
            amount=120.00,
            description='Electricity bill',
            date=date.today(),
            type_id=utilities_type.id
        )
        
        db.session.add_all([expense1, expense2, expense3])
        db.session.commit()
        
        yield
        
        db.session.remove()
