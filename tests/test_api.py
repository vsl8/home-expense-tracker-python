"""
Unit tests for API endpoints.
"""

import json
import pytest
from datetime import date, timedelta


class TestExpenseTypeAPI:
    """Tests for expense type API endpoints."""

    def test_get_expense_types_empty(self, client):
        """Test getting expense types when none exist."""
        response = client.get("/api/expense-types")
        assert response.status_code == 200
        assert json.loads(response.data) == []

    def test_get_expense_types(self, client, init_database):
        """Test getting all expense types."""
        response = client.get("/api/expense-types")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 3
        assert any(t["name"] == "Food" for t in data)
        assert any(t["name"] == "Transport" for t in data)
        assert any(t["name"] == "Utilities" for t in data)

    def test_get_expense_type_by_id(self, client, init_database):
        """Test getting a single expense type."""
        # First get all types to find an ID
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        type_id = types[0]["id"]

        response = client.get(f"/api/expense-types/{type_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["id"] == type_id

    def test_get_expense_type_not_found(self, client):
        """Test getting a non-existent expense type."""
        response = client.get("/api/expense-types/999")
        assert response.status_code == 404

    def test_create_expense_type(self, client):
        """Test creating a new expense type."""
        payload = {
            "name": "Entertainment",
            "description": "Entertainment expenses",
            "color": "#ff00ff",
            "icon": "bi-controller",
        }

        response = client.post("/api/expense-types", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["name"] == "Entertainment"
        assert data["description"] == "Entertainment expenses"
        assert data["color"] == "#ff00ff"

    def test_create_expense_type_no_name(self, client):
        """Test creating expense type without name fails."""
        payload = {"description": "No name provided"}

        response = client.post("/api/expense-types", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 400
        assert "error" in json.loads(response.data)

    def test_create_expense_type_duplicate_name(self, client, init_database):
        """Test creating expense type with duplicate name fails."""
        payload = {"name": "Food"}  # Already exists

        response = client.post("/api/expense-types", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 400
        assert "already exists" in json.loads(response.data)["error"]

    def test_update_expense_type(self, client, init_database):
        """Test updating an expense type."""
        # Get existing type
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        type_id = types[0]["id"]

        payload = {"name": "Updated Name", "description": "Updated description"}

        response = client.put(
            f"/api/expense-types/{type_id}", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"

    def test_delete_expense_type(self, client, init_database):
        """Test deleting (soft delete) an expense type."""
        # Get existing type
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        type_id = types[0]["id"]

        response = client.delete(f"/api/expense-types/{type_id}")
        assert response.status_code == 200

        # Verify it's no longer returned (soft deleted)
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        assert not any(t["id"] == type_id for t in types)


class TestExpenseAPI:
    """Tests for expense API endpoints."""

    def test_get_expenses_empty(self, client):
        """Test getting expenses when none exist."""
        response = client.get("/api/expenses")
        assert response.status_code == 200
        assert json.loads(response.data) == []

    def test_get_expenses(self, client, init_database):
        """Test getting all expenses."""
        response = client.get("/api/expenses")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data) == 3

    def test_get_expense_by_id(self, client, init_database):
        """Test getting a single expense."""
        response = client.get("/api/expenses")
        expenses = json.loads(response.data)
        expense_id = expenses[0]["id"]

        response = client.get(f"/api/expenses/{expense_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["id"] == expense_id

    def test_get_expense_not_found(self, client):
        """Test getting a non-existent expense."""
        response = client.get("/api/expenses/999")
        assert response.status_code == 404

    def test_create_expense(self, client, init_database):
        """Test creating a new expense."""
        # Get an expense type ID
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        type_id = types[0]["id"]

        payload = {"amount": 45.99, "description": "Test expense", "date": date.today().isoformat(), "type_id": type_id}

        response = client.post("/api/expenses", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["amount"] == 45.99
        assert data["description"] == "Test expense"

    def test_create_expense_missing_amount(self, client, init_database):
        """Test creating expense without amount fails."""
        response = client.get("/api/expense-types")
        types = json.loads(response.data)

        payload = {"description": "Missing amount", "type_id": types[0]["id"]}

        response = client.post("/api/expenses", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 400

    def test_create_expense_invalid_type(self, client):
        """Test creating expense with invalid type fails."""
        payload = {"amount": 100, "type_id": 999}  # Non-existent type

        response = client.post("/api/expenses", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 400

    def test_update_expense(self, client, init_database):
        """Test updating an expense."""
        response = client.get("/api/expenses")
        expenses = json.loads(response.data)
        expense_id = expenses[0]["id"]

        payload = {"amount": 999.99, "description": "Updated expense"}

        response = client.put(f"/api/expenses/{expense_id}", data=json.dumps(payload), content_type="application/json")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["amount"] == 999.99
        assert data["description"] == "Updated expense"

    def test_delete_expense(self, client, init_database):
        """Test deleting an expense."""
        response = client.get("/api/expenses")
        expenses = json.loads(response.data)
        expense_id = expenses[0]["id"]
        initial_count = len(expenses)

        response = client.delete(f"/api/expenses/{expense_id}")
        assert response.status_code == 200

        # Verify deletion
        response = client.get("/api/expenses")
        expenses = json.loads(response.data)
        assert len(expenses) == initial_count - 1

    def test_filter_expenses_by_type(self, client, init_database):
        """Test filtering expenses by type."""
        response = client.get("/api/expense-types")
        types = json.loads(response.data)
        food_type = next(t for t in types if t["name"] == "Food")

        response = client.get(f'/api/expenses?type_id={food_type["id"]}')
        assert response.status_code == 200

        expenses = json.loads(response.data)
        assert all(e["type_name"] == "Food" for e in expenses)

    def test_filter_expenses_by_date_range(self, client, init_database):
        """Test filtering expenses by date range."""
        today = date.today().isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()

        response = client.get(f"/api/expenses?start_date={today}&end_date={tomorrow}")
        assert response.status_code == 200


class TestDashboardAPI:
    """Tests for dashboard API endpoints."""

    def test_get_dashboard_stats_empty(self, client):
        """Test dashboard stats with no data."""
        response = client.get("/api/dashboard/stats")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["total_all_time"] == 0
        assert data["expense_count"] == 0

    def test_get_dashboard_stats(self, client, init_database):
        """Test dashboard stats with data."""
        response = client.get("/api/dashboard/stats")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["total_all_time"] > 0
        assert data["expense_count"] == 3
        assert "category_breakdown" in data
        assert len(data["category_breakdown"]) == 3


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
