# Python Testing Patterns — Advanced Reference

Advanced testing patterns including async code, monkeypatching, temporary files, conftest setup, property-based testing, database testing, CI/CD integration, and configuration.

## Pattern 6: Testing Async Code

```python
# myapp/network.py
import asyncio


async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    await asyncio.sleep(0.1)
    return {"url": url, "data": "result"}
```

```python
# tests/conftest.py
from collections.abc import AsyncIterator

import httpx
import pytest_asyncio
from myapp.config import AppConfig
from tests.fixtures.configuration import app_config


@pytest_asyncio.fixture
async def async_client(app_config: AppConfig) -> AsyncIterator[httpx.AsyncClient]:
    """Provide an HTTP client for one async test."""
    async with httpx.AsyncClient(base_url=app_config.api_base_url) as client:
        yield client
```

```python
# tests/test_network.py
import asyncio

import httpx
import pytest
from myapp.network import fetch_data


@pytest.mark.asyncio
async def test_fetch_data():
    """Test async function."""
    result = await fetch_data("https://api.example.com")

    assert result["url"] == "https://api.example.com"
    assert "data" in result


@pytest.mark.asyncio
async def test_concurrent_fetches():
    """Test concurrent async operations."""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    assert len(results) == 3
    assert all("data" in r for r in results)


@pytest.mark.asyncio
async def test_with_async_fixture(async_client: httpx.AsyncClient) -> None:
    """Test that the async client is open during the test."""
    assert not async_client.is_closed
```

## Pattern 7: Monkeypatch for Testing

```python
# myapp/config.py
import os


def get_database_url() -> str:
    """Get database URL from environment."""
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")
```

```python
# tests/test_config.py
import pytest
from myapp.config import AppConfig, get_database_url


def test_database_url_default():
    """Test default database URL."""
    # Will use actual environment variable if set
    url = get_database_url()

    assert url


def test_database_url_custom(monkeypatch):
    """Test custom database URL with monkeypatch."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"


def test_database_url_not_set(monkeypatch):
    """Test when env var is not set."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"


def test_monkeypatch_attribute(
    monkeypatch: pytest.MonkeyPatch,
    app_config: AppConfig,
) -> None:
    """Test that monkeypatch overrides an attribute of the configured object."""
    monkeypatch.setattr(app_config, "api_key", "test-key")

    assert app_config.api_key == "test-key"
```

## Pattern 8: Temporary Files and Directories

```python
# myapp/file_operations.py
from pathlib import Path


def save_data(filepath: Path, data: str):
    """Save data to file."""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """Load data from file."""
    return filepath.read_text()
```

```python
# tests/test_file_operations.py
from myapp.file_operations import load_data, save_data


def test_file_operations(tmp_path):
    """Test file operations with temporary directory."""
    # tmp_path is a pathlib.Path object
    test_file = tmp_path / "test_data.txt"

    # Save data
    save_data(test_file, "Hello, World!")

    # Verify file exists
    assert test_file.exists()

    # Load and verify data
    data = load_data(test_file)
    assert data == "Hello, World!"


def test_multiple_files(tmp_path):
    """Test with multiple temporary files."""
    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    for filename, content in files.items():
        filepath = tmp_path / filename
        save_data(filepath, content)

    # Verify all files created
    assert len(list(tmp_path.iterdir())) == 3

    # Verify contents
    for filename, expected_content in files.items():
        filepath = tmp_path / filename
        assert load_data(filepath) == expected_content
```

## Pattern 9: Fixture Registration and Parameterization

Register fixtures from their established topic owners; keep the existing session, database,
event-loop and autouse environment lifecycles in the suite's lifecycle wiring.

```python
# tests/conftest.py
from tests.fixtures.users import sample_user, sample_users
```

Those fixtures bind the canonical user root and shared generation mechanism, rather than copying
model constructors into registration. Parametrize a topic fixture with the application's existing
finite family when a test must exercise every supported option:

```python
# tests/fixtures/database.py
import pytest
from myapp.database import DatabaseBackend


@pytest.fixture(params=tuple(DatabaseBackend))
def db_backend(request: pytest.FixtureRequest) -> DatabaseBackend:
    """Provide each supported database backend."""
    return DatabaseBackend(request.param)
```

Consumers use this fixture through the suite's registration, composing it with the existing
database setup and asserting the behavior under test for each backend.

## Pattern 10: Property-Based Testing

```python
# myapp/text.py
def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]
```

```python
# tests/test_properties.py
from hypothesis import given, strategies as st
from myapp.text import reverse_string


@given(st.text())
def test_reverse_twice_is_original(s):
    """Property: reversing twice returns original."""
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_length(s):
    """Property: reversed string has same length."""
    assert len(reverse_string(s)) == len(s)


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Property: addition is commutative."""
    assert a + b == b + a


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst):
    """Property: sorted list is ordered."""
    sorted_lst = sorted(lst)

    # Same length
    assert len(sorted_lst) == len(lst)

    # All elements present
    assert set(sorted_lst) == set(lst)

    # Is ordered
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## Testing Database Code

Use the application's established model and metadata registry, the suite's existing in-memory
SQLite configuration, and its topic user fixtures. The user fixtures supply non-persisted ORM
instances from the configured shared generation mechanism and canonical roots: `user` lets the
database assign its ID, `users` provides two distinct users, and `duplicate_email_users` provides
distinct users with the same email for the constraint case. Register those fixtures without moving
their construction into the session lifecycle.

```python
# tests/conftest.py
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from myapp.config import AppConfig
from myapp.models import Base
from tests.fixtures.configuration import app_config
from tests.fixtures.users import duplicate_email_users, user, users


@pytest.fixture(scope="function")
def db_session(app_config: AppConfig) -> Iterator[Session]:
    """Provide an isolated database session for one test."""
    engine = create_engine(app_config.database_url)

    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()
```

```python
# tests/test_database_models.py
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from myapp.models.users import User


def test_create_user(db_session: Session, user: User) -> None:
    """Test that creating a user preserves its name and assigns an ID."""
    expected_name = user.name

    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == expected_name


def test_query_user(db_session: Session, users: tuple[User, User]) -> None:
    """Test that querying users returns both inserted rows."""
    db_session.add_all(users)
    db_session.commit()

    stored_users = db_session.query(User).all()

    assert len(stored_users) == 2


def test_unique_email_constraint(
    db_session: Session,
    duplicate_email_users: tuple[User, User],
) -> None:
    """Test that inserting another user with the same email fails."""
    first_user, second_user = duplicate_email_users

    db_session.add(first_user)
    db_session.commit()

    db_session.add(second_user)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Configuration Files

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
    e2e: marks end-to-end tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--cov=myapp",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```
