# Unit Tests

This directory contains unit tests for the T-shirt Fulfillment application. Unit tests focus on testing individual components in isolation.

## Directory Structure

```
/unit/
  /domain/              # Tests for domain models
    test_order.py       # Tests for Order entity
    test_design.py      # Tests for Design entity
  /use_cases/           # Tests for use cases
    test_order_processor.py  # Tests for order processing
    test_design_generator.py # Tests for design generation
  /repositories/        # Tests for repositories
    test_order_repository.py # Tests for order repository
  /services/            # Tests for services
    test_llm_service.py      # Tests for LLM service
  conftest.py           # Unit test-specific fixtures
```

## Writing Unit Tests

### Test Structure

Each test should follow the Arrange-Act-Assert pattern:

```python
def test_something():
    # Arrange - set up the test data and conditions
    order = Order(id="123", customer_name="Test")
    
    # Act - perform the action being tested
    result = order.update_status("processing")
    
    # Assert - verify the results
    assert order.status == "processing"
```

### Mocking Dependencies

Use pytest fixtures to mock dependencies:

```python
@pytest.fixture
def mock_service():
    return MagicMock()

def test_with_mock(mock_service):
    # Use the mock in your test
    mock_service.do_something.return_value = "expected result"
```

## Running Unit Tests

To run all unit tests:

```bash
pytest tests/unit
```

To run tests for a specific component:

```bash
pytest tests/unit/domain/test_order.py
```

To run a specific test:

```bash
pytest tests/unit/domain/test_order.py::test_order_creation
```

## Test Coverage

To run tests with coverage:

```bash
pytest --cov=tshirt_fulfillment tests/unit
```