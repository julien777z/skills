# python-testing-patterns — detailed patterns and worked examples

## Fundamental Patterns

### Pattern 1: Basic pytest Tests
```python
# myapp/calculator.py
class Calculator:
    """Simple calculator for testing."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")

        return a / b
```
```python
# tests/test_calculator.py
import pytest
from myapp.calculator import Calculator


def test_addition():
    """Test addition."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0


def test_subtraction():
    """Test subtraction."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_multiplication():
    """Test multiplication."""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(0, 5) == 0


def test_division():
    """Test division."""
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    assert calc.divide(5, 2) == 2.5


def test_division_by_zero():
    """Test division by zero raises error."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### Pattern 2: Fixtures for Setup and Teardown

Use the suite's existing session-scoped configuration fixture, registered from its topic owner.
The following example separates the application class, resource lifecycle wiring and consuming tests; fixture
scope follows the lifetime of the resource.
```python
# myapp/database.py
class Database:
    """Simple database class."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """Connect to database."""
        self.connected = True

    def disconnect(self):
        """Disconnect from database."""
        self.connected = False

    def query(self, sql: str) -> list:
        """Execute query."""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]
```
```python
# tests/conftest.py
from collections.abc import Iterator

import httpx
import pytest
from myapp.config import AppConfig
from myapp.database import Database
from tests.fixtures.configuration import app_config


@pytest.fixture
def db(app_config: AppConfig) -> Iterator[Database]:
    """Provide a connected database for one test."""
    database = Database(app_config.database_url)
    database.connect()

    try:
        yield database
    finally:
        database.disconnect()


@pytest.fixture(scope="module")
def api_client(app_config: AppConfig) -> Iterator[httpx.Client]:
    """Provide an HTTP client for one test module."""
    with httpx.Client(base_url=app_config.api_base_url) as client:
        yield client
```
```python
# tests/test_database.py
from myapp.database import Database


def test_database_query(db: Database) -> None:
    """Test that a connected database accepts a query."""
    results = db.query("SELECT * FROM users")

    assert len(results) == 1
    assert results[0]["name"] == "Test"


# tests/test_api_client.py
import httpx


def test_api_client(api_client: httpx.Client) -> None:
    """Test that the configured client is open during the test."""
    assert not api_client.is_closed
```

### Pattern 3: Parameterized Tests
```python
# myapp/validation.py
def is_valid_email(email: str) -> bool:
    """Check if email is valid."""
    return "@" in email and "." in email.split("@")[1]
```
```python
# tests/test_validation.py
import pytest
from myapp.calculator import Calculator
from myapp.validation import is_valid_email


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain", False),
    ("", False),
])
def test_email_validation(email, expected):
    """Test email validation with various inputs."""
    assert is_valid_email(email) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition_parameterized(a, b, expected):
    """Test addition with multiple parameter sets."""
    calc = Calculator()
    assert calc.add(a, b) == expected


# Using pytest.param for special cases
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    """Test with custom test IDs."""
    assert (value > 0) == expected
```

### Pattern 4: Mocking with unittest.mock
```python
# myapp/api_client.py
import requests


class APIClient:
    """Simple API client."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """Fetch user from API."""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, data: dict) -> dict:
        """Create new user."""
        response = requests.post(f"{self.base_url}/users", json=data)
        response.raise_for_status()
        return response.json()
```
```python
# tests/test_api_client.py
from unittest.mock import Mock, patch

import pytest
import requests
from myapp.api_client import APIClient


def test_get_user_success():
    """Test successful API call with mock."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)

        assert user["id"] == 1
        assert user["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_get_user_not_found():
    """Test API call with 404 error."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)


@patch("requests.post")
def test_create_user(mock_post):
    """Test user creation with decorator syntax."""
    client = APIClient("https://api.example.com")

    mock_post.return_value.json.return_value = {"id": 2, "name": "Jane Doe"}
    mock_post.return_value.raise_for_status.return_value = None

    user_data = {"name": "Jane Doe", "email": "jane@example.com"}
    result = client.create_user(user_data)

    assert result["id"] == 2
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.kwargs["json"] == user_data
```

### Pattern 5: Testing Exceptions
```python
# myapp/arithmetic.py
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ZeroDivisionError("Division by zero")

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")

    return a / b
```
```python
# tests/test_arithmetic.py
import pytest
from myapp.arithmetic import divide


def test_zero_division():
    """Test exception is raised for division by zero."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_zero_division_with_message():
    """Test exception message."""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)


def test_type_error():
    """Test type error exception."""
    with pytest.raises(TypeError, match="must be numbers"):
        divide("10", 5)


def test_exception_info():
    """Test accessing exception info."""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)
```

For advanced patterns including async testing, monkeypatching, temporary files, conftest setup, property-based testing, database testing, CI/CD integration, and configuration files, see [references/advanced-patterns.md](./advanced-patterns.md)

## Test Design Principles

### One Behavior Per Test

Each test should verify exactly one behavior. This makes failures easy to diagnose and tests easy to maintain.
```python
# BAD - testing multiple behaviors
def test_user_service():
    user = service.create_user(data)
    assert user.id is not None
    assert user.email == data["email"]
    updated = service.update_user(user.id, {"name": "New"})
    assert updated.name == "New"

# GOOD - focused tests
def test_create_user_assigns_id():
    user = service.create_user(data)
    assert user.id is not None

def test_create_user_stores_email():
    user = service.create_user(data)
    assert user.email == data["email"]

def test_update_user_changes_name():
    user = service.create_user(data)
    updated = service.update_user(user.id, {"name": "New"})
    assert updated.name == "New"
```

### Test Error Paths

Always test failure cases, not just happy paths.
```python
def test_get_user_raises_not_found():
    with pytest.raises(UserNotFoundError) as exc_info:
        service.get_user("nonexistent-id")

    assert "nonexistent-id" in str(exc_info.value)

def test_create_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="Invalid email format"):
        service.create_user({"email": "not-an-email"})
```
