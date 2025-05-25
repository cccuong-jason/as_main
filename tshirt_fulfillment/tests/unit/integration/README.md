# Integration Tests

This directory contains integration tests for the T-shirt Fulfillment application. Integration tests focus on testing how components work together.

## Directory Structure

```
/integration/
  test_order_flow.py    # End-to-end order processing
  test_design_flow.py   # End-to-end design generation
  test_admin_flow.py    # End-to-end admin functionality
  conftest.py           # Integration test-specific fixtures
```

## Writing Integration Tests

Integration tests should test the interaction between multiple components. They typically involve:

1. Setting up test data across multiple components
2. Executing a workflow that spans multiple components
3. Verifying the results across the system

### Example Integration Test

```python
def test_order_creation_and_processing(integrated_order_processor, order_data):
    # Create an order
    create_result = integrated_order_processor.create_order(order_data)
    assert create_result.success is True
    order_id = create_result.order.id

    # Process the order
    process_result = integrated_order_processor.process_order(order_id)
    assert process_result.success is True

    # Verify the order status was updated
    get_result = integrated_order_processor.get_order(order_id)
    assert get_result.order.status == "processing"

    # Verify a design was created
    assert process_result.design is not None
    assert process_result.design.prompt == order_data["design_prompt"]
```

## Running Integration Tests

To run all integration tests:

```bash
pytest tests/integration
```

To run tests for a specific flow:

```bash
pytest tests/integration/test_order_flow.py
```

## Test Database

Integration tests may require a test database. Use the `db_session` fixture from `conftest.py` to access the test database.

```python
def test_with_database(db_session):
    # Use the test database session
    result = db_session.query(Order).filter_by(id="test_id").first()
```

## API Testing

For testing the API endpoints, use the `api_client` fixture:

```python
def test_api_endpoint(api_client):
    response = api_client.post("/api/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["id"] == order_data["id"]
```
