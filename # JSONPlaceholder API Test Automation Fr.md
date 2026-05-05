# JSONPlaceholder API Test Automation Framework

## Agenda
1. Framework Overview
2. Architecture & Components
3. Key Features
4. Demo: Running Tests
5. Q&A

---

## 1. Framework Overview

### What is this framework?
- **Purpose**: Automated testing of REST APIs using Python & Pytest
- **Target API**: JSONPlaceholder (https://jsonplaceholder.typicode.com)
- **Goal**: Demonstrate real-world API testing skills

### Why build this?
- **Interview Ready**: Shows Python, Pytest, API testing expertise
- **Scalable**: Modular design for easy extension
- **Production-Ready**: Includes CI/CD, reporting, logging

---

## 2. Architecture & Components

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Test Execution                           │
│  pytest tests/ -v                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer                               │
│  ├── conftest.py (Fixtures & Setup)                         │
│  ├── test_*.py (Test Cases)                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Source Layer (src/)                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│  │   API       │ │  Database   │ │   Schemas   │ │  Utils  │ │
│  │  Clients    │ │   Manager   │ │             │ │         │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                External Services                            │
│  JSONPlaceholder API    │    SQLite In-Memory DB            │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

#### 2.1 Configuration (`config/config.py`)
- **Singleton Pattern**: One config instance
- **Settings**: Base URL, timeouts, thresholds
- **Environment**: Configurable via environment variables

#### 2.2 API Layer (`src/api/`)
```python
# Base Client (base_client.py)
class BaseAPIClient:
    def get(self, endpoint, params=None):
    def post(self, endpoint, data):
    # ... with retry & logging decorators

# Specific Clients
class UsersAPI(BaseAPIClient):    # /users endpoints
class PostsAPI(BaseAPIClient):    # /posts endpoints
class CommentsAPI(BaseAPIClient): # /comments endpoints
class AlbumsAPI(BaseAPIClient):   # /albums endpoints
class TodosAPI(BaseAPIClient):    # /todos endpoints
```

#### 2.3 Database Layer (`src/database/db_manager.py`)
- **SQLite In-Memory**: ":memory:" connection
- **Purpose**: Simulate backend validation
- **Tables**: users, posts, comments, albums, todos
- **Singleton**: One DB instance per test session

#### 2.4 Schema Validation (`src/schemas/schemas.py`)
- **JSON Schema**: Define expected response structure
- **Validation**: Check required fields, data types
- **Examples**: USER_SCHEMA, POST_SCHEMA, etc.

#### 2.5 Utilities (`src/utils/`)
- **Logger**: Console + file logging
- **Decorators**: @retry, @log_api_call
- **Helpers**: Email validation, ID extraction, etc.

---

## 3. Key Features

### 3.1 Test Types
| Type | Marker | Purpose | Example |
|------|--------|---------|---------|
| **Smoke** | `@pytest.mark.smoke` | Quick validation | Status codes, response time |
| **Regression** | `@pytest.mark.regression` | Full functionality | Data validation, relationships |
| **Schema** | `@pytest.mark.schema` | Contract validation | JSON structure compliance |
| **Database** | `@pytest.mark.database` | API vs DB comparison | Data consistency |
| **Negative** | `@pytest.mark.negative` | Error handling | Invalid IDs, edge cases |

### 3.2 Advanced Features
- **Parallel Execution**: `pytest -n auto`
- **Retry Mechanism**: Automatic retry on failures
- **Cross-API Validation**: Validate relationships between endpoints
- **CI/CD Ready**: Jenkins pipeline included
- **Multiple Reports**: HTML, Allure, Console

### 3.3 Design Patterns
- **Singleton**: Config, Logger, Database
- **Decorator**: Retry, Logging
- **Factory**: API client creation
- **Page Object**: Adapted for API endpoints

---

## 4. Demo: Running Tests

### Setup
```bash
# 1. Navigate to project
cd "/Users/madhurilabade/PIP Project 1/PlaceholderTestLab"

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run Tests
```bash
# All tests
pytest -v

# Smoke tests only
pytest -m smoke -v

# With HTML report
pytest --html=reports/report.html --self-contained-html -v

# Parallel execution
pytest -n auto -v

# Specific test file
pytest tests/test_users.py -v
```

### Sample Output
```
tests/test_users.py::TestUsersAPI::test_get_all_users_status_code PASSED
tests/test_users.py::TestUsersAPI::test_users_schema_validation PASSED
tests/test_users.py::TestUsersAPI::test_users_count_in_db PASSED
...
========================= 13 passed in 2.34s =========================
```

---

## 5. Test Execution Flow

```
1. pytest starts
   └── Loads conftest.py fixtures

2. Session fixtures initialize
   ├── Create API clients
   ├── Initialize SQLite database
   └── Fetch & store data from APIs

3. Tests execute
   ├── Validate status codes
   ├── Validate schemas
   ├── Validate data relationships
   ├── Compare API vs DB data
   └── Test negative scenarios

4. Reports generated
   ├── Console output
   ├── HTML report (reports/report.html)
   ├── Allure report (allure-results/)
   └── Log file (logs/test_execution.log)
```

---

## 6. Benefits for Our Team

### For Developers
- **Learn Python Testing**: Real-world Pytest usage
- **API Testing Skills**: REST API validation techniques
- **Design Patterns**: Singleton, Decorator, Factory

### For QA Engineers
- **Automation Framework**: Ready-to-use for API testing
- **Scalable Design**: Easy to extend for new APIs
- **CI/CD Integration**: Jenkins pipeline included

### For Interview Preparation
- **Portfolio Project**: Demonstrate testing expertise
- **Real-World Scenarios**: Schema validation, cross-API testing
- **Advanced Features**: Parallel execution, reporting

---

## 7. Q&A

### Common Questions
**Q: Why SQLite in-memory?**  
A: Simulates backend validation without external dependencies.

**Q: How to add new API endpoints?**  
A: Create new API client class inheriting from BaseAPIClient.

**Q: Can this be used for other APIs?**  
A: Yes, modify config.py BASE_URL and update schemas.

**Q: What's the retry mechanism?**  
A: @retry decorator retries failed requests up to 3 times.

---

## 8. Next Steps

1. **Explore the Code**: Review src/ and tests/ directories
2. **Run Tests**: Try the demo commands
3. **Customize**: Add your own test cases
4. **Extend**: Add new API endpoints or features

---

*Framework Location: /Users/madhurilabade/PIP Project 1/PlaceholderTestLab*  
*Author: Madhuri Labade*  
*Date: [Current Date]*
