# T-shirt Fulfillment Testing

This directory contains tests for the T-shirt Fulfillment application. The tests are organized by domain and test type.

## Test Structure

```
/tests/
  /unit/                  # Unit tests for individual components
    /domain/              # Tests for domain models
      test_order.py       # Tests for Order entity
      test_design.py      # Tests for Design entity
    /use_cases/           # Tests for use cases
      test_order_processor.py  # Tests for order processing
      test_design_generator.py # Tests for design generation
    /repositories/        # Tests for repositories
      test_order_repository.py # Tests for order repository
      test_design_repository.py # Tests for design repository
    /services/            # Tests for services
      test_llm_service.py      # Tests for LLM service
      test_drive_service.py    # Tests for Drive service

  /integration/           # Integration tests between components
    test_order_flow.py    # End-to-end order processing
    test_design_flow.py   # End-to-end design generation
    test_admin_flow.py    # End-to-end admin functionality

  /regression/            # Regression tests for bug fixes
    test_order_regression.py  # Regression tests for orders
    test_design_regression.py # Regression tests for designs
    test_admin_regression.py  # Regression tests for admin

  conftest.py             # Shared test fixtures
```

## Running Tests

To run all tests:

```bash
pytest
```

To run tests for a specific domain:

```bash
pytest tests/unit/domain/test_order.py
```

To run tests with coverage:

```bash
pytest --cov=tshirt_fulfillment
```

## Test Fixtures

Test fixtures are defined in `conftest.py` files. There is a global `conftest.py` at the root of the tests directory, and domain-specific fixtures in their respective directories.
