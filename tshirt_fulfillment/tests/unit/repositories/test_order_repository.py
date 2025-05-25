# Unit tests for OrderRepository
from unittest.mock import MagicMock

import pytest

from tshirt_fulfillment.src.core.domain.order import Order
from tshirt_fulfillment.src.core.repositories.order_repository import OrderRepository


@pytest.fixture
def db_session():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def order_repository(db_session):
    """Create an order repository with a mock database session"""
    return OrderRepository(db_session)


def test_save_order(order_repository, order_data):
    """Test saving an order to the repository"""
    # Arrange
    order = Order(**order_data)

    # Act
    saved_order = order_repository.save(order)

    # Assert
    assert saved_order == order
    order_repository.db_session.add.assert_called_once_with(order)
    order_repository.db_session.commit.assert_called_once()


def test_get_order_by_id(order_repository, order_data):
    """Test retrieving an order by ID"""
    # Arrange
    order = Order(**order_data)

    # Mock the query chain
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = order
    order_repository.db_session.query.return_value = mock_query

    # Act
    retrieved_order = order_repository.get_by_id(order.id)

    # Assert
    assert retrieved_order == order
    # Verify the query chain was called correctly
    order_repository.db_session.query.assert_called_once()
    mock_query.filter_by.assert_called_once_with(id=order.id)
    mock_query.filter_by.return_value.first.assert_called_once()


def test_get_order_by_id_not_found(order_repository):
    """Test retrieving an order by ID when it doesn't exist"""
    # Arrange
    order_repository.db_session.query().filter_by().first.return_value = None

    # Act
    retrieved_order = order_repository.get_by_id("nonexistent_id")

    # Assert
    assert retrieved_order is None


def test_get_all_orders(order_repository, order_data):
    """Test retrieving all orders"""
    # Arrange
    order1 = Order(**order_data)
    order2 = Order(
        id="order456",
        customer_name="Another Customer",
        customer_email="another@example.com",
        design_prompt="A t-shirt with a sunset",
        size="M",
        color="Red",
        quantity=2,
        status="pending",
    )
    order_repository.db_session.query().all.return_value = [order1, order2]

    # Act
    orders = order_repository.get_all()

    # Assert
    assert len(orders) == 2
    assert order1 in orders
    assert order2 in orders


def test_update_order(order_repository, order_data):
    """Test updating an order"""
    # Arrange
    order = Order(**order_data)

    # Act
    updated_order = order_repository.update(order)

    # Assert
    assert updated_order == order
    order_repository.db_session.add.assert_called_once_with(order)
    order_repository.db_session.commit.assert_called_once()


def test_delete_order(order_repository, order_data):
    """Test deleting an order"""
    # Arrange
    order = Order(**order_data)
    order_repository.db_session.query().filter_by().first.return_value = order

    # Act
    order_repository.delete(order.id)

    # Assert
    order_repository.db_session.delete.assert_called_once_with(order)
    order_repository.db_session.commit.assert_called_once()


def test_delete_order_not_found(order_repository):
    """Test deleting an order that doesn't exist"""
    # Arrange
    order_repository.db_session.query().filter_by().first.return_value = None

    # Act/Assert
    with pytest.raises(ValueError, match="Order not found"):
        order_repository.delete("nonexistent_id")
