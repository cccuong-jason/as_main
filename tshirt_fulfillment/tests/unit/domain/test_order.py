# Unit tests for Order domain model
import pytest

from tshirt_fulfillment.src.core.domain.order import Order
from tshirt_fulfillment.src.core.domain.order import OrderStatus


def test_order_creation():
    """Test that an order can be created with valid data"""
    # Arrange
    order_data = {
        "id": "order123",
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "design_prompt": "A t-shirt with a mountain landscape",
        "size": "L",
        "color": "Blue",
        "quantity": 1,
        "status": "pending",
    }

    # Act
    order = Order(**order_data)

    # Assert
    assert order.id == order_data["id"]
    assert order.customer_info["name"] == order_data["customer_name"]
    assert order.customer_info["email"] == order_data["customer_email"]
    assert order.customer_message == order_data["design_prompt"]
    assert order.customer_info["size"] == order_data["size"]
    assert order.customer_info["color"] == order_data["color"]
    assert order.customer_info["quantity"] == order_data["quantity"]
    assert order.status == OrderStatus.PENDING


def test_order_validation():
    """Test that order validation works correctly"""
    # Arrange/Act/Assert
    with pytest.raises(ValueError):
        Order(
            id="order123",
            customer_name="Test Customer",
            customer_email="invalid-email",  # Invalid email should fail validation
            design_prompt="A t-shirt with a mountain landscape",
            size="L",
            color="Blue",
            quantity=0,  # Invalid quantity should fail validation
            status="pending",
        )


def test_order_status_transition():
    """Test that order status transitions work correctly"""
    # Arrange
    order = Order(
        id="order123",
        customer_name="Test Customer",
        customer_email="test@example.com",
        design_prompt="A t-shirt with a mountain landscape",
        size="L",
        color="Blue",
        quantity=1,
        status="pending",
    )

    # Act
    order.update_status(OrderStatus.PROCESSING)

    # Assert
    assert order.status == OrderStatus.PROCESSING
    assert len(order.phases) > 0
    assert order.phases[-1].phase == f"status_changed_to_{OrderStatus.PROCESSING.value}"

    # Act/Assert - Test order result
    design_path = "/path/to/design.png"
    excel_path = "/path/to/excel.xlsx"
    drive_link = "https://drive.example.com/file"

    order.set_result(
        design_path=design_path,
        excel_path=excel_path,
        drive_link=drive_link,
        notification_sent=True,
    )

    assert order.result.design_path == design_path
    assert order.result.excel_path == excel_path
    assert order.result.drive_link == drive_link
    assert order.result.notification_sent is True
