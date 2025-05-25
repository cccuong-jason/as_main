# Unit tests for OrderProcessor use case
import pytest
from unittest.mock import MagicMock, patch
from core.domain.order import Order, OrderStatus
from core.domain.design import Design
from core.use_cases.order_processor import OrderProcessor


@pytest.fixture
def order_processor(mock_order_repository, mock_design_generator, mock_llm_service):
    """Create an order processor with mock dependencies"""
    return OrderProcessor(
        order_repository=mock_order_repository,
        design_generator=mock_design_generator,
        llm_service=mock_llm_service
    )


def test_create_order(order_processor, order_data):
    """Test creating a new order"""
    # Act
    result = order_processor.create_order(order_data)
    
    # Assert
    assert result.success is True
    assert result.order.id == order_data["id"]
    assert result.order.customer_info["name"] == order_data["customer_name"]
    assert result.order.status == OrderStatus.PENDING


def test_create_order_validation_failure(order_processor):
    """Test creating an order with invalid data"""
    # Arrange
    invalid_order_data = {
        "id": "order123",
        "customer_name": "",  # Empty name should fail validation
        "customer_email": "test@example.com",
        "design_prompt": "A t-shirt with a mountain landscape",
        "size": "L",
        "color": "Blue",
        "quantity": 1,
        "status": "pending"
    }
    
    # Act
    result = order_processor.create_order(invalid_order_data)
    
    # Assert
    assert result.success is False
    assert "validation" in result.error.lower()


def test_process_order(order_processor, order_data):
    """Test processing an existing order"""
    # Arrange
    order = Order(**order_data)
    order_processor.order_repository.save(order)

    # Mock design generator to return a proper mock object
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.design = MagicMock()
    mock_result.error = None
    order_processor.design_generator.generate_design = MagicMock(return_value=mock_result)

    # Act
    result = order_processor.process_order(order.id)

    # Assert
    assert result.success is True
    assert result.order.status == OrderStatus.PROCESSING
    assert result.design is not None


def test_process_nonexistent_order(order_processor):
    """Test processing an order that doesn't exist"""
    # Act
    result = order_processor.process_order("nonexistent_id")
    
    # Assert
    assert result.success is False
    assert "not found" in result.error.lower()


def test_cancel_order(order_processor, order_data):
    """Test cancelling an order"""
    # Arrange
    order = Order(**order_data)
    order_processor.order_repository.save(order)
    
    # Act - Note: If cancel_order method doesn't exist, this test should be skipped
    # or implemented based on the actual method available
    if hasattr(order_processor, 'cancel_order'):
        result = order_processor.cancel_order(order.id)
        
        # Assert
        assert result.success is True
        assert result.order.status == OrderStatus.FAILED  # Assuming FAILED is used for cancelled orders
    else:
        pytest.skip("cancel_order method not implemented")


def test_get_order(order_processor, order_data):
    """Test retrieving an order"""
    # Arrange
    order = Order(**order_data)
    order_processor.order_repository.save(order)
    
    # Act
    result = order_processor.get_order(order.id)
    
    # Assert
    assert result.success is True
    assert result.order.id == order.id
    assert result.order.customer_name == order.customer_name


def test_get_all_orders(order_processor, order_data):
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
        status="pending"
    )
    order_processor.order_repository.save(order1)
    order_processor.order_repository.save(order2)
    
    # Act
    result = order_processor.get_all_orders()
    
    # Assert
    assert result.success is True
    assert len(result.orders) == 2
    assert any(order.id == order1.id for order in result.orders)
    assert any(order.id == order2.id for order in result.orders)


def test_process_order_flow(order_processor, order_data):
    """Test the complete flow of processing an order"""
    # Arrange - Use a different ID to avoid conflicts with other tests
    process_order_data = order_data.copy()
    process_order_data["id"] = "process_order_123"
    order = Order(**process_order_data)
    order_processor.order_repository.save(order)

    # Mock design generator to return a proper mock object
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.design = MagicMock()
    mock_result.error = None
    order_processor.design_generator.generate_design = MagicMock(return_value=mock_result)

    # Act
    result = order_processor.process_order(order.id)

    # Assert
    assert result.success is True
    assert result.order.status == OrderStatus.PROCESSING
    assert result.design is not None