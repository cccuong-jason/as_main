# Regression Tests

This directory contains regression tests for the T-shirt Fulfillment application. Regression tests focus on ensuring that previously fixed bugs do not reoccur.

## Directory Structure

```
/regression/
  test_order_regression.py  # Regression tests for orders
  test_design_regression.py # Regression tests for designs
  test_admin_regression.py  # Regression tests for admin
  conftest.py               # Regression test-specific fixtures
```

## Writing Regression Tests

Regression tests should be created whenever a bug is fixed. They should:

1. Clearly document the bug that was fixed
2. Test the specific conditions that caused the bug
3. Verify that the fix works correctly

### Example Regression Test

```python
@pytest.mark.regression
def test_order_quantity_validation_regression():
    """
    Regression test for order quantity validation.
    This test ensures that the bug where orders with quantity=0 were being accepted
    does not reoccur.
    """
    # Arrange/Act/Assert
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        Order(
            id="order123",
            customer_name="Test Customer",
            customer_email="test@example.com",
            design_prompt="A t-shirt with a mountain landscape",
            size="L",
            color="Blue",
            quantity=0,  # Invalid quantity
            status="pending"
        )
```

## Running Regression Tests

To run all regression tests:

```bash
pytest tests/regression
```

To run regression tests for a specific domain:

```bash
pytest tests/regression/test_order_regression.py
```

To run all regression tests across the project:

```bash
pytest -m regression
```

## Regression Test Data

Use the `regression_data` fixture from `conftest.py` to access test data specific to known bugs:

```python
def test_with_regression_data(regression_data):
    # Use the regression test data
    bug_case = regression_data["known_bug_cases"]["zero_quantity"]
    # Test that the bug is fixed
```

## Historical Database

For testing against historical data, use the `mock_database_with_history` fixture:

```python
def test_with_historical_data(mock_database_with_history):
    # Use the historical database to verify fixes against real-world data
    historical_orders = mock_database_with_history.orders
```
