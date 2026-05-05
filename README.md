# JSONPlaceholder API Test Automation Framework

A scalable and reusable API automation testing framework using Python and Pytest.

## Features

- ✅ Functional API Testing
- ✅ Schema (Contract) Validation
- ✅ Cross-API Data Validation
- ✅ API vs Fake Database Validation
- ✅ Negative & Edge Case Testing
- ✅ Parallel Test Execution
- ✅ HTML & Allure Reports
- ✅ Jenkins CI/CD Pipeline

## Project Structure

```
PlaceholderTestLab/
├── config/          # Configuration settings
├── src/
│   ├── api/         # API clients
│   ├── database/    # SQLite database manager
│   ├── schemas/     # JSON schemas
│   └── utils/       # Utilities & helpers
├── tests/           # Test suites
├── reports/         # Test reports
├── logs/            # Execution logs
└── Jenkinsfile      # CI/CD pipeline
```

## Installation

```bash
# Clone repository
cd PlaceholderTestLab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests
pytest -m smoke

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run parallel tests
pytest -n auto

# Run with Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## Test Markers

- `@pytest.mark.smoke` - Quick validation tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.negative` - Negative test scenarios
- `@pytest.mark.schema` - Schema validation tests
- `@pytest.mark.database` - Database validation tests

## Jenkins Setup

1. Install Jenkins with Python and Allure plugins
2. Create a new Pipeline job
3. Point to Jenkinsfile in repository
4. Run the pipeline

## API Endpoints Covered

| API | Endpoints |
|-----|-----------|
| Users | GET /users, GET /users/{id} |
| Posts | GET /posts, GET /posts/{id}, GET /posts?userId={id} |
| Comments | GET /comments, GET /comments?postId={id} |
| Albums | GET /albums, GET /albums?userId={id} |
| Todos | GET /todos, GET /todos?userId={id} |

## Author

Madhuri Labade
