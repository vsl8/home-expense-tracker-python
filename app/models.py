"""
Database models for the Expense Tracker application.
"""

from datetime import datetime
from app import db


class ExpenseType(db.Model):
    """Model for expense categories/types."""

    __tablename__ = "expense_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    color = db.Column(db.String(7), default="#007bff")  # Hex color for charts
    icon = db.Column(db.String(50), default="bi-cash")  # Bootstrap icon class
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship
    expenses = db.relationship("Expense", backref="expense_type", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "icon": self.icon,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "expense_count": len(self.expenses),
        }


class Expense(db.Model):
    """Model for individual expense records."""

    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    type_id = db.Column(db.Integer, db.ForeignKey("expense_types.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "type_id": self.type_id,
            "type_name": self.expense_type.name if self.expense_type else None,
            "type_color": self.expense_type.color if self.expense_type else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
