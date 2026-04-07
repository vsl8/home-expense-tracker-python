"""
Unit tests for database models.
"""
import pytest
from datetime import date
from app import db
from app.models import ExpenseType, Expense


class TestExpenseTypeModel:
    """Tests for ExpenseType model."""
    
    def test_create_expense_type(self, app):
        """Test creating an expense type."""
        with app.app_context():
            expense_type = ExpenseType(
                name='Test Type',
                description='A test expense type',
                color='#ff0000',
                icon='bi-cash'
            )
            db.session.add(expense_type)
            db.session.commit()
            
            assert expense_type.id is not None
            assert expense_type.name == 'Test Type'
            assert expense_type.description == 'A test expense type'
            assert expense_type.color == '#ff0000'
            assert expense_type.icon == 'bi-cash'
            assert expense_type.is_active is True
    
    def test_expense_type_to_dict(self, app):
        """Test converting expense type to dictionary."""
        with app.app_context():
            expense_type = ExpenseType(
                name='Dict Test',
                description='Test description',
                color='#00ff00'
            )
            db.session.add(expense_type)
            db.session.commit()
            
            result = expense_type.to_dict()
            
            assert result['name'] == 'Dict Test'
            assert result['description'] == 'Test description'
            assert result['color'] == '#00ff00'
            assert 'id' in result
            assert 'created_at' in result
            assert 'expense_count' in result
    
    def test_expense_type_unique_name(self, app):
        """Test that expense type names must be unique."""
        with app.app_context():
            type1 = ExpenseType(name='Unique Name')
            db.session.add(type1)
            db.session.commit()
            
            type2 = ExpenseType(name='Unique Name')
            db.session.add(type2)
            
            with pytest.raises(Exception):
                db.session.commit()


class TestExpenseModel:
    """Tests for Expense model."""
    
    def test_create_expense(self, app, init_database):
        """Test creating an expense."""
        with app.app_context():
            expense_type = ExpenseType.query.first()
            
            expense = Expense(
                amount=99.99,
                description='Test expense',
                date=date.today(),
                type_id=expense_type.id
            )
            db.session.add(expense)
            db.session.commit()
            
            assert expense.id is not None
            assert expense.amount == 99.99
            assert expense.description == 'Test expense'
            assert expense.type_id == expense_type.id
    
    def test_expense_to_dict(self, app, init_database):
        """Test converting expense to dictionary."""
        with app.app_context():
            expense = Expense.query.first()
            result = expense.to_dict()
            
            assert 'id' in result
            assert 'amount' in result
            assert 'description' in result
            assert 'date' in result
            assert 'type_id' in result
            assert 'type_name' in result
            assert 'type_color' in result
    
    def test_expense_relationship(self, app, init_database):
        """Test expense relationship with expense type."""
        with app.app_context():
            expense = Expense.query.first()
            
            assert expense.expense_type is not None
            assert expense.expense_type.name is not None
    
    def test_cascade_delete(self, app, init_database):
        """Test that deleting expense type cascades to expenses."""
        with app.app_context():
            expense_type = ExpenseType.query.filter_by(name='Food').first()
            initial_expense_count = Expense.query.filter_by(type_id=expense_type.id).count()
            
            assert initial_expense_count > 0
            
            db.session.delete(expense_type)
            db.session.commit()
            
            remaining = Expense.query.filter_by(type_id=expense_type.id).count()
            assert remaining == 0
