"""
API routes for expense and expense type CRUD operations.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Expense, ExpenseType

api_bp = Blueprint('api', __name__)


# ============== Expense Types API ==============

@api_bp.route('/expense-types', methods=['GET'])
def get_expense_types():
    """Get all expense types."""
    types = ExpenseType.query.filter_by(is_active=True).all()
    return jsonify([t.to_dict() for t in types])


@api_bp.route('/expense-types/<int:type_id>', methods=['GET'])
def get_expense_type(type_id):
    """Get a single expense type by ID."""
    expense_type = ExpenseType.query.get_or_404(type_id)
    return jsonify(expense_type.to_dict())


@api_bp.route('/expense-types', methods=['POST'])
def create_expense_type():
    """Create a new expense type."""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    # Check for duplicate name
    existing = ExpenseType.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Expense type with this name already exists'}), 400
    
    expense_type = ExpenseType(
        name=data['name'],
        description=data.get('description', ''),
        color=data.get('color', '#007bff'),
        icon=data.get('icon', 'bi-cash')
    )
    
    db.session.add(expense_type)
    db.session.commit()
    
    return jsonify(expense_type.to_dict()), 201


@api_bp.route('/expense-types/<int:type_id>', methods=['PUT'])
def update_expense_type(type_id):
    """Update an expense type."""
    expense_type = ExpenseType.query.get_or_404(type_id)
    data = request.get_json()
    
    if data.get('name'):
        # Check for duplicate name (excluding current type)
        existing = ExpenseType.query.filter(
            ExpenseType.name == data['name'],
            ExpenseType.id != type_id
        ).first()
        if existing:
            return jsonify({'error': 'Expense type with this name already exists'}), 400
        expense_type.name = data['name']
    
    if 'description' in data:
        expense_type.description = data['description']
    if 'color' in data:
        expense_type.color = data['color']
    if 'icon' in data:
        expense_type.icon = data['icon']
    
    db.session.commit()
    return jsonify(expense_type.to_dict())


@api_bp.route('/expense-types/<int:type_id>', methods=['DELETE'])
def delete_expense_type(type_id):
    """Delete an expense type (soft delete)."""
    expense_type = ExpenseType.query.get_or_404(type_id)
    expense_type.is_active = False
    db.session.commit()
    return jsonify({'message': 'Expense type deleted successfully'})


# ============== Expenses API ==============

@api_bp.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses with optional filtering."""
    query = Expense.query
    
    # Filter by type
    type_id = request.args.get('type_id', type=int)
    if type_id:
        query = query.filter_by(type_id=type_id)
    
    # Filter by date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    # Sort by date descending
    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify([e.to_dict() for e in expenses])


@api_bp.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Get a single expense by ID."""
    expense = Expense.query.get_or_404(expense_id)
    return jsonify(expense.to_dict())


@api_bp.route('/expenses', methods=['POST'])
def create_expense():
    """Create a new expense."""
    data = request.get_json()
    
    if not data or not data.get('amount') or not data.get('type_id'):
        return jsonify({'error': 'Amount and type_id are required'}), 400
    
    # Validate expense type exists
    expense_type = ExpenseType.query.get(data['type_id'])
    if not expense_type or not expense_type.is_active:
        return jsonify({'error': 'Invalid expense type'}), 400
    
    # Parse date
    expense_date = datetime.utcnow().date()
    if data.get('date'):
        expense_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    
    expense = Expense(
        amount=float(data['amount']),
        description=data.get('description', ''),
        date=expense_date,
        type_id=data['type_id']
    )
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify(expense.to_dict()), 201


@api_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an expense."""
    expense = Expense.query.get_or_404(expense_id)
    data = request.get_json()
    
    if data.get('amount'):
        expense.amount = float(data['amount'])
    if 'description' in data:
        expense.description = data['description']
    if data.get('date'):
        expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if data.get('type_id'):
        expense_type = ExpenseType.query.get(data['type_id'])
        if not expense_type or not expense_type.is_active:
            return jsonify({'error': 'Invalid expense type'}), 400
        expense.type_id = data['type_id']
    
    db.session.commit()
    return jsonify(expense.to_dict())


@api_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense (hard delete)."""
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})


# ============== Dashboard Stats ==============

@api_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics."""
    from sqlalchemy import func
    
    today = datetime.utcnow().date()
    
    # Total expenses
    total = db.session.query(func.sum(Expense.amount)).scalar() or 0
    
    # Today's expenses
    today_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date == today
    ).scalar() or 0
    
    # This month's expenses
    month_start = today.replace(day=1)
    month_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= month_start
    ).scalar() or 0
    
    # Count by category
    category_stats = db.session.query(
        ExpenseType.name,
        ExpenseType.color,
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count')
    ).join(Expense).group_by(ExpenseType.id).all()
    
    return jsonify({
        'total_all_time': round(total, 2),
        'total_today': round(today_total, 2),
        'total_this_month': round(month_total, 2),
        'expense_count': Expense.query.count(),
        'category_breakdown': [
            {
                'name': stat[0],
                'color': stat[1],
                'total': round(stat[2], 2),
                'count': stat[3]
            }
            for stat in category_stats
        ]
    })
