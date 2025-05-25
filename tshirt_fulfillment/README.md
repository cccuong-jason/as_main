# T-shirt Fulfillment AI Agent

## Project Structure

```
tshirt_fulfillment/
├── src/                      # Source code
│   ├── core/                # Core business logic
│   │   ├── domain/         # Domain models and entities
│   │   ├── repositories/   # Repository interfaces
│   │   ├── use_cases/     # Business use cases
│   │   └── constants.py    # Application constants
│   ├── interfaces/         # Interface adapters
│   │   └── api/           # FastAPI endpoints
│   └── adapters/          # External service adapters
│       └── services/      # External service implementations
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── conftest.py        # Test configuration
├── config/                # Configuration files
│   └── settings.py        # Application settings
├── scripts/               # Utility scripts
├── docker/               # Docker-related files
│   ├── Dockerfile        # Main Dockerfile
│   └── docker-compose.yml # Docker Compose configuration
├── pyproject.toml        # Poetry and tool configuration
├── pytest.ini           # Pytest configuration
└── README.md            # Project documentation
```

## Development Setup

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Run the application:
```bash
# Using Docker
docker-compose up

# Using Poetry
poetry run uvicorn src.interfaces.api.fastapi_app:app --reload
```

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src
```

## Code Quality

```bash
# Run pre-commit hooks
poetry run pre-commit run --all-files

# Format code
poetry run ruff format .
```
