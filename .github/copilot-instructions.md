# Copilot Instructions for Home Expense Tracker

This is a Flask-based single-page application (SPA) for tracking home expenses with comprehensive reporting and export capabilities.

## Build, Test, and Lint Commands

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run with HTML report
pytest --html=test-report.html --self-contained-html

# Run specific test function
pytest tests/test_api.py::test_create_expense -v

# Run marked tests only
pytest -m integration
pytest -m "not slow"
```

### Linting and Formatting

```bash
# Check code formatting (no changes)
black --check --diff app tests

# Format code
black app tests

# Run flake8
flake8 app tests

# Run pylint
pylint app
```

### Running the Application

```bash
# Direct Python (development)
python run.py

# Docker development (hot reload)
./build.sh dev

# Docker production
./build.sh prod

# Docker commands (via build.sh)
./build.sh build      # Build image
./build.sh test       # Run tests in container
./build.sh lint       # Run linting
./build.sh logs       # View logs
./build.sh stop       # Stop containers
./build.sh clean      # Clean up resources
```

## High-Level Architecture

### Application Factory Pattern

The app uses Flask's application factory pattern (`app/__init__.py`):
- `create_app(config_name)` creates Flask instances
- Pass `"testing"` for in-memory SQLite database during tests
- Database tables are auto-created on app initialization via `db.create_all()`

### Three-Blueprint Structure

1. **main_bp** (`app/routes/main.py`): Serves the SPA's index.html
2. **api_bp** (`app/routes/api.py`): CRUD endpoints for expenses and expense types (mounted at `/api`)
3. **reports_bp** (`app/routes/reports.py`): Reporting, chart data, Excel/PDF exports (mounted at `/api/reports`)

### Data Model Relationships

- **ExpenseType** (1) → (many) **Expense** via `expense_type` backref
- Foreign key: `Expense.type_id` → `ExpenseType.id`
- Cascade delete: Deleting an ExpenseType removes all associated Expenses
- Both models have `to_dict()` methods for JSON serialization

### Report Date Ranges

The `get_date_range(period)` function in `reports.py` calculates start/end dates for:
- `daily`, `weekly`, `monthly`, `quarterly`, `half-yearly`, `yearly`
- Used consistently across dashboard stats, chart data, and exports

### Frontend Integration

- Single HTML template at `app/templates/index.html`
- Frontend makes AJAX calls to API endpoints
- Uses Chart.js for visualization, Bootstrap for UI

## Key Conventions

### Model Serialization

All models implement `to_dict()` that returns JSON-serializable dictionaries:
- Convert datetime/date objects to ISO format strings using `.isoformat()`
- Include related object fields (e.g., `Expense.to_dict()` includes `type_name` and `type_color` from the related ExpenseType)
- Check for `None` before calling `.isoformat()` or accessing related objects

### Database Queries

- Use `ExpenseType.query.filter_by(is_active=True).all()` to exclude soft-deleted types
- Use `get_or_404()` for single-item retrieval in API endpoints
- Commit changes via `db.session.commit()`, rollback errors with `db.session.rollback()`

### Error Handling in API Endpoints

Standard pattern across all API routes:
```python
try:
    # database operations
    db.session.commit()
    return jsonify(data), 200
except Exception as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 500
```

### Test Fixtures

Tests use function-scoped fixtures from `conftest.py`:
- `app`: Creates test app with in-memory database
- `client`: Flask test client for making requests
- `init_database`: Pre-populates test data (3 expense types, 3 expenses)

All fixtures use `scope="function"` to ensure test isolation. Database is dropped after each test.

### Code Style

- **Line length**: 120 characters (enforced by black, flake8, pylint)
- **Import sorting**: Use `isort` with black profile
- **Disabled pylint rules**: C0114, C0115, C0116 (docstrings), R0903 (too few public methods), W0613 (unused argument)
- **Excluded from checks**: migrations, `__pycache__`, venv, build directories

### Date Handling

- Store dates as `db.Date` type, not datetime, for expense records
- Use `datetime.utcnow().date()` for current date
- Use `dateutil.relativedelta` (not timedelta) for month/year arithmetic

### Environment Variables

- `DATABASE_URL`: Database connection (default: `sqlite:///expenses.db`)
- `SECRET_KEY`: Flask secret key (default: `dev-secret-key-change-in-production`)
- `FLASK_ENV`: Environment mode (production/development)
- `FLASK_DEBUG`: Enable debug mode (0/1)

### Docker Multi-Stage Build

Production Dockerfile uses multi-stage build:
1. **Builder stage**: Installs dependencies in virtualenv
2. **Production stage**: Copies only necessary files, runs as non-root user `appuser` (UID 1000)

Development uses `Dockerfile.dev` with Flask dev server and volume mounts for hot reload.

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci-cd.yml`) runs on push/PR:
1. **Lint job**: flake8, pylint, black formatting check
2. **Test job**: pytest with coverage (needs: lint)
3. **SonarQube**: Code quality analysis
4. **Build**: Docker image creation
5. **Deploy stages**: DEV → QA → PROD (production requires manual approval)

Required secrets: `SONAR_TOKEN`, `SONAR_HOST_URL`

## Testing Requirements

- **Coverage threshold**: 70% minimum (configured in pytest.ini)
- **Test markers**: `@pytest.mark.slow` and `@pytest.mark.integration` available
- Omit from coverage: `*/tests/*`, `*/__init__.py`, `*/migrations/*`

## Common Tasks

### Adding a New API Endpoint

1. Add route function to appropriate blueprint (api.py or reports.py)
2. Use `request.get_json()` for POST/PUT data
3. Validate required fields, return 400 if missing
4. Wrap database operations in try/except with rollback
5. Return JSON response with appropriate status code
6. Add corresponding test in `tests/test_api.py` or `tests/test_reports.py`

### Adding a New Model Field

1. Add column to model in `app/models.py`
2. Update `to_dict()` method to include new field
3. Update API endpoints that create/update the model
4. Add database migration if using Alembic (not currently configured)
5. Update tests to include new field in assertions

### Adding a New Report Type

1. Add period calculation logic to `get_date_range()` if needed
2. Create new endpoint in `reports_bp`
3. Query expenses within date range using SQLAlchemy filters
4. Aggregate data using SQLAlchemy's `func.sum()`, `group_by()`, etc.
5. Return JSON for charts or generate Excel/PDF for exports
6. Add tests in `tests/test_reports.py`
