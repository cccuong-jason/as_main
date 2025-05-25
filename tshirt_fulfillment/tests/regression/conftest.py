# Test fixtures for regression tests
from unittest.mock import MagicMock

import pytest

# Import fixtures from the main conftest.py
pytestmark = pytest.mark.usefixtures("order_data", "design_data", "mock_llm_service")


@pytest.fixture
def regression_data():
    """Data specific to regression tests"""
    return {
        "known_bug_cases": {
            "zero_quantity": {
                "id": "order123",
                "customer_name": "Test Customer",
                "customer_email": "test@example.com",
                "design_prompt": "A t-shirt with a mountain landscape",
                "size": "L",
                "color": "Blue",
                "quantity": 0,  # This previously caused a bug
                "status": "pending",
            },
            "invalid_email": {
                "id": "order124",
                "customer_name": "Test Customer",
                "customer_email": "invalid-email",  # This previously caused a bug
                "design_prompt": "A t-shirt with a mountain landscape",
                "size": "L",
                "color": "Blue",
                "quantity": 1,
                "status": "pending",
            },
            "duplicate_id": {
                "id": "duplicate_id",  # This previously caused a bug
                "customer_name": "Test Customer",
                "customer_email": "test@example.com",
                "design_prompt": "A t-shirt with a mountain landscape",
                "size": "L",
                "color": "Blue",
                "quantity": 1,
                "status": "pending",
            },
        }
    }


@pytest.fixture
def mock_order_repository():
    """Mock for order repository using MagicMock for regression tests"""
    mock_repo = MagicMock()
    mock_repo.orders = {}

    # Set up the save method to raise an error for duplicate IDs
    def save_side_effect(order):
        if order.id in mock_repo.orders:
            raise ValueError("Order with this ID already exists")
        mock_repo.orders[order.id] = order
        return order

    mock_repo.save.side_effect = save_side_effect

    return mock_repo


@pytest.fixture
def mock_database_with_history():
    """Mock database with historical data for regression testing"""
    db = MagicMock()

    # Simulate database with historical data
    db.orders = [
        {"id": "order001", "status": "completed", "created_at": "2023-01-01T12:00:00Z"},
        {"id": "order002", "status": "completed", "created_at": "2023-01-02T12:00:00Z"},
        {"id": "order003", "status": "failed", "created_at": "2023-01-03T12:00:00Z"},
    ]

    db.designs = [
        {"id": "design001", "status": "completed", "created_at": "2023-01-01T12:00:00Z"},
        {"id": "design002", "status": "failed", "created_at": "2023-01-02T12:00:00Z"},
    ]

    return db
