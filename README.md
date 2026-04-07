# Home Expense Tracker

A single-page Flask application for tracking home expenses with comprehensive reporting and export capabilities.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Expense Management**: Add, edit, and delete expenses with categories
- **Category Management**: Create custom expense categories with colors and icons
- **Dashboard**: Visual overview with statistics and charts
- **Reports**: Generate reports for different periods:
  - Daily
  - Weekly
  - Monthly
  - Quarterly
  - Half-yearly
  - Yearly
- **Export Options**: 
  - Export to Excel (.xlsx)
  - Export to PDF
- **Charts**: Interactive charts using Chart.js
  - Pie charts for category distribution
  - Bar charts for category comparison
  - Line charts for spending trends
- **Lightweight Database**: SQLite for easy setup and portability

## Screenshots

The application provides a modern, responsive interface with:
- Dashboard with expense statistics
- Expense list with filtering
- Category management
- Interactive reports with charts

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/home-expense-tracker.git
cd home-expense-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
home-expense-tracker/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Main routes (SPA serving)
│   │   ├── api.py           # CRUD API endpoints
│   │   └── reports.py       # Reports and export endpoints
│   └── templates/
│       └── index.html       # SPA template
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_models.py       # Model unit tests
│   ├── test_api.py          # API endpoint tests
│   └── test_reports.py      # Report endpoint tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pipeline
├── requirements.txt
├── run.py
├── pytest.ini
├── sonar-project.properties
├── .flake8
├── .gitignore
└── README.md
```

## API Endpoints

### Expense Types

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expense-types` | Get all expense types |
| GET | `/api/expense-types/<id>` | Get single expense type |
| POST | `/api/expense-types` | Create expense type |
| PUT | `/api/expense-types/<id>` | Update expense type |
| DELETE | `/api/expense-types/<id>` | Delete expense type |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | Get all expenses (with filters) |
| GET | `/api/expenses/<id>` | Get single expense |
| POST | `/api/expenses` | Create expense |
| PUT | `/api/expenses/<id>` | Update expense |
| DELETE | `/api/expenses/<id>` | Delete expense |

### Dashboard & Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Get dashboard statistics |
| GET | `/api/reports/summary` | Get report summary |
| GET | `/api/reports/chart-data` | Get chart data |
| GET | `/api/reports/export/excel` | Export to Excel |
| GET | `/api/reports/export/pdf` | Export to PDF |

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run with HTML report
pytest --html=test-report.html --self-contained-html
```

## CI/CD Pipeline

The project includes a comprehensive GitHub Actions pipeline with:

1. **Linting**: flake8, pylint, black code formatting check
2. **Testing**: pytest with coverage reporting
3. **SonarQube**: Code quality and coverage analysis
4. **Build**: Create deployment artifact
5. **Deploy to DEV**: Automatic deployment on push
6. **Deploy to QA**: Automatic deployment after DEV success
7. **Deploy to PROD**: Manual approval required

### Required Secrets

Configure these secrets in your GitHub repository:

- `SONAR_TOKEN`: SonarQube authentication token
- `SONAR_HOST_URL`: SonarQube server URL

### Environment Protection

The production environment requires reviewer approval before deployment.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:///expenses.db` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |

## Development

### Code Style

The project uses:
- **black** for code formatting
- **flake8** for linting
- **pylint** for static analysis

### Format code:
```bash
black app tests
```

### Run linters:
```bash
flake8 app tests
pylint app
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Chart.js](https://www.chartjs.org/) - For interactive charts
- [Bootstrap](https://getbootstrap.com/) - For responsive UI
- [ReportLab](https://www.reportlab.com/) - For PDF generation
- [OpenPyXL](https://openpyxl.readthedocs.io/) - For Excel generation
