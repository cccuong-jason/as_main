# Integration tests for Order flow
import pytest
from tshirt_fulfillment.core.domain.order import Order, OrderStatus
from tshirt_fulfillment.core.domain.design import Design, DesignProvider
from tshirt_fulfillment.core.use_cases.order_processor import OrderProcessor
from tshirt_fulfillment.core.use_cases.design_generator import DesignGenerator


@pytest.fixture
def order_processor(mock_order_repository, mock_design_repository, mock_llm_service):
    """Create an order processor with mock dependencies"""
    design_generator = DesignGenerator(
        design_repository=mock_design_repository,
        llm_service=mock_llm_service
    )
    
    return OrderProcessor(
        order_repository=mock_order_repository,
        design_generator=design_generator
    )


def test_create_order_flow(order_processor, order_data):
    """Test the complete flow of creating an order"""
    # Act
    result = order_processor.create_order(order_data)
    
    # Assert
    assert result.success is True
    assert result.order.id == order_data["id"]
    assert result.order.status == OrderStatus.PENDING
    
    # Verify the order was saved to the repository
    saved_order = order_processor.order_repository.get_by_id(order_data["id"])
    assert saved_order is not None
    assert saved_order.id == order_data["id"]


def test_process_order_flow(order_processor, order_data):
    """Test the complete flow of processing an order"""
    # Arrange - Use a different ID to avoid conflicts with other tests
    process_order_data = order_data.copy()
    process_order_data["id"] = "process_order_123"
    order = Order(**process_order_data)
    order_processor.order_repository.save(order)
    
    # Act
    result = order_processor.process_order(order.id)
    
    # Assert
    assert result.success is True
    assert result.order.status == OrderStatus.PROCESSING
    
    # Verify the design was generated
    assert result.design is not None
    assert result.design.parameters.prompt == order.customer_message
    assert result.design.image_path is not None